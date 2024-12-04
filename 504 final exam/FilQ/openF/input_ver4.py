from FilQ.openF.main_extract import *
from FilQ.stat.main_stat import *  
from FilQ.filter.main_filter import *
import sys, gzip, time, statistics as stat

def record_seq_phred(file_path):
    results = []
    Seq_Qual = {"Sequence": [], "Phred_33": []}
    with gzip.open(file_path, 'rt') as file:
        line_count = 0
        sequence = ""
        quality = ""
        for line in file:
            line = line.strip()
            line_count += 1
            if line_count % 4 == 2:
                sequence = line
            elif line_count % 4 == 0:
                quality = line
                results.append((sequence, quality))  
            if len(results) == 30000:
                break
        for sequence, quality in results:
            Seq_Qual["Sequence"].append(sequence)
            Seq_Qual["Phred_33"].append(quality)

    return Seq_Qual

def QScore():
    raw_Phred = record_seq_phred(file_path=file_name)["Phred_33"]
    Q_Score = {}
    for rec, phred_str in enumerate(raw_Phred, start=1):
        scores = [ord(phred) - 33 for phred in phred_str]
        Q_avg = round(sum(scores) / len(scores), 2)
        Q_Score[rec] = Q_avg
    return Q_Score

def Qmedian():
    Q_values = QScore()
    Q_sorted = list(sorted(Q_values.values()))
    Q2 = round(stat.median(Q_sorted), 2)
    mid = len(Q_sorted) // 2
    if len(Q_sorted) % 2 == 0:
        lower_half = Q_sorted[:mid]
        upper_half = Q_sorted[mid:]
    else:
        lower_half = Q_sorted[:mid]
        upper_half = Q_sorted[mid+1:]
    Q1 = round(stat.median(lower_half), 2)
    Q3 = round(stat.median(upper_half), 2)
    return Q1, Q2, Q3

def filter_read():
    Q1, Q2, Q3 = Qmedian()
    Q_values = QScore()
    filtered_reads = {}
    
    for rec, Q_avg in Q_values.items():
        if Q2 <= Q_avg <= Q3:
            filtered_reads[rec] = Q_avg
    
    return filtered_reads

def show_filtered_reads_summary():
    filtered_reads = filter_read()
    num_reads = len(filtered_reads)
    median_quality_score = round(stat.median(filtered_reads.values()), 2)
    
    print(f"Number of filtered reads: {num_reads}")
    print(f"Median quality score of filtered reads: {median_quality_score}")
    
    print("Filtered reads and their quality scores:")
    print(filtered_reads)

def get_bar_readID(file_path, limit):
    result = {"Read Number": [], "Read ID": [], "Barcode": []}
    reads_id = extract_fastq_ids(file_path, limit) # [(nums_id, rec_ids)]
    for nums_id, rec_ids in reads_id:
        rec_id = re.match(r"^(@\S+) \S+ \S+ \S+ \S+ \S+ \S+", rec_ids)
        bar_id = re.search(r"barcode=(\S+)", rec_ids)
          # Extract the record ID
        if rec_id:
            rec_id = rec_id.group(0)
            result["Read Number"].append(nums_id)  # Add the Read Number
            result["Read ID"].append(rec_id)
        if bar_id:
            bar_id = bar_id.group(1)
            result["Barcode"].append(bar_id)
    result["Barcode"] = list(set(result["Barcode"]))

    return result

file_name = sys.argv[1]

start_time = time.time()
print(QScore())
print(Qmedian())
show_filtered_reads_summary()
end_time = time.time()
execution_time = end_time - start_time
print(f"Time Use: {execution_time:.3f} s")
