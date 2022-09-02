from tracemalloc import start
from xml_parser import Parser
import sys
from indexer import Indexer
from page import Page
import os
from time import time
import subprocess

if __name__ == "__main__":
    # import cProfile
    # import pstats
    
    # with cProfile.Profile() as profile:
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
    start_time = time()
    parser = Parser(sys.argv[1])
    
    
    ind = Indexer()
    ind.writePages()
    ind.writeTitleFile()
    
    finalToken = ind.mergedata()
    
    end_time = time()
    initialToken = len(Page.uniqueWords)
    
    print(f"Time taken: {end_time - start_time}")
    # size = os.path.getsize(sys.argv[2])
    size = subprocess.check_output(['du','-sh', sys.argv[2]]).split()[0].decode('utf-8')
    stat_file = open(sys.argv[3], "w")
    stat_file.write(f"{size}\n{str(finalToken)}\n{Indexer.final_file_count}")
    stat_file.close()
    
    # stats = pstats.Stats(profile)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.dump_stats(filename="profile.prof")