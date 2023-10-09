import os
import re
from time import sleep, strftime, localtime
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.utils import keys_to_typing
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from locators import Locators
import traceback

# Initialize Chrome options
options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')
options.add_argument('--password-store=basic')
options.add_argument("--use-fake-ui-for-media-stream")  # Allow access to microphone and camera without prompting
options.add_experimental_option(
    "prefs",
    {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    },
)

params = {
    "behavior": "allow",
    "downloadPath": os.getcwd(),  # Or whatever path you want
}

print("Creating driver...")
driver = uc.Chrome(options=options, use_subprocess=True)
driver.maximize_window()
driver.execute_cdp_cmd("Page.setDownloadBehavior", params)


class EnhancedActionChains(ActionChains):
    def send_keys_1by1(self, keys_to_send, time_s=0.2):
        typing = keys_to_typing(keys_to_send)

        for key in typing:
            self.key_down(key)
            self.key_up(key)
            self.w3c_actions.key_action.pause(time_s)

        return self


def wait_with_screenshot(seconds):
    for _ in range(seconds):
        sleep(1)
        driver.save_screenshot('live.png')  # For debugging


def wait_for_element(by, value):
    try:
        driver.save_screenshot('wait_for_element.png')  # For debugging
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"Timeout waiting for element with {by} = {value}")
        return None


def login_process():
    load_dotenv()
    zoom_link = os.getenv("ZOOM_MEETING_LINK")
    if zoom_link is not None:
        print(zoom_link)
        driver.get(zoom_link)

    action = EnhancedActionChains(driver)

    try:
        # Wait for page elements to load
        wait_with_screenshot(2)
        print("Zoom Login page")
        # Find and input Zoom Meeting ID
        input_zoom_id_field = wait_for_element(By.XPATH, Locators.ZOOM_ID_INPUT_FIELD)
        if input_zoom_id_field:
            zoom_id = os.getenv("ZOOM_MEETING_ID")
            input_zoom_id_field.send_keys(zoom_id)
            print("Entered Zoom Meeting ID")
        else:
            print("Zoom ID input field not found.")
            return

        # Click Join button
        join_button_home = wait_for_element(By.XPATH, Locators.ZOOM_JOIN_BUTTON_HOME)
        if join_button_home:
            join_button_home.click()
            print("Join button pressed.")
            wait_with_screenshot(1)
        else:
            print("Join button not found.")
            return

        # Switch to Zoom iframe
        zoom_iframe = wait_for_element(By.CLASS_NAME, Locators.ZOOM_IFRAME_CLASS)
        if zoom_iframe:
            driver.switch_to.frame(zoom_iframe)
        else:
            print("Zoom iframe not found.")
            return

        # Input Passcode and Name
        passcode_input = wait_for_element(By.XPATH, Locators.ZOOM_PASSCODE_INPUT_FIELD)
        if passcode_input:
            zoom_passcode = os.getenv("ZOOM_MEETING_PASSCODE")
            passcode_input.send_keys(zoom_passcode)
            print("Passcode entered.")
        else:
            print("Zoom passcode input field not found.")
            return

        name_input = driver.find_element(By.XPATH, Locators.ZOOM_NAME_INPUT_FIELD)
        if name_input:
            name_input.send_keys('Zoom Bot')
            print("Zoom Bot entered in name field")
        else:
            print("Zoom name input field not found.")
            return

        # Click Join button inside the iframe
        join_button = wait_for_element(By.XPATH, Locators.ZOOM_IFRAME_JOIN_BUTTON)
        if join_button:
            join_button.click()
            print("Join Meeting button pressed.")
            wait_with_screenshot(1)
        else:
            print("Join button inside iframe not found.")
            return

        # Wait for the lobby to appear
        wait_with_screenshot(2)

        # Check for incorrect passcode error
        try:
            error_message = driver.find_element(By.ID, Locators.ZOOM_ERROR_MESSAGE_ON_WRONG_PASSCODE)
            if "Incorrect Password" in error_message.text:
                print("Incorrect passcode entered. Ending the call.")
                return
        except NoSuchElementException:
            pass  # No error message found
        # wait in lobby to until Host admits the bot in
        waiting_in_lobby()


    except Exception as e:
        # Log error and exit
        print(f'Error finding element:', e)
        traceback.print_exc()
        exit()


def after_login():
    # check for the participants
    inside_meeting_room()


