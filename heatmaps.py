import os

import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "heatmaps")

def click_density(clicks, width, height):
    grid = np.zeros((height, width))
    for x, y in clicks:
        x = int(x)
        y = int(y)
        if 0 <= x < width and 0 <= y < height:
            grid[y, x] += 1

    grid = gaussian_filter(grid, sigma=width * 0.015)
    return np.ma.masked_where(grid < 0.05 * grid.max(), grid)

def save_figure(file_name):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    plt.savefig(file_name, bbox_inches="tight")
    plt.close()
    print("Saved:", file_name)

def draw_heatmap(screen_id, clicks, image_name, name_part, folder_name):
    image = Image.open(image_name)
    width, height = image.size

    plt.figure(figsize=(16, 10))
    plt.imshow(image)
    plt.imshow(click_density(clicks, width, height), cmap="jet", alpha=0.5)
    plt.title(os.path.basename(image_name) + " - " + str(len(clicks)) + " " + name_part)
    plt.axis("off")

    save_figure(os.path.join(OUTPUT_DIR, folder_name, "heatmap_" + name_part.replace(" ", "_") + "_" + screen_id.replace(":", "-") + ".png"))