## ========================================================
## Project: Quality Control and Summary Metrics of Nucleotide Sequences
## Description:
##   This script performs quality control and generates summary metrics 
##   for nucleotide sequences provided in a tab-delimited input file. 
##   It removes sequences that contain ambiguous bases ('N'), fall below 
##   a minimum length threshold, or are duplicated. 
##   Two types of reports are produced: 
##     1. A removal report detailing sequences filtered out at each QC step.
##     2. A metrics summary report including sequence length statistics, 
##        GC content, and proportions of removed sequences. 
##   Additionally, the script visualizes key aspects of the dataset, 
##   including histograms of sequence length and GC content, and a pie chart 
##   showing reasons for sequence removal.
## ========================================================

#_Environment Set up -----------------
import pandas as pd
from sys import argv
import matplotlib.pyplot as plt
import seaborn as sns
import math

#_Command line set up -----------------
file_input=argv[1]
dataset=pd.read_csv(file_input, sep="\t")
seq_column=argv[2]
length_column=argv[3]
min_length=int(argv[4])

#_Definition of functions -----------------

original_rows= len(dataset) 
#To determine the number of observations/sequences present in the original data set for downstream analysis.

def filter_ambiguous(dataset,seq_column):
    fail_list=[]
    for seq in dataset[seq_column]:
        n_count=seq.count('N')
        if n_count >= 1:
            fail_list.append(seq)
    removed_list=dataset[dataset[seq_column].isin(fail_list)]
    dataset_clean=dataset[~dataset[seq_column].isin(fail_list)]
    removal_reason="ambiguous_N"
    return(dataset_clean,removed_list,removal_reason)
#To later remove sequences with at least one 'N'.

def filter_length(dataset,length_column, min_length):
    fail_list=[]
    for length in dataset[length_column]:
        if length <min_length:
            fail_list.append(length)  
    removed_list=dataset[dataset[length_column].isin(fail_list)]
    dataset_clean=dataset[~dataset[length_column].isin(fail_list)]
    removal_reason="short_length"
    return(dataset_clean,removed_list,removal_reason)
#To later remove sequences with a length below the set threshold.

def filter_duplicate(dataset, seq_column):
    removed_list = dataset[dataset.duplicated(subset=seq_column, keep='first')]
    dataset_clean = dataset.drop_duplicates(subset=seq_column, keep='first')
    removal_reason = "duplicate"
    return dataset_clean, removed_list, removal_reason
#To later remove duplicate sequences and keep only the first one.

#_Creation of summary reports -----------------

#__For removed sequences -----------------
removal_records=[]
#To then append the filtered observations

data, removed, reason = filter_ambiguous(dataset, seq_column)
removal_records.append((removed, reason))
data, removed, reason = filter_length(data, length_column, min_length)
removal_records.append((removed, reason))
data, removed, reason = filter_duplicate(data, seq_column)
removal_records.append((removed, reason))
#To filter the data set to keep sequences: 
 #1. With non-ambiguous bases
 #2. With a length above the set threshold
 #3. That are duplicated.

columns_to_keep = [seq_column, length_column]
for i in range(len(removal_records)):
    df, reason = removal_records[i]
    df = df[columns_to_keep].copy()
    df.loc[:, 'reason_removed'] = reason
    removal_records[i] = df
#To label each removed sequence with the reason it failed the quality control (QC) criteria.

removal_report = pd.concat(removal_records, ignore_index=True)
#To merge all filtered-out sequences into one removal report. 

removed_rows = len(removal_report)
#To determine the number of observations/sequences removed in the filtering steps.

fraction_rows = (removed_rows / original_rows) * 100
#To determine what proportion of the original dataset was removed during the filtering steps.

removed_reason_count = removal_report['reason_removed'].value_counts()
#To quantify how many sequences were removed by each QC filtering step.

removal_report.to_csv("QC_removal_report.tsv", sep="\t", index=False)
#To export the report into the host computer

#__For metrics -----------------
data.loc[:,'GC_percentage'] = (data[seq_column].str.upper().str.count('G') + data[seq_column].str.upper().str.count('C')) / data[seq_column].str.len() * 100
#To quantity the proportion of 'G' and 'C' bases in the sequence, accounting for any lowercase bases.

summary_data = {'metric': [], 'value': []}
#To create empty containers regarding the type of metric and its value

numeric_cols = [length_column]
#To specify the numeric column in the data set for which the metrics will be calculated

if 'GC_percentage' in data.columns:
    numeric_cols.append('GC_percentage')
#To include GC percentage in the summary metrics if it is present in the dataset.

for col in numeric_cols:
    summary_data['metric'] += [f'min_{col}', f'max_{col}', f'mean_{col}', f'median_{col}', f'std_{col}']
    summary_data['value'] += [
        data[col].min(),
        data[col].max(),
        data[col].mean(),
        data[col].median(),
        data[col].std()
    ]
#To compute the metric values and assign them to the respective columns.

summary_data['metric'] += ['removed_rows', 'fraction_rows'] + [f'removed_{r}' for r in removed_reason_count.index]
summary_data['value'] += [removed_rows, fraction_rows] + list(removed_reason_count.values)
#To append filtering-related summary metrics, including total and reason-specific removed sequences.

metrics_summary = pd.DataFrame(summary_data)
metrics_summary.to_csv("QC_metrics_report.csv", index=False)
#To export the the report into the host computer

#_Visualizations -----------------

#__Summary metrics -----------------

#___ Histogram of sequence lengths -----------------
n=len(data[length_column])
number_bins=int(math.sqrt(n))
#To set up the number of bins used in both downstream histogram plots.

sns.histplot(
    data=data[length_column],
    bins=number_bins,
    color='green',
    kde=False
)
plt.title('Distribution of sequence lengths')
plt.xlabel('Frequency')
plt.ylabel('Sequence length')
plt.savefig("Sequence_length_distribution.png", dpi=300)
plt.close()
#To plot and export the figure for reporting purposes

#___ Histogram of GC content -----------------
n=len(data['GC_percentage'])
number_bins=int(math.sqrt(n))
#To set up the number of bins used in both downstream histograam plots.

sns.histplot(
    data=data['GC_percentage'],
    bins=number_bins,
    color='blue',
    kde=True #Set as true to show distribution density
)
plt.title('Proportion of G & C bases in the sequences')
plt.xlabel('Percentage')
plt.ylabel('Number of sequences')
plt.savefig("gc_base_proportion.png", dpi=300)
plt.close()
#To plot and export the figure for reporting purposes

#___ Pie chart of removal reasons -----------------
plt.pie(
     x=removed_reason_count.values,
     labels=None,
     autopct='%1.1f%%',
     colors=['orange','pink','blue'],
     startangle=90
 )
plt.legend(
    labels=removed_reason_count.index,
    loc='best',           
)
plt.title('Reason for sequence removal')
plt.savefig("Sequence_removal_reason.png", dpi=300)
plt.close()
#To plot and export the figure for reporting purposes
