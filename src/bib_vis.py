__author__ = 'arosado'

import pycurl
import urllib.parse
import collections
import types
from Bio import Entrez
#import HTMLParser
#import sys
from lxml import etree
import lxml.html
import re
import io
import os
import pickle
#import json

Journal = collections.namedtuple('Journal', ['Rank', 'AbrevTitle', 'IsiLink', 'ISSN', 'TotalCit', 'ImpactFactor', 'FiveYearImpactFactor',
                                                 'ImmedIndex', 'Articles', 'CitedHalfLife', 'EigenfactorScore', 'ArticleInfluenceScore'])
Article = collections.namedtuple('Article', ['DOI', 'Title', 'Source', 'PmcRefCount', 'Issue', 'SO', 'ISSN', 'Volume',
                                              'FullJournalName', 'RecordStatus', 'ESSN', 'ELocationID', 'Pages', 'PubStatus',
                                              'AuthorList', 'EPubDate', 'PubDate', 'NlmUniqueID', 'LastAuthor', 'ArticleIds',
                                              'Item', 'History', 'LangList', 'HasAbstract', 'References', 'PubTypeList', 'Id'])
Journals = []
Articles = []

from tkinter import tix
#from pdfminer.pdfparser import PDFParser, PDFDocument
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.pdfdevice import PDFDevice, PDFTextDevice
#from pdfminer.converter import PDFPageAggregator
#import pdfminer.layout

