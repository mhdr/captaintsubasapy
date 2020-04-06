from lib import CTDT, Config
import inspect


class Tsubasa:
    config: Config = None
    MODE_STORY_SOLO = 1

    def __init__(self):
        self.config = Config.get_instance()

    ########################################################################################################################

    def run_001(self):
        """
        run app
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("001").click():
            return True
        else:
            return False

    ########################################################################################################################

    def run_002(self):
        """
        enter app
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("002").click():
            return True
        else:
            return False

    ########################################################################################################################

    def run_003(self):
        """
        go to story mode
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("003").click():
            return True
        else:
            return False

    ########################################################################################################################

    def run_004(self):
        """
        go to story mode - second page
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("004").click():
            return True
        else:
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

        if CTDT.locate_template("005").available():
            CTDT.click_location("001", clicks=5, interval=0.1)
            return True

    ########################################################################################################################

    def run_006(self):
        """
        story mode - road to 2002
        :return:
        """
        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("006").click():
            return True
        else:
            return False

    ########################################################################################################################

    def run_007(self):
        """
        difficulty - very hard
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("007").click(2):
            return True
        else:
            return False

    ########################################################################################################################

    def run_008(self):
        """
        play match button
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("008").click(2):
            return True
        else:
            return False

    ########################################################################################################################

    def run_009(self):
        """
        solo play
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("009").click():
            return True
        else:
            return False

    ########################################################################################################################

    def run_010(self):
        """
        select friend
        :return:
        """
        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("010").click():
            return True
        else:
            return False

    ########################################################################################################################

    def run_011(self):
        """
        kick off button
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("011").click():
            return True
        else:
            return False

    ########################################################################################################################

    def run_012(self):
        """
        go to scenario list
        :return:
        """

        modes = {self.MODE_STORY_SOLO}
        if self.config.mode not in modes: return False

        if CTDT.locate_template("012").click():
            return True
        else:
            return False

    ########################################################################################################################
    ########################################################################################################################

    def run(self):

        # enter app
        if self.run_001():
            return

        # enter app
        elif self.run_002():
            return

        # go to story mode
        elif self.run_003():
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

        # difficulty - very hard
        elif self.run_007():
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
