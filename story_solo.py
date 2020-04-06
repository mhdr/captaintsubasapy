from lib import CTDT


class StorySolo:
    """
    story mode solo bonus xp
    """

    @staticmethod
    def run():

        #  run app
        if CTDT.locate_template("001").click(): return True

        # run app
        if CTDT.locate_template("002").click(): return True

        # go to story mode
        if CTDT.locate_template("003").click(): return True

        # go to story mode - second page
        if CTDT.locate_template("004").click(): return True

        # if in story mode and if we are at the beginning of the scroll ( scrollbar is on left )
        #  we should scroll to right
        if CTDT.locate_template("005").available():
            CTDT.click_location("001", clicks=5, interval=0.1)
            return True

        # story mode - road to 2002
        if CTDT.locate_template("006").click(): return True

        # difficulty - very hard
        if CTDT.locate_template("007").click(2): return True

        # solo play
        if CTDT.locate_template("009").click(): return True

        # play match button
        if CTDT.locate_template("008").click(2): return True

        # select friend
        if CTDT.locate_template("010").click(): return True

        return False
