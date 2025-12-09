# Split Notebooks Guide

## Overview

The analysis has been split into 6 separate notebooks for better organization and clarity. Each notebook focuses on a specific aspect of the analysis.

## Notebook Structure

### 06a_data_loading_and_cleaning.ipynb
- **Purpose**: Load and clean the final CVS dataset
- **What it does**: 
  - Imports libraries
  - Loads the processed dataset
  - Cleans numeric columns
  - Formats FIPS codes
- **Run this first**: Always start here

### 06b_exploratory_analysis.ipynb
- **Purpose**: Answer key questions about clinic distribution and access
- **What it does**:
  - Q1: Analyzes clinic count distribution
  - Q2: Examines relationship between SVI and clinic access
  - Q3: Compares health burden with clinic presence
  - Q4: Identifies underserved counties
- **Prerequisites**: Run 06a first
- **Key outputs**: `health_burden_score` column created

### 06c_geographic_analysis.ipynb
- **Purpose**: Create maps showing spatial patterns
- **What it does**:
  - Map 1: Clinic distribution across US
  - Map 2: Social vulnerability index
  - Map 3: Health burden scores
  - Map 4: Access gap (need vs access)
- **Prerequisites**: Run 06a and 06b first
- **Key outputs**: Gap score calculations, geographic visualizations

### 06d_advanced_visualizations.ipynb
- **Purpose**: Create detailed statistical visualizations
- **What it does**:
  - Box plots comparing groups
  - Histograms showing distributions
  - Bar charts for top counties and states
- **Prerequisites**: Run 06a, 06b, and 06c first
- **Note**: This notebook will be created with all visualizations and explanations

### 06e_clustering_analysis.ipynb
- **Purpose**: Use K-means clustering to identify county segments
- **What it does**:
  - Prepares features for clustering
  - Determines optimal number of clusters
  - Performs K-means clustering
  - Interprets cluster results
- **Prerequisites**: Run all previous notebooks
- **Key outputs**: Cluster assignments, expansion recommendations by cluster

### 06f_business_insights.ipynb
- **Purpose**: Final business recommendations and summary
- **What it does**:
  - Summarizes all findings
  - Provides strategic recommendations
  - Identifies next steps
- **Prerequisites**: Run all previous notebooks

## Running the Notebooks

### Option 1: Run Sequentially
1. Run all cells in `06a_data_loading_and_cleaning.ipynb`
2. Run all cells in `06b_exploratory_analysis.ipynb`
3. Continue in order through `06f_business_insights.ipynb`

### Option 2: Run Independently
Each notebook can be run independently if you uncomment the data loading code at the top. However, running sequentially is recommended to maintain data consistency.

## Generating the PDF Report

### Using Quarto (Recommended)

1. **Install Quarto**: Download from https://quarto.org/docs/get-started/

2. **Render the report**:
   ```bash
   quarto render report.qmd
   ```

3. **Output**: The PDF will be saved as `report.pdf` in the project root

### What's in the Report

The Quarto report (`report.qmd`) includes:
- Executive summary with key statistics
- Distribution visualizations (histograms)
- Comparative analysis (box plots, bar charts)
- Top underserved counties
- Strategic recommendations
- All with lowercase explanations following your style

## Notes

- All notebooks use **lowercase comments** and **"what this means"** explanations
- Each visualization includes explanations similar to your original style
- The notebooks are designed to be self-contained but work best when run in sequence
- The Quarto report combines all findings into a professional PDF document

## Troubleshooting

If you encounter errors:
1. Make sure you've run previous notebooks in order
2. Check that required columns exist (health_burden_score, population, etc.)
3. Ensure all libraries are installed (pandas, numpy, matplotlib, seaborn, plotly, sklearn)

