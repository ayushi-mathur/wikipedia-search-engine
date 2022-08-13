import xml.sax
from page import Page

class HandlePages(xml.sax.ContentHandler):
    
    def __init__(self) -> None:
        super().__init__()
        self.currTag = ''
        self.title = ''
        self.text = ''
        self.pageId = 0
        self.numbytes = 0
        self.currText = ''
        self.scounts = 0
    
    def startElement(self, tag, attrs):
        self.currTag = tag
        if tag == 'text':
            attrib_set = attrs.getNames()
            if "bytes" in attrib_set:
                self.numbytes = int(attrs.getValue("bytes"))
    
    def endElement(self, tag):
        if tag == 'page':
            pag = Page()
            # if self.currTag == ""
            # self.text = self.text.join(self.currText)
            print(self.text)
            processed_data = pag.processCorpus(self.text, self.title)
            
            print(processed_data[0])
            # if len(processed_data)>1:
            #     print(processed_data[1])
            self.currTag = ''
            self.title = ''
            self.text = ''
            self.pageId = ''
            self.currText = ''
            # TODO
            # pag = Page()
        elif tag == 'text':
            if self.numbytes > 1000 or True:
                self.text = self.text.join(self.currText)
    
    def characters(self, content):
        if self.currTag == 'title':
            self.title = "".join([self.title, content])
        elif self.currTag == 'text':
            if self.numbytes < 1000:
                self.text = "".join([self.text, content])
                # print(content)
                
            else:
                self.currText = "".join([self.currText, content])
                if self.scounts<300:
                    self.scounts+=1
                else:
                    self.text = "".join([self.text, self.currText])
                    self.currText = ''
                    self.scounts = 0
        elif self.currTag == 'id' and self.pageId == '':
            self.pageId = content
    
class Parser():
    
    def __init__(self, file) -> None:
        self.parser = xml.sax.make_parser()
        self.handler = HandlePages()
        self.parser.setContentHandler(self.handler)
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.parser.parse(file)