import json
from statistics import median
from screens import MAIN_WINDOW,CONTEXT_MENU,SETTINGS_SAVED,SCREEN_NAMES, SETTINGS_CHANGED, SETTINGS_DEFAULT

def percent(part, whole):
    if not whole:
        return "n/a"
    return f"{part / whole:.0%}"

class Study:

    def __init__(self,path):
        with open(path) as f:
            self.data = json.load(f)
        self.clicks_per_screen, self.first_clicks_per_screen = self._collect_clicks()

    def tasks(self):
        for respondent in self.data.values():
            for task in respondent["answers"].values():
                yield task

    def _collect_clicks(self):

        clicks_per_screen = {}
        first_clicks_per_screen = {}
        for task in self.tasks():
            for screen_id, clicks in task["clicks"].items():
                points=[(c["frame_click_x"], c["frame_click_y"])for c in clicks]
                clicks_per_screen.setdefault(screen_id, []).extend(points)

                if points:
                    first_clicks_per_screen.setdefault(screen_id, []).append(points[0])

        return clicks_per_screen, first_clicks_per_screen

    def first_click_correct(self, screen_id):
        correct = 0
        people = 0
        for task in self.tasks():
            clicks = task["clicks"].get(screen_id, [])
            if clicks:
                people += 1
                if clicks[0]["is_hotspot_click"]:
                    correct += 1
        return correct, people

    def print_stats(self):
        total = len(self.data)
        gave_up_on = {}
        durations_completed = []
        durations_gave_up = []
        never_opened_menu = 0
        saved_and_closed_tab = 0
        saved_and_stopped = 0
        saved_then_wandered = 0
        never_saved = 0
        completed_without_saving = 0
        completed = 0
        gave_up = 0
        hits = 0
        misses = 0
        reached = {}

        for task in self.tasks():
            path = task["path"].split(",")
            seconds = task["duration"] / 1000

            if task["result"] == "completed":
                completed += 1
                durations_completed.append(seconds)
                if SETTINGS_SAVED not in path:
                    completed_without_saving += 1
            else:
                gave_up += 1
                durations_gave_up.append(seconds)

                last = path[-1]
                gave_up_on[last] = gave_up_on.get(last, 0) + 1

                if CONTEXT_MENU not in path:
                    never_opened_menu += 1
                elif SETTINGS_SAVED in path:
                    after_saving = path[path.index(SETTINGS_SAVED):]
                    if last == MAIN_WINDOW:
                        saved_and_closed_tab += 1
                    elif after_saving == [SETTINGS_SAVED]:
                        saved_and_stopped += 1
                    else:
                        saved_then_wandered += 1
                else:
                    never_saved += 1

            screens = set(task["path"].split(","))
            for screen in screens:
                reached[screen] = reached.get(screen, 0) + 1

            for clicks in task["clicks"].values():
                for click in clicks:
                    if click["is_hotspot_click"]:
                        hits += 1
                    else:
                        misses += 1

        print("=== Task result ===")
        print("Respondents:", total)
        print("Completed:", completed, percent(completed, total))
        print("Gave up:", gave_up, percent(gave_up, total))

        print("=== Clicks ===")
        all_clicks = hits + misses
        print("Total:", all_clicks)
        print("Misclicks:", misses, percent(misses, all_clicks))

        print("=== Funnel ===")
        for screen_id, name in SCREEN_NAMES.items():
            count = reached.get(screen_id, 0)
            print(name, count, percent(count, total))

        print("=== Where they gave up ===")
        for screen_id, name in SCREEN_NAMES.items():
            if screen_id in gave_up_on:
                print(name, gave_up_on[screen_id])

        print("=== What actually happened ===")
        print("Never opened the menu:", never_opened_menu)
        print("Saved, then closed the tab:", saved_and_closed_tab)
        print("Saved, then stopped on Saved:", saved_and_stopped)
        print("Saved, went back, then gave up:", saved_then_wandered)
        print("Opened the menu but never saved:", never_saved)
        print("Completed without saving:", completed_without_saving)
        actually_done = completed - completed_without_saving + saved_and_closed_tab
        print("Saved and back in the code:", actually_done, percent(actually_done, total))

        print("=== Duration (median) ===")
        print("Completed:", round(median(durations_completed)), "s")
        print("Gave up:", round(median(durations_gave_up)), "s")

        print("=== First click on the right spot ===")
        for screen_id in [MAIN_WINDOW, CONTEXT_MENU, SETTINGS_DEFAULT, SETTINGS_CHANGED, SETTINGS_SAVED]:
            correct, people = self.first_click_correct(screen_id)
            print(SCREEN_NAMES[screen_id], correct, "of", people, percent(correct, people))
