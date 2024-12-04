import sys

def record_v2(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.readlines()
        return file_contents

def record_seq_phred(file_path):
    recoed_sp = record_v2(file_path)
    results = []
    R_Seq_Qual = {"Sequence":[],"Phred_33":[]}
    for num_q, q in enumerate(range(0, len(recoed_sp), 4)):
        x = recoed_sp[q].strip()
        R_Seq_Qual.setdefault("Read",[]).append(x)
        if num_q == 2:
            break
    for num_i, i in enumerate(range(1, len(recoed_sp), 4)):  # line2 อยู่ที่ index 1 และ line4 อยู่ที่ index 3 ในทุกกลุ่ม
        sequence = recoed_sp[i].strip()    # line2: Sequence
        quality = recoed_sp[i + 2].strip() # line4: Quality
        results.append((sequence, quality))
        if num_i == 2:
            break
    for m, n in results:
        R_Seq_Qual.setdefault("Sequence",[]).append(m)
        R_Seq_Qual.setdefault("Phred_33",[]).append(n)
    return R_Seq_Qual

# def record_r(file_path):
#     recoed_sp = record_v2(file_path)
#     result = []
#     for num_i, i in enumerate(range(0, len(recoed_sp), 4)):
#         x = recoed_sp[i].strip()
#         result.append(x)
#         if num_i == 1:
#             break
#     return result


# file_name = sys.argv[1]
# print(record(file_name))

# New function to separate description, runid, sampleid, and other components
# def separate_fields(line):
#     # Split the line by whitespace
#     parts = line.split()

#     # Initialize a dictionary to store the results
#     result = {}

#     # Iterate over the parts and assign to corresponding fields
#     for part in parts:
#         if part.startswith('@'):
#             result['Name'] = part[1:]  # Remove '@' symbol from description
#         # elif part.startswith('runid='):
#         #     result['runid'] = part.split('=')[1]
#         # elif part.startswith('sampleid='):
#         #     result['sampleid'] = part.split('=')[1]
#         # elif part.startswith('read='):
#         #     result['read'] = part.split('=')[1]
#         else:
#             # Store any other fields as key-value pairs (e.g., ch, start_time, barcode)
#             key_value = part.split('=')
#             if len(key_value) == 2:
#                 result[key_value[0]] = key_value[1]

#     # return result
#     print(result)



file_name = sys.argv[1]
print(record_seq_phred(file_name))
# lines = record(file_name)

# for line in lines:
#     print(separate_fields(line))
#     if line:
#         extracted_fields = separate_fields(line)
#         # Print each field line by line
#         for key, value in extracted_fields.items():
#             print(f"{key}: {value}")
#     else:
#         print("No valid line found.")