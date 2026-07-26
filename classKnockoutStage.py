# کلاس KnockoutStage
class KnockoutStage:
    """کلاس یک مرحله از دور حذفی"""

    def __init__(self, round_name, matches):
        self.round_name = round_name
        self.matches = matches

    def round_play(self):
        """اجرای تمام مسابقات این مرحله"""
        for match in self.matches:
            match.play()

    def winners_get(self):
        """برگرداندن لیست تیم های برنده"""
        return [match.winner for match in self.matches]

    def results_display(self):
        """چاپ خلاصه نتایج تمام مسابقات این مرحله"""
        print(f"===== {self.round_name} =====")
        for match in self.matches:
            print(match)

