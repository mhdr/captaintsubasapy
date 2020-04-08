from lib import CTDT, Config
import inspect
from datetime import datetime


class Tsubasa:
    config: Config = None

    MODE_ALL = 0
    MODE_STORY_SOLO = 1

    EnergyRecovery_None = 1
    EnergyRecovery_WaitToRecover = 2
    EnergyRecovery_Ad = 3
    EnergyRecovery_Energyball = 4
    EnergyRecovery_Dreamball = 5

    energy_recovery_dialog_datetime: datetime = None

    def __init__(self):
        self.config = Config.get_instance()

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

        modes = {self.MODE_STORY_SOLO}
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
        difficulty - very hard
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("007").click(2):
            return True

        return False

    ########################################################################################################################

    def run_008(self):
        """
        play match button
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

        modes = {self.MODE_STORY_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("009").click():
            return True

        return False

    ########################################################################################################################

    def run_010(self):
        """
        select friend
        :return:
        """
        modes = {self.MODE_STORY_SOLO}
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

        modes = {self.MODE_STORY_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if CTDT.locate_template("011").click():
            return True

        return False

    ########################################################################################################################

    def run_012(self):
        """
        go to scenario list
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
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

        modes = {self.MODE_STORY_SOLO}
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

        modes = {self.MODE_STORY_SOLO}
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

        modes = {self.MODE_STORY_SOLO}
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

        modes = {self.MODE_STORY_SOLO}
        if self.MODE_ALL not in modes:
            if self.config.mode not in modes: return False

        if self.config.energy_recovery == self.EnergyRecovery_None:
            return True

        # if energy recovery dialog is open
        if CTDT.locate_template("016").available():

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
            elif self.config.energy_recovery == self.EnergyRecovery_Energyball:
                pass
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
    ########################################################################################################################

    def run(self):

        # difficulty - very hard
        if self.run_007():
            return

        # solo play
        elif self.run_009():
            return

        # play match button
        elif self.run_008():
            return

        # select friend
        elif self.run_010():
            return

        # kick off button
        elif self.run_011():
            return

        # go to scenario list
        elif self.run_012():
            return

        # after match - you win
        elif self.run_013():
            return

        # after match - breakdown
        elif self.run_014():
            return

        # after match - rank up
        elif self.run_015():
            return

        # energy recovery dialog
        elif self.run_016():
            return

        # go to story mode
        if self.run_003():
            return

        # go to story mode - second page
        elif self.run_004():
            return

        # if in story mode and if we are at the beginning of the scroll ( scrollbar is on left )
        # we should scroll to right
        elif self.run_005():
            return

        # story mode - road to 2002
        elif self.run_006():
            return


        ######################################## MODE_ALL ##############################################################

        # enter app
        elif self.run_001():
            return

        # enter app
        elif self.run_002():
            return

        # close news dialog
        elif self.run_017():
            return