class BibTextParser:


    Articles = []

    bibFilesURLs = []
    Entrez.email = "aaron.rosado@gmail.com"
    currentDirectoryURL = ''
    articleCollectionPickleFileName = ''
    pmidList = []
    currentBibFile = FileNotFoundError

    def handleBibReference(self, bibRef):
        #Process a Bibliography Reference
        #Return a PMID from the reference

        entryComponents = re.split("\.\s", bibRef)

        refPMID = self.processBibRefComponents(entryComponents)

        return refPMID

    def processBibRefComponents(self, bibRefComponents):
        return bibRefComponents


    # def parseTxtFile(self):

    def retrieveArticleNCBIHTMLFromPMCID(self, pmcid):
        #Take a parsed reference element and use it to acquire HTML from NCBI
        c = pycurl.Curl()
        c.setopt(pycurl.HTTPHEADER, ["Accept:"])

        searchURL = "http://www.ncbi.nlm.nih.gov/pubmed/?term="
        parsedReference = urllib.parse.quote(pmcid)
        fullSearchURL = searchURL + parsedReference

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

    def retrieveArticleNCBIHTMLFromBrokenDownRefComponents(self, refComponents):

        c = pycurl.Curl()
        c.setopt(pycurl.HTTPHEADER, ["Accept:"])

        searchURL = "http://www.ncbi.nlm.nih.gov/pubmed/?term="

        refSearchString = "'"

        for component in refComponents:
            refSearchString = refSearchString + component + "'"

        parsedReference = urllib.parse.quote(refSearchString)
        fullSearchURL = searchURL + parsedReference

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

    def parseBibHTMLForPMID(self, htmlBytes):
        #Parse HTML generated from cURL pubmed search
        #Returns a PMID
        pmid = "Error retreiving PMID"
        root = etree.HTML(htmlBytes, parser=None, base_url=None)

        for element in root.iter():
            if (element.tag == 'dl'):
                if (element.get('class') == 'rprtid'):
                    rprtid = element.getchildren()
                    if (len(rprtid[1].getchildren()) > 0):
                        subElements = rprtid[1].getchildren()
                        pmid = subElements[0].text
                    else:
                        pmid = rprtid[1].text

        return pmid

    def parseBibText(self):
        self.bibFilesURLs = os.listdir(self.currentDirectoryURL)
        for bibURL in self.bibFilesURLs:
            currentBibURL = self.currentDirectoryURL + '/' + bibURL
            self.currentBibFile = io.open(currentBibURL, mode='r', encoding="utf-8")
            for line in self.currentBibFile:
                brokenDownReference = re.split('\.\s', line)
                if (len(brokenDownReference) > 1):
                    pmid = self.retrievePMIDfromBrokenDownReference(brokenDownReference)
                    self.pmidList.append(pmid)

            self.currentBibFile.close()

    def retrievePMIDfromBrokenDownReference(self, brokenDownReference):
        for refComponent in brokenDownReference:
            if re.search('PMID', refComponent):
                processedRefComponents = re.findall("(?<=PMID:)\s*\d+(?=\s)", refComponent)
                if (len(processedRefComponents) > 0):
                    prePmid = re.findall('\d+', processedRefComponents[0])
                    pmid = prePmid[0]
                    return pmid
            if re.search('PMCID', refComponent):
                processedRefComponents = re.findall("(?<=PMCID:)\s*PMC\d+", refComponent)
                if (len(processedRefComponents) > 0):
                    prePmcid = re.findall('PMC\d+', processedRefComponents[0])
                    pmcid = prePmcid[0]
                    refNCBIHTML = self.retrieveArticleNCBIHTMLFromPMCID(pmcid)
                    pmid = self.parseBibHTMLForPMID(refNCBIHTML)
                    return pmid
        # borkenDownReferenceLength = len(brokenDownReference)
        # ncbiSearchString = "'"+ brokenDownReference[0] + "' " + brokenDownReference[1]
        relevantRefComponents = [brokenDownReference[0], brokenDownReference[1]]
        refNCBIHTML = self.retrieveArticleNCBIHTMLFromBrokenDownRefComponents(relevantRefComponents)
        pmid = self.parseBibHTMLForPMID(refNCBIHTML)
        if (pmid == 'Error retreiving PMID'):
            refNCBIHTML = self.retrieveArticleNCBIHTMLFromBrokenDownRefComponents(brokenDownReference[0])
            pmid = self.parseBibHTMLForPMID(refNCBIHTML)
        return pmid


                # handle = Entrez.esummary(db="pubmed", id=formatedPMID)
                # record = Entrez.read(handle)
                #
                # self.Articles.append(self.Article(**record[0]))


    def buildArticleCollection(self):
        pmidListString = ''
        for x in range(len(self.pmidList)):
            if(self.pmidList[x] != 'Error retreiving PMID'):
                pmidListString = pmidListString + ' ' + self.pmidList[x]

        handle = Entrez.esummary(db="pubmed", id=pmidListString)
        record = Entrez.read(handle)

        for x in range(0, len(record)):
            if ('DOI' not in record[x]):
                record[x]['DOI'] = ''
                Articles.append(Article(**record[x]))
            else:
                Articles.append(Article(**record[x]))

        self.Articles = Articles


    def saveArticlePickle(self):
        file = open('article.pickle', 'wb')
        pickle.dump(Articles, file)

    def openArticlePickle(self):
        file = open('article.pickle', 'rb')
        pickle.load(file)

    def __init__(self, directoryPath):
        self.currentDirectoryURL = directoryPath

