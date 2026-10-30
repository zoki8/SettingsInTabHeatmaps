import os

from heatmaps import draw_heatmap
from saliency import draw_saliency
from screens import find_images
from study import Study

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "folder", "responses.json")
IMAGES_DIR = os.path.join(BASE_DIR, "jb_heatmaps")

def main():

    study = Study(DATA_FILE)
    images = find_images(IMAGES_DIR)

    for screen_id, clicks in study.clicks_per_screen.items():
        if screen_id not in images:
            print("No image for", screen_id)
            continue
        image_name = images[screen_id]

        if clicks:
            draw_heatmap(screen_id, clicks, image_name, "clicks", "clicks")

        if screen_id in study.first_clicks_per_screen:
            first_clicks = study.first_clicks_per_screen[screen_id]
            draw_heatmap(screen_id, first_clicks, image_name, "first clicks", "first clicks")
            draw_saliency(screen_id, first_clicks, image_name)

    study.print_stats()

if __name__ == "__main__":
    main()