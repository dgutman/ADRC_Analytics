#!/usr/bin/python
# -*- coding: latin-1 -*-
# This will read a list of ADRC publications and try and do some basic network stats on them... I am using a list of publications provided by Janet as a starting point
import re,sys,os
from Bio import Entrez
from Bio.Entrez import efetch, read
import pickle ## Will store Author data object
import urllib2
import simplejson


# I am interested in getting the following attributes:
# AUTHOR LIST, AUTHOR LOCATION, Author University

### I am using this list of authors to then build a connectivity matrix--- but first I need to see who's represented
## The current version returns a hash (with PMID as the key)

### the input file in this case is a text document with PMID or PMCID's
### I wrote a very basic REGEX to pull out the necessary PMID's so I can pull them from PubMed

""" PMCID - PMID - Manuscript ID - DOI Converter
 Enter IDs into the text box using the specified format.
 Separate multiple IDs with spaces or commas. Note: you cannot mix different types of IDs in a single request.
 PMID: use simple numbers, e.g., 23193287.
 PMCID: include the ‘PMC’ prefix, e.g., PMC3531190.
 You may drop the prefix if you select the checkbox for ‘Process as PMCIDs’.
 Manuscript ID: include the relevant prefix, e.g., NIHMS236863 or EMS48932.
 DOI: enter the complete string, e.g., 10.1093/nar/gks1195.
"""

pmid_regex = re.compile('PMID:*\s*(\d+)') ## matches 0 or more spaces
pmcid_regex = re.compile('PMCID:*\s*(PMC\d+)')
debug = False
PMID_LIST = []
PMCID_LIST = []
not_matched = 0
author_affiliation_list = []  # This will likely have to be hand parsed

def format_ddate(ddate):
    """Turn a date dictionary into an ISO-type string (YYYY-MM-DD)."""
    year = ddate['Year']
    month = ddate['Month']
    day = ddate['Day']
    if not month.isdigit():
        month = months_rdict.get(month, None)
        if not month:
            return None
    return "%s-%s-%s" % (year, month.zfill(2), day.zfill(2))

def get_pmid_from_pmcid(pmcid):
	req_url = 'http://www.pubmedcentral.nih.gov/utils/idconv/v1.0/?ids=%s&format=json'
	req = urllib2.Request( ( req_url % pmcid) )
	opener = urllib2.build_opener()
	f= opener.open(req)
	mydata = simplejson.load(f)
	try:
		pmid = mydata['records'][0]['pmid']
		return pmid
	except:
		return None


def get_metadata_from_PMID( pmid, output_errors=False, dump_xml=False ):
    """This function will take an input PMID and parse the attributes I am interested in for the cytoscape plugin...."""
    handle = efetch(db='pubmed', id=pmid, retmode='xml')
    xml_data = read(handle)[0]
    verbose_output = False
#   output_errors= False
    author_affiliation_list = []
    cur_paper_author_list = []

    try:
        date_completed = format_ddate( xml_data['MedlineCitation']['DateCompleted'] )
    except:
        print "Date Completed not available??",pmid
	## Will try date created	
	#date_completed = None
	#date_created = format_ddate( xml_data['MedlineCitation']['DateCreated'] )
	## I am removing the difference between date completed and created-- it doens't really matter for my purposes
	date_completed = format_ddate( xml_data['MedlineCitation']['DateCreated'] )
	
	#fp_error.write('Date Completed Not Avaiable:\n'+str(xml_data)+'\n\n')    

    try:
        otherID = xml_data['MedlineCitation']['OtherID']
    except:
        print "Other ID Not availble??",pmid

    try:
        MeshHeadings = xml_data['MedlineCitation']['MeshHeadingList']
    except:
        print "Unable to get mesheadings for",pmid
	if output_errors: fp_error.write('MESH NOT AVAIABLE:\n'+str(xml_data)+'\n\n')    
    
    try:
        article = xml_data['MedlineCitation']['Article']
        if verbose_output: print xml_data
        for author in article['AuthorList']:
            #author_key = { 'LastNAme': author['LastName'], 'Initials': author['Initials'] }
	    #print author 
	    if 'LastName' in author:
        	author_key =    author['LastName'] + ','+  author['Initials'] 
		#print author,author_key
		cur_paper_author_list.append(author_key)
	    elif 'CollectiveName' in author:
		print "FOUND A COLLECTION EXAMPLE",author
            if 'Affiliation' in author:
	    	author_affil = author['Affiliation']
	    	author_affiliation_list.append( (author, author_affil) )
	    #	print author_affil
	    #	sys.exit()
    except NameError as e:
	print e
    except IndexError:
        return None
    except:
        print "unable to proces article tag",pmid
        print "Unexpected error parsing author string:", sys.exc_info()[0]
	if output_errors: fp_error.write('Article NOT AVAILABLE\n'+str(xml_data)+'\n\n')    
	print author
	#print xml_data

    try:
        abstract = article['Abstract']['AbstractText'][0]
    except:
        print "Unable to get abstract for",pmid




    if dump_xml:
        print xml_data
	return xml_data		
    else:
	return { 'auth_list': cur_paper_author_list, 'affiliations': author_affiliation_list, 'publication_date': date_completed }

