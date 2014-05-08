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


curated_author_affils_fp = open('affiliations_manually_curated.csv','r')



curated_author_data = curated_author_affils_fp.readlines()

curated_author_datadict = {}
## Build unique author list
##The format of this file should be  pmid;#;Lastname;#;FirstName;#;Initials;#;Affiliation;#;University;#;State;#;City;#;
university_index = []


unknown_author_affiliation_dict = {}


for line in curated_author_data:
	cols = line.rstrip().split(';')
	pmid = cols[1]
	lastname = cols[3]
	firstname = cols[5]
	initials = cols[7]
	affil_string = cols[9]
	university = cols[11]
	state = cols[13]
	city = cols[15]
	if university:
#		print pmid,state,city
		author_initials = lastname+ ','+  initials
		if author_initials not in curated_author_datadict:
			curated_author_datadict[author_initials] = { 'lastname': lastname, 'firstname':firstname, 'university':university, 'state': state, 'city': city }
			if university not in university_index:
				university_index.append(university)
		else:
			cur_university_info = curated_author_datadict[author_initials]['university']
			if university != cur_university_info:
				print "author mismatch???",cols
				print university,cur_university_info

##Unique Author List--- I need to figure out how many universities are present, and assign an ID to each one

pprint( university_index)
print len(university_index)


def extract_affiliation_info( pmid_datahash):
    """This subfunction will extract the author affiliation info and dump this to a file for subsequent curation """
    for pmid in pmid_datahash:  
	affiliation_list = pmid_datahash[pmid]['affiliations']
    #print affiliation_list
	for affil in affiliation_list:
	    print type(affil)
	    author_info_string = "pmid;%s;LastName;%s;FirstName;%s;Initials;%s;Affiliation;%s;University;;State;;City;;" % (  pmid, affil[0]['LastName'], affil[0]['ForeName'],affil[0]['Initials'],affil[1])
	    #print author_info_string
            affil_fp.write(author_info_string.encode('utf-8')+'\n')



def build_author_pairs_by_year ( pmid_datahash, year_to_analyze):
    author_occurrence_hash = {}
    author_pairs = []

    for pmid in pmid_datahash:
	author_list = pmid_datahash[pmid]['auth_list']
	#print pmid_datahash[pmid]
	pub_year = pmid_datahash[pmid]['publication_date'].split('-')[0]
    
	#print author_list
#        print pub_year,year_to_analyze
	if int(pub_year) == year_to_analyze:
       	    author_pairs.extend( list( itertools.combinations(author_list,2) ) )
#    print author_pairs
  	    for author in author_list:
	        if author in author_occurrence_hash:
		    author_occurrence_hash[author] +=1
   	        else:
		    author_occurrence_hash[author] = 1
    return( author_occurrence_hash, author_pairs) 

#print len(set(author_pairs)),"author pairs present"
### NEED TO REMOVE DUPLICATE AUTHOR PAIRS.. e.g.  Lah, Levey == Levey, Lah
#pprint(author_occurrence_hash)

def generate_cooccurrence_info( author_pairs, author_occurrence_hash):
	author_cooccurrence_hash = Counter(author_pairs) ### now also need to generate the list of cooccurrence

	min_paper_count = 1

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
		if author_name in curated_author_datadict:
			print curated_author_datadict[author_name]['university'],author_uid,author_name
		else:
			print author_name.encode('utf-8'),"not in datadict??!"
			unknown_author_affiliation_dict[author_name] = 1

			if author_name not in unknown_author_affiliation_dict:
				unknown_author_affiliation_dict[author_name] = 1
			else:
				unknown_author_affiliation_dict[author_name] += 1

		
		## group_id is used for colors.. right now I only have 20 colors to choose from though..
		try:  
			author_university = curated_author_datadict[author_name]['university']
			group_id = university_index.index(author_university)
		except:
			group_id = 0
#			print 'NEED;---;',curated_author_datadict[author_name]
			#print author_name.encode('utf-8'),'NEED'
		node_list.append( { 'name':author_name, 'group': group_id % 20 } )


	#print node_list

	for k in sorted(filtered_author_dict.items(), key = lambda t: t[1]):
		(author_name, author_uid) = k
		#print author_name

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
#				print node_info
				link_list.append(node_info)
				author_linkage_string = '"%s";%d;"%s"' % ( filtered_author_list[i][0], author_cooccurrence_count, filtered_author_list[k][0])
				cytoscape_fp.write( author_linkage_string.encode('utf-8') + '\n' )
	

	json_object = { 'nodes':node_list, 'links': link_list}
	#pprint( json_object)
	#json.dump(json_object, js_fp)
	return json_object



#http://nsaunders.wordpress.com/2013/09/17/web-scraping-using-mechanize-pmid-to-pmcidnihmsid/
#http://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/
#"""The service can provide output in a number of formats, as specified by the format parameter, which can be one of "html", "xml", "json", or "csv". "xml" is the dafault, and several examples of this response format are given above. Examples of each of the other formats is shown below.



years_to_scan = [2011,2012,2013]

### I am going to write a separate graph/nodelist for each year... and then output this as a JSON object
multiyear_json_object = {}
for year in years_to_scan:
    (author_occurrence_hash, author_pairs ) = build_author_pairs_by_year (pmid_datahash, year)
    print len(author_occurrence_hash),"authors are present in this stack",year
    print len(author_pairs),"pairs for year",year

    json_link_data = generate_cooccurrence_info(author_pairs, author_occurrence_hash)
    multiyear_json_object[year]= json_link_data
json.dump(multiyear_json_object, js_fp)




for author in unknown_author_affiliation_dict:
	print author.encode('utf-8'),"has no info"


print len(unknown_author_affiliation_dict),"authors need lookup"


for pmid in pmid_datahash:
	author_list = pmid_datahash[pmid]['auth_list']
	for auth in author_list:
		if auth in unknown_author_affiliation_dict:
			(lastname,initial) = auth.encode('utf-8').split(',')
			print "pmid;%s;Lastname;%s;Firstname;;Initials;%s;Affiliation;;University;;;State;;;City;;" % ( pmid, lastname, initial )



#pmid;None;Lastname;Betarbet;Firstname;Ranjita;Initials;RS;Affiliation;Emory;University;Emory University;State;GA;City;Atlanta;

