import requests
import time
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.utils import keys_to_typing
from selenium.webdriver.common.keys import Keys
import subprocess
import shlex
import os
import glob
import random
import sys
import json
from dotenv import load_dotenv

options = uc.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--password-store=basic')
options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )
params = {
    "behavior": "allow",
    "downloadPath": os.getcwd(), # Or whatever path you want
}

print("Creating driver...")
driver = uc.Chrome(options=options, use_subprocess=True, version_main=114)
driver.execute_cdp_cmd("Page.setDownloadBehavior", params)


ALONE_TIMEOUT = 60*5 # 5 mins
LOBBY_TIMEOUT = 60*10 # 10 mins :)
MAX_LENGTH = 2*60*60 # 2 hours


load_dotenv()
status_url = os.getenv("STATUS_URL")
uuid = os.getenv("UUID")
def send_status(msg):
    try:
        if msg:
            requests.post(status_url, data={"uuid": uuid, "status": msg})
    except:
        pass

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
        time.sleep(1)
        driver.save_screenshot('live.png') # For debugging

def stopStream():
    driver.execute_script("""
        var stopelm = document.createElement("p");
        stopelm.setAttribute("id","stoprecord");
        document.querySelector('body').appendChild(stopelm)
    """) 

def check_if_detected(driver):
    try:
        if '<div jsname="r4nke" class="roSPhc">You can\'t join this video call</div>' in driver.page_source:
            send_status("DETECTED")
            return True
    except:
        pass
    return False


def timed_out(driver, start_time):
    try:
        if (time.time() - start_time > MAX_LENGTH):
            return True
    except:
        pass
    return False


def check_if_in_call(driver):
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[10]")
        return True
    except Exception as e:
        pass
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[13]/div[3]/div[10]")
        return True
    except Exception as e:
        pass
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[13]/div[3]/div[11]")
        return True
    except Exception as e:
        pass
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]")
        return True
    except Exception as e:
        pass
    return False
    
def is_kicked(driver):
    try:
        kicked = driver.find_element(
            By.CSS_SELECTOR, "#ow3 > div > div > h1.roSPhc")
        return True
    except:
        pass
    return False

