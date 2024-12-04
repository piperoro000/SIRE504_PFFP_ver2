import re, gzip

def read_file(file_path):
    """
    Open a file, handling gzip-compressed and uncompressed files.

    Args:
        file_path (str): Path to the FastQ file (both the compressed and uncompressed).

    Returns:
        file object: Open file object.
    """
    if file_path.endswith(".gz"):
        return gzip.open(file_path, 'rt')  # Open gzip-compressed file in text mode
    elif file_path.endswith(".fastq"):
        return open(file_path, 'r')  # Open uncompressed FastQ file
    else:
        raise ValueError("Unsupported file format. Please provide a .fastq or .fastq.gz file.")


def extract_fastq_ids(file_path):
    """
    Extract FastQ record IDs from the file.

    Args:
        file_path (str): Path to the FastQ file (both the compressed and uncompressed).

    Returns:
        list: List of tuples (record_number, record_id).
    """
    file = read_file(file_path)
    record_ids = []
    record_count = 0
    line_count = 0  # Initialize line count
    for line in file:
        line = line.strip()
        line_count += 1
        if line_count % 4 == 1:  # Record ID line
            record_count += 1
            record_ids.append((record_count, line))
    return record_ids

def extract_strand(file_path):
    """
    Extract DNA strand symbol from the file.

    Args:
        file_path (str): Path to the FastQ file (both the compressed and uncompressed).

    Returns:
        list: List of tuples (record_number, strand).
    """
    file = read_file(file_path)
    strand_ids = []
    record_count = 0
    line_count = 0  # Initialize line count
    for line in file:
        line = line.strip()
        line_count += 1
        if line_count % 4 == 3:  # Record ID line
            record_count += 1
            strand_ids.append((record_count, line))
    return strand_ids


def extract_sequences(file_path):
    """
    Extract sequences from a FastQ file.

    Args:
        file_path (str): Path to the FastQ file (both the compressed and uncompressed).

    Returns:
        dict: Dictionary with barcodes as keys and a list of sequences as values.
    """
    sequences = {}
    line_count = 0  # Initialize line counter
    read_number = 0
    bar_id = None  # Initialize bar_id for sequence association
    file = read_file(file_path)
    
    for line in file:
        line = line.strip()
        line_count += 1
        if line_count % 4 == 1:  # Record ID line
            record_count = 0
            bar_id = re.search(r"barcode=(\S+)", line)
            if bar_id:
                barcode = bar_id.group(1)
                if barcode not in sequences:
                    sequences[barcode] = []
        elif line_count % 4 == 2 and bar_id:  # Sequence line
            read_number += 1
            sequences[barcode].append((read_number,line))

    return sequences

def extract_phred(file_path):
    """
    Extract Phred quality scores from a FastQ file.

    Args:
        file_path (str): Path to the FastQ file (both the compressed and uncompressed).

    Returns:
        list: List of tuples (record_number, quality_score).
    """
    phred_quality = []
    line_count = 0
    read_number = 0  # Initialize read number

    file = read_file(file_path)
    for line in file:
        line = line.strip()
        line_count += 1
        if line_count % 4 == 1:  # Record ID line
            read_number += 1
        elif line_count % 4 == 0:  # Quality score line
            phred_quality.append((read_number, line))
                
    return phred_quality
