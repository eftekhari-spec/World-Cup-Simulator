
from classMatch import Match

# کلاس Group
class Group:
    """کلاس گروه."""

    def __init__(self, name, teams):
        self.name = name
        self.teams = teams

    def matches_all_play(self):
        """اجرای تمام مسابقات گروه"""
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match = Match(self.teams[i], self.teams[j], is_knockout=False)
                match.play()

    def ranking_get(self):
        """رتبه بندی تیم های گروه"""

        teams_sorted = sorted(
            self.teams,
            key=lambda t: (t.points, t.goal_difference(), t.goals_for, -t.rank),
            reverse=True
        )
        return teams_sorted

    def advance_teams(self):
        """برگرداندن دو تیم صعود کننده"""
        ranking = self.ranking_get()
        return ranking[0], ranking[1]

    def display_table(self):
        """چاپ جدول رده بندی گروه"""
        print(f"===== Group {self.name} =====")
        ranking = self.ranking_get()
        for i, team in enumerate(ranking, start=1):
            gd = team.goal_difference()
            gd_text = f"+{gd}" if gd > 0 else str(gd)
            print(f"{i}. {team.name}: {team.points} pts, GD {gd_text}, GF {team.goals_for}")

