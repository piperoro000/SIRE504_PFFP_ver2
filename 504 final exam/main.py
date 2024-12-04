#!/usr/bin/env python
from FilQ.openF.main_extract import *
from FilQ.stat.main_stat import *  
from FilQ.filter.main_filter import *
from FilQ.result_report.main_report import *
from argparse import ArgumentParser

import sys, gzip, time, statistics as stat

def argparserlocal():
    """
    Argument parser for command-line tools related to sequence quality and filtering.
    """
    parser = ArgumentParser(
        prog='Python FastQ Filtering Program',
        description='Process and filter sequence quality scores.'
    )
    subparsers = parser.add_subparsers(
        title='Commands',
        description='Choose one of the following commands:',
        dest='command'
    )
    subparsers.required = True

    # Subcommand: Filter Reads
    """
    python main.py filterRead -f test.fastq -q 25 -o filtered_reads.fastq
    -h, --help: 
        show this help message and exit
    -f FILE, --file FILE: 
        Path to the input FASTQ file.
    -q QCUTOFF, --qcutoff QCUTOFF
        Quality score threshold for filtering reads.
    -o OUTPUT, --output OUTPUT
        Name of the output FASTQ file for filtered reads.
    """
    filter_command = subparsers.add_parser(
        'filterRead',
        help='Filter reads based on quality score threshold (Qcutoff).'
    )
    filter_command.add_argument(
        '-f', '--file',
        type=str,
        required=True,
        help='Path to the input FASTQ file.'
    )
    filter_command.add_argument(
        '-q', '--qcutoff',
        type=int,
        required=True,
        help='Quality score threshold for filtering reads.'
    )
    filter_command.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Name of the output FASTQ file for filtered reads.'
    )

    # Subcommand: Generate Summary Report
    """
    python main.py generateReport -f test.fastq -q 25 -o filtered_reads.fastq
     -h, --help:
        show this help message and exit
    -f FILE, --file FILE:
        Path to the input FASTQ file.
    -q QCUTOFF, --qcutoff QCUTOFF:
        Quality score threshold for QC pass/fail classification.
  -o OUTPUT, --output OUTPUT:
        Name of the output TSV file for the report.
    """
    summary_command = subparsers.add_parser(
        'generateReport',
        help='Generate a TSV report summarizing the QC status of reads.'
    )
    summary_command.add_argument(
        '-f', '--file',
        type=str,
        required=True,
        help='Path to the input FASTQ file.'
    )
    summary_command.add_argument(
        '-q', '--qcutoff',
        type=int,
        required=True,
        help='Quality score threshold for QC pass/fail classification.'
    )
    summary_command.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Name of the output TSV file for the report.'
    )

    return parser


def main():
    parser = argparserlocal()
    args = parser.parse_args()

    if args.command == 'filterRead':
        print("Filtering reads based on quality score...")
        try:
            write_fastq(args.file, args.output, args.qcutoff)
            print(f"New FASTQ file '{args.output}' written successfully.")
        except Exception as e:
            print(f"Error while filtering reads: {e}")

    elif args.command == 'generateReport':
        print("Generating report summarizing QC status...")
        try:
            pass_report_csv(args.file, args.qcutoff, args.output)
            print(f"Report '{args.output}' generated successfully.")
        except Exception as e:
            print(f"Error while generating report: {e}")


# if __name__ == "__main__":
#     start_time = time.time()
#     file_path = sys.argv[0]
#     extract_sequences(file_path)
#     # main()
#     end_time = time.time()
#     print(f"Execution Time: {(end_time - start_time) / 60:.3f} minutes")

if __name__ == "__main__":
    file_name = sys.argv[1]
    # Qcutoff = int(sys.argv[2])
    # file_naming = sys.argv[3]
    start_time = time.time()
    # print(extract_fastq_ids(file_name))
    # print(extract_sequences(file_name))
    # print(extract_strand(file_name))
    # print(extract_phred(file_name))
#     # # Test the filter_read function
#     # # print("Number of good read:", len(filtered_reads))
#     # # print(prop_good_total(technology_id,file_name,limit))
#     # # print(Qmax(file_name,limit))
#     # # print(QScore(file_name,limit))
#     # # print(QScore())
#     # # print(Qmedian(file_name,limit))
#     # print(filter_goodread(file_name,limit,Qcutoff))
#     # print(percent_fil_out(file_name,limit))
#     # pass_report_csv(file_name, limit, Qcutoff, file_naming)
#     # print(filter_pass_reads(technology_id, file_name, limit))
#     # print(filter_notpass_reads(technology_id, file_name, limit))
#     # print(get_bar_readID(file_name, limit))
    # write_fastq(file_name, file_naming, Qcutoff)
    end_time = time.time()
    execution_time = end_time - start_time
    print (f"Time Use: {execution_time/60:.3f} min")

#     # Test the filter_read function
#     # technology_id = 3  # Example technology ID for Illumina
#     # filtered_reads = filter_goodread(technology_id)
#     # print("Number of good read:", len(filtered_reads))
#     # print(f"Filtered reads for technology {technology_id}: {filtered_reads}")