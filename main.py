from Spimi_Inverter import Spimi_Inverter
from Spimi_Merger import  Spimi_Merger
from Query import Query
def inverter():
    """
    Inverter
    """
    process = Spimi_Inverter()
    process.GetAllFiles()
    process.SplitIntoDoc()
    process.processWithoutCompression()

def merger():
    """
    merger
    """
    merger = Spimi_Merger()
    merger.openBlocksAndGetFinalIndex()

def query():
    """
    query
    """
    query = Query()
    query.read_index()
    query.ranking_query()

if __name__ == '__main__':
    """
    BM25 testing results are in the folder "testing_results"
    each case was writen into a file.
    """
    # inverter()
    # merger()
    query()
