import sys
import re
import os
from bisect import bisect_left
from Stemmer import Stemmer

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
        file_path = f"{self.index_path}index_{field}{file_no}.txt"
        print(file_path)
        self.field_doc_heading[field] = []
        while(os.path.exists(file_path)):
            with open(file_path, "r") as f:
                self.field_doc_heading[field].append(f.readline())
            file_no+=1
            file_path = f"{self.index_path}index_{field}{file_no}.txt"
    
    def processQuery(self, query, field):
        print(self.field_doc_heading[field])
        i = bisect_left(self.field_doc_heading[field], query)
        if i:
            return i-1
        return -1

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
    while True:
        word = input()
        field = input()
        print(a.processQuery(word, field))
        print("----------------")
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