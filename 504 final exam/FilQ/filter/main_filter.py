from FilQ.stat.main_stat import Qmedian

def filter_goodread(file_path, Qcutoff):
    """
    Filters sequence reads from a FASTQ file based on a quality score threshold (Qcutoff) and returns only the records meeting the cutoff.

    Args:
        file_path (str): Path to the FASTQ file.
        Qcutoff (int): Quality score threshold. Reads with a median quality score greater than or equal to this value are retained.

    Returns:
        A dictionary where: Keys are record IDs of filtered reads, values are the median Phred quality scores for these records.
    """
    Q_values =  Qmedian(file_path)
    filtered_reads = {}   
    for rec, Q2 in Q_values.items():
        if int(Q2) >= Qcutoff:
            filtered_reads[rec] = Q2
    return filtered_reads