def inside_meeting_room():
    try:
        min_users = os.getenv("ZOOM_MINIMUM_PARTICIPANTS")
        print("Logging data..")
        participants = []
        driver.find_elements(By.XPATH, Locators.ZOOM_PARTICIPANTS_BUTTON)[0].click()

        wait_with_screenshot(5)

        max_call_duration = os.getenv("ZOOM_TOTAL_TIMEOUT_LIMIT")
        zoom_total_timeout = int(max_call_duration)  # 10
        zoom_total_timeout *= 60  # time in seconds
        now_secs = 0
        while True:
            try:
                is_ended = driver.find_elements(By.XPATH, Locators.ZOOM_MEETING_ENDED_BY_HOST)
                if len(is_ended) != 0:
                    print('Host ended the meeting.')
                    raise Exception

                limit_exceeded = driver.find_elements(By.XPATH, Locators.ZOOM_FREE_MEETING_ENDED)
                if len(limit_exceeded) != 0:
                    print('Meeting has ended due to time limit.')
                    raise Exception

                meeting_upgraded = driver.find_elements(By.XPATH, Locators.ZOOM_MEETING_UPGRADED_HOST)
                if len(meeting_upgraded) != 0:
                    print('Meeting has been upgraded.')
                    driver.find_elements(By.XPATH, Locators.ZOOM_UNDER_dIV_OKAY_BTN)[0].click()

                is_recording = driver.find_elements(By.XPATH, Locators.ZOOM_IS_RECORDING_CHECK)
                if len(is_recording) != 0:
                    driver.find_elements(By.XPATH, Locators.ZOOM_GOT_IT_BUTTON)[0].click()

                ask_audio = driver.find_elements(By.XPATH, Locators.ZOOM_ASK_AUDIO_BUTTON)
                if len(ask_audio) != 0:
                    sleep(1)
                    print("Host asked to un mute.")
                    driver.find_elements(By.XPATH, Locators.ZOOM_STAY_MUTED_BUTTON)[0].click()
                    print("Request rejected.")

                ask_video = driver.find_elements(By.XPATH, Locators.ZOOM_ASK_FOR_VIDEO)
                if len(ask_video) != 0:
                    sleep(1)
                    print("Host asked to enable video.")
                    driver.find_elements(By.XPATH, Locators.ZOOM_LATER_BUTTON)[0].click()
                    print("Request rejected for video.")

                active_users = driver.find_elements(By.CLASS_NAME, Locators.ZOOM_PARTICIPANTS_BTN_CLASS)
                for user in active_users[0:]:
                    temp_text = re.findall(r"^<span .*\">(.*)<\/span.*\">(.*)<\/span>",
                                           user.get_attribute("innerHTML").strip())
                    u_name = temp_text[0][0] + temp_text[0][1]
                    if not any(participant['Name'] == u_name for participant in participants):
                        participants.append({'Name': u_name, 'Timestamp': strftime("%H:%M:%S", localtime())})
                write_file(participants)
                print('Total number of participants: ', len(participants))

                # Check if the bot has been kicked out
                if is_kicked():
                    wait_with_screenshot(2)
                    break
                    return

                # Waiting alone in the Meeting room
                # if (len(activeUsers=2) <= int(minUsers=1)) and (now_secs > zoom_total_timeout):
                #     print("Minimum users amount reached. -- Leaving from meeting...")
                #     write_file(participants)
                #     driver.quit()

                # Total time out use case
                if now_secs > zoom_total_timeout:
                    print("Meeting Timeout, ending the meeting.")
                    write_file(participants)
                    # driver.quit()
                    wait_with_screenshot(2)
                    break
                    return
                sleep(10)
                now_secs += 10  # second ++
                print("Nowsecs:", now_secs)
            except Exception as e:
                wait_with_screenshot(1)
                print('Seems like session has been ended')
                traceback.print_exc()
                write_file(participants)
                break

        driver.quit()
        print("Leaving meeting room!")
        return
    except Exception as e:
        print('-' * 25)
        traceback.print_exc()
        write_file(participants)
        driver.quit()


def write_file(participants):
    try:
        with open("zoom_attendance.txt", 'w', encoding='utf-8') as f:
            f.write(f"Total participants: {len(participants)}\n")
            for user_data in participants:
                line = f"{user_data['Name']}, {user_data['Timestamp']}\n"
                f.write(line)
            print("Data saved successfully!")
    except IOError as e:
        print(f"Error occurred while writing to the disk: {e}")
        traceback.print_exc()


# Method to check if the bot admitted in the meeting room.
def is_admitted():
    try:
        leave_button = driver.find_element(By.XPATH, Locators.ZOOM_MEETING_ROOM_LEAVE_BUTTON)
        if leave_button:
            return True
    except NoSuchElementException:
        pass
    return False


# Method to check if the bot is in lobby, wait until Host approval for X mints
def waiting_in_lobby():
    try:
        lobby_entered_time = datetime.now()
        lobby_time_out = os.getenv("ZOOM_WAITING_IN_LOBBY_TIMEOUT")
        lobby_time_out = int(lobby_time_out)  # Convert the string to an integer
        waiting_time = timedelta(minutes=lobby_time_out)
        print("Waiting inside lobby, awaiting Host's approval.")

        # Wait inside lobby till specific time or till Bots admission
        while datetime.now() - lobby_entered_time < waiting_time:
            on_hold_element = None
            try:
                # This element is only present while the bot is in Lobby of zoom
                on_hold_element = driver.find_element(By.CLASS_NAME, Locators.ZOOM_LOBBY_CLASS_NAME)
            except NoSuchElementException:
                pass

            if on_hold_element:
                pass  # Skip the iteration if the bot is still in the lobby
            else:
                if is_admitted():
                    print("Bot has entered the Meeting Room.")
                    # Join the call after hosts approval via after_login() method
                    wait_with_screenshot(5)
                    after_login()
                    return

    except Exception as e:
        print(f'Error in waiting_in_lobby:', e)
        traceback.print_exc()

    # If 5 minutes passed and still in the lobby, press exit button
    exit_button = wait_for_element(By.XPATH, Locators.ZOOM_LOBBY_EXIT_BUTTON)
    print("Host did not let Bot in.")
    if exit_button:
        exit_button.click()
        print("Exiting the lobby and call.")
    else:
        print("Exit button not found in the lobby.")


def is_kicked():
    try:
        kick_modal = driver.find_element(By.CSS_SELECTOR, Locators.ZOOM_KICKED_OUT_MODAL)
        if "You have been removed" in kick_modal.text:
            exit_button = driver.find_element(By.XPATH, Locators.ZOOM_KICKED_OUT_MODAL_EXIT_BUTTON)
            exit_button.click()
            print("Bot has been removed from the meeting. Exiting the meeting.")
            return True
    except NoSuchElementException:
        pass
    return False


if __name__ == '__main__':
    login_process()

    print("Call ended successfully", flush=True)
