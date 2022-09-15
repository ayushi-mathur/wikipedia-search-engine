import sys
import re
import os
from bisect import bisect_left
import pickle
import heapq
from page import Page
from indexer import Indexer
from time import time
import linecache

MAX_BODY = 420
FIELD_TO_WEIGHT_FIELDQ = {"t": 55, "b": 1.2, "i": 20, "c": 15, "r": 16, "l": 16}
FIELD_TO_WEIGHT_NORMALQ = {"t": 45, "b": 0.3, "i": 10, "c": 1, "r": 0.1, "l": 0.1}
class fileQuery:
    def __init__(self, index_path) -> None:
        self.field_doc_heading = {}
        self.preprocess_heading()

    def preprocess_heading(self):
        self.filedwise_heading('b')
        self.filedwise_heading('t')
        self.filedwise_heading('r')
        self.filedwise_heading('i')
        self.filedwise_heading('c')
        self.filedwise_heading('l')
        
    def filedwise_heading(self, field):
        file_path = f"{sys.argv[2]}/preindex_{field}"
        self.field_doc_heading[field] = []
        with open(file_path, "r") as f:
            data = f.read()
            data = data.split("\n")
            self.field_doc_heading[field] = data
    
    def processQuery(self, query, field):
        i = bisect_left(self.field_doc_heading[field], query)
        if i:
            return i-1
        return -1

class DocQuery():
    def __init__(self, field, file_no) -> None:
        self.field = field
        self.file_no = file_no
        fil = open(f"{sys.argv[2]}/offset_{field}{file_no}.txt", "r")
        offsets = fil.read()
        self.offsets = offsets.split("\n")
        self.indexfilepath = f"{sys.argv[2]}/index_{field}{file_no}.txt"
        fil.close()
    
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
            indexfile.seek(int(self.offsets[mid]))
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
        titles = fil.read().split("\n")
        self.title_arr = [normalizeTitles(title) for title in titles]
    
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
        # fil = open(f"{sys.argv[2]}/titleoffset{str(file_no)}.txt", "r")
        # self.offsets = fil.read().split()
        # fil.close()
    
    # Returns all documents in which that query is present
    def fetchLine(self, query):
        query = normalizeTitles(query)
        # print(self.offsets[:10])
        # num_words = len(self.offsets)
        titlefile = open(self.title_file, "r")
        data = titlefile.read()
        data = data.split("\n")
        lower = 0
        indexer = Indexer()
        query_num = indexer.decode_number(query)
        base = data[0].split(" ", 1)[0]

        base_num = indexer.decode_number(base)
        line_no = query_num-base_num
        ans = data[line_no]
        titlefile.close()
        return ans       

    # Linecache optimization
    # def fetchLine(self, query):
    #     query = normalizeTitles(query)
    #     # print(self.offsets[:10])
    #     # num_words = len(self.offsets)

    #     # titlefile = open(self.title_file, "r")
    #     # data = titlefile.readline().strip()
    #     data = linecache.getline(self.title_file, 0).strip()
    #     # data = data.split("\n")
    #     lower = 0
    #     indexer = Indexer()
    #     query_num = indexer.decode_number(query)
    #     base = data.split(" ", 1)[0]

    #     base_num = indexer.decode_number(base)
    #     line_no = query_num-base_num
    #     # ans = data[line_no]
    #     ans = linecache.getline(self.title_file, line_no)
    #     # titlefile.close()
    #     return ans 
    # OFFSET BASED FUNCTION. UNUSED.
    # def fetchLine(self, query):
    #     query = normalizeTitles(query)
    #     # print(self.offsets[:10])
    #     num_words = len(self.offsets)
    #     titlefile = open(self.title_file, "r")
    #     lower = 0
    #     # -2 coz the last value indicates the final empty line, that we shouldn't search in.
    #     upper = num_words-2
    #     # print(f"QUERY->{query}")
    #     while lower<=upper:
    #         mid = (lower+upper)//2
    #         titlefile.seek(int(self.offsets[mid]))
    #         linez = titlefile.readline().strip()
    #         # print(linez)
    #         word = linez.split()[0]
    #         word = normalizeTitles(word)
    #         # print(word)
    #         if word==query:
    #             titlefile.close()
    #             return linez
    #         if word<query:
    #             lower = mid+1
    #         else: upper = mid-1
        
    #     titlefile.close()
    #     return ""

class IDFQuery:
    cached_idf = {}
    def __init__(self) -> None:
        preindexfile = f"{sys.argv[2]}/idf_preindex.txt"
        preindexfile = open(preindexfile, "r")
        data = preindexfile.read().split("\n")
        self.preindex = data
        preindexfile.close()
    
    def process_query(self, query):
        if query in IDFQuery.cached_idf:
            return IDFQuery.cached_idf[query]
        fileno = bisect_left(self.preindex, query) - 1
        # print(f"FILEEEE {fileno}")
        # exit(0)
        # if not fileno:
        #     IDFQuery.cached_idf[query] = 0
        #     return 0
        fil = "".join([sys.argv[2], '/idf_', str(fileno) + '.txt'])
        fil = open(fil, "r")
        data = fil.read()
        data = data.split("\n")
        bin_search_data = [ele.split()[0] for ele in data]

        word_idx = bisect_left(bin_search_data, query)
        if word_idx != len(bin_search_data) and bin_search_data[word_idx] == query:
            IDFQuery.cached_idf[query] = float(data[word_idx].split()[1])
            return float(data[word_idx].split()[1])
        else:
            IDFQuery.cached_idf[query] = 0
            return 0