class IsiParser:

    isiCurl = pycurl.Curl()
    initialJCRurl = 'http://admin-router.webofknowledge.com/?DestApp=JCR'
    isiPickleFileName = ''
    SID = ''
    initialCookies = []
    updatedCookies = []
    currentHTML = ''
    #Journal = collections.namedtuple('Journal', ['Rank', 'AbrevTitle', 'IsiLink', 'ISSN', 'TotalCit', 'ImpactFactor', 'FiveYearImpactFactor',
    #                                             'ImmedIndex', 'Articles', 'CitedHalfLife', 'EigenfactorScore', 'ArticleInfluenceScore'])
    totalNumberOfJournals = 8471
    totalNumberOfPages = 424

    Journals = []



    def intiateJCRConnection(self):
        self.isiCurl.setopt(pycurl.URL, self.initialJCRurl)
        self.isiCurl.setopt(pycurl.HTTPHEADER, ["Accept:"])
        e = io.BytesIO()
        self.isiCurl.setopt(pycurl.WRITEFUNCTION, e.write)
        self.isiCurl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.isiCurl.setopt(pycurl.MAXREDIRS, 10)
        self.isiCurl.setopt(pycurl.COOKIEFILE, 'cookie.txt')
        self.isiCurl.perform()

        self.initialCookies = self.isiCurl.getinfo(pycurl.INFO_COOKIELIST)
        self.SID = self.getSIDFromCookies(self.initialCookies)

    def getSIDFromCookies(self, cookies):

        for cookie in cookies:
            foundSID = re.findall('(?<=SID\s["]).*(?=["])', cookie)
            if (len(foundSID) > 0):
                return foundSID[0]

    def postToGetAllJournalInformation(self, SID):
        self.isiCurl.setopt(pycurl.URL, 'http://admin-apps.webofknowledge.com/JCR/JCR')
        fullPostField = 'edition=science&science_year=2012&social_year=2012&view=category&RQ=SELECT_ALL&change_limits=&Submit.x=1&SID=' + \
                        SID + '&query_new=true'
        self.isiCurl.setopt(pycurl.POSTFIELDS, fullPostField)
        e = io.BytesIO()
        self.isiCurl.setopt(pycurl.WRITEFUNCTION, e.write)
        self.isiCurl.perform()

        self.updatedCookies = self.isiCurl.getinfo(pycurl.INFO_COOKIELIST)

        self.currentHTML = e.getvalue()

    def parseJCR(self):
        cursor = 1
        self.parseJCRHtml(self.currentHTML)
        for x in range(1,self.totalNumberOfPages):
            cursor = cursor + 20
            newCursorUrl = 'http://admin-apps.webofknowledge.com/JCR/JCR?RQ=SELECT_ALL&cursor='+cursor.__str__()
            self.isiCurl.setopt(pycurl.URL, newCursorUrl)
            e = io.BytesIO()
            self.isiCurl.setopt(pycurl.WRITEFUNCTION, e.write)
            self.isiCurl.perform()
            self.currentHTML = e.getvalue()
            self.parseJCRHtml(self.currentHTML)

        return Journals



    def parseJCRHtml(self, jcrHtml):
        root = etree.HTML(jcrHtml, parser=None, base_url=None)
        for element in root.iter():
            if ((element.tag == 'table') and (element.getchildren()[0].getchildren()[0].get('class') == 'dataTableHeader')):
                journalData = element.getchildren()
                for journalEntry in journalData[4:(len(journalData)-2)]:
                    dataEntry = journalEntry.getchildren()
                    spacer = dataEntry[0].text
                    rank = dataEntry[1].text
                    journalInfo = dataEntry[2].getchildren()[0]
                    abvJournalTitle = journalInfo.text
                    isiLink = journalInfo.get('href')
                    ISSN = dataEntry[3].text
                    totalCites = dataEntry[4].text
                    impactFactor = dataEntry[5].text
                    fiveYearImpactFactor = dataEntry[6].text
                    immedIndex = dataEntry[7].text
                    articles = dataEntry[8].text
                    citedHalfLife = dataEntry[9].text
                    eigenfactorScore = dataEntry[10].text
                    articleInfluenceScore = dataEntry[11].text

                    Journals.append(Journal(rank, abvJournalTitle, isiLink, ISSN, totalCites, impactFactor, fiveYearImpactFactor, immedIndex, articles, citedHalfLife, eigenfactorScore, articleInfluenceScore))

    def saveJournalPickle(self):
        file = open('journal.pickle', 'wb')
        pickle.dump(Journals, file, pickle.HIGHEST_PROTOCOL)

    def openJournalPickle(self):
        file = open('journal.pickle', 'rb')
        self.Journals = pickle.load(file)
        print('Successful')


    def  __init__(self, isiPickleFileName):
        #setup the file
        self.isiPickleFileName = isiPickleFileName







BibPars = BibTextParser('C:/Users/arosado/Documents/GitHub/ADRC_Analytics/src/input_data')
#testHtmlBytes = BibPars.parseBibText()
#BibPars.buildArticleCollection()
#BibPars.saveArticlePickle()
#BibPars.openArticlePickle()

IsiP = IsiParser('test')
# # IsiP.intiateJCRConnection()
# # IsiP.postToGetAllJournalInformation(IsiP.SID)
# # IsiP.parseJCR()
# # IsiP.saveJournalPickle()
IsiP.openJournalPickle()


