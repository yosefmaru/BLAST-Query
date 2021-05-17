from Bio.Blast import NCBIXML

def blast_parse(file):
    result_handle = open(file)
    blast_record = NCBIXML.parse(result_handle)
    return blast_record

if __name__ == "__main__":
    result = blast_parse("my_blast.xml")
    E_VALUE_THRESH = 0.04
    for record in result: 
        if record.alignments: 
            print("\n") 
            print("query: %s" % record.query)
            for align in record.alignments: 
                for hsp in align.hsps:
                    if hsp.expect < E_VALUE_THRESH:
                        print("match: %s " % align.title)
                        break
        break
