# Click heatmaps for the "Settings in a Tab" prototype

Test task for the JetBrains internship "AI-Powered UX Validation via Human Vision Simulation".

The code takes the click export from an unmoderated Lyssna test and:

- makes a heatmap of all clicks for every screen of the prototype
- makes a heatmap of only the first click of each person on every screen
- runs a simple saliency model (spectral residual, Hou & Zhang 2007) on every screen and checks how many first clicks land in the 20% most salient area, compared to a plain edge map
- prints the numbers for the report (success rate, funnel, where people gave up, what actually happened, misclicks, time, first click success)

The report with the results is in `Heatmap_report.pdf`.

## Files

- `main.py` – runs everything
- `study.py` – `Study` class that loads the data, collects the clicks and prints the stats
- `heatmaps.py` – draws the click heatmaps
- `saliency.py` – saliency map, edge map and the first click comparison
- `screens.py` – screen ids and finding the screenshot for each screen

## How to run

```
pip install -r requirements.txt
python main.py
```

`responses.json` has to be in `folder/` and the screen images in `jb_heatmaps/`, next to the code.
The images are expected to be named like `[1-12541] Default (Prototypes for research).jpeg`.
All images are saved to the `heatmaps/` folder.

The study data and the prototype screenshots are not included.
