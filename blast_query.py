from Bio.Blast import NCBIWWW
from Bio import SeqIO

# help(NCBIWWW.qblast)
# fileName="sequence-1.fasta"

def is_fasta(filename):
    with open(filename, "r") as handle:
        fasta = SeqIO.parse(handle, "fasta")
        return any(fasta) # False when `fasta` is empty, i.e. wasn't a FASTA file
def run_query(filename):
    fastaString = open(filename).read()
    if is_fasta(filename):
        resultHandle = NCBIWWW.qblast("blastn", "nt", fastaString)
        with open("my_blast.xml", "w") as out_handle:
            out_handle.write(resultHandle.read())
        resultHandle.close()
        return True
    else:
        return None