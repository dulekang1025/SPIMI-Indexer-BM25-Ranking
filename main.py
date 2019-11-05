from Spimi_Inverter import Spimi_Inverter
from Spimi_Merger import  Spimi_Merger
from Query import Query
def inverter():
    process = Spimi_Inverter()
    process.GetAllFiles()
    process.SplitIntoDoc()
    process.processDocumentWithCompression()
    # process.processWithoutCompression()

def merger():
    merger = Spimi_Merger()
    merger.openBlocksAndGetFirstLine()

def query():
    query = Query()
    query.readIndex()
    query.startQyery()
if __name__ == '__main__':
    # inverter()
    # merger()
    query()
