from telegram import Bot

from lib import CTDT, Config
from datetime import datetime


class Tsubasa:
    config: Config = None

    MODE_STORY_SOLO = 1
    MODE_EVENT_SOLO = 2
    MODE_SOLO = 3
    MODE_CLUB_SHARED = 4

    EnergyRecovery_None = 1
    EnergyRecovery_WaitToRecover = 2
    EnergyRecovery_Ad = 3
    EnergyRecovery_Energyball = 4
    EnergyRecovery_Dreamball = 5
    EnergyRecovery_None_Telegram = 6

    Difficulty_Normal_Horizontal = 1
    Difficulty_Hard_Horizontal = 2
    Difficulty_VeryHard_Horizontal = 3
    Difficulty_Extreme_Horizontal = 4
    Difficulty_Normal_Vertical = 5
    Difficulty_Hard_Vertical = 6
    Difficulty_VeryHard_Vertical = 7
    Difficulty_Extreme_Vertical = 8

    Telegram_Disabled = 0
    Telegram_Enabled = 1

    # the time energy recovery dialog is opened
    # we use this to open and close energy recovery dialog once in a three minutes
    energy_recovery_dialog_datetime: datetime = None

    # the time we sent a msg in telegram that we are out of energy
    # because we send this msg once in an hour
    energy_recovery_send_telegram_datetime = None

    count_played_match: int = 0
    bot: Bot

    def __init__(self):
        self.config = Config.get_instance()
        if self.config.telegram_disabled == 0:
            self.bot = Bot(token=self.config.telegram_token)

    def increase_count_played_match(self):
        self.count_played_match += 1

    def send_count_played_match(self):
        try:
            if self.config.telegram_disabled == 0:
                output: str = "Count : {0} , Date : {1}".format(self.count_played_match, datetime.now())
                self.bot.send_message(self.config.telegram_chatid, output)
        except Exception as ex:
            print(str(ex))

    def send_telegram_message(self, msg: str):
        try:
            if self.config.telegram_disabled == 0:
                self.bot.send_message(self.config.telegram_chatid, msg)
        except Exception as ex:
            print(str(ex))

    ########################################################################################################################

    def run_001(self):
        """
        run app
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        if CTDT.template("001").click(wait=4):
            self.send_telegram_message("Run App : {0}".format(datetime.now()))
            return True

        return False

    ########################################################################################################################

    def run_002(self):
        """
        enter app
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        if CTDT.template("002").click(wait=5):
            return True

        return False

    ########################################################################################################################

    def run_003(self):
        """
        go to story mode
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        if CTDT.template("003").click():
            return True

        return False

    ########################################################################################################################

    def run_004(self):
        """
        go to story mode - second page
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("004").click():
            return True

        return False

    ########################################################################################################################

    def run_005(self):
        """
        if in story mode and if we are at the beginning of the scroll ( scrollbar is on left )
        we should scroll to right
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("005").available():
            CTDT.point("001").click(clicks=5, interval=0.1)
            return True

        return False

    ########################################################################################################################

    def run_006(self):
        """
        story mode - road to 2002
        :return:
        """
        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("006").click():
            return True

        return False

    ########################################################################################################################

    def run_007(self):
        """
        difficulty
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        if self.config.difficulty == self.Difficulty_Normal_Horizontal:
            pass
        elif self.config.difficulty == self.Difficulty_Hard_Horizontal:
            pass
        elif self.config.difficulty == self.Difficulty_VeryHard_Horizontal:

            # difficulty - very hard horizontal
            if CTDT.template("007").click():
                return True

        elif self.config.difficulty == self.Difficulty_Extreme_Horizontal:

            # difficulty - extreme horizontal
            if CTDT.template("025").click():
                return True

        elif self.config.difficulty == self.Difficulty_Normal_Vertical:

            # difficulty - normal vertical
            if CTDT.template("039").click():
                return True

        elif self.config.difficulty == self.Difficulty_Hard_Vertical:
            pass

        elif self.config.difficulty == self.Difficulty_VeryHard_Vertical:

            # difficulty - very hard vertical
            if CTDT.template("031").click():
                return True

        elif self.config.difficulty == self.Difficulty_Extreme_Vertical:
            pass

        return False

    ########################################################################################################################

    def run_008(self):
        """
        play match button
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
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

    def run_009(self):
        """
        solo play
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("009").click():
            return True

        return False

    ########################################################################################################################

    def run_010(self):
        """
        select friend -> FP
        :return:
        """
        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("010").click():
            return True

        return False

    ########################################################################################################################

    def run_011(self):
        """
        kick off button
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("011").click():
            # send number of matched played to telegram bot
            self.increase_count_played_match()
            self.send_count_played_match()

            return True

        return False

    ########################################################################################################################

    def run_012(self):
        """
        after match -> go to scenario list
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("012").click(delay=1):
            return True

        return False

    ########################################################################################################################

    def run_013(self):
        """
        after match - you win
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO, self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        if CTDT.template("013").click():
            return True

        return False

    ########################################################################################################################

    def run_014(self):
        """
        after match - breakdown
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("014").click():
            return True

        return False

    ########################################################################################################################

    def run_015(self):
        """
        after match - rank up
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.template("015").click():
            return True

        return False

    ########################################################################################################################

    def run_016(self):
        """
        energy recovery dialog
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        if self.config.energy_recovery == self.EnergyRecovery_None:
            return False

        # if energy recovery dialog is open
        if CTDT.template("016").available():

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
                pass

            # if energy recovery config is using energy balls
            elif self.config.energy_recovery == self.EnergyRecovery_Energyball:

                # click on restore button to recover energy
                if CTDT.template("018").click():
                    return True

            elif self.config.energy_recovery == self.EnergyRecovery_Dreamball:
                pass

            # if we just want to inform out of energy in telegram
            elif self.config.energy_recovery == self.EnergyRecovery_None_Telegram:

                if self.energy_recovery_send_telegram_datetime is None:
                    # inform in telegram that we are out of energy
                    self.send_telegram_message("Out of energy : {0}".format(datetime.now()))

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

                return True

        return False

    ########################################################################################################################

    def run_017(self):
        """
        close news dialog
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        # check if new title is available
        if CTDT.template("019").available():
            # click on close button
            if CTDT.template("020").click():
                return True

        return False

    ########################################################################################################################

    def run_018(self):
        """
        restart match after game crash
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        # check if restart match dialog in open
        if CTDT.template("021").available():
            # click on restart button
            if CTDT.template("022").click():
                return True

        return False

    ########################################################################################################################

    def run_019(self):
        """
        story mode home -> select events
        :return:
        """

        modes = {self.MODE_EVENT_SOLO}
        if self.config.mode not in modes: return False

        # select events mode
        if CTDT.template("023").click():
            return True

        return False

    ########################################################################################################################

    def run_020(self):
        """
        event match -> select event
        :return:
        """

        modes = {self.MODE_EVENT_SOLO}
        if self.config.mode not in modes: return False

        # select events mode
        if CTDT.template("024").click():
            return True

        return False

    ########################################################################################################################

    def run_021(self):
        """
        after match -> special bonus
        :return:
        """

        modes = {self.MODE_EVENT_SOLO, self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        # after match -> special bonus
        if CTDT.template("026").click():
            return True

        return False

    ########################################################################################################################

    def run_022(self):
        """
        after match -> clear rewards
        :return:
        """

        modes = {self.MODE_EVENT_SOLO, self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        # after match -> clear rewards
        if CTDT.template("027").click():
            return True

        return False

    ########################################################################################################################

    def run_023(self):
        """
        club shared play button
        :return:
        """

        modes = {self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        # click on club shared play button
        if CTDT.template("032").click():
            return True

        return False

    ########################################################################################################################

    def run_024(self):
        """
        energy recovered dialog -> appears after energy recovery dialog
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO, self.MODE_SOLO}
        if self.config.mode not in modes: return False

        # if energy recovered dialog
        if CTDT.template("029").available():
            #  click ok button
            CTDT.template("030").click()
            return True

        return False

    ########################################################################################################################

    def run_025(self):
        """
        club shared play - accepting member list -> rank
        :return:
        """

        modes = {self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        if CTDT.template("035").available():
            # click on rank
            if CTDT.template("033").click():
                return True

            # return true for faster loop in joining game
            return True

        return False

    ########################################################################################################################

    def run_026(self):
        """
        join button
        :return:
        """

        modes = {self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        # click on join button
        if CTDT.template("034").click():
            self.increase_count_played_match()
            self.send_count_played_match()
            return True

        return False

    ########################################################################################################################

    def run_027(self):
        """
        failed to join dialog
        :return:
        """

        modes = {self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        # failed to join dialog -> title
        if CTDT.template("036").available():

            # ok button
            if CTDT.template("037").click():
                return True

        return False

    ########################################################################################################################

    def run_028(self):
        """
        go to scenario list ->  shared play
        :return:
        """

        modes = {self.MODE_CLUB_SHARED}
        if self.config.mode not in modes: return False

        # go to scenario list button
        if CTDT.template("038").click():
            return True

        return False

    ########################################################################################################################
    ########################################################################################################################

    def run(self):

        # club shared play - accepting member list -> rank
        if self.run_025():
            return "025"

        # club shared play button
        elif self.run_023():
            return "023"

        # join button
        elif self.run_026():
            return "024"

        # difficulty
        if self.run_007():
            return "007"

        # solo play
        elif self.run_009():
            return "009"

        # play match button
        elif self.run_008():
            return "008"

        # select friend
        elif self.run_010():
            return "010"

        # kick off button
        elif self.run_011():
            return "011"

        # go to scenario list
        elif self.run_012():
            return "012"

        # go to scenario list -> shared play
        elif self.run_028():
            return "028"

        # after match - you win
        elif self.run_013():
            return "013"

        # after match - breakdown
        elif self.run_014():
            return "014"

        # after match - rank up
        elif self.run_015():
            return "015"

        # energy recovered dialog
        elif self.run_024():
            return "024"

        # energy recovery dialog
        elif self.run_016():
            return "016"

        # go to story mode
        elif self.run_003():
            return "003"

        # go to story mode - second page
        elif self.run_004():
            return "004"

        # if in story mode and if we are at the beginning of the scroll ( scrollbar is on left )
        # we should scroll to right
        elif self.run_005():
            return "005"

        # story mode - road to 2002
        elif self.run_006():
            return "006"

        # story mode home -> select events
        elif self.run_019():
            return "019"

        # event matche -> select event
        elif self.run_020():
            return "020"

        # after match -> special bonus
        elif self.run_021():
            return "021"

        # after match -> clear rewards
        elif self.run_022():
            return "022"

        # failed to join dialog
        elif self.run_027():
            return "027"

        ######################################## MODE_ALL ##############################################################

        # enter app
        elif self.run_001():
            return "001"

        # enter app
        elif self.run_002():
            return "002"

        # close news dialog
        elif self.run_017():
            return "017"

        # restart match dialog
        elif self.run_018():
            return "018"
