# محمد افتخاری
# 404130383
# عنوان پروژه:  شبیه‌ساز جام جهانی 2026
# تاریخ : [1405/05/04]

# کتابخانه ها:
import random          # برای قرعه کشی و شبیه سازی پنالتی
import csv             # برای خواندن فایل تیم ها
import os              # برای بررسی وجود فایل csv
import numpy as np     # برای تولید تعداد گل با توزیع پواسون 

from classGroup import Group
from classKnockoutStage import KnockoutStage
from classMatch import Match
from classTeam import Team


# کلاس WorldCupSimulator (کلاس اصلی)
class WorldCupSimulator:
    """کلاس اصلی شبیه ساز جام جهانی."""

    def __init__(self):
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None

    def load_teams_from_csv(self, filename):
        """خواندن فایل CSV و ساخت لیست اشیاء Team"""
        try:
            self.teams = []
            with open(filename, mode='r', encoding='utf-8') as file:
                file_text = csv.reader(file)
                next(file_text, None)
                for row in file_text:
                    if not row:
                        continue
                    name, attack, defense, rank = row
                    team = Team(name, int(attack), int(defense), int(rank))
                    self.teams.append(team)

            print(f"تعداد {len(self.teams)} تیم با موفقیت بارگذاری شد.")
            return True

        except Exception as error:
            print(f"خطا در خواندن فایل: {error}")
            return False

    def groups_draw_and_seed(self, verbose=True):
        """قرعه کشی گروه ها بر اساس سیدبندی رنکینگ فیفا."""
        sorted_teams = sorted(self.teams, key=lambda t: t.rank)

        pot1 = sorted_teams[0:8]
        pot2 = sorted_teams[8:16]
        pot3 = sorted_teams[16:24]
        pot4 = sorted_teams[24:32]
        pots = [pot1, pot2, pot3, pot4]

        group_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        groups_teams = {name: [] for name in group_names}

        for pot in pots:
            shuffled_pot = pot[:]
            random.shuffle(shuffled_pot)
            for i in range(len(shuffled_pot)):
                team = shuffled_pot[i]
                group_name = group_names[i]
                team.group = group_name
                groups_teams[group_name].append(team)

        self.groups = []
        for name in group_names:
            new_group = Group(name, groups_teams[name])
            self.groups.append(new_group)

        if verbose:
            print("قرعه کشی گروه ها با موفقیت انجام شد.")

    def stage_group_run(self, verbose=True):
        """اجرای مرحله گروهی برای همه گروه ها"""
        for team in self.teams:
            team.reset_stats()

        for group in self.groups:
            group.matches_all_play()
            if verbose:
                group.display_table()

    def bracket_knockout_setup(self):
        """ساخت براکت یک هشتم نهایی طبق قانون ثابت فیفا"""
        firsts = {}
        seconds = {}
        for group in self.groups:
            first_team, second_team = group.advance_teams()
            firsts[group.name] = first_team
            seconds[group.name] = second_team

        pairs = [
            (firsts['A'], seconds['B']),
            (firsts['C'], seconds['D']),
            (firsts['E'], seconds['F']),
            (firsts['G'], seconds['H']),
            (firsts['B'], seconds['A']),
            (firsts['D'], seconds['C']),
            (firsts['F'], seconds['E']),
            (firsts['H'], seconds['G']),
        ]

        matches = [Match(t1, t2, is_knockout=True) for t1, t2 in pairs]
        self.round_of_16 = KnockoutStage('Round of 16', matches)

    def stage_knockout_run(self):
        """اجرای کامل مراحل حذفی"""
        # یک هشتم نهایی
        self.round_of_16.round_play()
        winners_r16 = self.round_of_16.winners_get()

        # یک چهارم نهایی
        qf_matches = [Match(winners_r16[i], winners_r16[i + 1], is_knockout=True) for i in range(0, len(winners_r16), 2)]
        self.quarterfinals = KnockoutStage('Quarterfinals', qf_matches)
        self.quarterfinals.round_play()
        winners_qf = self.quarterfinals.winners_get()

        # نیمه نهایی
        sf_matches = [Match(winners_qf[i], winners_qf[i + 1], is_knockout=True) for i in range(0, len(winners_qf), 2)]
        self.semifinals = KnockoutStage('Semifinals', sf_matches)
        self.semifinals.round_play()
        winners_sf = self.semifinals.winners_get()

        # فینال
        final_match = Match(winners_sf[0], winners_sf[1], is_knockout=True)
        self.final = KnockoutStage('Final', [final_match])
        self.final.round_play()

        self.champion = final_match.winner

    def simulation_full_run(self, verbose=False):
        """اجرای کامل یک دور جام جهانی (گروهی + حذفی)"""
        for team in self.teams:
            team.reset_stats()

        self.groups_draw_and_seed(verbose=verbose)
        self.stage_group_run(verbose=verbose)
        self.bracket_knockout_setup()
        self.stage_knockout_run()

        return self.champion

    def champion_likely_most(self, simulations_num=1000):
        """اجرای شبیه سازی چندباره جام جهانی و محاسبه درصد قهرمانی"""
        if simulations_num <= 0:
            print("خطا: تعداد شبیه سازی باید عددی مثبت باشد.")
            return

        champion_count = {team.name: 0 for team in self.teams}

        for _ in range(simulations_num):
            champion = self.simulation_full_run(verbose=False)
            champion_count[champion.name] += 1

        print(f"\nشبیه سازی {simulations_num} بار انجام شد.")
        print("درصد قهرمانی هر تیم:")

        sorted_results = sorted(champion_count.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_results:
            if count > 0:
                percent = (count / simulations_num) * 100
                print(f"{name}: {percent:.1f}%")

    def bracket_display(self):
        """نمایش کامل براکت حذفی مربوط به آخرین شبیه سازی انجام شده"""
        if self.round_of_16 is None:
            print("ابتدا باید یک شبیه سازی کامل انجام شود.")
            return

        print("\n===== Knockout Bracket =====")
        self.round_of_16.results_display()
        self.quarterfinals.results_display()
        self.semifinals.results_display()
        self.final.results_display()
        print(f"\n🏆 قهرمان جام جهانی: {self.champion.name}")

    def main(self):
        """تابع اصلی برنامه و مدیریت منو"""
        while True:
            print("\n===== شبیه ساز جام جهانی =====")
            print("1) بارگذاری تیم ها از فایل CSV")
            print("2) انجام قرعه کشی گروه ها (سیدبندی خودکار)")
            print("3) اجرای مرحله گروهی و نمایش جدول هر گروه")
            print("4) اجرای کامل جام (گروهی + حذفی) و نمایش براکت کامل")
            print("5) شبیه سازی 1000 باره و گزارش درصد قهرمانی")
            print("6) نمایش براکت حذفی آخرین شبیه سازی")
            print("7) خروج")

            choice = input("گزینه مورد نظر را وارد کنید: ").strip()

            if choice == '1':
                current_dir = os.path.dirname(os.path.abspath(__file__))
                filename = os.path.join(current_dir, "worldcup_2026_teams.txt")
                simulator.load_teams_from_csv(filename)

            elif choice == '2':
                if len(simulator.teams) == 0:
                    print("ابتدا تیم ها را بارگذاری کنید.")
                else:
                    simulator.groups_draw_and_seed(verbose=True)

            elif choice == '3':
                if len(simulator.teams) == 0:
                    print("ابتدا تیم ها را بارگذاری کنید.")
                elif len(simulator.groups) == 0:
                    print("ابتدا قرعه کشی گروه ها را انجام دهید.")
                else:
                    simulator.stage_group_run(verbose=True)

            elif choice == '4':
                if len(simulator.teams) == 0:
                    print("ابتدا تیم ها را بارگذاری کنید.")
                else:
                    simulator.simulation_full_run(verbose=True)
                    simulator.bracket_display()

            elif choice == '5':
                if len(simulator.teams) == 0:
                    print("ابتدا تیم ها را بارگذاری کنید.")
                else:
                    num_input = input("تعداد شبیه سازی را وارد کنید (پیش فرض 1000، برای پیش فرض خالی بگذارید): ").strip()
                    if num_input == '':
                        num_simulations = 1000
                    else:
                        try:
                            num_simulations = int(num_input)
                        except ValueError:
                            print("خطا: عدد وارد شده معتبر نیست!")
                            continue
                    simulator.champion_likely_most(num_simulations)

            elif choice == '6':
                if len(simulator.teams) == 0:
                    print("ابتدا تیم ها را بارگذاری کنید.")
                else:
                    simulator.bracket_display()

            elif choice == '7':
                print("خروج از برنامه...")
                break

            else:
                print("گزینه نامعتبر است. لطفا دوباره تلاش کنید.")

simulator = WorldCupSimulator()
simulator.main()