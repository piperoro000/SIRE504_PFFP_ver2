from FilQ.openF.main_extract import extract_phred
import statistics as stat


def phred_to_score(phred_char):
    """
    Converts a single Phred character into its corresponding quality score.

    Args:
        phred_char (str): A single character from the quality string of a FASTQ file.

    Returns:
        An integer representing the Phred quality score.
    """
    return ord(phred_char) - 33

def QScore(file_path):
    """
    Generates a dictionary of Phred quality scores for each sequence record in a FASTQ file.

    Args:
        file_path (str): Path to the FastQ file (both the compressed and uncompressed).

    Returns:
        A dictionary where: Keys are record IDs (e.g., sequence names), values are lists of integer Phred quality scores for the corresponding sequences.

    """
    raw_Phred = extract_phred(file_path)
    Q_Score = {}
    for rec, phred_str in raw_Phred:
        scores = [phred_to_score(phred) for phred in phred_str] 
        Q_Score[rec] = scores

    return Q_Score

def Qmedian(file_path):
    Q_values = QScore(file_path).items() # (1,[21,22])
    Q_Q_Q = {} 
    for rec, qual in Q_values:
        qual_sorted = list(sorted(qual))
        Q2 = round(stat.median(qual_sorted),2)
        Q_Q_Q[rec] = Q2

    return Q_Q_Q









