import os

MAIN_WINDOW = "1:12610"
CONTEXT_MENU = "1:12676"
SETTINGS_DEFAULT = "1:12541"
SETTINGS_CHANGED = "1:12401"
SETTINGS_SAVED = "1:12472"
CODE = "1:12624"
CODE_NOT_SAVED = "1:12650"

SCREEN_NAMES = {
    MAIN_WINDOW: "Main Window",
    CONTEXT_MENU: "Context menu",
    SETTINGS_DEFAULT: "Default",
    SETTINGS_CHANGED: "Changed",
    SETTINGS_SAVED: "Saved",
    CODE: "Code",
    CODE_NOT_SAVED: "Code (not saved)",
}

def find_images(folder):
    images = {}
    for name in os.listdir(folder):
        if name.startswith("[") and "]" in name:
            screen_id = name[1:name.index("]")].replace("-", ":")
            images[screen_id] = os.path.join(folder, name)
    return images
