class Locators:
    ZOOM_ID_INPUT_FIELD = '//input[@class="join-meetingId"]'
    ZOOM_JOIN_BUTTON_HOME = '//button[contains(@class, "btn-join") and contains(@class, "btn-primary")]'
    ZOOM_IFRAME_CLASS = 'pwa-webclient__iframe'
    ZOOM_PASSCODE_INPUT_FIELD = '//input[@id="input-for-pwd"]'
    ZOOM_NAME_INPUT_FIELD = '//input[(@id="input-for-name")]'
    ZOOM_IFRAME_JOIN_BUTTON = '//*[@id="root"]/div/div[1]/div/div[2]/button'
    ZOOM_KICKED_OUT_MODAL = 'div.zm-modal-body-title'
    ZOOM_KICKED_OUT_MODAL_EXIT_BUTTON = '//button[contains(@class, "zm-btn") ' \
                                        'and contains(@class, "zm-btn--primary") ' \
                                        'and contains(@class, "zm-btn__outline--blue")]'
    ZOOM_ERROR_MESSAGE_ON_WRONG_PASSCODE = 'error-for-pwd'
    ZOOM_PARTICIPANTS_BUTTON = "//span[text()='Participants']"
    ZOOM_MEETING_ENDED_BY_HOST = "//div[text()='This meeting has been ended by host']"
    ZOOM_FREE_MEETING_ENDED = "//div[text()='This free Zoom meeting has ended']"
    ZOOM_MEETING_UPGRADED_HOST = "//div[text()='This meeting has been upgraded by the host and now includes unlimited minutes.']"
    ZOOM_UNDER_dIV_OKAY_BTN = "//button[text()='OK']"
    ZOOM_IS_RECORDING_CHECK = "//div[text()='This meeting is being recorded']"
    ZOOM_GOT_IT_BUTTON = "//button[text()='Got it']"
    ZOOM_ASK_AUDIO_BUTTON = "//div[text()='The host would like you to speak']"
    ZOOM_STAY_MUTED_BUTTON = "//button[text()='Stay Muted']"
    ZOOM_ASK_FOR_VIDEO = "//div[text()='The host has asked you to start your video']"
    ZOOM_LATER_BUTTON = "//button[text()='Later']"
    ZOOM_PARTICIPANTS_BTN_CLASS = "participants-item__name-section"
    # ZOOM_LOBBY_STATUS = "//span[text()='Host has joined. We've let them know you're here']"
    ZOOM_LOBBY_STATUS = "//*[@id='root']/div/div[2]/div/div[1]/div[2]/div[1]/div[3]/span"
    ZOOM_LOBBY_EXIT_BUTTON = "//*[@id='root']/div/div[2]/div/div[1]/div[2]/div[1]/div[4]/button"
    ZOOM_LOBBY_CLASS_NAME = "meeting-on-hold"
    ZOOM_MEETING_ROOM_LEAVE_BUTTON = "//*[@id='foot-bar']/div[3]/button"

    # meet
    MEET_NAME_INPUT_FIELD = 'input[placeholder="Your name"]'
    MEET_ASK_TO_JOIN_BUTTON = "//*[contains(text(),'Ask to join')]"
    MEET_JOIN_NOW_BUTTON = "//*[contains(text(),'Join now')]"
    MEET_CHECK_IF_IN_CALL_LOCATOR_ONE = "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[10]"
    MEET_CHECK_IF_IN_CALL_LOCATOR_TWO = "/html/body/div[1]/c-wiz/div[1]/div/div[13]/div[3]/div[10]"
    MEET_CHECK_IF_IN_CALL_LOCATOR_THREE = "/html/body/div[1]/c-wiz/div[1]/div/div[13]/div[3]/div[11]"
    MEET_CHECK_IF_IN_CALL_LOCATOR_FOUR = "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]"
    MEET_KICKED_OUT_MODAL = "#ow3 > div > div > h1.roSPhc"
    MEET_ALONE_IN_ROOM_LOCATOR = "#ow3 > div.T4LgNb > div > div:nth-child(13) > div.crqnQb > " \
                                 "div.UnvNgf.Sdwpn.P9KVBf.IYIJAc.BIBiNe > div.jsNRx > div.fXLZ2 > div > div " \
                                 "> div:nth-child(2) > div > div"
    MEET_ROOM_PARTICIPANTS_ONE = "/html/body/div[1]/c-wiz/div[1]/div/div[13]/div[3]/div[10]/div/div/div[3]/div[1]/div[2]/div/div/div"
    MEET_ROOM_PARTICIPANTS_TWO = "/html/body/div[1]/c-wiz/div[1]/div/div[13]/div[3]/div[11]/div/div/div[3]/div[1]/div[2]/div/div/div"
    MEET_ROOM_PARTICIPANTS_THREE = "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[10]/div/div/div[3]/div[1]/div[2]/div/div/div"
    MEET_ROOM_PARTICIPANTS_FOUR = "/html/body/div[1]/c-wiz/div[1]/div/div[14]/div[3]/div[11]/div/div/div[3]/div[1]/div[2]/div/div/div"
