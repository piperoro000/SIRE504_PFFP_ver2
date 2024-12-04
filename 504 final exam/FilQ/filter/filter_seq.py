
def filter_reads(reads_data, min_length=5000, min_quality=50):
    filtered_reads = {"Sequence": [], "Phred_33": []}
    
    for seq, quality in zip(reads_data["Sequence"], reads_data["Phred_33"]):
        # Calculate length and average quality score
        if len(seq) >= min_length:
            quality_scores = calculate_quality_score(quality)
            avg_quality = sum(quality_scores) / len(quality_scores)
            
            # Apply filter conditions
            if avg_quality >= min_quality:
                filtered_reads["Sequence"].append(seq)
                filtered_reads["Phred_33"].append(quality)
    
    return filtered_reads

# Example usage:
# Assuming R_Seq_Qual contains your read sequences and quality scores
filtered_data = filter_reads(R_Seq_Qual)
print(filtered_data)

def filter_goodseq(file_path,limit):
    # cut_off = cutoff
    Q_values = QScore(file_path,limit)
    Q_thedsold = Qmedian(file_path,limit)
    filtered_reads = {}
    for rec, Q_avg in Q_values.items():
        if rec in Q_thedsold.keys():
            # print(rec)
            q = Q_thedsold[rec]
            Q1 = int(q[0])
            Q3 = int(q[2])
            range_Q13 = list(range(Q1, Q3))
            # print(range_Q13)
            for Q in Q_avg:
                # print(Q_avg)
                # print(Q)    
                if Q in range_Q13:
                    # print(Q_avg)
                    filtered_reads.setdefault(rec, []).append(Q)
    return filtered_reads

def percent_fil_out(file_path,limit): # {rec: [Q2, %filter]}
    Q_values = QScore(file_path,limit)
    Q_thedsold = Qmedian(file_path,limit)
    Q_filtered = filter_goodseq(file_path,limit)
    percent_fil = {}
    for rec, Q_avg in Q_values.items():
        q = Q_thedsold[rec]
        if rec in Q_filtered.keys() and Q_thedsold.keys():
            percent_cutoff = ((len(Q_avg)-len(Q_filtered[rec]))/len(Q_avg))*100
            # print(f"Read Number {rec}")
            percent_fil.setdefault(rec, []).append(q[1])
            percent_fil[rec].append(round(percent_cutoff, 1))
            # print(f"Before Cut-off: {len(Q_avg)}")
            # print(f"After Cut-off: {len(Q_filtered[rec])}") 
            # print(f"% cut off: {round(percent_cutoff)}%")
    return percent_fil