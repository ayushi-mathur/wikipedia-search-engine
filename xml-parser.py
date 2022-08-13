import xml.sax

class HandlePages(xml.sax.ContentHandler):
    
    def __init__(self) -> None:
        super().__init__()
        self.currData = ''
        self.title = ''
        self.text = ''
        self.pageId = ''
        # self.idFlag = 0 Not necessary?
        self.numbytes = 0
        self.currText = ''
        self.scounts = 0
    
    def startElement(self, tag, attrs):
        self.CurrentData = tag
        if tag == 'text':
            attrib_set = attrs.getNames()
            if "bytes" in attrib_set:
                self.numbytes = int(attrs.getValue("bytes"))
    
    def endElement(self, tag):
        if tag == 'page':
            # TODO
            # pag = Page()
            pass
        elif tag == 'text':
            if self.numbytes > 50000:
                self.text.join(self.currText)
    
    def characters(self, content):
        if self.CurrentData == 'title':
            self.title.join(content)
        elif self.CurrentData == 'text':
            if self.numbytes < 50000:
                self.text.join(content)
            else:
                self.currText.join(content)
                if self.scounts<3000:
                    self.scounts+=1
                else:
                    self.text.join(self.currText)
                    self.currText = ''
                    self.scounts = 0
        elif self.currData == 'id' and self.pageId == '':
            self.pageId = content
    
    