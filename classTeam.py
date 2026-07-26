import numpy as np
import random

def generate_goals(lam):
    """
    تولید تعداد گل یک تیم با استفاده از توزیع پواسون.

    Args:
        lam (float): میانگین گل مورد انتظار (لامبدا)

    Returns:
        int: تعداد گل تولید شده (همیشه عدد صحیح غیر منفی)
    """
    if lam < 0:
        lam = 0
    goals = np.random.poisson(lam)
    return int(goals)

def simulate_penalty_kick(kicker, opponent):
    """
    شبیه سازی یک ضربه پنالتی بین یک زننده و یک دروازه بان حریف.

    Args:
        kicker (Team): تیمی که پنالتی می زند
        opponent (Team): تیم حریف (دفاع کننده)

    Returns:
        bool: True اگر پنالتی گل شود، در غیر این صورت False
    """
    probability = 0.75 + (kicker.attack - opponent.defense) / 250

    if probability < 0.6:
        probability = 0.6
    if probability > 0.9:
        probability = 0.9

    random_number = random.random()
    return random_number < probability


class Team:
    """کلاس تیم ملی فوتبال. اطلاعات و آمار هر تیم را نگه می دارد."""

    def __init__(self, name, attack, defense, rank):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank

        self.goals_for = 0       # جمع گل زده در کل مسابقات
        self.goals_against = 0   # جمع گل خورده در کل مسابقات
        self.points = 0          # امتیاز (فقط در مرحله گروهی معنا دارد)
        self.group = None        # نام گروه (بعد از قرعه کشی مقدار می گیرد)

    def goal_difference(self):
        """محاسبه تفاضل گل تیم"""
        return self.goals_for - self.goals_against

    def reset_stats(self):
        """صفر کردن آمار تیم قبل از شروع یک شبیه سازی جدید"""
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def simulate_match(self, opponent, is_knockout=False):
        """شبیه سازی نتیجه یک مسابقه ۹۰ دقیقه ای (و وقت اضافه/پنالتی در صورت نیاز)"""
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8

        self_goals = generate_goals(lambda_self)
        opponent_goals = generate_goals(lambda_opponent)

        penalty_result = None

        if is_knockout and self_goals == opponent_goals:
            et_lambda_self = lambda_self * 0.33
            et_lambda_opponent = lambda_opponent * 0.33

            et_self_goals = generate_goals(et_lambda_self)
            et_opponent_goals = generate_goals(et_lambda_opponent)

            self_goals += et_self_goals
            opponent_goals += et_opponent_goals

            if self_goals == opponent_goals:
                penalty_result = self._simulate_penalty_shootout(opponent)

        winner = None
        if is_knockout:
            if self_goals > opponent_goals:
                winner = self
            elif opponent_goals > self_goals:
                winner = opponent
            elif penalty_result is not None:
                pens_self, pens_opponent = penalty_result
                if pens_self > pens_opponent:
                    winner = self
                else:
                    winner = opponent

        return self_goals, opponent_goals, winner, penalty_result

    def _simulate_penalty_shootout(self, opponent):
        """شبیه سازی ضربات پنالتی"""
        pens_self = 0
        pens_opponent = 0

        for i in range(5):
            if simulate_penalty_kick(self, opponent):
                pens_self += 1
            if simulate_penalty_kick(opponent, self):
                pens_opponent += 1

        while pens_self == pens_opponent:
            goal_self = simulate_penalty_kick(self, opponent)
            goal_opponent = simulate_penalty_kick(opponent, self)

            if goal_self:
                pens_self += 1
            if goal_opponent:
                pens_opponent += 1

            if goal_self != goal_opponent:
                break

        return pens_self, pens_opponent

    def __str__(self):
        return self.name
