import time

import pyautogui
from telegram import Bot

from lib import CTDT, Config
from datetime import datetime

from telegram_bot import TelegramBot


class Tsubasa:
    config: Config = None

    MODE_STORY_SOLO = 1
    MODE_EVENT_SOLO = 2
    MODE_SOLO = 3
    MODE_CLUB_SHARED = 4
    MODE_CLUB_JOIN = 5
    MODE_GLOBAL_SHARED = 6
    MODE_GLOBAL_JOIN = 7
    MODE_EVOLE_PLAYER = 8

    EnergyRecovery_WaitToRecover = 2
    EnergyRecovery_Ad = 3
    EnergyRecovery_Energyball = 4
    EnergyRecovery_Dreamball = 5
    EnergyRecovery_None_Telegram = 6

    Telegram_Disabled = 0
    Telegram_Enabled = 1

    # the time energy recovery dialog is opened
    # we use this to open and close energy recovery dialog once in a three minutes
    energy_recovery_dialog_datetime: datetime = None

    # the time we sent a msg in telegram that we are out of energy
    # because we send this msg once in an hour
    energy_recovery_send_telegram_datetime = None

    # the time that there is a change in joining members in accepting members in join play
    # if None it means no member is joined or we are not on accepting members page
    member_joined_datetime: datetime = None

    # count the number of users in accepting members using in join play
    member_joined_count: int = 0

    # count the number of matched played
    count_played_match: int = 0

    # the time we clicked on 0,0 to prevent screen off
    prevent_screen_datetime = None

    # start time of viewing ad
    ad_viewing_time = None

    # it will increase on every cycle that is present and reset 0 otherwise so we can detect app freeze
    count_now_loading = 0

    # telegral bot
    bot: Bot

    # telegral notify bot
    bot_notify: Bot

    telegram: TelegramBot = None

    # the time that we exited the app for resseting ad
    # because we do not want repeated exit of app
    exit_app_for_ad_time = None

    # detect inactive user in shared play
    # if we reaches to max number in config it means user is inactive and we should go home and try again
    count_preparing: int = 0

    # maximum number of searching in shared play
    # if we reaches to this number it means users are not sharing and we should retry
    count_sharing: int = 0

    def __init__(self, telegram: TelegramBot):
        self.config = Config.get_instance()
        if self.config.telegram_disabled == 0:
            self.bot = Bot(token=self.config.telegram_token)
            self.bot_notify = Bot(token=self.config.telegram_token2)
            self.telegram = telegram

    def increase_count_played_match(self):
        self.count_played_match += 1

    def send_count_played_match(self):
        try:
            if self.config.telegram_disabled == 0:
                output: str = "Count : {0} , Date : {1}".format(self.count_played_match,
                                                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                self.bot.send_message(self.config.telegram_chatid, output)
        except Exception as ex:
            print(str(ex))

    def send_telegram_message(self, msg: str, notify=False):
        try:
            if self.config.telegram_disabled == 0:

                if notify == False:
                    self.bot.send_message(self.config.telegram_chatid, msg)
                else:
                    self.bot_notify.send_message(self.config.telegram_chatid2, msg)

        except Exception as ex:
            print(str(ex))

    ########################################################################################################################

    def run_001(self, modes: set):
        """
        run app
        :return:
        """

        if self.config.mode not in modes: return False

        if CTDT.template("001").click(wait=5):
            self.send_telegram_message("Run App : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return True

        return False

    ########################################################################################################################

    def run_002(self, modes: set):
        """
        enter app
        :return:
        """

        if self.config.mode not in modes: return False

        if CTDT.template("002").click(wait=5):
            return True

        return False

    ########################################################################################################################

    def run_003(self, modes: set):
        """
        go to story mode
        :return:
        """

        if self.config.mode not in modes: return False

        if CTDT.template("003").click():
            return True

        return False

    ########################################################################################################################

    def run_007(self, modes: set):
        """
        difficulty
        :return:
        """

        if self.config.mode not in modes: return False

        # normal
        if self.config.difficulty == 1:

            # difficulty normal
            if CTDT.template("057").click():
                # exit app gracefully if required
                self.run_044()

                return True

        # hard
        elif self.config.difficulty == 2:

            # difficulty hard
            if CTDT.template("058").click():
                # exit app gracefully if required
                self.run_044()

                return True

        # very hard
        elif self.config.difficulty == 3:

            # difficulty very hard
            if CTDT.template("059").click():
                # exit app gracefully if required
                self.run_044()

                return True

        # extreme
        elif self.config.difficulty == 4:

            # difficulty extreme
            if CTDT.template("060").click():
                # exit app gracefully if required
                self.run_044()

                return True

        return False

    ########################################################################################################################

    def run_008(self, modes: set):
        """
        play match button
        :return:
        """

        if self.config.mode not in modes: return False

        # skip ticket button is not present beside play match button = 0
        if self.config.play_match_with_skip_ticket_button == 0:

            # play match button without skip ticket
            if CTDT.template("028").click():
                return True

        # skip ticket button is present beside play match button = 1
        elif self.config.play_match_with_skip_ticket_button == 1:

            # play match button with skip ticket
            if CTDT.template("008").click(1):
                return True

        return False

    ########################################################################################################################

    def run_009(self, modes: set):
        """
        play type : solo, shared play
        :return:
        """

        if self.config.mode not in modes: return False

        if self.config.mode == self.MODE_STORY_SOLO:

            if self.config.global_shared_play_enabled == 1:

                if CTDT.template("050").click():
                    return True
            else:

                if CTDT.template("009").click():
                    return True

        elif self.config.mode == self.MODE_EVENT_SOLO:

            if self.config.global_shared_play_enabled == 1:

                if CTDT.template("050").click():
                    return True
            else:

                if CTDT.template("009").click():
                    return True

        elif self.config.mode == self.MODE_SOLO:

            if self.config.global_shared_play_enabled == 1:

                if CTDT.template("050").click():
                    return True
            else:

                if CTDT.template("009").click():
                    return True

        elif self.config.mode == self.MODE_CLUB_JOIN:

            if self.config.global_shared_play_enabled == 1:
                pass
            else:
                if CTDT.template("040").click():
                    return True

        elif self.config.mode == self.MODE_GLOBAL_SHARED:

            # global shared play
            if CTDT.template("051").click():
                return True

        elif self.config.mode == self.MODE_GLOBAL_JOIN:

            # recruit share play
            if CTDT.template("063").click():
                return True

        return False

    ########################################################################################################################

    def run_010(self, modes: set):
        """
        select friend -> FP
        :return:
        """

        if self.config.mode not in modes: return False

        if CTDT.template("010").click():
            return True

        return False

    ########################################################################################################################

    def run_012(self, modes: set):
        """
        after match -> go to scenario list
        :return:
        """

        # sometimes 012 and sometimes 028 appears fo scenario list
        # this one is when the result is win
        if self.config.mode not in modes: return False

        if CTDT.template("012").click():
            return True
        else:
            # go to scenario list button
            # this one is when the result is loss
            if CTDT.template("038").click():
                return True

        return False

    ########################################################################################################################

    def run_013(self, modes: set):
        """
        after match - you win
        :return:
        """

        if self.config.mode not in modes: return False

        if CTDT.template("013").click():
            return True

        return False

    ########################################################################################################################

    def run_014(self, modes: set):
        """
        after match - breakdown
        :return:
        """

        if self.config.mode not in modes: return False

        if CTDT.template("014").click():
            return True

        return False

    ########################################################################################################################

    def run_015(self, modes: set):
        """
        after match - rank up
        :return:
        """

        if self.config.mode not in modes: return False

        if CTDT.template("015").click():
            self.send_telegram_message("Rank Up : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            return True

        return False

    ########################################################################################################################

    def run_016(self, modes: set):
        """
        energy recovery dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # if energy recovery dialog is open
        if CTDT.template("016").available():

            if self.energy_recovery_send_telegram_datetime is None:
                # inform in telegram that we are out of energy
                self.send_telegram_message(
                    "Out of Energy : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                # sleep to avoid problem in telegram bot
                time.sleep(0.2)

                self.send_telegram_message(
                    "Out of Energy : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), notify=True)

                self.energy_recovery_send_telegram_datetime = datetime.now()
            else:

                # check previous time we sent the telegram msg
                diff = datetime.now() - self.energy_recovery_send_telegram_datetime
                seconds = diff.total_seconds()

                # reset time after timeout
                # after reaching timeout period which is 1 hour by default we will set datetime to None
                # so we can send out of energy msg in telegram again
                if seconds >= self.config.wait_telegram_msg_energy_recovery:
                    self.energy_recovery_send_telegram_datetime = None

            # if energy recovery config is wait to recover energy over time
            if self.config.energy_recovery == self.EnergyRecovery_WaitToRecover:

                if self.energy_recovery_dialog_datetime is None:
                    # this is the first time we saw energy recovery dialog
                    # so we should save the time
                    self.energy_recovery_dialog_datetime = datetime.now()
                else:

                    # check the amount of time energy recovery dialog is open
                    diff = datetime.now() - self.energy_recovery_dialog_datetime
                    seconds = diff.total_seconds()

                    # click on  cancel button
                    # app will trigger another play after this
                    if seconds > self.config.wait_energy_recovery:
                        # click on cancel button
                        CTDT.template("017").click()

                        # reset for next use
                        self.energy_recovery_dialog_datetime = None

                return True
            elif self.config.energy_recovery == self.EnergyRecovery_Ad:

                # view ad button
                if CTDT.template("066").click():
                    # save start time of viewing ad
                    self.ad_viewing_time = datetime.now()
                    self.send_telegram_message(
                        "Start Watching AD : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    return True
                else:

                    if self.exit_app_for_ad_time is None:
                        self.exit_app_for_ad_time = datetime.now()

                    # check previous time we exited from app for resetting ad
                    diff = datetime.now() - self.exit_app_for_ad_time
                    seconds = diff.total_seconds()

                    if seconds > self.config.wait_exit_app_ad:
                        # we should close app and try again
                        CTDT.point("002").click()
                        # reset flag
                        self.exit_app_for_ad_time = None
                        self.send_telegram_message(
                            "Close App : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                    return True


            # if energy recovery config is using energy balls
            elif self.config.energy_recovery == self.EnergyRecovery_Energyball:

                # if owned recovery ball is bigger than minimum restore energy
                if CTDT.ocr_number("081") > self.config.min_recovery_ball:

                    # click on restore button to recover energy
                    if CTDT.template("018").click():
                        return True

            elif self.config.energy_recovery == self.EnergyRecovery_Dreamball:
                pass

            # if we just want to inform out of energy in telegram
            elif self.config.energy_recovery == self.EnergyRecovery_None_Telegram:
                return True

        return False

    ########################################################################################################################

    def run_017(self, modes: set):
        """
        close news dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # check if new title is available
        if CTDT.template("019").available():
            # click on close button
            if CTDT.template("020").click():
                return True

        return False

    ########################################################################################################################

    def run_018(self, modes: set):
        """
        restart match after game crash
        :return:
        """

        if self.config.mode not in modes: return False

        # check if restart match dialog in open
        if CTDT.template("021").available():
            # click on restart button
            if CTDT.template("022").click():
                # inform in telegram that match is restarting
                self.send_telegram_message(
                    "Restarting Match : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return True

        return False

    ########################################################################################################################

    def run_021(self, modes: set):
        """
        after match -> special bonus
        :return:
        """

        if self.config.mode not in modes: return False

        # after match -> special bonus
        if CTDT.template("026").click():
            return True

        return False

    ########################################################################################################################

    def run_022(self, modes: set):
        """
        after match -> clear rewards
        :return:
        """

        if self.config.mode not in modes: return False

        # after match -> clear rewards
        if CTDT.template("027").click():
            return True

        return False

    ########################################################################################################################

    def run_023(self, modes: set):
        """
        club shared play button
        :return:
        """

        if self.config.mode not in modes: return False

        # click on club shared play button
        if CTDT.template("032").click():
            return True

        return False

    ########################################################################################################################

    def run_024(self, modes: set):
        """
        energy recovered dialog -> appears after energy recovery dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # if energy recovered dialog
        if CTDT.template("029").available():
            #  click ok button
            if CTDT.template("030").click():
                self.send_telegram_message(
                    "Energy Recovered : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return True

        return False

    ########################################################################################################################

    def run_025(self, modes: set):
        """
        club shared play - search again -> members
        :return:
        """

        if self.config.mode not in modes: return False

        if CTDT.template("035").available():
            # click on rank
            if CTDT.template("033").click():
                return True

            # return true for faster loop in joining game
            return True

        return False

    ########################################################################################################################

    def run_026(self, modes: set):
        """
        join button
        :return:
        """

        if self.config.mode not in modes: return False

        # click on join button
        if CTDT.template("034").click():
            self.increase_count_played_match()
            self.send_count_played_match()
            return True

        return False

    ########################################################################################################################

    def run_027(self, modes: set):
        """
        failed to join dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # failed to join dialog -> title
        if CTDT.template("036").available():

            # ok button
            if CTDT.template("037").click():
                return True

        return False

    ########################################################################################################################

    def run_028(self, modes: set):
        """
        kick off button - join
        :return:
        """

        if self.config.mode not in modes: return False

        modes1 = {self.MODE_STORY_SOLO,
                  self.MODE_EVENT_SOLO,
                  self.MODE_SOLO}

        # modes with join
        modes2 = {self.MODE_CLUB_JOIN, self.MODE_GLOBAL_JOIN}

        if self.config.mode in modes1:

            # kick off button for simple matches
            if CTDT.template("011").click():
                # send number of matched played to telegram bot
                self.increase_count_played_match()
                self.send_count_played_match()

                return True

        # kick off button with join matches
        elif self.config.mode in modes2:

            # if kick off button available
            if CTDT.template("045").available():

                # first we should count the number of members
                # and check if there is a change on it
                count_members = 0

                if not CTDT.template("042").available():
                    count_members = 1
                    if not CTDT.template("043").available():
                        count_members = 2
                        if not CTDT.template("044").available():
                            count_members = 3

                # if there is a change in number of members we should update datetime and number of members
                if count_members != self.member_joined_count:
                    # there is a change in number of members
                    self.member_joined_datetime = datetime.now()
                    self.member_joined_count = count_members

                # calculate seconds that members are waiting
                diff = datetime.now() - self.member_joined_datetime
                seconds = diff.total_seconds()

                # compare number of members with predefined wait time in config
                # for example if there 1 member wait 60 seconds then kick off
                # if there are 2 members wait 30 seconds and then kick off
                # if there are 3 members wait 5 seconds and then kick off
                kickoff = False
                if self.member_joined_count == 1:
                    if seconds > self.config.wait_after_member1_join:
                        kickoff = True
                elif self.member_joined_count == 2:
                    if seconds > self.config.wait_after_member2_join:
                        kickoff = True
                elif self.member_joined_count == 3:
                    if seconds > self.config.wait_after_member3_join:
                        kickoff = True

                # we can kick off
                if kickoff:
                    # click on kick off button
                    if CTDT.template("045").click():
                        # send number of matched played to telegram bot
                        self.increase_count_played_match()
                        self.send_count_played_match()

                        # reset variables
                        self.member_joined_datetime = None
                        self.member_joined_count = 0

                return True

        return False

    ########################################################################################################################

    def run_029(self, modes: set):
        """
        recruit button - join
        :return:
        """

        if self.config.mode not in modes: return False

        # recruit button
        if CTDT.template("041").click():
            return True

        return False

    ########################################################################################################################

    def run_030(self):
        """
        prevent screen off
        :return:
        """

        if self.prevent_screen_datetime is None:
            self.prevent_screen_datetime = datetime.now()

        diff = datetime.now() - self.prevent_screen_datetime
        seconds = diff.total_seconds()

        if seconds > self.config.prevent_screen_off:
            # click on 0,0
            pyautogui.moveTo(0, 0)
            pyautogui.click(0, 0)

            # reset datetime value
            self.prevent_screen_datetime = None

            return True

        return False

    ########################################################################################################################

    def run_031(self, modes: set):
        """
        unable to play dialog - max number of player -> shared
        :return:
        """

        if self.config.mode not in modes: return False

        # unable to play dialog - max number of player
        if CTDT.template("046").available():
            # ok button - unable to play dialog
            if CTDT.template("047").click():
                return True

        return False

    ########################################################################################################################

    def run_032(self, modes: set):
        """
        match condition have not met dialog - shared
        :return:
        """

        if self.config.mode not in modes: return False

        # match condition have not met dialog - join
        if CTDT.template("048").available():
            # close button - match condition have not met dialog
            if CTDT.template("049").click():
                return True

        return False

    ########################################################################################################################

    def run_033(self, modes: set):
        """
        connection error dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # connection error
        if CTDT.template("052").available():

            # ok button
            if CTDT.template("053").click():
                # after connection error the game goes to the first page
                self.send_telegram_message(
                    "Connection Error : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return True

        elif CTDT.template("064").available():

            # retry button
            if CTDT.template("065").click():
                # retry to connect
                self.send_telegram_message(
                    "Connection Error 2 : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                return True

        return False

    ########################################################################################################################

    def run_035(self, modes: set):
        """
        go to game -> change always
        :return:
        """

        if self.config.mode not in modes: return False

        if self.config.mode in {self.MODE_GLOBAL_SHARED, self.MODE_GLOBAL_JOIN}:

            # go to event
            if CTDT.template("023").click():
                return True

            # go to event match if we are in event match page(2) not on event page(1)
            #  we can detect it by checking if to event exchange shop is not available
            elif not CTDT.template("061").available():

                # 3rd anni pre event
                if CTDT.template("024").click():
                    return True

        elif self.config.mode in {self.MODE_STORY_SOLO}:

            # go to story mode - second page
            # use to play story mode only
            if CTDT.template("004").click():
                return True

            # begin scroll
            # if in story mode and if we are at the beginning of the scroll ( scrollbar is on left )
            # we should scroll to right
            elif CTDT.template("005").available():
                CTDT.point("001").click(clicks=5, interval=0.1)
                return True

            # end scroll
            # exact game picture ( it should change always to match)
            # for now -> story mode - evolve -> get drills all types
            elif CTDT.template("006").click():
                return True

        elif self.config.mode in {self.MODE_EVOLE_PLAYER}:

            # go to evolve player
            if CTDT.template("054").click():
                return True

        return False

    ########################################################################################################################

    def run_036(self, modes: set):
        """
        room closed dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # room closed dialog -> title
        if CTDT.template("055").available():

            # ok button
            if CTDT.template("056").click():
                return True

        return False

    ########################################################################################################################

    def run_037(self, modes: set):
        """
        after match -> shared play reward
        :return:
        """

        if self.config.mode not in modes: return False

        # after match -> shared play reward
        if CTDT.template("062").click():
            return True

        return False

    ########################################################################################################################

    def run_038(self, modes: set):
        """
        close ad
        :return:
        """

        if self.config.mode not in modes: return False

        if self.config.energy_recovery != self.EnergyRecovery_Ad:
            return False

        # close ad button
        if CTDT.template("067").available():
            # check the amount of time energy recovery dialog is open
            diff = datetime.now() - self.ad_viewing_time
            seconds = diff.total_seconds()

            if seconds > self.config.wait_finish_ad:

                # close ad after number of seconds we set in config
                if CTDT.template("067").click():
                    self.ad_viewing_time = None
                    self.send_telegram_message(
                        "End Watching AD : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    return True

            return True

        return False

    ########################################################################################################################

    def run_039(self, modes: set):
        """
        after ad - you win
        :return:
        """

        if self.config.mode not in modes: return False

        # you win
        if CTDT.template("068").click():
            return True

        return False

    ########################################################################################################################

    def run_040(self, modes: set):
        """
        after ad - dreamball lottery dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # dreamball lottery dialog -> title
        if CTDT.template("069").available():

            # dreamball lottery dialog -> next button
            if CTDT.template("070").click():
                return True
            # dreamball lottery dialog -> ok button
            elif CTDT.template("082").click():
                return True
            # dreamball lottery dialog ->  ok button ( ok / cancel )
            elif CTDT.template("083").click():
                return True

        return False

    ########################################################################################################################

    def run_041(self, modes: set):
        """
        after ad - ad viewing interrupted dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # ad viewing interrupted dialog -> title
        if CTDT.template("071").available():

            # ad viewing interrupted dialog -> ok button
            if CTDT.template("072").click(wait=self.config.wait_ad_view_interrupted):
                return True

        return False

    ########################################################################################################################

    def run_042(self, modes: set):
        """
        detect app freeze
        :return:
        """

        if self.config.mode not in modes: return False

        # detect app freeze
        # it will increase on every cycle that is present and reset 0 otherwise
        if CTDT.template("073").available():
            self.count_now_loading += 1
        elif CTDT.template("088").available():
            self.count_now_loading += 1
        else:
            self.count_now_loading = 0

        # close app and reset
        if self.count_now_loading > self.config.max_count_now_loading:
            CTDT.point("002").click()
            # inform in telegram that app is friezed
            self.send_telegram_message(
                "Freeze => Now Loading : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            self.send_telegram_message(
                "Close App : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            self.count_now_loading = 0
            return True

        return False

    ########################################################################################################################

    def run_043(self):
        """
        force exit app
        :return:
        """

        if self.telegram is None: return False

        if self.telegram.force_exit_app_flag:
            # exit and close app
            CTDT.point("002").click()
            self.send_telegram_message(
                "Close App : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            # reset flag
            self.telegram.reset_force_exit_app()

            return True

        return False

    ########################################################################################################################

    def run_044(self):
        """
        exit app
        :return:
        """

        if self.telegram is None: return False

        if self.telegram.exit_app_flag:
            # exit and close app
            CTDT.point("002").click()
            self.send_telegram_message(
                "Close App : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

            # reset exit app flag
            self.telegram.reset_exit_app()

            return True

        return False

    ########################################################################################################################

    def run_045(self):
        """
        pause app
        :return:
        """

        if self.telegram is None: return False

        if self.telegram.pause_flag:
            return True

        return False

    ########################################################################################################################

    def run_046(self):
        """
        go Home telegram command
        :return:
        """

        # if go home flag is true
        if self.telegram.go_home_flag:

            # go to Home
            if CTDT.template("074").click():
                self.telegram.reset_go_home_flag()
                return True

        return False

    ########################################################################################################################

    def run_047(self, modes: set):
        """
        shared play - count preparing - detect inactive user
        :return:
        """

        if self.config.mode not in modes: return False

        # if preparing available
        if CTDT.template("075").available():
            self.count_preparing = +1
        else:
            self.count_preparing = 0

        if self.count_preparing > self.config.max_count_preparing:

            # Home button
            if CTDT.template("074").click():
                # inform in telegram that user is not starting match
                self.send_telegram_message(
                    "Inactive User : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                self.count_preparing = 0
                return True

        return False

    ########################################################################################################################

    def run_048(self, modes: set):
        """
        shared play - confirm cancel dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # confirm cancel dialog
        if CTDT.template("076").available():
            # ok button on confirm cancel dialog
            if CTDT.template("077").click():
                return True

        return False

    ########################################################################################################################

    def run_049(self, modes: set):
        """
        after match - shared play - confirm change screen dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # confirm change screen dialog
        if CTDT.template("078").available():
            # cancel button on change screen dialog
            if CTDT.template("079").click():
                return True

        return False

    ########################################################################################################################

    def run_051(self, modes: set):
        """
        shared play - count searching - users are not sharing
        :return:
        """

        if self.config.mode not in modes: return False

        # if preparing available
        if CTDT.template("080").available():
            self.count_sharing = +1
        else:
            self.count_sharing = 0

        if self.count_sharing > self.config.max_count_sharing:

            # Home button
            if CTDT.template("074").click():
                # inform in telegram users are not sharing
                self.send_telegram_message(
                    "Failed Searching : {0}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

                self.count_sharing = 0
                return True

        return False

    ########################################################################################################################

    def run_052(self, modes: set):
        """
        after match - add friend dialog
        :return:
        """

        if self.config.mode not in modes: return False

        # add friend dialog - title
        if CTDT.template("084").available():
            # cancel button on add friend dialog
            if CTDT.template("085").click():
                return True

        return False

    ########################################################################################################################

    def run_053(self, modes: set):
        """
        new update data is available diaolg
        :return:
        """

        if self.config.mode not in modes: return False

        # new update data is available diaolg - title
        if CTDT.template("086").available():
            # new update data is available diaolg - ok button
            if CTDT.template("087").click():
                return True

        return False

    ########################################################################################################################
    ########################################################################################################################

    def run(self):

        # pause app
        if self.run_045():
            return "045"

        # force exit app
        elif self.run_043():
            return "043"

        ################## Telegram #############################

        # go Home telegram command
        elif self.run_046():
            return "046"

        ################## End Telegram #########################

        # shared play - search again -> members
        elif self.run_025(modes={self.MODE_CLUB_SHARED}):
            return "025"

        # shared play button
        elif self.run_023(modes={self.MODE_CLUB_SHARED}):
            return "023"

        # shared play - join button
        elif self.run_026(modes={self.MODE_CLUB_SHARED,
                                 self.MODE_GLOBAL_SHARED}):
            return "026"

        if self.run_007(modes={self.MODE_STORY_SOLO,
                               self.MODE_EVENT_SOLO,
                               self.MODE_SOLO,
                               self.MODE_CLUB_JOIN,
                               self.MODE_GLOBAL_SHARED,
                               self.MODE_GLOBAL_JOIN}):
            return "007"

        # energy recovered dialog
        elif self.run_024(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_JOIN}):
            return "024"

        # energy recovery dialog
        elif self.run_016(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_JOIN}):
            return "016"

        # after ad - dreamball lottery dialog
        elif self.run_040(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_GLOBAL_JOIN}):
            return "040"

        # play type : solo, shared play, join
        elif self.run_009(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "009"

        # recruit button - join
        elif self.run_029(modes={self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_JOIN}):
            return "029"

        # after ad - ad viewing interrupted dialog
        elif self.run_041(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_GLOBAL_JOIN}):
            return "041"

        # play match button
        elif self.run_008(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "008"

        # select friend
        elif self.run_010(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO}):
            return "010"

        # connection error dialog
        elif self.run_033(modes={self.MODE_STORY_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "033"

        # kick off button
        elif self.run_028(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_JOIN}):
            return "028"

        # after match - add friend dialog
        elif self.run_052(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_JOIN}):
            return "052"

        # go to scenario list
        # it should run before owned FP (run_014)
        elif self.run_012(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "012"

        # after match - you win
        elif self.run_013(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "013"

        # after match - breakdown
        elif self.run_014(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "014"

        # after match - rank up
        elif self.run_015(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_JOIN}):
            return "015"


        # after match - shared play - confirm change screen dialog
        elif self.run_049(modes={self.MODE_GLOBAL_SHARED}):
            return "049"

        # after match -> special bonus
        elif self.run_021(modes={self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "021"

        # after match -> clear rewards
        elif self.run_037(modes={self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "037"

        # after match -> clear rewards
        elif self.run_022(modes={self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "022"

        # failed to join dialog
        elif self.run_027(modes={self.MODE_CLUB_SHARED,
                                 self.MODE_GLOBAL_SHARED}):
            return "027"

        # room closed dialog
        elif self.run_036(modes={self.MODE_CLUB_SHARED,
                                 self.MODE_GLOBAL_SHARED}):
            return "036"

        # unable to play dialog - max number of player -> shared
        elif self.run_031(modes={self.MODE_CLUB_SHARED}):
            return "031"

        # match condition have not met dialog - shared
        elif self.run_032(modes={self.MODE_CLUB_SHARED}):
            return "032"

        # run app
        elif self.run_001(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "001"

        # enter app
        elif self.run_002(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "002"

        # go to story mode
        elif self.run_003(
                modes={self.MODE_STORY_SOLO,
                       self.MODE_EVENT_SOLO,
                       self.MODE_CLUB_SHARED,
                       self.MODE_GLOBAL_SHARED,
                       self.MODE_GLOBAL_JOIN}):
            return "003"

        # *** go to game
        elif self.run_035(modes={self.MODE_STORY_SOLO,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "035"

        # close news dialog
        elif self.run_017(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "017"

        # restart match dialog
        elif self.run_018(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "018"


        # close ad
        elif self.run_038(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_GLOBAL_JOIN}):
            return "038"

        # after ad - you win
        elif self.run_039(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_GLOBAL_JOIN}):
            return "039"


        # detect app freeze
        elif self.run_042(modes={self.MODE_STORY_SOLO,
                                 self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_GLOBAL_JOIN,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_CLUB_SHARED}):
            return "042"

        # shared play - count preparing - detect inactive user
        elif self.run_047(modes={self.MODE_GLOBAL_SHARED,
                                 self.MODE_CLUB_SHARED}):
            return "047"


        # shared play - count searching - users are not sharing
        elif self.run_051(modes={self.MODE_GLOBAL_SHARED,
                                 self.MODE_CLUB_SHARED}):
            return "051"

        # shared play - confirm cancel dialog
        elif self.run_048(modes={self.MODE_GLOBAL_SHARED,
                                 self.MODE_CLUB_SHARED}):
            return "048"

        # new update data is available diaolg
        elif self.run_053(modes={self.MODE_EVENT_SOLO,
                                 self.MODE_SOLO,
                                 self.MODE_CLUB_SHARED,
                                 self.MODE_CLUB_JOIN,
                                 self.MODE_GLOBAL_SHARED,
                                 self.MODE_GLOBAL_JOIN}):
            return "053"

        # prevent screen off
        elif self.run_030():
            return "030"
