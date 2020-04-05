from lib import CTDT


class Tsubasa:

    @staticmethod
    def solo():
        #  run app
        if CTDT.locate_template("001").click(): return True

        # run app
        if CTDT.locate_template("002").click(): return True

        # go to story mode
        if CTDT.locate_template("003").click(): return True

        # go to story mode - second page
        if CTDT.locate_template("004").click(): return True

        if CTDT.locate_template("005").available():
            CTDT.click_location(1758, 889, clicks=5, interval=0.1)
            return True

        return False
