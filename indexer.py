from collections import defaultdict, Counter
import string
import sys
import heapq
import os
from pprint import pprint
NUMPAGES_IN_PREINDEX = 15000
VOCAB_PER_FILE = 50000

class Indexer:
    indexMapT, indexMapB, indexMapL, indexMapR, indexMapC, indexMapI = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    fileCount, pageCount = 0, 0
    ALPHABET = "".join([string.digits, string.ascii_lowercase, string.ascii_uppercase, '+_'])
    ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
    BASE = len(ALPHABET)
    DICT_SUBDIV = 50000
    
    def __init__(self, title=[], body=[], info=[], categories=[], links=[], references=[]) -> None:
        self.title, self.body, self.info, self.categories, self.links, self.references = title, body, info, categories, links, references 
    
    # Encodes a positive integer to base 64 coding
    @staticmethod
    def num_encode(n):
        s = []
        while n>0:
            n, r = divmod(n, Indexer.BASE)
            s.append(Indexer.ALPHABET[r])
        return ''.join(reversed(s))

    # Decodes a base 64 coding to a positive integer
    @staticmethod
    def num_decode(s):
        n = 0
        for c in s:
            n = n * Indexer.BASE + Indexer.ALPHABET_REVERSE[c]
        return n

    def createIndex(self):
        Id = Indexer.num_encode(Indexer.pageCount)
        freq_dict = defaultdict(int)
        common_freq_dict = defaultdict(int)
        
        for word in self.title:
            freq_dict[word]+=1
            common_freq_dict[word]+=1
        title = freq_dict
        
        freq_dict = defaultdict(int)
        for word in self.categories:
            freq_dict[word]+=1
            common_freq_dict[word]+=1
        categories = freq_dict
        
        freq_dict = defaultdict(int)
        for word in self.info:
            freq_dict[word]+=1
            common_freq_dict[word]+=1
        info = freq_dict
        
        freq_dict = defaultdict(int)
        for word in self.references:
            freq_dict[word]+=1
            common_freq_dict[word]+=1
        references = freq_dict
        
        freq_dict = defaultdict(int)
        for word in self.body:
            freq_dict[word]+=1
            common_freq_dict[word]+=1
        body = freq_dict
        
        freq_dict = defaultdict(int)
        for word in self.links:
            freq_dict[word]+=1
            common_freq_dict[word]+=1
        links = freq_dict
        
        for word in common_freq_dict.keys():
            if word in title:
                Indexer.indexMapT[word].append(f"{Id}:{title[word]}")
            if word in references:
                Indexer.indexMapR[word].append(f"{Id}:{references[word]}")
            if word in info:
                Indexer.indexMapI[word].append(f"{Id}:{info[word]}")
            if word in body:
                Indexer.indexMapB[word].append(f"{Id}:{body[word]}")
            if word in categories:
                Indexer.indexMapC[word].append(f"{Id}:{categories[word]}")
            if word in links:
                Indexer.indexMapL[word].append(f"{Id}:{links[word]}")
        
        Indexer.pageCount += 1
        
        if Indexer.pageCount%NUMPAGES_IN_PREINDEX == 0:
            Indexer.writePages()
            
    
    @staticmethod
    def writePagesIntoTempIndexFile(fieldindicator, index, fileCount):

        data = list()
        for key in sorted(index.keys()):
            string = f"{key} {' '.join(index[key])}"
            data.append(string)

        filename = sys.argv[2] + '/index' + str(fieldindicator)+ str(fileCount) + '.txt'
        data = '\n'.join(data)
        f = open(filename, 'w')
        f.write(data)
        f.close()
    
    @staticmethod
    def writePages():
        Indexer.writePagesIntoTempIndexFile('t', Indexer.indexMapT, Indexer.fileCount)
        Indexer.writePagesIntoTempIndexFile('i', Indexer.indexMapI, Indexer.fileCount)
        Indexer.writePagesIntoTempIndexFile('b', Indexer.indexMapB, Indexer.fileCount)
        Indexer.writePagesIntoTempIndexFile('l', Indexer.indexMapL, Indexer.fileCount)
        Indexer.writePagesIntoTempIndexFile('c', Indexer.indexMapC, Indexer.fileCount)
        Indexer.writePagesIntoTempIndexFile('r', Indexer.indexMapR, Indexer.fileCount)

        Indexer.indexMapR = defaultdict(list)
        Indexer.indexMapI = defaultdict(list)
        Indexer.indexMapB = defaultdict(list)
        Indexer.indexMapL = defaultdict(list)
        Indexer.indexMapT = defaultdict(list)
        Indexer.indexMapC = defaultdict(list)

        Indexer.fileCount += 1
        
    def mergeFiles(file_field):
        pq = []
        wordsTopLine = {}
        files = {}
        topLine = {}
        pageCount = 0
        
        # print(Indexer.fileCount)
        finalFileCount = 0
        for ind in range(Indexer.fileCount):
            file_name = "".join([sys.argv[2], '/index', file_field + str(ind) + '.txt'])
            files[ind] = open(file_name, 'r')
            topLine[ind]=files[ind].readline().strip()
            if topLine[ind] != '':
                wordsTopLine[ind] = topLine[ind].split()
                tup = (wordsTopLine[ind][0], ind)
                heapq.heappush(pq, tup)
        
        top_ele = ""
        count = 1
        curr_word = ""
        curr_data = ""
        data = []
        
        while pq:
            top_ele = heapq.heappop(pq)
            new_ind = top_ele[1]
            
            if count%VOCAB_PER_FILE == 0:
                pageCount = Indexer.writeFile(pageCount, file_field, data)
                data = []
                count=1
            
            if curr_word!=top_ele[0] and curr_word!="":
                
                data.append(curr_data)
                count+=1
                curr_word = top_ele[0]
                curr_data = topLine[new_ind]
            else:
                curr_data += " " + " ".join(wordsTopLine[new_ind][1:])
                curr_word = top_ele[0]
            
            topLine[new_ind] = files[new_ind].readline().strip()
            if topLine[new_ind]!='':
                wordsTopLine[new_ind] = topLine[new_ind].split()
                tup = (wordsTopLine[new_ind][0], new_ind)
                heapq.heappush(pq, tup)
            else:
                files[new_ind].close()
                wordsTopLine[new_ind] = []
                file_name = "".join([sys.argv[2], '/index', file_field + str(new_ind) + '.txt'])
                os.remove(file_name)
        
        data.append(curr_data)
        count+=1
        Indexer.writeFile(pageCount, file_field, data)
        
    @staticmethod
    def writeFile(pageCount, file_field, data):
        fil = "".join([sys.argv[2], '/index_', file_field + str(pageCount) + '.txt'])
        fil = open(fil, "w")
        data = "\n".join(data)
        fil.write(data)
        fil.close()
        return pageCount+1
    
    @staticmethod
    def mergedata():
        Indexer.mergeFiles('b')
        Indexer.mergeFiles('t')
        Indexer.mergeFiles('l')
        Indexer.mergeFiles('r')
        Indexer.mergeFiles('c')
        Indexer.mergeFiles('i')