#Taken fromStackOverflow
#http://stackoverflow.com/questions/5360220/how-to-split-a-list-into-pairs-in-all-possible-ways
import pickle
import os,sys
import itertools

pickle_filename = 'adrc.p'

if os.path.isfile(pickle_filename):
    paper_author_lists = pickle.load( open(pickle_filename, "rb") )
else:
    paper_author_lists = {}

print len(paper_author_lists),"papers included in current data set"

### First need to iterate through all of the paper author lists

def all_pairs(lst):
    if len(lst) < 2:
        yield lst
        return
    a = lst[0]
    for i in range(1,len(lst)):
        pair = (a,lst[i])
        for rest in all_pairs(lst[1:i]+lst[i+1:]):
            yield [pair] + rest

for author_list in paper_author_lists:
    print author_list
#    print [ p for p in itertools.combinations(author_list,2) ]
    print list( itertools.combinations(author_list,2) )
#http://nsaunders.wordpress.com/2013/09/17/web-scraping-using-mechanize-pmid-to-pmcidnihmsid/
#    if len(author_list) ==4 :
#    	print [ p for p in all_pairs(author_list) ] 
#	sys.exit()
#http://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

#"""The service can provide output in a number of formats, as specified by the format parameter, which can be one of "html", "xml", "json", or "csv". "xml" is the dafault, and several examples of this response format are given above. Examples of each of the other formats is shown below.

#JSON
#>>> import urllib2
#>>> import simplejson
#>>> req = urllib2.Request("http://vimeo.com/api/v2/video/38356.json", None, {'user-agent':'syncstream/vimeo'})
#>>> opener = urllib2.build_opener()
#>>> f = opener.open(req)
#>>> f.read()   
#f = opener.open(req)
#simplejson.load(f)
#http://www.pubmedcentral.nih.gov/utils/idconv/v1.0/?ids=PMC2883744&format=json
#http://people.duke.edu/~ccc14/pcfb/biopython/BiopythonEntrez.html
#import urllib2
#import simplejson
#req_url = 'http://www.pubmedcentral.nih.gov/utils/idconv/v1.0/?ids=%s&format=json'
#req = urllib2.Request( (req_url % pmcid) )
#opener = urllib2.build_opener()
#f = opener.open(req)
#mydata = simplejson.load(f)

sample_json = {
  "status": "ok",
  "responseDate": "2013-09-23 14:28:14",
  "request": "ids=PMC2883744;format=json",
  "records": [
    {
      "pmcid": "PMC2883744",
      "pmid": "20495566",
      "doi": "10.1038/ng.590",
      "versions": [
        {
          "pmcid": "PMC2883744.1",
          "mid": "UKMS29888"
        },
        {
          "pmcid": "PMC2883744.2",
          "mid": "NIHMS198092",
          "current": True
        }
      ]
    }
  ]
}