def calculatescore(word, field, score_dict, isFieldQuery=False):
    file_no = a.processQuery(word, field)
    # print(f"{file_no} {word} {field}")
    dquery = DocQuery(field, file_no)
    doclist = dquery.fetchLine(word)
    # title_dict = {}
    # titlefilequery = TitleFileQuery()
    idfcalculator = IDFQuery()
    idf = idfcalculator.process_query(word)
    curr_field_weight = 1
    if isFieldQuery:
        curr_field_weight = FIELD_TO_WEIGHT_FIELDQ[field]
    else:
        curr_field_weight = FIELD_TO_WEIGHT_NORMALQ[field]
    # if isFieldQuery:
    #     curr_field_weight = 1
    for doc in doclist[1:]:
        doc_id, term_freq = doc.split(":")
        # doc_file = titlefilequery.processQuery(doc_id)
        # titlequery = TitleQuery(doc_file)
        
        # print(doc_data)
        # if (field == "t"  and not isFieldQuery) or field=="i":
        if field == "t" or field=="i":
            tf = 1
        else:
            if not isFieldQuery:
                tf = min(Indexer.decode_number(term_freq), MAX_BODY)
            else:
                tf = min(Indexer.decode_number(term_freq), 500)
        
        if doc_id in score_dict:
            # score_dict[doc_id] += curr_field_weight*tf   
            score_dict[doc_id] += curr_field_weight*tf*idf   
        else:
            # score_dict[doc_id] = curr_field_weight*tf
            score_dict[doc_id] = curr_field_weight*tf*idf
        
    # doc_data = titlequery.fetchLine(doc_id)
    # doc_data = doc_data.split(" ", 7)
    # doc_len = int(doc_data[FIELD_TO_INDEX[field]])
    # title_dict[doc_id] = doc_data[-1]

def clean_query(data):
    page = Page()
    data = page.getStemmedTokens(data, False)
    return data


def rank_documents(query):
    query = query.lower()
    score_dict = {}
    FIELD_TO_INDEX = {"t": 1, "b": 2, "i": 3, "c": 4, "r": 5, "l": 6}

    titlefilequery = TitleFileQuery()
    if re.match(r'[t|b|i|c|r|l]:', query):
        # print("CCCCCCCCCCCCCCCCCCCC")
        quer_arr = []
        quer_strings = re.findall(r'[t|b|c|i|l|r]:([^:]*)(?!\S)', query)
        tempFields = re.findall(r'([t|b|c|i|l|r]):', query)

        for idx, field in enumerate(tempFields):
            q_string = quer_strings[idx]
            q_data = clean_query(q_string)
            for word in q_data:
                calculatescore(word, field, score_dict, True)
        
        pq = []
        for docid in score_dict:
            pq.append((score_dict[docid], docid))
        heapq._heapify_max(pq)

        results = []
        i = 0
        while i <10:
            if not pq:
                break
            top_ele = heapq._heappop_max(pq)
            doc_id = top_ele[1]
            doc_file = titlefilequery.processQuery(doc_id)
            titlequery = TitleQuery(doc_file)
            doc_data = titlequery.fetchLine(doc_id)
            doc_data = doc_data.split(" ", 1)
            doc_title = doc_data[-1]
            if doc_title.startswith("Wikipedia:") or doc_title.startswith("Module:") or doc_title.startswith("Help:"):
                continue
            i+=1
            results.append(f"{doc_id}, {doc_title}")
        
        write_str = "\n".join(results)
        if write_str is None:
            write_str = ""
    
    else:
        tempFields = ['t', 'b', 'i', 'l', 'r', 'c']
        q_string = query
        for idx, field in enumerate(tempFields):
            q_data = clean_query(q_string)
            for word in q_data:
                calculatescore(word, field, score_dict, False)
        
        pq = []
        for docid in score_dict:
            pq.append((score_dict[docid], docid))
        heapq._heapify_max(pq)

        results = []
        i = 0
        while i<10:
            if not pq:
                break
            top_ele = heapq._heappop_max(pq)
            doc_id = top_ele[1]
            doc_file = titlefilequery.processQuery(doc_id)
            titlequery = TitleQuery(doc_file)
            doc_data = titlequery.fetchLine(doc_id)
            doc_data = doc_data.split(" ", 1)
            doc_title = doc_data[-1]
            if doc_title.startswith("Wikipedia:") or doc_title.startswith("Module:") or doc_title.startswith("Help:"):
                continue
            i+=1
            results.append(f"{doc_id}, {doc_title}")
        write_str = "\n".join(results)
    # write_str+=("\n"+str(score_dict.get("+AgN")))
    return write_str

if __name__ == "__main__":
    # import cProfile
    # import pstats
    
    # with cProfile.Profile() as profile:
    # if True:
    fil = open(sys.argv[1], "r")
    if os.path.exists("./queries_op.txt"):
        os.remove("./queries_op.txt")
    a = fileQuery(sys.argv[1])
    for line in fil.readlines():
        # while True:
        query = line
        start_time = time()
        write_str = rank_documents(query)
        # print(write_str)
        end_time = time()
        with open("./queries_op.txt", "a+") as f:
            if write_str is not None:
                f.write(write_str)
            f.write("\n")
            f.write(str(end_time-start_time))
            f.write("\n")
            f.write("\n")
