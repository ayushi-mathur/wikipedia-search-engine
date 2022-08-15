from xml_parser import Parser
import sys
from indexer import Indexer

if __name__ == "__main__":
    # import cProfile
    # import pstats
    
    # with cProfile.Profile() as profile:
    parser = Parser(sys.argv[1])
    ind = Indexer()
    ind.writePages()
    ind.mergedata()
    
    # stats = pstats.Stats(profile)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.dump_stats(filename="profile.prof")