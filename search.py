import sys
import re
import os
from bisect import bisect_left
from Stemmer import Stemmer
import pickle


class fileQuery:
    def __init__(self, index_path) -> None:
        self.field_doc_heading = {}
        self.index_path = index_path
        self.preprocess_heading()
        pass

    def preprocess_heading(self):
        self.filedwise_heading('b')
        self.filedwise_heading('t')
        self.filedwise_heading('r')
        self.filedwise_heading('i')
        self.filedwise_heading('c')
        self.filedwise_heading('l')
        
    def filedwise_heading(self, field):
        file_no = 0
        file_path = f"{self.index_path}/index_{field}{file_no}.txt"
        self.field_doc_heading[field] = []
        while(os.path.exists(file_path)):
            with open(file_path, "r") as f:
                self.field_doc_heading[field].append(f.readline())
            file_no+=1
            file_path = f"{self.index_path}/index_{field}{file_no}.txt"
    
    def processQuery(self, query, field):
        i = bisect_left(self.field_doc_heading[field], query)
        if i:
            return i-1
        return -1

class DocQuery():
    def __init__(self, field, file_no) -> None:
        self.field = field
        self.file_no = file_no
        fil = open(f"{sys.argv[1]}/offset_{field}{file_no}.pkl", "rb")
        self.offsets = pickle.load(fil)
        self.indexfilepath = f"{sys.argv[1]}/index_{field}{file_no}.txt"
    
    # Returns all documents in which that query is present
    def fetchLine(self, query):
        num_words = len(self.offsets)
        indexfile = open(self.indexfilepath, "r")
        lower = 0
        # -2 coz the last value indicates the final empty line, that we shouldn't search in.
        upper = num_words-2
        
        while lower<=upper:
            mid = (lower+upper)//2
            # print(mid)
            # print(f"upper -> {upper}")
            indexfile.seek(self.offsets[mid])
            linez = indexfile.readline().strip()
            linez_tok = linez.split()
            if linez_tok[0]==query:
                indexfile.close()
                return linez_tok
            if linez_tok[0]<query:
                lower = mid+1
            else: upper = mid-1
        
        indexfile.close()
        return []

def normalizeTitles(title):
    num_zer = 8 - len(title)
    title = "!"*num_zer + title
    return title

class TitleFileQuery:
    def __init__(self) -> None:
        fil = open(f"{sys.argv[2]}/title_pre_index.txt", "r")
        titles = fil.read().split()
        self.title_arr = [normalizeTitles(title) for title in titles]
        # print(self.title_arr)
            
    
    # Returns all documents in which that query is present
    def processQuery(self, query):
        query = normalizeTitles(query)
        i = bisect_left(self.title_arr, query)
        if i:
            return i-1
        return -1

class TitleQuery:
    def __init__(self, file_no) -> None:
        self.title_file = f"{sys.argv[2]}/title{str(file_no)}.txt"
        fil = open(f"{sys.argv[2]}/titleoffset{str(file_no)}.txt", "r")
        self.offsets = fil.read().split()
        fil.close()
    
    # Returns all documents in which that query is present
    def fetchLine(self, query):
        query = normalizeTitles(query)
        # print(self.offsets[:10])
        num_words = len(self.offsets)
        titlefile = open(self.title_file, "r")
        lower = 0
        # -2 coz the last value indicates the final empty line, that we shouldn't search in.
        upper = num_words-2
        # print(f"QUERY->{query}")
        while lower<=upper:
            mid = (lower+upper)//2
            titlefile.seek(int(self.offsets[mid]))
            linez = titlefile.readline().strip()
            # print(linez)
            word = linez.split()[0]
            word = normalizeTitles(word)
            # print(word)
            if word==query:
                titlefile.close()
                return linez
            if word<query:
                lower = mid+1
            else: upper = mid-1
        
        titlefile.close()
        return ""

class IDFQuery:
    def __init__(self) -> None:
        preindexfile = f"{sys.argv[2]}/idf_preindex.txt"
        preindexfile = open(preindexfile, "r")
        data = preindexfile.read().split("\n")
        self.preindex = data
        self.cached_idf = {}
        preindexfile.close()
    
    def process_query(self, query):
        if query in self.cached_idf:
            return self.cached_idf[query]
        fileno = bisect_left(self.preindex, query)
        if not fileno:
            self.cached_idf[query] = 0
            return 0
        fil = "".join([sys.argv[2], '/idf_', str(fileno) + '.txt'])
        fil = open(fil, "r")
        data = fil.read()
        data = data.split("\n")
        bin_search_data = [ele.split()[0] for ele in data]

        word_idx = bisect_left(bin_search_data, query)
        if word_idx != len(bin_search_data) and bin_search_data[word_idx] == query:
            self.cached_idf[query] = float(data[word_idx].split()[1])
            return float(data[word_idx].split()[1])
        else:
            self.cached_idf[query] = 0
            return 0

def fieldQuery(queries):
    for query in queries:
        field = query[0]
        word = query[1]
        if word != '' and word != ' ':
            pass
    pass

def calculatescore(word, field):
    FIELD_TO_INDEX = {"t": 1, "b": 2, "i": 3, "c": 4, "r": 5, "l": 6}
    file_no = a.processQuery(word, field)
    dquery = DocQuery(field, file_no)
    doclist = dquery.fetchLine(word)
    score_dict = {}
    title_dict = {}
    titlefilequery = TitleFileQuery()
    idfcalculator = IDFQuery()
    idf = idfcalculator.process_query(word)
    for doc in doclist[1:]:
        doc_id, term_freq = doc.split(":")
        # doc_file = titlefilequery.processQuery(doc_id)
        # titlequery = TitleQuery(doc_file)
        
        # print(doc_data)

        tf = int(term_freq)
        score_dict[doc_id] = tf*idf
        
    # doc_data = titlequery.fetchLine(doc_id)
    # doc_data = doc_data.split(" ", 7)
    # doc_len = int(doc_data[FIELD_TO_INDEX[field]])
    # title_dict[doc_id] = doc_data[-1]
    print("YAY")

if __name__ == "__main__":
    # import cProfile
    # import pstats
    
    # with cProfile.Profile() as profile:
    if True:
        stemmer = Stemmer('english')
        a = fileQuery(sys.argv[1])
        # while True:
        word = "canada"
        field = "b"
        calculatescore(word, field)
        # exit(0)
        # query_file = open(sys.argv[2], 'r')
        # for query in query_file.readlines():
        #     query = query.lower()
            
        #     if re.match(r'[t|b|i|c|r|l]:', query):
        #         quer_arr = []
        #         words = re.findall(r'[t|b|c|i|l|r]:([^:]*)(?!\S)', query)
        #         tempFields = re.findall(r'([t|b|c|i|l|r]):', query)
                
        #         words = stemmer.stemWords(words)
                
        #         for i in range(len(words)):
        #             for word in words[i].split():
        #                 quer_arr.append((tempFields[i], word))
            
        #         pageList, pageFreq = fieldQuery(quer_arr)
        # stats = pstats.Stats(profile)
        # stats.sort_stats(pstats.SortKey.TIME)
        # stats.dump_stats(filename="profile.prof")