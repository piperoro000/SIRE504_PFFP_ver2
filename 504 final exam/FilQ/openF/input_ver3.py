import sys, gzip, time, statistics as stat
# from collections import defaultdict


def extract_fastq_ids(file_path):
    record_ids = []  
    record_count = 0 
    
    with gzip.open(file_path, 'rt') as file:
        line_count = 0 
        for line in file:
            line = line.strip()  
            line_count += 1
            if line_count % 4 == 1:
                record_count += 1 
                record_ids.append((record_count, line))  
                if len(record_ids) == 100:
                    break
    return record_ids

# def record_seq_phred(file_path):
#     results = []
#     Seq_Qual = {"Sequence": [], "Phred_33": []}
#     with gzip.open(file_path, 'rt') as file:
#         line_count = 0
#         sequence = ""
#         quality = ""
#         for line in file:
#             line = line.strip()
#             line_count += 1
#             if line_count % 4 == 2:
#                 sequence = line
#             elif line_count % 4 == 0:
#                 quality = line
#                 results.append((sequence, quality))  
#             if len(results) == 100:
#                 break
#         for sequence, quality in results:
#             Seq_Qual["Sequence"].append(sequence)
#             Seq_Qual["Phred_33"].append(quality)

#     return Seq_Qual

def extract_phred(file_path):
    phred_quality = []  # เก็บ Phred Quality
    with gzip.open(file_path, 'rt') as file:
        line_count = 0
        quality = ""
        for line in file:
            line = line.strip()
            line_count += 1
            if line_count % 4 == 0:  # Phred Quality อยู่ในบรรทัดที่ 4 ของแต่ละ Record
                quality = line
                phred_quality.append(quality)  # เก็บ Phred Quality

            if len(phred_quality) == 100:
                break
    return phred_quality

def QScore():
    raw_Phred = extract_phred(file_path=file_name)
    Q_Score = {}
    for rec, phred_str in enumerate(raw_Phred, start=1):
        scores = [ord(phred) - 33 for phred in phred_str] 
        Q_avg = round(sum(scores) / len(scores), 2)
        Q_Score[rec] = Q_avg
    return Q_Score


# def Qmax(): 
#     Q_max = {}
#     Q_values = QScore()
#     for rec_q, max_q in Q_values.items():
#         Q_mean = list(Q_values.values())
#         if max_q == max(Q_mean):
#             Q_max[rec_q] = max_q
#     return Q_max

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

def filter_goodread(technology):
    
    TECH_CUTOFFS = {
    1: 30,  # Illumina
    2: 20,  # Sanger
    3: 20,  # PacBio
    4: 30   # Oxford Nanopore
}
    min_cutoff = TECH_CUTOFFS.get(technology, 20)  # Default to Q20 if technology is not found
    Q_values = QScore()
    filtered_reads = {}
    
    for rec, Q_avg in Q_values.items():
        if Q_avg >= min_cutoff:
            filtered_reads[rec] = Q_avg
    
    return filtered_reads

file_name = sys.argv[1]

# start_time = time.time()
# print(extract_fastq_ids(file_name))
# # print(Qmax())
# # print(QScore())
# # print(QScore())
# # print(Qmedian())
# end_time = time.time()
# execution_time = end_time - start_time
# print (f"Time Use: {execution_time:.3f} s")

# # Test the filter_read function
# technology_id = 3  # Example technology ID for Illumina
# filtered_reads = filter_goodread(technology_id)
# print("Number of good read:", len(filtered_reads))
# print(f"Filtered reads for technology {technology_id}: {filtered_reads}")