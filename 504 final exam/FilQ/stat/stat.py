import sys, gzip, time, statistics as stat
from FilQ.openF.input_ver3 import extract_fastq_ids, extract_phred

def QScore(file_path):
    raw_Phred = extract_phred(file_path)
    Q_Score = {}
    for rec, phred_str in enumerate(raw_Phred, start=1):
        scores = [ord(phred) - 33 for phred in phred_str] 
        Q_avg = round(sum(scores) / len(scores), 2)
        Q_Score[rec] = Q_avg
    return Q_Score

def Qmedian():
    Q_values = QScore()
    Q_sorted = list(sorted(Q_values.values()))
    Q2 = round(stat.median(Q_sorted),2)
    mid = len(Q_sorted) // 2 # divined into 2 groups
    if len(Q_sorted) % 2 == 0: #even data
        lower_half = Q_sorted[:mid]
        upper_half = Q_sorted[mid:]
    else: #odd data
        lower_half = Q_sorted[:mid]
        upper_half = Q_sorted[mid+1:]
    Q1 = round(stat.median(lower_half),2)
    Q3 = round(stat.median(upper_half),2)
    return Q1, Q2, Q3