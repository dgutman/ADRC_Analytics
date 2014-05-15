__author__ = 'arosado'

import pycurl
import urllib.parse
import collections
from Bio import Entrez
#import HTMLParser
#import sys
from lxml import etree
import lxml.html
import re
import io
#from pdfminer.pdfparser import PDFParser, PDFDocument
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.pdfdevice import PDFDevice, PDFTextDevice
#from pdfminer.converter import PDFPageAggregator
#import pdfminer.layout

class BibTextParser:
    Article = collections.namedtuple('Article', ['DOI', 'Title', 'Source', 'PmcRefCount', 'Issue', 'SO', 'ISSN', 'Volume',
                                              'FullJournalName', 'RecordStatus', 'ESSN', 'ELocationID', 'Pages', 'PubStatus',
                                              'AuthorList', 'EPubDate', 'PubDate', 'NlmUniqueID', 'LastAuthor', 'ArticleIds',
                                              'Item', 'History', 'LangList', 'HasAbstract', 'References', 'PubTypeList', 'Id'])

    Articles = []

    bibFile = FileNotFoundError
    Entrez.email = "aaron.rosado@gmail.com"
    currentFileURL = ''
    pmidList = []

    def handleBibReference(self, bibRef):
        #Process a Bibliography Reference and Obtain Component that can be used in a pubmed search
        entryComponents = re.split("\.\s", bibRef)
        if (len(entryComponents) > 4):
            journalRef = entryComponents[2] + ' ' + entryComponents[3]
        else:
            journalRef = entryComponents[2]

        #Use
        c = pycurl.Curl()
        c.setopt(pycurl.HTTPHEADER, ["Accept:"])

        searchURL = "http://www.ncbi.nlm.nih.gov/pubmed/?term="
        parsedReference = urllib.parse.quote(journalRef)
        fullSearchURL = searchURL + "'" + parsedReference + "'"

        c.setopt(pycurl.URL, fullSearchURL)
        c.setopt(pycurl.HTTPHEADER, ["Accept:"])
        e = io.BytesIO()
        c.setopt(pycurl.WRITEFUNCTION, e.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 10)
        c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
        c.perform()
        # handle = Entrez.esearch(db='pubmed', term=journalRef, field='title')
        # record = Entrez.read(handle)
        return e.getvalue()


    # def parseTxtFile(self):

    def parseBibHTMLForPMID(self, htmlBytes):
        #Parse HTML generated from cURL pubmed search
        #Returns a PMID
        parsedPMID = "Error retreiving PMID"
        root = etree.HTML(htmlBytes, parser=None, base_url=None)

        for element in root.iter():
            if (element.tag == 'meta'):
                x = element.attrib
                if (x.get("name") == "ncbi_term"):
                    parsedPMID = x.get("content")

        return parsedPMID

    def parseBibText(self):
        self.bibFile = io.open(self.currentFileURL, mode='r', encoding="utf-8")
        for line in self.bibFile:
            if (len(re.split('\.\s', line)) > 2):
                htmlFromNCBIForRef = self.handleBibReference(line)
                pmidFromNCBIRef = self.parseBibHTMLForPMID(htmlFromNCBIForRef)
                if (len(re.split('\[uid\]', pmidFromNCBIRef)) > 1):
                    formatedPMID = pmidFromNCBIRef[0:(len(pmidFromNCBIRef)-5)]
                    self.pmidList.append(formatedPMID)

                # handle = Entrez.esummary(db="pubmed", id=formatedPMID)
                # record = Entrez.read(handle)
                #
                # self.Articles.append(self.Article(**record[0]))


    def buildArticleCollection(self):
        pmidListString = ''
        for x in range(len(self.pmidList)):
            pmidListString = pmidListString + ' ' + self.pmidList[x]

        handle = Entrez.esummary(db="pubmed", id=pmidListString)
        record = Entrez.read(handle)

        for x in range(0, len(record)):
            self.Articles.append(self.Article(**record[x]))











    def __init__(self, currentFileURL):
        self.currentFileURL = currentFileURL


BibPars = BibTextParser("gutman_bib.txt")
testHtmlBytes = BibPars.parseBibText()
BibPars.buildArticleCollection()
