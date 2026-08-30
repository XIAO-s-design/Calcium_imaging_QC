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
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------
print (' STEP 1: Load the data and take a first look ') 
# -----------------------------------------------------
print("Loading data...")
df = pd.read_csv("calcium_imaging_raw_data.csv")
print(df.head(10))  # Print the first 10 rows to check the structure
print(df.info())  # Check basic info about the dataset (row count, data types)
#using the second method to check for missing values
print("-"* 20)
print(df.isna().sum())  # Check how many missing values (NaN) exist in each column

# -----------------------------------------------------
print ("STEP 2: Visualize each cell's raw signal to spot problems by eye")
# -----------------------------------------------------
print("Plotting raw signals for each cell...")
# Plot a line chart for each cell_id (time_sec on x-axis,
# F340_F380_ratio on y-axis). Use a for-loop to plot all cells on one
# figure for easy comparison.

cell_list = df['cell_id'].unique()
print(df['cell_id'].unique())    # Get a list of all unique cell_id values

# TODO 2.2: Plot — loop through each cell and plot its time series
plt.figure(figsize=(12, 6))
for cell in cell_list:
   cell_data = df[df['cell_id'] == cell]
   print(df['cell_id']==cell) 
   plt.plot(cell_data['time_sec'], cell_data['F340_F380_ratio'], label=cell)
plt.xlabel("Time (sec)")
plt.ylabel("F340/F380 Ratio")
plt.legend()
plt.title("Raw Calcium Signal - All Cells")
plt.savefig("raw_signals_all_cells.png", dpi=150) # Save the figure to a file for later reference, dots per inch (dpi) is set to 150 for good quality.
plt.show()

print("*"* 20)
cell = "cell_03"
mask = df["cell_id"] == cell
print(mask)
print(mask.sum()) # True=1,total True = 200, because each cell has 200 time points
cell_data = df[mask]
print(cell_data)
print(len(cell_data)) # 200

# After viewing this plot, My guess for abnormal cells: cell_05 and cell_09.
# I will verify this statistically in Step 4.


# -----------------------------------------------------
print ("STEP 3: Handle missing values")
# -----------------------------------------------------
#   - What could go wrong if you just drop rows with missing values?
#     (Hint: for time series data, dropping rows breaks the time continuity)
#   - Would interpolating from neighboring values make more sense?

# TODO 3.1: Linearly interpolate missing values, separately for each cell
# Hint: group by cell_id first, then apply .interpolate(method='linear')
# to the F340_F380_ratio column within each group. Framework below,
# fill in the rest:
#
df_clean = df.copy() # copy the original dataframe to a new one for cleaning, we want to keep the original data intact.
df_clean['F340_F380_ratio'] = df_clean.groupby('cell_id')['F340_F380_ratio'].transform(
   lambda x: x.interpolate(method='linear')) 
''' 
divide the df_clean into groups by cell_id, so it means each cell's data is in a separate group, 12 groups in total. 
Then we will only keep the F340_F380_ratio column, and apply the linear interpolation method to fill in the missing values. 
The transform function will return a series with the same index as the original dataframe, so we can assign it back to the F340_F380_ratio column in df_clean.
Lambda function is used to define an anonymous function that takes a series x (the F340_F380_ratio values for each cell) and applies the interpolate method to it.
Method='linear' specifies that we want to use linear interpolation, which estimates missing values by connecting the known data points with straight lines.
This is a common approach for time series data, as it preserves the overall trend and continuity of the signal.
'''
groupby = df_clean.groupby('cell_id')['F340_F380_ratio']
print(groupby) # <pandas.api.typing.SeriesGroupBy object at 0x10ae95cd0> ,groupby is lazy, it doesn't compute anything until we call a method on it. groupby is a SeriesGroupBy object.

# TODO 3.2: Verify there are no more missing values after interpolation
print(df_clean.isna().sum()) 
'''
check how many missing values (NaN) exist in each column after interpolation, should be 0 for f340_f380_ratio column.
but 'F340_F380_ratio' still has 1 missing value, probably because the first or last value of that cell is missing, and linear interpolation cannot fill in those values.
'''
print(df_clean[df_clean['F340_F380_ratio'].isna()]) #check which cell has missing value.
'''     
cell_id      time_sec  F340_F380_ratio
400  cell_03   0.0          NaN
So cell_03 has a missing value at time 0.0, which is the first time point for that cell.
But we could try to use limit_direction='both' in the interpolate method to fill in missing values at the beginning and end of the series. 
This is pandas interpolate method's parameter, which allows us to fill in missing values in both directions (forward and backward) from the known neighboring values.
'''
df_clean['F340_F380_ratio'] = df_clean.groupby('cell_id')['F340_F380_ratio'].transform(
   lambda x: x.interpolate(method='linear', limit_direction='both')
)
print(df_clean.isna().sum()) #check again, should be 0 for f340_f380_ratio column.