def alone_in_room(driver, start_time):
    try:
        participants = driver.find_elements(
            By.CSS_SELECTOR, "#ow3 > div.T4LgNb > div > div:nth-child(13) > div.crqnQb > div.UnvNgf.Sdwpn.P9KVBf.IYIJAc.BIBiNe > div.jsNRx > div.fXLZ2 > div > div > div:nth-child(2) > div > div")
        if participants and participants[0].text == "1"  and time.time() - start_time > ALONE_TIMEOUT:
            return True
    except:
        pass
    
    try:
        participants = driver.find_elements(
            By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[13]/div[3]/div[10]/div/div/div[3]/div[1]/div[2]/div/div/div")
        if participants and participants[0].text == "1"  and time.time() - start_time > ALONE_TIMEOUT:
            return True
    except:
        pass
    
    try:
        participants = driver.find_elements(
            By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[13]/div[3]/div[11]/div/div/div[3]/div[1]/div[2]/div/div/div")
        if participants and participants[0].text == "1"  and time.time() - start_time > ALONE_TIMEOUT:
            return True
    except:
        pass
    
    try:
        participants = driver.find_elements(
            By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[10]/div/div/div[3]/div[1]/div[2]/div/div/div")
        if participants and participants[0].text == "1"  and time.time() - start_time > ALONE_TIMEOUT:
            return True
    except:
        pass
    try:
        participants = driver.find_elements(
            By.XPATH, "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[3]/div[1]/div[2]/div/div/div")
        if participants and participants[0].text == "1"  and time.time() - start_time > ALONE_TIMEOUT:
            return True
    except:
        pass

    return False



def clickButton(by, name):
    try:
        if by == "class":
            btn = driver.find_element(By.CLASS_NAME, name)
        if by == "id":
            btn = driver.find_element(By.ID, name)
        if by == "xpath":
            btn = driver.find_element(By.XPATH, name)
        driver.execute_script("return arguments[0].scrollIntoView(true);", btn)
        btn.click()
        waitwithss(1)
    except Exception as e:
        print(f"Failed to click button with {by} - {name}")
        

def watchMutation():
  driver.execute_script("""
        function waitForElm(selector) {
            return new Promise(resolve => {
                if (document.querySelector(selector)) {
                    return resolve(document.querySelector(selector));
                }

                const observer = new MutationObserver(mutations => {
                    if (document.querySelector(selector)) {
                        resolve(document.querySelector(selector));
                        observer.disconnect();
                    }
                });

                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
            });
        }
        var speaker_content = "::::" + arguments[0].toString() + "::::";                 
        function getElementsByClass(className) {
            return document.getElementsByClassName(className);
        }
        function saveSpeakers() {
            const blob = new Blob([speaker_content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const downloadLink = document.createElement('a');
            downloadLink.href = url;
            downloadLink.download = "speakers.txt";
            document.body.appendChild(downloadLink);
            downloadLink.click();
        }
        waitForElm('#stoprecord').then((elm) => {
            saveSpeakers()
        });
        function switchStr(st, speaker_name) {
            var timestamp = (Math.ceil(Date.now()/1000)).toString()
            speaker_content +=  timestamp + "==>" + speaker_name + ";;;";
            
        }

        var current_video = null;

        setInterval(() => {
            var speaking = document.getElementsByClassName("lH9pqf atLQQ kssMZb")
            if(speaking.length > 0) {
                var speaker_video = speaking[0].parentElement.parentElement.parentElement.getElementsByTagName('video')[0];
                if(window.getComputedStyle(speaker_video).display == "none") {
                    speaker_video = speaking[0].parentElement.parentElement.parentElement.getElementsByTagName('video')[1];
                }
                var speaker_name = speaking[0].parentElement.parentElement.parentElement.getElementsByClassName("XEazBc adnwBd")[0].innerText;
                if (current_video != speaker_video) {
                    switchStr(speaker_video, speaker_name);
                    current_video = speaker_video;
                }
            } 
        }, 500)
""", int(time.time()))

def run_bot():

    link = os.getenv("MEETING_LINK")
    driver.get(link)
    waitwithss(2)
    action = EnhancedActionChains(driver)

    bot_email = os.getenv("BOT_LOGIN_EMAIL")
    bot_password = os.getenv("BOT_LOGIN_PASSWORD")
    # Start Login process otherwise cannot click continue :D
    send_status("LOGGING_IN")
    check_if_detected(driver)
    driver.find_element(By.XPATH, "//*[contains(text(),'Sign in')]").click()
    waitwithss(5)
    
    # Back to join screen
    check_if_detected(driver)
    driver.get(link)
    waitwithss(2)
    try:
        driver.find_element(By.XPATH, "//*[contains(text(),'Use without an account')]").click()
        waitwithss(2)
    except:
        pass
    action.send_keys_1by1("Joona's Wudpecker.io Notetaker").perform()
    # Try to join
    check_if_detected(driver)
    ask_to_join = driver.find_elements(By.XPATH, "//*[contains(text(),'Ask to join')]")
    if ask_to_join:
        driver.find_element(By.XPATH, "//*[contains(text(),'Ask to join')]").click()
    else:
        driver.find_element(By.XPATH, "//*[contains(text(),'Join now')]").click()
    waitwithss(1)

    # Waiting in Lobby
    send_status("IN_LOBBY")
    timer = time.time()
    inside = False

    while time.time() - timer < LOBBY_TIMEOUT:
        check_if_detected(driver)
        if check_if_in_call(driver):
            inside = True
            break

    if not inside:
        quit()

    # Meeting joined
    send_status("JOINED")
    start_time = time.time()
    watchMutation()
    with open('start.txt', 'w') as f:
        f.write('Bot joined')
    while True:
        if alone_in_room(driver, start_time):
            send_status("EXIT_ALONE")
            break
        if is_kicked(driver):
            send_status("EXIT_KICKED")
            break
        if timed_out(driver, start_time):
            send_status("EXIT_TIMEOUT")
            break
        waitwithss(5)

    # Call ended
    stopStream()
    print("Call ended successfully")


    waitwithss(2)

try:
    print('STARTING_BOT')
    run_bot()
except Exception as e:
    print(e)
    print('FAILED')
    send_status("FAILED")