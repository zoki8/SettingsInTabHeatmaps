import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, sobel, uniform_filter

from heatmaps import save_figure, OUTPUT_DIR
from study import percent


def saliency_map(image):
    width, height = image.size
    small_height = round(height * 128 / width)
    gray = np.array(image.convert("L").resize((128, small_height)), dtype=float)

    spectrum = np.fft.fft2(gray)
    log_amplitude = np.log(np.abs(spectrum) + 1e-8)
    phase = np.angle(spectrum)
    residual = log_amplitude - uniform_filter(log_amplitude, size=3)
    saliency = np.abs(np.fft.ifft2(np.exp(residual + 1j * phase))) ** 2
    saliency = gaussian_filter(saliency, sigma=2)

    saliency = np.array(Image.fromarray(saliency.astype(np.float32)).resize((width, height)))
    return saliency / saliency.max()

def edge_map(image):
    gray = np.array(image.convert("L"), dtype=float)
    edges = np.hypot(sobel(gray, axis=0), sobel(gray, axis=1))
    edges = gaussian_filter(edges, sigma=image.size[0] * 0.01)
    return edges / edges.max()

def count_inside(values, clicks):
    threshold = np.percentile(values, 80)
    inside = 0
    for x,y in clicks:
        x=int(x)
        y=int(y)
        if 0<=x<values.shape[1] and 0<=y<values.shape[0] and values[y,x] >= threshold:
            inside += 1
    return inside

def draw_saliency(screen_id, first_clicks, image_name):
    
    image=Image.open(image_name).convert("RGB")
    saliency = saliency_map(image)

    threshold = np.percentile(saliency, 80)
    inside = count_inside(saliency, first_clicks)
    inside_edges = count_inside(edge_map(image), first_clicks)
    n = len(first_clicks)
    print(screen_id, "first clicks in top 20% -", "saliency:", percent(inside, n), "edges only:", percent(inside_edges, n))
    
    shown = np.ma.masked_where(saliency < threshold, saliency)
    plt.figure(figsize=(16, 10))
    plt.imshow(image)
    plt.imshow(shown, cmap="jet", alpha=0.5)
    xs = [c[0] for c in first_clicks]
    ys = [c[1] for c in first_clicks]
    plt.scatter(xs, ys, s=15, color="black")
    plt.title(os.path.basename(image_name) + " - predicted saliency + " + str(len(first_clicks)) + " first clicks")
    plt.axis("off")
    
    save_figure(os.path.join(OUTPUT_DIR, "saliency", "saliency_" + screen_id.replace(":", "-") + ".png"))
    