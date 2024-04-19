import os
import csv
from pandas import *

DATA_DIR_NAME = "static"
DATA_DIR_PATH = os.path.join(os.getcwd(), DATA_DIR_NAME)

# Dictionary mapping IUPAC nucleotide codes to corresponding nucleotides.
IUPAC_TO_NT_MAP = {
    "W": ["A", "T"],
    "R": ["A", "G"],
    "K": ["G", "T"],
    "S": ["C", "G"],
    "Y": ["C", "T"],
    "M": ["A", "C"],
    "B": ["C", "G", "T"],
    "D": ["A", "G", "T"],
    "H": ["A", "C", "T"],
    "V": ["A", "C", "G"],
    "N": ["A", "C", "G", "T"]
}

# Function to check whether the input sequence is a valid dna sequence.
def validate_genome_seq(genome_seq):
    ok = True
    for ch in genome_seq:
        if ch == 'A' or ch == 'G' or ch == 'T' or ch == 'C':
            continue
        else:
            ok = False
    return ok


# Function to create dictionary from a csv file using one column as key and another column as value
def create_dict(csv_file, key_column, value_column):
    data_dict = dict()
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row[key_column]
            value = row[value_column]
            data_dict[key] = value
    return data_dict


con_seq_tf_family_map = create_dict(
    os.path.join(DATA_DIR_PATH, "tfbs_locator.csv"), 
    "Conserved Sequence", 
    "TF Family"
)

con_seq_ref_map = create_dict(
    os.path.join(DATA_DIR_PATH, "tfbs_locator.csv"), 
    "Conserved Sequence", 
    "Reference"
)

def locate_con_seq_in_genome_seq(conserved_seq, genome):
    indices = list()
    l1 = len(conserved_seq)
    l2 = len(genome)

    for i in range(l2 - l1 + 1):
        new = genome[i : i+l1]
        ok = True
        for j in range(l1):
            if conserved_seq[j]=='A' or conserved_seq[j]=='G' or conserved_seq[j]=='T' or conserved_seq[j]=='C':
                if (conserved_seq[j] != new[j]):
                    ok = False
                    break
            else:
                ch = conserved_seq[j]
                if new[j] in IUPAC_TO_NT_MAP[ch]:
                    continue
                else:
                    ok = False
                    break
        if ok:
            indices.append(i)

    return indices

def locate_all_con_sequences(genome):
    indices_dict = dict()
    for conserved_seq in con_seq_tf_family_map:
        indices = locate_con_seq_in_genome_seq(conserved_seq, genome)
        if len(indices) > 0:
            indices_dict[conserved_seq] = indices

    return indices_dict

def locate_con_sequences_and_add_refs(genome):
    con_seq_indices = locate_all_con_sequences(genome)
    output = dict()
    for con_seq in con_seq_indices:
        output[con_seq] = {
            "indices": con_seq_indices[con_seq],
            "ref": con_seq_ref_map[con_seq]
        }
    return output


tf_data = read_csv(os.path.join(DATA_DIR_PATH, "tf_finder.csv"))
family_name = tf_data["Family"].tolist()
tf_ids = tf_data["Transcript_ID"].tolist()
gene_ids = tf_data["Gene_ID"].tolist()

# Function to find all the transcription factors of a particular TF family.
def find_tf_ids(tf_family):
    res_dict = dict()
    l = len(tf_ids)

    for i in range(l):
        if (family_name[i] == tf_family):
            res_dict[tf_ids[i]] = gene_ids[i]
    # print(res_dict)
    return res_dict
