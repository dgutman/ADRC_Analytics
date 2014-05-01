#Taken fromStackOverflow
#http://stackoverflow.com/questions/5360220/how-to-split-a-list-into-pairs-in-all-possible-ways
import pickle
import os,sys
import itertools
from pprint import pprint 
pickle_filename = 'adrc.p'
from collections import OrderedDict
from collections import Counter
import json

if os.path.isfile(pickle_filename):
    pmid_datahash = pickle.load( open(pickle_filename, "rb") )
else:
    pmid_datahash = {}

print len(pmid_datahash),"papers included in current data set"

### First need to iterate through all of the paper author lists


js_fp= open('ADRC_metadata.json','w')


affil_fp = open('affiliations_rawtext.csv','w')

cytoscape_fp = open('cytoscape_simpleformat.csv','w')




## Build unique author list
author_occurrence_hash = {}
author_pairs = []
for pmid in pmid_datahash:
    author_list = pmid_datahash[pmid]['auth_list']
    print author_list
#    print [ p for p in itertools.combinations(author_list,2) ]
    
    author_pairs.extend( list( itertools.combinations(author_list,2) ) )
#    print author_pairs
    for author in author_list:
	if author in author_occurrence_hash:
		author_occurrence_hash[author] +=1
	else:
		author_occurrence_hash[author] = 1
    affiliation_list = pmid_datahash[pmid]['affiliations']
    #print affiliation_list
    for affil in affiliation_list:
	    print affil,"hi dave!"
	    print type(affil)
	    author_info_string = "pmid;%s;LastName;%s;FirstName;%s;Initials;%s;Affiliation;%s;University;;State;;City;;" % (  pmid, affil[0]['LastName'], affil[0]['ForeName'],affil[0]['Initials'],affil[1])
	    print author_info_string
  

#    affil_fp.write('pmid:'+pmid+';'+str(affiliation_list)+'\n')
            affil_fp.write(author_info_string.encode('utf-8')+'\n')

for a in author_occurrence_hash:
	print a,author_occurrence_hash[a]    

print len(author_occurrence_hash),"authors are present in this stack"

print len(author_pairs)


#print len(set(author_pairs)),"author pairs present"
### NEED TO REMOVE DUPLICATE AUTHOR PAIRS.. e.g.  Lah, Levey == Levey, Lah

#pprint(author_occurrence_hash)


author_cooccurrence_hash = {}  ### now also need to generate the list of cooccurrence

author_cooccurrence_hash = Counter(author_pairs)

min_paper_count = 5

filtered_author_list = []
filtered_author_dict = {}

author_id = 0  ## Need to define a unique ID for each author so I can then link them
for k in reversed(sorted(author_occurrence_hash.items(), key=lambda t: t[1])):
	(author,count) = k
	if count>=min_paper_count: 
		print k
		filtered_author_list.append(k)
		filtered_author_dict[author] = author_id
		
		author_id +=1

print len(filtered_author_list),"authors had more than",min_paper_count,"pubs"


node_list = []
for k in sorted(filtered_author_dict.items(), key = lambda t: t[1]):
	(author_name,author_uid) = k
	node_list.append( { 'name':author_name, 'group': author_uid % 20 } )

print node_list

for k in sorted(filtered_author_dict.items(), key = lambda t: t[1]):
	(author_name, author_uid) = k
	print author_name


## So now for a given author i... I want to see how many papers he/she has with author K...
## Need to make sure this recursion is actually correct


link_list = []

for i in range (0,len(filtered_author_dict) ):
	for k in range(i+1,len(filtered_author_dict) -1 ):
		#print i,filtered_author_list[i],k,filtered_author_list[k]
		author_cooccurrence_count  = 0
		(a1,pub_count_a1) = ( filtered_author_list[i] )
		(a2,pub_count_a2) = ( filtered_author_list[k ] )
		#print author_pairs_count
		if author_cooccurrence_hash[ (a1,a2)  ]:
			#print 'found it??',a1,a2, author_cooccurrence_hash[ (a1,a2) ]
			author_cooccurrence_count = author_cooccurrence_hash[ (a1,a2) ] 
		## Since ( a1, a2 ) == ( a2, a1) in this case, need to check for both possibilities
		if author_cooccurrence_hash[ (a2,a1)  ]:
			#print 'found it??',a1,a2, author_cooccurrence_hash[ (a2,a1) ]
			author_cooccurrence_count = author_cooccurrence_hash[ (a2,a1) ] 
		if author_cooccurrence_count > 0:
			#print a1,a2,"publish together",author_cooccurrence_count
			#print "Source",i,"target",k,"value",author_cooccurrence_count
			node_info = { 'source': i, 'target': k, 'value': author_cooccurrence_count }
#			print node_info
			link_list.append(node_info)
			author_linkage_string = '"%s";%d;"%s"' % ( filtered_author_list[i][0], author_cooccurrence_count, filtered_author_list[k][0])
			cytoscape_fp.write( author_linkage_string + '\n' )

#    {"source":1,"target":0,"value":1},

#pprint(link_list)

json_object = { 'nodes':node_list, 'links': link_list}
pprint( json_object)

## NOW I NEED TO GENERATE THE LINK LIST...
json.dump(json_object, js_fp)



#pprint( filtered_author_dict)


### NOW ACTUALLY BUILD THE JSON OBJECT WHICH CONSISTS OF A LIST OF NODES AND LINKS

## FOR NOW GROUP WILL BE BASED ON THE NUMBER OF PAPERS THEY'VE WRITTEN... maybe change later to something else

#{
#  "nodes":[
##    {"name":"Myriel","group":1},
#    {"name":"Napoleon","group":1},
#    {"name":"Mlle.Baptistine","group":1},
#    {"name":"Mme.Hucheloup","group":8}
#  ],
#"links":[
#    {"source":1,"target":0,"value":1},
#    {"source":2,"target":0,"value":8},
#    {"source":3,"target":0,"value":10},
#    {"source":3,"target":2,"value":6},
#    {"source":4,"target":0,"value":1},
#    {"source":5,"target":0,"value":1},
#    {"source":6,"target":0,"value":1},
##    {"source":7,"target":0,"value":1},
#    {"source":76,"target":58,"value":1},
#  ]
#}
#

#http://nsaunders.wordpress.com/2013/09/17/web-scraping-using-mechanize-pmid-to-pmcidnihmsid/

#http://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

#"""The service can provide output in a number of formats, as specified by the format parameter, which can be one of "html", "xml", "json", or "csv". "xml" is the dafault, and several examples of this response format are given above. Examples of each of the other formats is shown below.

""">>> from collections import OrderedDict

>>> # regular unsorted dictionary
>>> d = {'banana': 3, 'apple':4, 'pear': 1, 'orange': 2}

>>> # dictionary sorted by key -- OrderedDict(sorted(d.items()) also works
>>> OrderedDict(sorted(d.items(), key=lambda t: t[0]))
OrderedDict([('apple', 4), ('banana', 3), ('orange', 2), ('pear', 1)])

>>> # dictionary sorted by value
>>> OrderedDict(sorted(d.items(), key=lambda t: t[1]))
OrderedDict([('pear', 1), ('orange', 2), ('banana', 3), ('apple', 4)])

>>> # dictionary sorted by length of the key string
>>> OrderedDict(sorted(d.items(), key=lambda t: len(t[0])))
OrderedDict([('pear', 1), ('apple', 4), ('orange', 2), ('banana', 3)])
"""

