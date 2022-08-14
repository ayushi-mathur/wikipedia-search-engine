from xml_parser import Parser
import sys
from indexer import Indexer

if __name__ == "__main__":
    parser = Parser(sys.argv[1])
    ind = Indexer()
    ind.writePages()
    ind.mergedata()
    