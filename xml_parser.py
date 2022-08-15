import xml.sax
from page import Page
from indexer import Indexer

class HandlePages(xml.sax.ContentHandler):
    
    def __init__(self) -> None:
        super().__init__()
        self.currTag = ''
        self.title = ''
        self.text = ''
        self.pageId = 0
    
    def startElement(self, tag, attrs):
        self.currTag = tag
    
    def isUseful(self):
        return not self.title.startswith("Wikipedia:")

    def endElement(self, tag):
        if tag == 'page':
            if self.isUseful():
                pag = Page()
                title, infobox, body, categories, links, references = pag.processCorpus(self.text, self.title)
                i = Indexer(title, body, infobox, categories, links, references)
                i.createIndex()
            self.currTag = ''
            self.title = ''
            self.text = ''
            self.pageId = 0
    
    def characters(self, content):
        if self.currTag == 'title':
            self.title = f"{self.title}{content}"
        elif self.currTag == 'text':
            self.text = f"{self.text}{content}"
        elif self.currTag == 'id' and self.pageId == '':
            self.pageId = content
    
class Parser():
    
    def __init__(self, file) -> None:
        self.parser = xml.sax.make_parser()
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.handler = HandlePages()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(file)