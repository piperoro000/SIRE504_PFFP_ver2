from FilQ.openF.main_extract import *
from FilQ.stat.main_stat import *  
from FilQ.filter.main_filter import *
import re
import pandas as pd # type: ignore

def rep_id_pass(technology, file_path, limit):
    """
    Report all reads with their Read Number, IDs, and QC status (Pass or Not Pass).

    Args:
        technology (int): Sequencing technology ID.
        file_path (str): Path to the FastQ file.
        limit (int): Maximum number of records to process.

    Returns:
        pandas.DataFrame: A DataFrame containing Read Numbers, Read IDs, and QC status.
    """
    result = {"Barcode": [],"Read Number": [], "Read ID": [], "QC": []}
    good_id = filter_goodread(technology, file_path, limit)  # {nums_rec: Q_score}
    reads_id = extract_fastq_ids(file_path, limit)  # [(nums_id, rec_ids)]

    # Convert good_id keys to a set for faster lookup
    good_ids_set = set(good_id.keys())

    for nums_id, rec_ids in reads_id:
        rec_id = re.match(r"^@\S+", rec_ids)  # Extract the record ID
        bar_id = re.search(r"barcode=(\S+)", rec_ids) # Extract the record ID
        if bar_id:
                barcode = bar_id.group(1)
                result["Barcode"].append(barcode)
        result["Barcode"] = list(set(result["Barcode"]))
        if rec_id:
            rec_id = rec_id.group(0)
            if nums_id in good_ids_set:
                result["Read Number"].append(nums_id)
                result["Read ID"].append(rec_id)
                result["QC"].append("Pass")
            else:
                result["QC"].append("Not Pass")
                # print(f"Number of Bad Read: {len([qc for qc in result['QC'] if qc == 'Not Pass'])}")
    # print(f"{result["Barcode"][0]}")
    for barcode in result["Barcode"]:
        print(barcode)
        print(f"Read Number of Good Read: {result["Read Number"]}")
        print(f"Read ID of Good Read: {result["Read ID"]}")
        print(f"Number of Good Read: {len([qc for qc in result['QC'] if qc == 'Pass'])}")
    print(f"Number of Bad Read: {len([qc for qc in result['QC'] if qc == 'Not Pass'])}")

    
    # Convert the result to a pandas DataFrame
    df = pd.DataFrame(result)
    return df
    # return result

def filter_pass_reads(technology, file_path, limit):
    """
    Filter only the rows where QC status is 'Pass'.

    Args:
        df (pandas.DataFrame): DataFrame containing Read Numbers, Read IDs, and QC status.

    Returns:
        pandas.DataFrame: A DataFrame with only the 'Pass' reads.
    """
    df = rep_id_pass(technology, file_path, limit)
    pass_df = df[df["QC"] == "Pass"]
    return pass_df

def filter_notpass_reads(technology, file_path, limit):
    """
    Filter only the rows where QC status is 'Not Pass'.

    Args:
        df (pandas.DataFrame): DataFrame containing Read Numbers, Read IDs, and QC status.

    Returns:
        pandas.DataFrame: A DataFrame with only the 'Not Pass' reads.
    """
    # # Ensure df is a DataFrame
    # if not isinstance(df, pd.DataFrame):
    #     raise TypeError("Expected a pandas DataFrame as input")
    df = rep_id_pass(technology, file_path, limit)
    # Filter for 'Not Pass' QC
    not_pass_df = df[df["QC"] == "Not Pass"]
    return not_pass_df

def prop_good_total(technology,file_path,limit):
    filtered_reads = filter_goodread(technology,file_path,limit).items()
    total_reads = extract_fastq_ids(file_path,limit)
    prop_goodread = len(filtered_reads)/len(total_reads) * 100
    return(
    f"Number of good reads: {len(filtered_reads)} from {len(total_reads)}\n"
    f"Proportion of Good Reads: {round(prop_goodread,1)}%"
)

# def rep_id_pass(file_path, limit, Qcutoff):
#     """
#     Report all reads grouped by Barcode with their Read Number, IDs, and QC status (Pass or Not Pass).

#     Args:
#         technology (int): Sequencing technology ID.
#         file_path (str): Path to the FastQ file.
#         limit (int): Maximum number of records to process.

#     Returns:
#         None
#     """
#     result = {"Barcode": [], "Read Number": [], "Read ID": [], "QC": []}
#     good_id = filter_goodread(file_path,limit,Qcutoff)  # {rec: [Q2, %filter]}
#     reads_id = extract_fastq_ids(file_path, limit)  # [(nums_id, rec_ids)]

    
#     # Convert good_id keys to a set for faster lookup
#     good_ids_set = set(good_id.keys())

#     # Collect all results
#     for nums_id, rec_ids in reads_id:
#         rec_id = re.match(r"^@\S+", rec_ids)  # Extract the record ID
#         bar_id = re.search(r"barcode=(\S+)", rec_ids)  # Extract the barcode
#         if bar_id:
#             barcode = bar_id.group(1)
#             result["Barcode"].append(barcode)

#         if rec_id:
#             rec_id = rec_id.group(0)
#             result["Read Number"].append(nums_id)
#             result["Read ID"].append(rec_id)
#             if nums_id in good_ids_set:
#                 result["QC"].append("Pass")
#             else:
#                 result["QC"].append("Not Pass")

#     # Get unique barcodes
#     unique_barcodes = set(result["Barcode"])

#     # Group and print results by barcode
#     bar_base = count_total_bases(file_path,limit)
#     for barcode in unique_barcodes:
#         # Filter data for the current barcode
#         indices = [i for i, b in enumerate(result["Barcode"]) if b == barcode]
#         read_numbers = [result["Read Number"][i] for i in indices if result["QC"][i] == "Pass"]
#         read_ids = [result["Read ID"][i] for i in indices if result["QC"][i] == "Pass"]
#         num_good_reads = len(read_numbers)
#         # Print results for the current barcode
#         print(f"{barcode}")
#         print(f"Total sequence: {bar_base[barcode]:,}")
#         print(f"Read Number of Good Read: {read_numbers}")
#         print(f"Read ID of Good Read: {read_ids}")
#         print(f"Number of Good Read: {num_good_reads:,}")

