from collections import defaultdict
import string
import sys
import heapq
import os
import pickle as pkl
PREINDEX_PAGE_COUNT = 15000
VOCAB_PER_FILE = 50000
TITLE_PER_FILE = 50000
DICT_SIZE = 30000

class Indexer:
    indDictT, indDictB, indDictL, indDictR, indDictC, indDictI = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    file_cnt, pageCount = 0, 0
    titleIdMap = []
    articleFileCount = 0

    ENCODING = "".join([string.digits, string.ascii_lowercase, string.ascii_uppercase, '+!'])
    BASE = len(ENCODING)
    ENCODING_REVERSE = dict((c, i) for (i, c) in enumerate(ENCODING))
    
    def __init__(self, title=[], body=[], info=[], categories=[], links=[], references=[], og_title="") -> None:
        self.title, self.body, self.info, self.categories, self.links, self.references, self.og_title = title, body, info, categories, links, references, og_title
    
    @staticmethod
    def decode_number(s):
        n = 0
        for c in s:
            n = n * Indexer.BASE + Indexer.ENCODING_REVERSE[c]
        return n

    @staticmethod
    def encode_number(n):
        s = []
        while n:
            n, r = divmod(n, Indexer.BASE)
            s.append(Indexer.ENCODING[r])
        if s==[]:
            s=['0']
        return ''.join(reversed(s))


    def buildIndex(self):
        Id = Indexer.encode_number(Indexer.pageCount)
        Indexer.titleIdMap.append(f"{Id} {self.og_title}")
        freq_dict = {}
        common_freq_dict = {}
        
        for word in self.title:
            if word in freq_dict:
                freq_dict[word]+=1
            else:
                freq_dict[word]=1
            
            if word in common_freq_dict:
                common_freq_dict[word]+=1
            else:
                common_freq_dict[word] = 1
        title = freq_dict
        
        freq_dict = {}
        for word in self.categories:
            if word in freq_dict:
                freq_dict[word]+=1
            else:
                freq_dict[word]=1
            
            if word in common_freq_dict:
                common_freq_dict[word]+=1
            else:
                common_freq_dict[word] = 1
        categories = freq_dict
        
        freq_dict = {}
        for word in self.info:
            if word in freq_dict:
                freq_dict[word]+=1
            else:
                freq_dict[word]=1
            
            if word in common_freq_dict:
                common_freq_dict[word]+=1
            else:
                common_freq_dict[word] = 1
        info = freq_dict
        
        freq_dict = {}
        for word in self.references:
            if word in freq_dict:
                freq_dict[word]+=1
            else:
                freq_dict[word]=1
            
            if word in common_freq_dict:
                common_freq_dict[word]+=1
            else:
                common_freq_dict[word] = 1
        references = freq_dict
        
        freq_dict = {}
        for word in self.body:
            if word in freq_dict:
                freq_dict[word]+=1
            else:
                freq_dict[word]=1
            
            if word in common_freq_dict:
                common_freq_dict[word]+=1
            else:
                common_freq_dict[word] = 1
        body = freq_dict
        
        freq_dict = {}
        for word in self.links:
            if word in freq_dict:
                freq_dict[word]+=1
            else:
                freq_dict[word]=1
            
            if word in common_freq_dict:
                common_freq_dict[word]+=1
            else:
                common_freq_dict[word] = 1
        links = freq_dict
        
        for word in common_freq_dict.keys():
            if word in title:
                Indexer.indDictT[word].append(f"{Id}:{title[word]}")
            if word in references:
                Indexer.indDictR[word].append(f"{Id}:{references[word]}")
            if word in info:
                Indexer.indDictI[word].append(f"{Id}:{info[word]}")
            if word in body:
                Indexer.indDictB[word].append(f"{Id}:{body[word]}")
            if word in categories:
                Indexer.indDictC[word].append(f"{Id}:{categories[word]}")
            if word in links:
                Indexer.indDictL[word].append(f"{Id}:{links[word]}")
        
        Indexer.pageCount += 1
        
        if Indexer.pageCount%PREINDEX_PAGE_COUNT == 0:
            Indexer.writePages()
        if Indexer.pageCount%TITLE_PER_FILE == 0 and Indexer.pageCount>0:
            Indexer.writeTitleFile()
            
    @staticmethod
    def writeTitleFile():
        if len(Indexer.titleIdMap)==0:
            return
        data = "\n".join(Indexer.titleIdMap)
        filename = f"{sys.argv[2]}/title{str(Indexer.articleFileCount)}.txt"
        with open(filename, "w") as f:
            f.write(data)
        Indexer.titleIdMap = []
        Indexer.articleFileCount+=1

    @staticmethod
    def writePagesToTmpInd(fieldindicator, index, file_cnt):

        data = list()
        for key in sorted(index.keys()):
            string = f"{key} {' '.join(index[key])}"
            data.append(string)

        # filename = sys.argv[2] + '/index' + str(fieldindicator)+ str(file_cnt) + '.txt'
        fil = f"{sys.argv[2]}/index{str(fieldindicator)}{str(file_cnt)}.txt"
        data = '\n'.join(data)
        f = open(fil, 'w')
        f.write(data)
        f.close()
    
    @staticmethod
    def writePages():
        Indexer.writePagesToTmpInd('t', Indexer.indDictT, Indexer.file_cnt)
        Indexer.writePagesToTmpInd('i', Indexer.indDictI, Indexer.file_cnt)
        Indexer.writePagesToTmpInd('b', Indexer.indDictB, Indexer.file_cnt)
        Indexer.writePagesToTmpInd('l', Indexer.indDictL, Indexer.file_cnt)
        Indexer.writePagesToTmpInd('c', Indexer.indDictC, Indexer.file_cnt)
        Indexer.writePagesToTmpInd('r', Indexer.indDictR, Indexer.file_cnt)

        Indexer.indDictR = defaultdict(list)
        Indexer.indDictI = defaultdict(list)
        Indexer.indDictB = defaultdict(list)
        Indexer.indDictL = defaultdict(list)
        Indexer.indDictT = defaultdict(list)
        Indexer.indDictC = defaultdict(list)

        Indexer.file_cnt += 1
        
    def mergeIndexFiles(file_field):
        pq = []
        wordsFirstLine = {}
        files_arr = {}
        FirstLine = {}
        page_cnt = 0
        
        vocabfiledata = []
        
        # print(Indexer.file_cnt)
        for ind in range(Indexer.file_cnt):
            fil = "".join([sys.argv[2], '/index', file_field + str(ind) + '.txt'])
            files_arr[ind] = open(fil, 'r')
            FirstLine[ind]=files_arr[ind].readline().strip()
            if FirstLine[ind] == '':
                continue
            wordsFirstLine[ind] = FirstLine[ind].split()
            tup = (wordsFirstLine[ind][0], ind)
            heapq.heappush(pq, tup)
        
        top_ele = ""
        count = 1
        net_count = 0
        curr_word = ""
        curr_data = ""
        data = []
        curr_freq = 0
        
        offset = [0]
        
        while pq:
            top_ele = heapq.heappop(pq)
            new_ind = top_ele[1]
            
            if count%VOCAB_PER_FILE == 0:
                page_cnt = Indexer.writeFile(page_cnt, file_field, data, offset)
                data = []
                count=1
                offset = [0]
                
            if curr_word!=top_ele[0] and curr_word!="":
                
                data.append(curr_data)
                
                offset.append(offset[-1]+len(curr_data)+1)
                count+=1
                vocabfiledata.append(f"{curr_word} {curr_freq}-{page_cnt}")
                curr_word = top_ele[0]
                curr_data = FirstLine[new_ind]
                net_count += 1
                curr_freq = 1
            else:
                # curr_data += " " + " ".join(wordsTopLine[new_ind][1:])
                curr_data = f"{curr_data} {' '.join(wordsFirstLine[new_ind][1:])}"
                curr_word = top_ele[0]
                curr_freq+=1
            
            FirstLine[new_ind] = files_arr[new_ind].readline().strip()
            if FirstLine[new_ind]!='':
                wordsFirstLine[new_ind] = FirstLine[new_ind].split()
                tup = (wordsFirstLine[new_ind][0], new_ind)
                heapq.heappush(pq, tup)
            else:
                files_arr[new_ind].close()
                wordsFirstLine[new_ind] = []
                fil = "".join([sys.argv[2], '/index', file_field + str(new_ind) + '.txt'])
                os.remove(fil)
        
        data.append(curr_data)
        offset.append(offset[-1]+len(curr_data)+1)
        count+=1
        vocabfiledata.append(f"{curr_word} {curr_freq}-{page_cnt}")
        Indexer.writeFile(page_cnt, file_field, data, offset)
        
        with open(sys.argv[2] + "/vocab" + file_field+".txt", "a") as f:
            vocabfiledata = "\n".join(vocabfiledata)
            f.write(vocabfiledata)
        return net_count
    
    @staticmethod
    def mergeVocabulary():
        pq = []
        wordsFirstLine = {}
        files = {}
        firstLine = {}
        page_cnt = 0
        count = 1
        
        vocabfiledata = []
        file_cnt = 6
        FIELDS = ['b', 't', 'c', 'i', 'r', 'l']
        
        # print(Indexer.file_cnt)
        finalFileCount = 0
        for ind in range(file_cnt):
            fil = "".join([sys.argv[2], '/vocab', FIELDS[ind] + '.txt'])
            files[ind] = open(fil, 'r')
            firstLine[ind]=files[ind].readline().strip()
            if firstLine[ind] != '':
                wordsFirstLine[ind] = firstLine[ind].split()
                tup = (wordsFirstLine[ind][0], ind)
                heapq.heappush(pq, tup)
        
        top_ele = ""
        curr_word = ""
        curr_data = ""
        data = []
        curr_freq = 0
        
        while pq:
            top_ele = heapq.heappop(pq)
            new_ind = top_ele[1]
            
            if count%DICT_SIZE == 0:
                page_cnt = Indexer.writeVocabFile(page_cnt, data)
                data = []
                count=1

            if curr_word!=top_ele[0] and curr_word!="":
                
                data.append(curr_data)
                curr_word = top_ele[0]
                curr_data = f"{curr_word} {FIELDS[new_ind]}-{wordsFirstLine[new_ind][1]}"
                curr_freq = 0
                count+=1
            else:
                # curr_data += " " + " ".join(wordsTopLine[new_ind][1:])
                # curr_data = f"{curr_data} {' '.join(wordsTopLine[new_ind][1:])}"
                curr_data = f"{curr_data} {FIELDS[new_ind]}-{wordsFirstLine[new_ind][1]}"
                curr_word = top_ele[0]
                curr_freq+=1
            
            firstLine[new_ind] = files[new_ind].readline().strip()
            if firstLine[new_ind]!='':
                wordsFirstLine[new_ind] = firstLine[new_ind].split()
                tup = (wordsFirstLine[new_ind][0], new_ind)
                heapq.heappush(pq, tup)
            else:
                files[new_ind].close()
                wordsFirstLine[new_ind] = []
                fil = "".join([sys.argv[2], '/vocab', FIELDS[new_ind] + '.txt'])
                os.remove(fil)
        
        data.append(curr_data)
        Indexer.writeVocabFile(page_cnt, data)
        # with open(sys.argv[2] + "/vocab.txt", "a") as f:
        #     vocabfiledata = "\n".join(data)
        #     f.write(vocabfiledata)
    
    @staticmethod
    def writeFile(pageCount, file_field, data, offset):
        fil = "".join([sys.argv[2], '/index_', file_field + str(pageCount) + '.txt'])
        fil = open(fil, "w")
        data = "\n".join(data)
        fil.write(data)
        fil.close()
        
        pkl_file = open(f"{sys.argv[2]}/offset_{file_field}{pageCount}.pkl", "wb")
        pkl.dump(offset, pkl_file)
        pkl_file.close()
        return pageCount+1
    
    @staticmethod
    def writeVocabFile(pageCount, data):
        fil = "".join([sys.argv[2], '/vocab_', str(pageCount) + '.txt'])
        fil = open(fil, "w")
        data = "\n".join(data)
        fil.write(data)
        fil.close()
        return pageCount+1
    
    @staticmethod
    def mergedata():
        total_count = 0
        total_count += Indexer.mergeIndexFiles('b')
        total_count += Indexer.mergeIndexFiles('t')
        total_count += Indexer.mergeIndexFiles('l')
        total_count += Indexer.mergeIndexFiles('r')
        total_count += Indexer.mergeIndexFiles('c')
        total_count += Indexer.mergeIndexFiles('i')
        Indexer.mergeVocabulary()
        return total_count
