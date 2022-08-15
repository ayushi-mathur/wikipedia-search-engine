from xml_parser import Parser
import sys
from indexer import Indexer
from page import Page

if __name__ == "__main__":
    # import cProfile
    # import pstats
    
    # with cProfile.Profile() as profile:
    parser = Parser(sys.argv[1])
    ind = Indexer()
    ind.writePages()
    
    finalToken = ind.mergedata()
    initialToken = len(Page.uniqueTokens)
    
    stat_file = open(sys.argv[3], "w")
    stat_file.write(f"{str(initialToken)}\n")
    stat_file.write(f"{str(finalToken)}")
    stat_file.close()
    
    # stats = pstats.Stats(profile)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.dump_stats(filename="profile.prof")