if __name__ == "__main__":

    Entrez.email = "dagutman@gmail.com"     # Always tell NCBI who you are
    adrc_file_list = 'input_data/emory_adrc_pubs_v1.txt' ## This is a bibliography pasted as a text file
    pickle_results = True
    pickle_filename = 'adrc.p'

    if os.path.isfile(pickle_filename):
	pmid_metadata_hash = pickle.load( open(pickle_filename, "rb") )
    else:
	pmid_metadata_hash = {}


    #Open and then reaed the file containing the bibliography info
    adrc_fp = open(adrc_file_list,'r')
    adrc_raw_paper_list = adrc_fp.readlines()

    fp_out = open('input_data/need_pmid.txt','w') ## Dump files that need PMID that I coudlnt' fine

    fp_error = open('input_data/parsing_issues.txt','w') # Other debug output
    pub_list = [ pub.strip('\n') for  pub in adrc_raw_paper_list if len(pub)>1 ]   ## turns it into a list and removes the blank spaces

#  Scan through file line by line looking for PMID or PMCID--- each reference is only on a single line
    for pub in pub_list:
        found_PMID = False
        if 'PMID' in pub:
    #    print pub
            m = pmid_regex.search(pub)
            if m:
                if debug: print m.group(0),m.group(1)
                PMID_LIST.append(m.group(1))
                found_PMID = True
            else:
                print "PMID found but pattern not parsed properly...",pub
        elif 'PMCID' in pub and not found_PMID:
            if debug: print "SEarching for PMCID"
            m = pmcid_regex.search(pub)
            if m:
                if debug: print m.group(0),m.group(1)
                PMCID_LIST.append(m.group(1))
                found_PMID = True
            else:
                print "PMID found but pattern not parsed properly...",pub
            
        else:
            print "Did not find PMID or PMCID",pub
    	    fp_out.write(pub+'\n')        
            not_matched += 1
        
    print not_matched,"entries did not have a PMC or PMID"


    for pmid in PMID_LIST:
        if pmid not in pmid_metadata_hash:
		print pmid
       ### If the metadata is already in the pickle file... I don't need to reparse it
        	paper_metadata = get_metadata_from_PMID(pmid)
	        pmid_metadata_hash[pmid] = paper_metadata
	else:
		print "Skipping",pmid,"as we already have data for it..."

    print PMCID_LIST
    for pmcid in PMCID_LIST:
	pmid  = get_pmid_from_pmcid(pmcid)
	print "FOUND IT?",pmid,pmcid
	## Check for None condition
        if pmid and pmid not in pmid_metadata_hash:
		paper_metadata = get_metadata_from_PMID(pmid)
	        pmid_metadata_hash[pmid] = paper_metadata	
	else:
		print "Skipping",pmid,"as we already have data for it..."



    print author_affiliation_list
    if pickle_results:
	pickle.dump( pmid_metadata_hash, open( pickle_filename, "wb" ) )

