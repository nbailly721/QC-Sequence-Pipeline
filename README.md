## Quality Control and Summary Metrics of Nucleotide Sequences ##

### Description

This project performs quality control and generates summary metrics for nucleotide sequences provided in a tab-delimited input file. The workflow removes sequences that contain ambiguous bases ('N'), fall below a minimum length threshold, or are duplicated. Two types of reports are produced:

1. **Removal report** – Details sequences filtered out at each QC step.  
2. **Metrics summary report** – Includes sequence length statistics, GC content, and proportions of removed sequences.  

Additionally, the workflow visualizes key aspects of the dataset, including histograms of sequence length and GC content, and a pie chart showing reasons for sequence removal. The script is fully reproducible and can be applied to any nucleotide dataset formatted as a TSV file.

### Workflow Overview

#### Data Ingestion & Preparation (Python)
- Load input sequences from a tab-delimited file (e.g., `bold.tsv`) via command-line arguments.  
- Specify the sequence column, length column, and minimum sequence length.  
- Inspect dataset size and basic metadata.

#### Quality Control Filtering
- **Ambiguous Base Filter:** Remove sequences containing 'N'.  
- **Length Filter:** Remove sequences shorter than the minimum threshold.  
- **Duplicate Filter:** Remove duplicate sequences, keeping only the first occurrence.  

#### Summary Reports
- **Removal Report (`QC_removal_report.tsv`)**  
  Contains all sequences removed during QC with the reason for removal.  

- **Metrics Summary (`QC_metrics_report.csv`)**  
  Computes metrics including min, max, mean, median, and standard deviation of sequence lengths and GC content, as well as total and reason-specific removed sequences.

#### Visualizations
- Histogram of sequence lengths (`Sequence_length_distribution.png`).  
- Histogram of GC content (`gc_base_proportion.png`).  
- Pie chart of removal reasons (`Sequence_removal_reason.png`).  

All plots are automatically saved for reporting purposes.

### Datasets Used

- **Sample Dataset:** `sample/bold.tsv` (Retrieved from the BOLD data base)
- 
  (Contains example nucleotide sequences for testing the script.)

### Processed/Generated Files

- `QC_removal_report.tsv` – Filtered-out sequences with reasons.  
- `QC_metrics_report.csv` – Summary metrics for sequences passing QC.  
- `Sequence_length_distribution.png` – Histogram of sequence lengths.  
- `gc_base_proportion.png` – Histogram of GC content.  
- `Sequence_removal_reason.png` – Pie chart showing reasons for removal.

### Packages Used

- **Python Packages**
  - `pandas` – Data manipulation and table handling.  
  - `matplotlib` – Plotting and figure export.  
  - `seaborn` – Enhanced statistical visualizations.  
  - `math` – Numeric calculations (e.g., number of histogram bins).  

### Key Results

- Visualizations of sequence length, GC content, and reasons for removal.  
- Reports documenting which sequences were filtered and summary metrics.  

### Files in This Repository

- `sequence_qc_summary.py` – Full Python script for QC and metrics generation.  
- `README.md` – This file.  
- `sample/` – Folder containing a sample TSV input and expected output files:
  - `bold.tsv` – Example input sequences.  
  - `QC_metrics_report.csv` – Example metrics summary.  
  - `QC_removal_report.tsv` – Example removal report.  
  - `Sequence_length_distribution.png` – Example histogram of sequence lengths.  
  - `gc_base_proportion.png` – Example histogram of GC content.  
  - `Sequence_removal_reason.png` – Example pie chart of removal reasons.  

### Important Notes

- The script is fully reproducible using the provided sample input.  
- Easily adaptable to other nucleotide sequence datasets by modifying command-line arguments.  
- Quality control and visualization steps are modular and can be reused independently.  

### Real-World Relevance

- Supports preprocessing of nucleotide datasets for downstream analyses (e.g., alignment, phylogenetics).  
- Helps identify low-quality or problematic sequences early in the workflow.  
- Provides a reproducible computational pipeline for QC and summary statistics.