# -----------------------------------------------------
print ('STEP 4: Statistically flag "abnormal cells"')
# -----------------------------------------------------
# Approach:
#   Abnormal cells tend to have "too many outliers" or "unusually large
#   fluctuations." A simple method: calculate the standard deviation (std)
#   of each cell's signal. Normal cells should fall within a similar range.
#   If a cell's std is significantly higher than the others (e.g., above
#   the mean std + 2 standard deviations across all cells), flag it as
#   "potentially abnormal."

# TODO 4.1: Group by cell_id and calculate the std of F340_F380_ratio for each cell
cell_std = df_clean.groupby('cell_id')['F340_F380_ratio'].std()
# cell_std = None  # <- placeholder
print(cell_std)  # Print the std for each cell to see the range of values

# TODO 4.2: Identify cells with significantly elevated std (e.g., above the overall mean + 2 std)
print('cell_std check variance') # Print the mean of the std values across all cells to see the average variability
threshold = cell_std.mean() + 2 * cell_std.std()
outlier_cells = cell_std[cell_std > threshold]
print(outlier_cells) # Series([], Name: F340_F380_ratio, dtype: float64)
print(cell_std.mean()) #0.1874753255065197, sum = all cells std / 12
print(cell_std.std()) #0.04897702172108888, std = sqrt(sum((x - mean)^2) / n-1), calculate the standard deviation of the std values across all cells to check how much variation there is in the std values themselves.
print(threshold) #0.28542936894869747
'''
The outlier_cells output is an empty series, which means no cells have a standard deviation above the threshold.
Compare values of cell_std to the threshold, but there are no cells that exceed the threshold (0.285), the max std is 0.252, so outlier_cells is empty.
cell_05 and cell_09 are not flagged as abnormal based on this statistical method, so that means std alone is not enough to identify abnormal cells.
The reason for this could be that the abnormal cells have a lot of fluctuations, but they are not extreme enough to push the std above the threshold.
So we need to use another method to identify abnormal cells, such as looking for sudden spikes or drops in the signal that are not consistent with the rest of the cells.
'''
print('STEP 4.3: Identify cells with unusually large jumps in their signal')
max_jump = df_clean.groupby('cell_id')['F340_F380_ratio'].apply(lambda x: x.diff().abs().max())
print(max_jump) # Print the maximum jump for each cell to see if any cells have unusually large jumps in their signal.
'''
diff() calculates the difference between each consecutive value in the series,
abs() takes the absolute value of those differences, and max() finds the largest of those absolute differences for each cell.
This will help us identify cells that have sudden spikes or drops in their signal, which could indicate abnormal behavior.
'''

'''
abnormal cells tend to have two characteristics:
1. They have a slightly higher standard deviation than the other cells (the slightly overall drift, This drift has little impact on the differences between adjacent two points), but not enough to be flagged as an outlier based on the std threshold.
2. They have random spikes or drops in their signal (artifact spikes) that are not consistent with the rest of the cells, which can be identified by looking at the maximum jump in the signal.
When I used std to identify abnormal cells, std measured the overall variability of the signal (200 time points), but slightly drift + artifact spikes in the signal can cancel each other out, so std alone is not enough to identify abnormal cells.
So i used the maximum jump method to identify abnormal cells, which looks for sudden changes in the signal.
std is a measure of overall variability, while max jump is a measure of sudden changes.

So first, I used figure to visually identify abnormal cells (cell_05 and cell_09), 
then I used std to check if they are flagged as abnormal, but they were not. 
Then I used max jump to check if they have unusually large jumps in their signal, and they were flagged as abnormal.
'''

# -----------------------------------------------------
print('STEP 5: Write a cleaning report (this is the final deliverable clients')
# -----------------------------------------------------
# TODO 5.1: Save the cleaned data to a new CSV file
df_clean.to_csv('calcium_imaging_cleaned_data.csv', index=False) #keep the index=False to avoid writing the index column to the CSV file, as it is not needed for the cleaned data.

# TODO 5.2: Write a short summary (3-5 sentences) covering:
#   - How many missing values were handled
#   - What method you used to handle them, and why you chose it
#   - Which cells were flagged as abnormal, and what you'd recommend the
#     client do with that data (exclude it? flag and keep it?)
#
'''
Summary:
1. In this calcium imaging dataset, there were missing values (NaN) in the F340/F380 ratio readings for some time points, 43 values in total. 
2. To handle these missing values, I used linear interpolation within each cell's time series to estimate the missing readings based on neighboring values. 
This method was chosen because it preserves the overall trend and continuity of the signal, which is important for time series data.
But cell_03 had a missing value at the first time point (0.0 sec), which was filled using limit_direction='both' in the interpolation method to allow filling from both directions.
3. After cleaning the data, I statistically analyzed the signals and identified two abnormal cells (cell_05 and cell_09) that exhibited unusually large jumps in the signal, likely due to focus drift and artifact spikes.
4. I recommend that exclude these abnormal cells from further analysis to ensure the integrity of the results, or at least flag them for caution if they are to be included in any downstream analyses.
'''


