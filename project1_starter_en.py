"""
=====================================================
Practice Project 1: Calcium Imaging Signal Cleaning
=====================================================

BACKGROUND:
You've received raw calcium imaging data exported from microscopy software,
recorded from pancreatic beta cells. Experimental setup: 12 cells, 200 time
points each (1 frame every 0.5 sec, 100 seconds total recording).
Acetylcholine (ACh) was added at the 30-second mark (frame 60). Healthy
cells should show a rise in calcium signal (F340/F380 ratio) after
stimulation, followed by a gradual decay back to baseline.

DATA ISSUES (your job is to handle these):
1. Some time points have missing readings (NaN) — likely dropped frames
   from the imaging system.
2. Two cells (you need to identify which ones yourself) show abnormal
   signals — likely caused by focus drift during the experiment, plus
   sudden artifact spikes.

FILE: calcium_imaging_raw_data.csv
Columns:
  - cell_id: cell identifier (cell_01 ~ cell_12)
  - time_sec: time in seconds
  - F340_F380_ratio: fluorescence ratio (higher value = higher intracellular
    calcium concentration)

Your task is broken into 5 steps below, each with TODO prompts. Write the
code yourself, one section at a time. If you get stuck, share the error
message or your question with Claude for help debugging.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------
# STEP 1: Load the data and take a first look
# -----------------------------------------------------
df = pd.read_csv("calcium_imaging_raw_data.csv")

# TODO 1.1: Print the first 10 rows to check the structure
# Hint: use .head(10)


# TODO 1.2: Check basic info about the dataset (row count, data types)
# Hint: use .info()


# TODO 1.3: Check how many missing values (NaN) exist in each column
# Hint: use .isna().sum()


# -----------------------------------------------------
# STEP 2: Visualize each cell's raw signal to spot problems by eye
# -----------------------------------------------------
# Hint: plot a line chart for each cell_id (time_sec on x-axis,
# F340_F380_ratio on y-axis). Use a for-loop to plot all cells on one
# figure for easy comparison.

# TODO 2.1: Get a list of all unique cell_id values
# Hint: use df['cell_id'].unique()
cell_list = None  # <- replace with your code

# TODO 2.2: Plot — loop through each cell and plot its time series
plt.figure(figsize=(12, 6))
# for cell in cell_list:
#     cell_data = df[df['cell_id'] == cell]
#     plt.plot(cell_data['time_sec'], cell_data['F340_F380_ratio'], label=cell)
# plt.xlabel("Time (sec)")
# plt.ylabel("F340/F380 Ratio")
# plt.legend()
# plt.title("Raw Calcium Signal - All Cells")
# plt.savefig("raw_signals_all_cells.png", dpi=150)
# plt.show()

# After viewing this plot, you should be able to roughly guess which 2
# cells look abnormal. Write your guess here as a comment, then verify
# it with code in Step 4:
# My guess for abnormal cells: ____ and ____


# -----------------------------------------------------
# STEP 3: Handle missing values
# -----------------------------------------------------
# Think about this before coding (clients ask this kind of question a lot
# in freelance work):
#   - What could go wrong if you just drop rows with missing values?
#     (Hint: for time series data, dropping rows breaks the time continuity)
#   - Would interpolating from neighboring values make more sense?

# TODO 3.1: Linearly interpolate missing values, separately for each cell
# Hint: group by cell_id first, then apply .interpolate(method='linear')
# to the F340_F380_ratio column within each group. Framework below,
# fill in the rest:
#
# df_clean = df.copy()
# df_clean['F340_F380_ratio'] = df_clean.groupby('cell_id')['F340_F380_ratio'].transform(
#     lambda x: x.interpolate(method='linear')
# )

# TODO 3.2: Verify there are no more missing values after interpolation
# Hint: run .isna().sum() again to confirm


# -----------------------------------------------------
# STEP 4: Statistically flag "abnormal cells" (don't just eyeball it —
# write code that makes the decision)
# -----------------------------------------------------
# Approach:
#   Abnormal cells tend to have "too many outliers" or "unusually large
#   fluctuations." A simple method: calculate the standard deviation (std)
#   of each cell's signal. Normal cells should fall within a similar range.
#   If a cell's std is significantly higher than the others (e.g., above
#   the mean std + 2 standard deviations across all cells), flag it as
#   "potentially abnormal."

# TODO 4.1: Group by cell_id and calculate the std of F340_F380_ratio
# for each cell
# Hint: use df_clean.groupby('cell_id')['F340_F380_ratio'].std()
cell_std = None  # <- replace with your code

# TODO 4.2: Identify cells with significantly elevated std
# (e.g., above the overall mean + 2 std)
# Hint:
# threshold = cell_std.mean() + 2 * cell_std.std()
# outlier_cells = cell_std[cell_std > threshold]
# print(outlier_cells)


# -----------------------------------------------------
# STEP 5: Write a cleaning report (this is the final deliverable clients
# care about most in freelance work)
# -----------------------------------------------------
# TODO 5.1: Save the cleaned data to a new CSV file
# Hint: df_clean.to_csv("calcium_imaging_cleaned_data.csv", index=False)

# TODO 5.2: Write a short summary (3-5 sentences) covering:
#   - How many missing values were handled
#   - What method you used to handle them, and why you chose it
#   - Which cells were flagged as abnormal, and what you'd recommend the
#     client do with that data (exclude it? flag and keep it?)
#
# Write your summary directly here as a comment — practicing how to
# communicate results clearly in English is just as important as writing
# the code itself:
#
# Summary:
# ____________________________________________________
# ____________________________________________________
# ____________________________________________________


# -----------------------------------------------------
# OPTIONAL BONUS (if you want extra practice):
# -----------------------------------------------------
# 1. Plot only the "cleaned" signals and compare against the raw signal
#    plot to see how well the interpolation worked.
# 2. Calculate each normal cell's "peak response amplitude" (peak value
#    after stimulation minus baseline value) — this is one of the most
#    commonly reported metrics in electrophysiology/calcium imaging papers.
# 3. Try using scipy.optimize.curve_fit to fit an exponential rise-decay
#    function to one cell's response curve — this previews the
#    "dose-response curve" project coming up in Month 2.
