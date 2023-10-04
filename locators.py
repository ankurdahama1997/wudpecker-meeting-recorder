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
