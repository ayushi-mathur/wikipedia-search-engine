from Stemmer import Stemmer
import re

class Page():
    # Directly using NLTK stopwords to avoid package import
    stopWords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])
    stemmer = Stemmer('english')
    uniqueWords = set()

    def __init__(self) -> None:
        pass
    
    def cleanData(self, data):
        tokens_to_replace = ['—', '|', '&apos;', '&', "'", '–', '=', '#', '[', ':', '&quot;', ']', '^', '%', '`', '!', '+', '&lt;', '{', '"', '&gt;', '&nbsp;', '}', '*', '/', '~', '.', ',', '@', '_', '(', '\n', ';', '\\', '>', '<', 'http', '-', ')', '$', '?', '&amp;', "\n"]
        for token in tokens_to_replace:
            data = data.replace(token, " ")
        return data

    def isValid(self, ele):
        if ele in Page.stopWords:
            return False
        length = len(ele)
        if ele.isalpha() and len(ele)>=3 and len(ele)<=12:
            return True
        if ele.isnumeric() and len(ele)<=6:
            return True
        return False
    
    def getStemmedTokens(self, data, isPage=True):
        data = data.encode("ascii", errors="ignore").decode()

        data = self.cleanData(data)
        
        data = data.split()
        if isPage:
            for ele in data:
                Page.uniqueWords.add(ele)

        stemmedtokens = [ele for ele in data if self.isValid(ele)]
        stemmedtokens = Page.stemmer.stemWords(stemmedtokens)
        return stemmedtokens
    
    def processCorpus(self, text, title):
        
        # Case lowering
        text = text.lower()
        title = title.lower()
        # text = text.replace("\n", " ")
        # title = title.replace("\n", " ")

        string_to_replace = [" ==", "== "]
        for s in string_to_replace:
            text = text.replace(s, "==")
        
        data = text.split("==references==")
        if len(data)==1:
            references, externalLinks = [], []
        else:
            references = self.getReferences(data[1])
            externalLinks = self.getExternalLinks(data[1])
        title = self.getStemmedTokens(title)
        body = self.getBody(data[0])
        infobox = self.getInfoBox(data[0])
        categories = self.getCategories(text)
        return title, infobox, body, categories, externalLinks, references
    
    def getBody(self, text):
        # text = re.sub(r'\{\{.*\}\}', r' ', text)
        text = re.sub(r'{{infobox(.|\n|\r)*?^}}$', r' ', text, flags=re.M)

        body = self.getStemmedTokens(text)
        return body
    
    def getInfoBox(self, text):
        infobox_data = ""
        infobox_text = text.split("{{infobox")
        for i in range(1, len(infobox_text)):
            curr_infobox = infobox_text[i].split("\n")
            for line in curr_infobox:
                if line.strip() == "}}": break
                infobox_data = " ".join([infobox_data, line])
        infobox = self.getStemmedTokens(infobox_data)
        return infobox
    
    def getReferences(self, text):
        # Remove data after the next == to remove the external links
        data = text.split('==', maxsplit=1)
        data = data[0]

        references = self.getStemmedTokens(data)
        return references
    
    def getCategories(self, text):
        data = text.split("[[category:")
        categories = ""
        for i in range(1, len(data)):
            index = data[i].find("\]\]")
            categories = " ".join([categories, data[i][:index]])
        categories = self.getStemmedTokens(categories)
        return categories
    
    def getExternalLinks(self, text):
        data = text.split("==external links==")
        if len(data)>1:
            data = data[1]
            external_links = self.getStemmedTokens(data)
            return external_links
        return []
