# Calcium Imaging Signal Cleaning & Quality Control

**A data cleaning and QC pipeline for β-cell calcium imaging time-series data**

## Overview

This project demonstrates a full data cleaning workflow for fluorescence
ratio (F340/F380) calcium imaging data collected from pancreatic beta
cells during a pharmacological stimulation experiment. The pipeline
handles common real-world issues in imaging data: missing frames,
signal drift, and measurement artifacts — using both visual inspection
and statistical outlier detection.

## Skills Demonstrated

- Time-series data wrangling with **pandas** (grouping, transformation,
  interpolation)
- Data visualization with **matplotlib** for exploratory quality control
- Statistical outlier detection (std-based thresholding) applied to
  biological signal data
- Producing a clear, client-ready written summary of data quality
  findings and recommendations

## Dataset

Simulated data mimicking a real calcium imaging experiment:
- 12 cells, 200 time points each (0.5 sec/frame, 100 sec total)
- Stimulus (ACh) applied at t = 30 sec
- Realistic imperfections: randomly dropped frames (missing values),
  and 2 cells exhibiting focus-drift artifacts

## Workflow

1. **Data loading & inspection** — check structure, types, missing values
2. **Exploratory visualization** — plot raw signals for all cells to spot
   irregularities by eye
3. **Missing value handling** — linear interpolation applied per-cell to
   preserve time-series continuity
4. **Automated outlier detection** — flag cells with abnormally high
   signal variance using a standard-deviation threshold
5. **Reporting** — cleaned dataset exported + written summary of
   findings and recommendations

## Why This Matters

This kind of cleaning pipeline is one of the most commonly requested
tasks in freelance biological/scientific data analysis work — clients
frequently need raw instrument output turned into a clean, analysis-ready
dataset with a clear explanation of what was changed and why.

## Tools Used

`Python` · `pandas` · `numpy` · `matplotlib`

## Background

Built by a PhD researcher specializing in pancreatic islet cell
electrophysiology and calcium imaging, applying real lab data-analysis
workflows to freelance-style data cleaning tasks.

---
*This is a practice/portfolio project using simulated data, built to
demonstrate data cleaning and QC skills for scientific data analysis work.*
