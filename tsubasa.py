from telegram import Bot

from lib import CTDT, Config
from datetime import datetime


class Tsubasa:
    config: Config = None

    MODE_ALL = 0
    MODE_STORY_SOLO = 1
    MODE_EVENT_SOLO = 2

    EnergyRecovery_None = 1
    EnergyRecovery_WaitToRecover = 2
    EnergyRecovery_Ad = 3
    EnergyRecovery_Energyball = 4
    EnergyRecovery_Dreamball = 5

    Difficulty_Normal = 1
    Difficulty_Hard = 2
    Difficulty_VeryHard = 3
    Difficulty_Extreme = 4

    energy_recovery_dialog_datetime: datetime = None

    count_played_match: int = 0
    bot: Bot

    def __init__(self):
        self.config = Config.get_instance()
        self.bot = Bot(token=self.config.telegram_token)

    def increase_count_played_match(self):
        self.count_played_match += 1

    def send_count_played_match(self):
        if self.config.telegram_disabled == 0:
            output: str = "Count : {0} , Date : {1}".format(self.count_played_match, datetime.now())
            self.bot.send_message(self.config.telegram_chatid, output)

    def send_telegram_message(self, msg: str):
        self.bot.send_message(self.config.telegram_chatid, msg)

    ########################################################################################################################

    def run_001(self):
        """
        run app
        :return:
        """

        modes = {self.MODE_ALL}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("001").click(wait=4):
            self.send_telegram_message("Run App : {0}".format(datetime.now()))
            return True

        return False

    ########################################################################################################################

    def run_002(self):
        """
        enter app
        :return:
        """

        modes = {self.MODE_ALL}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("002").click(wait=5):
            return True

        return False

    ########################################################################################################################

    def run_003(self):
        """
        go to story mode
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("003").click():
            return True

        return False

    ########################################################################################################################

    def run_004(self):
        """
        go to story mode - second page
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("004").click():
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
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("005").available():
            CTDT.click_location("001", clicks=5, interval=0.1)
            return True

        return False

    ########################################################################################################################

    def run_006(self):
        """
        story mode - road to 2002
        :return:
        """
        modes = {self.MODE_STORY_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("006").click():
            return True

        return False

    ########################################################################################################################

    def run_007(self):
        """
        difficulty
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if self.config.difficulty == self.Difficulty_Normal:
            pass
        elif self.config.difficulty == self.Difficulty_Hard:
            pass
        elif self.config.difficulty == self.Difficulty_VeryHard:

            # difficulty - very hard
            if CTDT.locate_template("007").click(2):
                return True

        elif self.config.difficulty == self.Difficulty_Extreme:

            # difficulty - extreme
            if CTDT.locate_template("025").click(2):
                return True

        return False

    ########################################################################################################################

    def run_008(self):
        """
        play match button -> with skip ticket
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("008").click(1):
            return True

        return False

    ########################################################################################################################

    def run_009(self):
        """
        solo play
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("009").click():
            return True

        return False

    ########################################################################################################################

    def run_010(self):
        """
        select friend -> FP
        :return:
        """
        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("010").click():
            return True

        return False

    ########################################################################################################################

    def run_011(self):
        """
        kick off button
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("011").click():
            # send number of matched played to telegram bot
            self.increase_count_played_match()
            self.send_count_played_match()

            return True

        return False

    ########################################################################################################################

    def run_012(self):
        """
        go to scenario list
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("012").click():
            return True

        return False

    ########################################################################################################################

    def run_013(self):
        """
        after match - you win
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("013").click(wait=1):
            return True

        return False

    ########################################################################################################################

    def run_014(self):
        """
        after match - breakdown
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("014").click(wait=2):
            return True

        return False

    ########################################################################################################################

    def run_015(self):
        """
        after match - rank up
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("015").click(wait=2):
            return True

        return False

    ########################################################################################################################

    def run_016(self):
        """
        energy recovery dialog
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if self.config.energy_recovery == self.EnergyRecovery_None:
            return False

        # if energy recovery dialog is open
        if CTDT.locate_template("016").available():

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
                        CTDT.locate_template("017").click()

                        # reset for next use
                        self.energy_recovery_dialog_datetime = None

                return True
            elif self.config.energy_recovery == self.EnergyRecovery_Ad:
                pass

            # if energy recovery config is using energy balls
            elif self.config.energy_recovery == self.EnergyRecovery_Energyball:

                # click on restore button to recover energy
                if CTDT.locate_template("018").click():
                    return True

            elif self.config.energy_recovery == self.EnergyRecovery_Dreamball:
                pass

        return False

    ########################################################################################################################

    def run_017(self):
        """
        close news dialog
        :return:
        """

        modes = {self.MODE_ALL}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        # check if new title is available
        if CTDT.locate_template("019").available():
            # click on close button
            if CTDT.locate_template("020").click():
                return True

        return False

    ########################################################################################################################

    def run_018(self):
        """
        restart match after game crash
        :return:
        """

        modes = {self.MODE_ALL}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        # check if restart match dialog in open
        if CTDT.locate_template("021").available():
            # click on restart button
            if CTDT.locate_template("022").click():
                return True

        return False

    ########################################################################################################################

    def run_019(self):
        """
        story mode home -> select events
        :return:
        """

        modes = {self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        # select events mode
        if CTDT.locate_template("023").click():
            return True

        return False

    ########################################################################################################################

    def run_020(self):
        """
        event match -> select event
        :return:
        """

        modes = {self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        # select events mode
        if CTDT.locate_template("024").click():
            return True

        return False

    ########################################################################################################################

    def run_021(self):
        """
        after match -> special bonus
        :return:
        """

        modes = {self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        # after match -> special bonus
        if CTDT.locate_template("026").click():
            return True

        return False

    ########################################################################################################################

    def run_022(self):
        """
        after match -> clear rewards
        :return:
        """

        modes = {self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        # after match -> clear rewards
        if CTDT.locate_template("027").click():
            return True

        return False

    ########################################################################################################################

    def run_023(self):
        """
        play match button -> without skip ticket
        :return:
        """

        modes = {self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        # after match -> clear rewards
        if CTDT.locate_template("028").click():
            return True

        return False

    ########################################################################################################################

    def run_024(self):
        """
        energy recovered dialog -> appears after energy recovery dialog
        :return:
        """

        modes = {self.MODE_STORY_SOLO, self.MODE_EVENT_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        # if energy recovered dialog
        if CTDT.locate_template("029").available():
            #  click ok button
            CTDT.locate_template("030").click()
            return True

        return False

    ########################################################################################################################
    ########################################################################################################################

    def run(self):

        # difficulty
        if self.run_007():
            return "007"

        # solo play
        elif self.run_009():
            return "009"

        # play match button -> with skip ticket
        elif self.run_008():
            return "008"

        # play match button -> without skip ticket
        elif self.run_023():
            return "023"

        # select friend
        elif self.run_010():
            return "010"

        # kick off button
        elif self.run_011():
            return "011"

        # go to scenario list
        elif self.run_012():
            return "012"

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
