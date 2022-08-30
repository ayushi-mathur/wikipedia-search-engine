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
            print(mid)
            print(f"upper -> {upper}")
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

def fieldQuery(queries):
    for query in queries:
        field = query[0]
        word = query[1]
        if word != '' and word != ' ':
            pass
    pass

if __name__ == "__main__":
    stemmer = Stemmer('english')
    a = fileQuery(sys.argv[1])
    # while True:
    #     word = input()
    #     field = input()
    #     file_no = a.processQuery(word, field)
    #     dquery = DocQuery(field, file_no)
    #     doclist = dquery.fetchLine(word)
    #     print(doclist)
    #     print("----------------")
    query_file = open(sys.argv[2], 'r')
    for query in query_file.readlines():
        query = query.lower()
        
        if re.match(r'[t|b|i|c|r|l]:', query):
            quer_arr = []
            words = re.findall(r'[t|b|c|i|l|r]:([^:]*)(?!\S)', query)
            tempFields = re.findall(r'([t|b|c|i|l|r]):', query)
            
            words = stemmer.stemWords(words)
            
            for i in range(len(words)):
                for word in words[i].split():
                    quer_arr.append((tempFields[i], word))
        
            pageList, pageFreq = fieldQuery(quer_arr)