import os
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.utils import keys_to_typing
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import traceback
from dotenv import load_dotenv
from locators import Locators

options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')
options.add_argument('--password-store=basic')
# options.add_argument('--headless')  # Use headless Chrome
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
        global driver

        for key in typing:
            self.key_down(key)
            self.key_up(key)
            self.w3c_actions.key_action.pause(time_s)

        return self


def waitwithss(sec):
    for i in range(0, sec):
        sleep(1)
        driver.save_screenshot('live.png')  # For debugging


def wait_for_element(by, value):
    driver.save_screenshot('wait_for_element.png')  # For debugging
    return WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, value)))


def login_process():
    load_dotenv()
    zoom_link = os.getenv("ZOOM_MEETING_LINK")
    if zoom_link is not None:
        driver.get(zoom_link)
    action = EnhancedActionChains(driver)

    try:
        # Wait for page elements to load
        waitwithss(1)

        # Find and input Zoom Meeting ID
        input_zoom_id_field = driver.find_element(By.XPATH, Locators.ZOOM_ID_INPUT_FIELD)
        zoom_id = os.getenv("ZOOM_MEETING_ID")
        input_zoom_id_field.send_keys(zoom_id)

        # Click Join button
        join_button_home = driver.find_element(By.XPATH, Locators.ZOOM_JOIN_BUTTON_HOME)
        join_button_home.click()

        # Switch to Zoom iframe
        zoom_iframe = driver.find_element(By.CLASS_NAME, Locators.ZOOM_IFRAME_CLASS)
        driver.switch_to.frame(zoom_iframe)

        # Input Passcode and Name
        passcode_input = wait_for_element(By.XPATH, Locators.ZOOM_PASSCODE_INPUT_FIELD)
        zoom_passcode = os.getenv("ZOOM_MEETING_PASSCODE")
        passcode_input.send_keys(zoom_passcode)
        name_input = driver.find_element(By.XPATH, Locators.ZOOM_NAME_INPUT_FIELD)
        name_input.send_keys('Zoom Bot')

        # Click Join button inside the iframe
        join_button = wait_for_element(By.XPATH, Locators.ZOOM_IFRAME_JOIN_BUTTON)
        join_button.click()

        # Wait for the meeting to start, we can add a transition here as well
        waitwithss(5)

        # Check for incorrect passcode error
        try:
            error_message = driver.find_element(By.ID, Locators.ZOOM_ERROR_MESSAGE_ON_WRONG_PASSCODE)
            if "Incorrect Password" in error_message.text:
                print("Incorrect passcode entered. Ending the call.")

                return
        except NoSuchElementException:
            pass  # No error message found

        # If you reach this point, it means you are in the meeting lobby
        print("IN_LOBBY")
        while True:
            if is_kicked():
                print("Kicked out from the call")
                break
                waitwithss(2)

    except NoSuchElementException as e:
        # Log error and exit
        print('Error finding element:', e)
        exit()


# participants detection in progress
def after_login():
    # open participants list
    try:
        wait_for_bar = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'video-avatar__avatar')))
        driver.execute_script('document.getElementById("wc-footer").className = "footer";')
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="wc-footer"]/div/div[2]/div[1]/button'))).click()
    except Exception:
        traceback.print_exc()
        print('error occured, not able to open participants list in time')

    # read name div
    try:
        sleep(4)
        name_div = driver.find_elements(by=By.CLASS_NAME, value='participants-item-position')
    except Exception:
        traceback.print_exc()
        print('unable to read participants 1')

    # loop the div and parse names
    try:
        print('Participants:')
        for idx, participant in enumerate(name_div, 1):
            name = participant.find_element(by=By.TAG_NAME, value='span')
            print(idx, name.text.replace('\n', ' '))
    except Exception:
        traceback.print_exc()
        print('unable to read participants 2')


def is_kicked():
    try:
        # Check if the "You have been removed" modal is present
        kick_modal = driver.find_element(By.CSS_SELECTOR, Locators.ZOOM_KICKED_OUT_MODAL)
        if "You have been removed" in kick_modal.text:
            # Click the exit button
            exit_button = driver.find_element(By.XPATH, Locators.ZOOM_KICKED_OUT_MODAL_EXIT_BUTTON)
            exit_button.click()
            print("Bot has been removed from the meeting. Exiting the meeting.")
            return True
    except NoSuchElementException:
        pass
    return False


def stopStream():
    driver.execute_script("""
        var stopelm = document.createElement("p");
        stopelm.setAttribute("id","stoprecord");
        document.querySelector('body').appendChild(stopelm)
    """)


if __name__ == '__main__':
    login_process()

    stopStream()
    print("Call ended successfully", flush=True)
    # after_login()
