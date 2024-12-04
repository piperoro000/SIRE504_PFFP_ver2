from FilQ.openF.main_extract import *
from FilQ.stat.main_stat import *  
from FilQ.filter.main_filter import *
import re
import pandas as pd # type: ignore

def pass_report_csv(file_path , Qcutoff, file_naming):
    """
    Generates a detailed TSV (tab-separated values) report containing:
        Read Number
        Read IDs
        Barcodes 
        QC status (Pass or not based on Qcutoff)
    Saves the report as a .tsv file.

    Args:
        file_path (str): Path to the input FASTQ file.
        Qcutoff (int): Quality score threshold. Reads with median quality scores equal to or exceeding this cutoff are marked as "Pass".
        file_naming (str): Name of the output TSV file.
    
    Returns:
        A .tsv file summarizing the QC status for all reads in the input FASTQ file.
    """
    result = {"Barcode": [],"Read Number": [], "Read ID": [], "QC": []}
    good_id = filter_goodread(file_path, Qcutoff)  # {nums_rec: Q_score}
    reads_id = extract_fastq_ids(file_path)  # [(nums_id, rec_ids)]

    for nums_id, rec_ids in reads_id:
        rec_id = re.match(r"^@\S+", rec_ids)  # Extract the record ID
        bar_id = re.search(r"barcode=(\S+)", rec_ids) # Extract the record ID
        if bar_id:
                barcode = bar_id.group(1)
    
        if rec_id:
            rec_id = rec_id.group(0)
            
            if nums_id in good_id:
                result["Read Number"].append(nums_id)
                result["Read ID"].append(rec_id)
                result["QC"].append("Pass")
                result["Barcode"].append(barcode)
                        
    # Convert the result to a pandas DataFrame
    df = pd.DataFrame(result)
    df.to_csv(file_naming, sep='\t', index=False)
    print(f"New TSV file '{file_naming}' written successfully with {len(result['Read Number'])} passing reads.")
 
def write_fastq(file_path, file_naming, Qcutoff):
    """
    Creates a new FASTQ file containing only the reads that pass the quality score threshold (Qcutoff).
        
    Parameters:
        file_path (str): Path to the input FASTQ file.
        file_naming (str): Name of the output FASTQ file.
        Qcutoff (int): Quality score threshold. Only reads meeting or exceeding this score are included.

    Returns:
        A .tsv file summarizing the QC status for all reads in the input FASTQ file.
    """
    # Filter good reads based on quality score
    filtered_reads = filter_goodread(file_path , Qcutoff)  # {rec_num: Q_score}

    # Extract data from the FASTQ file
    line1 = extract_fastq_ids(file_path )  # [(record_number, rec_id)]
    line2_dict = extract_sequences(file_path )  # Dictionary with barcodes as keys
    # print(line2_dict.keys())
    line2 = [ line2_dict[bar] for bar in line2_dict.keys() ]
    line2 = line2[0] + line2[1]
    print(line2)
    # for bar in line2_dict.keys():
    #     print(f"Barcode: {bar}, Sequences: {line2_dict[bar]}")
    line3 = extract_strand(file_path)
    line4 = extract_phred(file_path)  # [(record_number, quality_score)]

    # Open the new FASTQ file for writing
    with open(file_naming, "w") as new_fastq:
        for record_num in filtered_reads.keys():
            # Find the record ID for the filtered record
            # print(record_num)

            read_id = None
            for rec_num, read in line1:
                if rec_num == record_num:
                    read_id = read  # Extract rec_id

            # Find the sequence for the filtered record
            seq = None
            for rec_num, seq_data in line2:
                # print(f"input rec: {rec_num}")
                if rec_num == record_num:
                    # print(f"condition match: {rec_num}")
                    # print(f"function condition match: {record_num}")
                    seq = seq_data
                    
            dna_strand = None
            for rec_num, strand in line3:
                if rec_num == record_num:
                    dna_strand = strand

                # Find the quality score for the filtered record
            quality_score = None
            for rec_num, phred_score in line4:
                if rec_num == record_num:
                    quality_score = phred_score

                # Write the FASTQ record
            new_fastq.write(f"{read_id}\n")
            new_fastq.write(f"{seq}\n")
            new_fastq.write(f"{dna_strand}\n")
            new_fastq.write(f"{quality_score}\n")
            print(f" Rec {rec_num} successfully write ")
        
    print(f"New FASTQ file '{file_naming}' written successfully with {len(filtered_reads)} passing reads.")

