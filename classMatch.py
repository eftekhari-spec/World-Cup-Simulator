# کلاس Match
class Match:
    """کلاس مسابقه بین دو تیم."""

    def __init__(self, team1, team2, is_knockout=False):
        self.team1 = team1
        self.team2 = team2
        self.goals1 = 0
        self.goals2 = 0
        self.is_knockout = is_knockout
        self.winner = None
        self.penalty_result = None

    def play(self):
        """اجرای مسابقه، به روزرسانی آمار تیم ها و تعیین برنده"""
        goals1, goals2, winner, penalty_result = self.team1.simulate_match(self.team2, self.is_knockout)

        self.goals1 = goals1
        self.goals2 = goals2
        self.winner = winner
        self.penalty_result = penalty_result

        self.team1.goals_for += goals1
        self.team1.goals_against += goals2
        self.team2.goals_for += goals2
        self.team2.goals_against += goals1

        if not self.is_knockout:
            if goals1 > goals2:
                self.team1.points += 3
            elif goals2 > goals1:
                self.team2.points += 3
            else:
                self.team1.points += 1
                self.team2.points += 1

    def __str__(self):
        text = f"{self.team1.name} {self.goals1}-{self.goals2} {self.team2.name}"
        if self.penalty_result is not None:
            text += f" ({self.penalty_result[0]}-{self.penalty_result[1]} pens)"
        if self.is_knockout and self.winner is not None:
            text += f" -> برنده: {self.winner.name}"
        return text
