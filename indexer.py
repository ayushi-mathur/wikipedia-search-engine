from collections import defaultdict
import string

class Indexer():
    indexMapT, indexMapB, indexMapL, indexMapR, indexMapC, indexMapI = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    fileCount, pageCount = 0, 0
    
    ALPHABET = "".join([string.digits, string.ascii_lowercase, string.ascii_uppercase, '+_'])
    ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
    BASE = len(ALPHABET)
    
    # Encodes a positive integer to base 64 coding
    @classmethod
    def num_encode(n):
        s = []
        while 1:
            n, r = divmod(n, Indexer.BASE)
            s.append(Indexer.ALPHABET[r])
            if n == 0: break
        return ''.join(reversed(s))

    # Decodes a base 64 coding to a positive integer
    @classmethod
    def num_decode(s):
        n = 0
        for c in s:
            n = n * Indexer.BASE + Indexer.ALPHABET_REVERSE[c]
        return n

    def __init__(self, title, body, info, categories, links, references) -> None:
        self.title, self.body, self.info, self.categories, self.links, self.references = title, body, info, categories, links, references 
    
    def createIndex(self):
        Id = self.num_encode(Indexer.pageCount)
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
        
        