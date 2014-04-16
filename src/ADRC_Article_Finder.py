
# This will read a list of ADRC publications and try and do some basic network stats on them... I am using a list of publications provided by Janet as a starting point

# In[4]:

import re
from Bio import Entrez
Entrez.email = "dagutman@gmail.com"     # Always tell NCBI who you are

adrc_file_list = 'adrc_pubs.txt'
adrc_fp = open('ADRC_Data/adrc_pubs.txt','r')
adrc_raw_paper_list = adrc_fp.readlines()


# PMCID - PMID - Manuscript ID - DOI Converter
# Enter IDs into the text box using the specified format. Separate multiple IDs with spaces or commas. Note: you cannot mix different types of IDs in a single request.
# 
# PMID: use simple numbers, e.g., 23193287.
# PMCID: include the ‘PMC’ prefix, e.g., PMC3531190. You may drop the prefix if you select the checkbox for ‘Process as PMCIDs’.
# Manuscript ID: include the relevant prefix, e.g., NIHMS236863 or EMS48932.
# DOI: enter the complete string, e.g., 10.1093/nar/gks1195.

# In[5]:

pub_list = [ pub.strip('\n') for  pub in adrc_raw_paper_list if len(pub)>1 ]   ## turns it into a list and removes the blank spaces


# In[6]:

pmid_regex = re.compile('PMID:*\s*(\d+)') ## matches 0 or more spaces
pmcid_regex = re.compile('PMCID:*\s*(PMC\d+)')
debug = False
len(pub_list)
PMID_LIST = []
PMCID_LIST = []
not_matched = 0
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
        not_matched += 1
        
print not_matched,"entries did not have a PMC or PMID"


# Out[6]:

#     Did not find PMID or PMCID Publications:
#     Did not find PMID or PMCID Boname JM, Thomas M, Stagg HR, Xu P, Peng J, Lehner PJ.  Efficient internalization of MHC I requires lysine-11 and lysine-63 mixed linkaqe polyubiquitin chains.  Traffic. 2010 Feb; 11(2):210-20. Epub 2009 Nov 17.  NIHMS:  159904
#     Did not find PMID or PMCID Campbell NL, Boustani MA, Lane KA, Gao S, Hendrie H, Khan BA, Murrell JR, Unverzagt FW, Hake A, Smith-Oamble V, Hall K.  Use of anticholinergics and the risk of cognitive impairment in an African American population.  Neurology. 2010 Jul13; 75(2):152-9.  PMC:  2905930
#     PMID found but pattern not parsed properly... Crawford SB, Hanfelt JJ:  Testing for qualitative interaction of multiple sources of informative dropout in longitudinal data. (2011) Journal of Applied Statistics 38 (6):1249-1264.  PMCID in progress
#     Did not find PMID or PMCID Crutcher, M.D., Calhoun-Haney, R., Manzanares, C.M., Lah, J.J., Levey, A.I., Zola, S.M.  Eye tracking during a visual paired comparison task as a predictor of early dementia.  Am J. Alzheimers Disease Other Dementias.  2009 Jun-Jul; 24(3): 258-66. PMC2701976
#     Did not find PMID or PMCID Gandy S, Simon AJ, Steele JW, Lublin AL, Lah JJ, Walker LC, Levey AI, Krafft GA, Levy E, Checier F, Glabe C, Bilker WB, Abel T, Schmeidler J, Ehrlich ME.  Days to criterion as an indicator of toxicity associated with human Alzheimer amyloid-beta oligomers.  Ann Neural. 2010 Aug; 68(2):220-30.  DOI:  10.1002/ana.22052
#     Did not find PMID or PMCID Franco M, Seyfried NT, Brand AH, Peng J (co-corresponding author), Mayor U (2010) A novel strategy to isolate ubiquitin conjugates reveals wide role of ubiquitination during neural development  Mol Cell Proteomics 2010 Sept 22 [Epub ahead of print]
#     Did not find PMID or PMCID Goldstein FC, Mao H, Wang L, Ni C, Lah JJ, Levey AI.  White Matter Integrity and Episodic Memorv Performance in Mild Cognitive Impairment: A Diffusion Tensor Imaging Study.  Brain Imaging Behav. 2009 Jun; 3(2):132-141.  PMC:  2894481
#     Did not find PMID or PMCID Goldstein FC, Ashley AV, Miller E, Alexeeva O, Zanders L, King V.  The Montreal Cognitive Assessment as a screen for mild cognitive impairment and ementia in African American older adults attending a memory disorders clinic.  J Geriatr Psychiatr Neurol (In Press).
#     Did not find PMID or PMCID Hampstead BM, Sathian K, Phillips PA, Amaraneni A, Delaune WR, Stringer AY.  Mnemonic strategy training improves memory for object location associations in both healthy elderly and patients with amnestic mild cognitive impairment: a randomized, single-blind study.  Neuropsychology. 2012 May;26(3):385-99. doi: 10.1037/a0027545. Epub 2012 Mar 12.  PMIS:  22409311  PMC: 3348454
#     Did not find PMID or PMCID Herskowitz JH, Seyfried NT, Duong DM, Xia Q, Rees HD, Gearing M, Peng J, Lah JJ, Levey AI.  Phosphoproteomic analysis reveals site-specific changes in GFAP and NDRG2 phosphorvlation in frontotemporal lobar degeneration.  J Proteome Res.2010 Dec 3; 9(12):6368-79.  Epub 2010 Oct 22.  PMC:  2997170
#     Did not find PMID or PMCID Hong Y, Chan CB, Kwon IS, LI X, Song M, Lee HP, Liu X, Sompol P, Jin P, Lee HG.  SRPK2 phosphorylates tau and mediates the cognitive defects in Alzheimer’s disease.  J Neurosci. 2012;32:17262-72.  PMC: 3518045
#     Did not find PMID or PMCID Jacobson AD, Zhang NY, Xu P, Han'KJ, Noone S, Peng J, Liu CWO.  The lysine 48 and lysine 63 ubiquitin conjugates are processed differently by the 26 s proteasome.
#     Did not find PMID or PMCID J Bioi Chern. 2009 Dec 18; 284(51):35485-94. Epub.  PMC:  2790778
#     Did not find PMID or PMCID Jiang H, Cheng D, Llu IN, 'Peng J, Feng J.  Protein kinase C inhibits autophagy and phosphorylates LC3.  Biochem Biophys Res Commun. 2010 May 14; 395(4):471-6. Epub 2010 Apr 14.  PMC:  2873090
#     Did not find PMID or PMCID Jun G, Naj AC, Beecham GW, Wang LS, Buros J, Gallins PJ, Buxbaum JD, Ertekin-Taner N, Fallin MD, Friedland R, Inzelberg R, Kramer P, Rogaeva E, St George-Hyslop P; Alzheimer's Disease Genetics Consortium, Cantwell LB, Dombroski BA, Saykin AJ, Reiman EM, Bennett DA, Morris JC, Lunetta KL, Martin ER, Montine T J, Goate AM, Blacker D, Tsuang DW, Beekly D, Cupples LA, Hakonarson H,  Kukull W, Foroud TM, Haines J, Mayeux R, Farrer LA, Pericak-Vance MA, Schellenberg GD.  Meta-analysis confirms CR1, CLU, and PICALM as alzheimer disease risk loci and reveals interactions with APOE genotypes.  Arch Neural. 2010 Dec; 67(12):1473-84. Epub 2010 Aug 9.  NIHMS:  5232067
#     Did not find PMID or PMCID Jutras MJ, Buffalo EA.  Synchronous neural activity and memorv formation.
#     Did not find PMID or PMCID Curr Opin Neurobiol. 2010 Apr; 20(2):150-5. Epub 2010 Mar 18. Review. 
#     Did not find PMID or PMCID  PMC:  2862842
#     Did not find PMID or PMCID Jutras MJ, Buffalo EA.  Recognition memorv signals in the macaque hippocampus.
#     Did not find PMID or PMCID Proc Natl Acad Sci USA. 2010 Jan 5; 107(1):401-6. Epub 2009 Dec 14.
#     Did not find PMID or PMCID PMC:  2806723
#     Did not find PMID or PMCID Jutras MJ, Fries P, Buffalo EA.  Gamma-band synchronization in the macaque hippocampus and memorv formation.  J Neurosci. 2009 Oct 7; 29(40):12521-31.
#     Did not find PMID or PMCID PMC:  2785486
#     Did not find PMID or PMCID Kim, H., Cho, Y.S., Do, E.Y-L. (2011) “Using Pen-Based Computing in Technology for Health”. Human-Computer Interaction. Users and Applications. Lecture Notes in Computer Science. J. Jacko, ed., pp. 192-201: Springer Berlin / Heidelberg
#     Did not find PMID or PMCID Kim H, Hsiao, H, Do, E.  Home based computerized cognitive assessment for dementia screening.  Journal of Ambient Intelligence and Smart Environment. 2013 – in press.
#     Did not find PMID or PMCID Rosen RF, Tomidokoro Y, Ghiso JA, Walker LC.  SDS-PAGE/immunoblot detection of Abeta multimers in human cortical tissue homogenates using antigen-epitope retrieval.
#     Did not find PMID or PMCID J Vis Exp. 2010 Apr 23; (38). pii: 1916. doi: 10.3791/1916.  NIHMS273637
#     Did not find PMID or PMCID Rui Y, Gu J, Yu K, Hartzell HC, Zheng JQ.  Inhibition of AMPA receptor trafficking at hippocampal synapses by beta-amyloid oligomers: the mitochondrial contribution.
#     Did not find PMID or PMCID Mol Brain. 2010 Mar 26; 3:10.  PMC:  2853530
#     Did not find PMID or PMCID Seyfried NT, Gozal YM, Dammer EB, Xia Q, Duong OM, Cheng 0, Lah JJ, Levey AI, Peng J.  Multiplex SILAC analysis of a cellular TDP-43 proteinopathy model reveals protein inclusions associated with SUMOylation and diverse polyubiguitin chains.
#     Did not find PMID or PMCID Mol Cell Proteomics. 2010 Apr; 9(4):705-18. Epub 2010 Jan 4.  PMC:  2860236
#     Did not find PMID or PMCID Sollinger AB, Goldstein FC, Lah JJ, Levey AI, Factor SA.  Mild cognitive impairment in Parkinson's disease: subtypes and motor characteristics.  Parkinsonism Relat Disord. 2010 Mar; 16(3):177-80. Epub 2009 Nov 25.  NIHMS:  161322
#     Did not find PMID or PMCID Steenland K, Macneil J, Bartell S, Lah J.  Analyses of diagnostic patterns at 30 Alzheimer's disease centers in the US.  Neuroepidemiology. 2010;35(1):19-27. Epub 2010 Apr 2.  PMC:  2919431
#     Did not find PMID or PMCID Steenland K, MacNeil J, Seals R, Levey A.  Factors affecting survival of patients with neurodegenerative disease.  Neuroepidemiology. 2010; 35(1):28-35. Epub 2010 Apr 8.
#     Did not find PMID or PMCID PMC:  2919432
#     Did not find PMID or PMCID Steenland K, Zhao L, Goldstein F, Cellar J, Lah J.  Biomarkers for predicting cognitive decline in those with normal cognition.  J Alz Dis (In Press).
#     Did not find PMID or PMCID Van Deerlin VM, Sieiman PM, Martinez-Lage M, Chen-Plotkin A, Wang LS, Graff-Radford NR, Dickson OW, Rademakers R, Boeve BF, Grossman M, Arnold SE, Mann OM, Pickering-Brown SM, Seelaar H, Heutink P, van Swieten JC, Murrell JR, Ghetti B, Spina S, Grafman J, Hodges J, Spillantini MG, Gilman S, Lieberman AP, Kaye JA, Woltjer RL, Bigio EH, Mesulam M, AI-Sarraj S, Troakes C, Rosenberg RN, White CL 3rd, Ferrer I, Llad6 A, Neumann M, Kretzschmar HA, Hulette CM, Welsh-Bohmer KA, Miller BL, Alzualde A, Lopez de Munain A, McKee AC, Gearing M, Levey AI, Lah JJ, Hardy J, Rohrer JD, Lashley T, Mackenzie IR, Feldman HH, Hamilton RL, Dekosky ST, van der Zee J, Kumar-Singh S, Van Broeckhoven C, Mayeux R, Vonsattel JP, Troncoso JC, Kril JJ, Kwok JB, Halliday GM, Bird TO, Ince PG, Shaw PJ, Cairns NJ, Morris JC, McLean CA, DeCarli C, Ellis WG, Freeman SH, Frosch MP, Growdon JH, Perl DP, Sano M, Bennett DA, Schneider JA, Beach TG, Reiman EM, Woodruff BK, Cummings J, Vinters HV, Miller CA, Chui HC, Alafuzoff I, Hartikainen P, Seilhean 0, Galasko 0, Masliah E, Cotman CW, Tunon MT, Martinez MC, Munoz DG, Carroll SL, Marson 0, Riederer PF, Bogdanovic N, Schellenberg GO, Hakonarson H, Trojanowski JQ, Lee VM.  Common variants at 7p21 are associated with frontotemporal lobar degeneration with TDP-43 inclusions. Nat Genet. 2010 Mar; 42(3):234-9. Epub 2010 Feb 14.  PMC:  2828525
#     Did not find PMID or PMCID Zhou JY, Afjehi-Sadat L, Asress S, Duong DM, Cudkowicz M, Glass JD, Peng J.  Galectin-3 is a candidate biomarker for amyotrophic lateral sclerosis: discovery by a proteomics approach.  J Proteome Res. 2010 Oct 1; 9(10):5133-41.  PMC:  2948604
#     Did not find PMID or PMCID Indirectly supported by ADRC  (Did not add previous years – not sure we should focus on these??)
#     Did not find PMID or PMCID Armstrong RA, Gearing M, Bigio EH, Cruz-Sanchez FF, Duyckaerts C, Mackenzie IR, Perry RH, Skullerud K, Yokoo H, Cairns NJ.  The spectrum and severity of FUS-immunoreactive inclusions in the frontal and temporal lobes of ten cases of neuronal intermediate filament inclusion disease.  Acta Neuropathol 2010, in press (published online October 1, 2010).
#     Did not find PMID or PMCID Chen-Plotkin AS, Markinez-Lage M, Sleiman PMA, Hu W, Greene R, McCarty E, Bing S, Grossman M, Schellenberg G, Hatanpaa KJ, Weiner MF, White CL III, Brooks W, Halliday GM, Kril JJ, Gearing M, Beach TG, Graff-Radford NR, Dickson DW, Rademakers R, Boeve BF, Pickering-Brown SM, Snowden J, van Swieten JC, Seelaar H, Murrell JR, Ghetti B, Spina S, Grafman J, Kaye JA, Woltjer RL, Mesulam M, Lladó A, Miller BL, Alzualde A, Moreno F, Rohrer JD, Mackenzie IRA, Feldman HH, Hamilton RL, Cruts M, Engelborghs S, De Deyn PP, Van Broeckhoven C, Bird TD, Cairns NJ, Goate A, Frosch MP, Riederer PF, Bogdanovic N, Lee VMY, Trojanowski JQ, Van Deerlin VM.  Genetic and clinical features of progranulin-associated frontotemporal lobar degeneration.  Arch Neurol 2011, in press.
#     Did not find PMID or PMCID Childers, WS; Ni, R. Mehta, AK; Lynn, DG 2009 Peptide Membranes in Chemical Evolution, Curr Op. Chem Biol., 13: 652-9.
#     Did not find PMID or PMCID Childers, WS; Lu, K. Mehta, AK; Lynn, DG 2009, Templating Molecular Arrays in Amyloid’s Cross- Groves, J. Am. Chem. Soc. 131: 10165-72.
#     Did not find PMID or PMCID Childers, WS; Mehta, AK; Ni, R; Taylor, JV; Lynn, DG. 2010. Peptides Organized as Bilayer Membranes, Angewandte Chimie Intl Ed. http://dx.doi.org/10.1002/anie.201000212 and in Angew. Chimie http://dx.doi.org/10.1002/ange.201000212
#     Did not find PMID or PMCID Edbauer D, Cheng D, Batterton MN, Wang CF, Duong DM, Yaffe MB, Peng J (co-corresponding author) and Sheng M (2009) Identification and characterization of neuronal MAP kinase substrates using a specific phosphomotif antibody. Mol. Cell. Proteomics 8:681-98.
#     Did not find PMID or PMCID Factor SA, Steenland NK, Higgins DS, Molho ES, Kay DM, Montimurro J, Rosen AR,
#     Did not find PMID or PMCID Factor SA, Steenland NK, Higgins DS, Molho ES, Kay DM, Montimurro J, Rosen AR,
#     Did not find PMID or PMCID Gallagher MD, Suh E, Grossman M, Elman L, McCluskey L, Van Swieten JC, Al-Sarraj S, Neumann M, Gelpi E, Ghetti B, Rohrer JD, Halliday G, Van Broeckhoven C, Seilhean D, Shaw PJ, Frosch MP, International Collaboration for Frontotemporal Dementia, Trojanowski JQ, Lee VMY, Van Deerlin V, Chen-Plotkin AS.  TMEM106B is a genetic modifier of frontotemporal lobar degeneration with C9orf72 hexanucleotide repeat expansions.  Acta Neuropathologica 2013, in press.  
#     Did not find PMID or PMCID  
#     Did not find PMID or PMCID Gaugler, J. E., Mittelman, M. S., Hepburn, K., & Newcomer, R.  (2009).  Predictors of caregiver adaptation across the nursing home transition.  Psychology and Aging, 24, 385-396.
#     Did not find PMID or PMCID Gillian Hue, Jessica Sales, Dawn Comeau, David G. Lynn and Arri Eisen, 2010, The American Science Pipeline: sustaining innovation in a time of economic crisis, Chemical Biology Education, 9: 431–434.
#     Did not find PMID or PMCID Gillis MM, Quinn KM, Phillips PA, Hampstead BM.  Impaired retention is responsible for temporal order memory deficits in mild cognitive impairment.  Acta Psychologic.  2013  143(1):88-95.
#     Did not find PMID or PMCID Gillian Hue, Jessica Sales, Dawn Comeau, David G. Lynn and Arri Eisen, 2010, The American Science Pipeline: sustaining innovation in a time of economic crisis, Chemical Biology Education, 9: 431–434.
#     Did not find PMID or PMCID Jacobson AD, Zhang NY, Xu P, Han KJ, Noone S, Peng J, and Liu CW (2009) The lysine 48 and lysine 63 ubiquitin conjugates are processed differently by the 26S proteasome. J. Biol Chem. 284:35485-94. PMC2790978
#     Did not find PMID or PMCID Jun G, Naj AC, Beecham GW, Wang L-S, Buros J, Gallins PJ, Buxbaum JD, Ertekin-Taner N, Fallin MD, Friedland R, Inzelberg R, Kramer P, Rogaeva E, St. George-Hyslop P, Alzheimer’s Disease Genetics Consortium, Cantwell L, Dombroski BA, Saykin AJ, Reiman EM, Bennett DA, Morris JC, Lunetta KL, Martin ER, Montine TJ, Goate AM, Blacker D, Tsuang DW, Beekly D, Cupples LA, Hakonarson H, Kukull W, Foroud TM, Haines J, Mayeux R, Farrer LA, Pericak-Vance MA, Schellenberg GD.  Meta-analysis confirms CR1, CLU, and PICALM as Alzheimer’s disease risk loci and reveals interactions with APOE genotypes.  Arch Neurol 2010, in press (published online August 9, 2010).
#     Did not find PMID or PMCID Lewis, ML, Hobday, JV, Hepburn, K (2010). Internet-Based Program for Dementia Caregivers.
#     Did not find PMID or PMCID Am. J. Alzheimer’s disease & Other Dementias 25(8) 674-679. 
#     Did not find PMID or PMCID Liang, Y.; Lynn, D.G. Berland, KM (2010). Direct Observation of Nucleation and Growth in Amyloid Self-Assembly, J. Am. Chem. Soc.; 132(18) 6306-6308 DOI: 10.1021/ja910964c.
#     Did not find PMID or PMCID Liu Z, Oh SM, Okada M, Liu X, Cheng D, Peng J, Brat DJ, Sun SY, Zhou W, Gu W, Ye K (2009) Human BRE1 is an E3 ubiquitin ligase for Ebp1 tumor suppressor. Mol Biol Cell 20:757-68. PMC2633391
#     Did not find PMID or PMCID Naj AC, Jun G, Beecham GW, Wang L-S, Vardarajan BN, Buros J, Gallins PJ, Buxbaum JD, Jarvik GP, Crane PK, Larson EB, Bird TD, Boeve BF, Graff-Radford NR, De Jager PL, Evans E, Schneider JA, Carrasquillo MM, Ertekin-Taner N, Younkin SG, Cruchaga C, Kauwe JSK, Nowotny P, Kramer P, Hardy J, Huentelman MJ, Myers AJ, Barmada MM, Demirci FY, Baldwin CT, Green RC, Rogaeva E, St. George-Hyslop P, Alzheimer’s Disease Genetics Consortium, Cantwell L, Dombroski BA, Beekly D, Lunetta KL, Martin ER, Kamboh MI, Saykin AJ, Reiman EM, Bennett DA, Morris JC, Montine TJ, Goate AM, Blacker D, Tsuang DW, Hakonarson H, Kukull WA, Foroud TM, Haines JL, Mayeux R, Pericak-Vance MA, Farrer LA, Schellenberg GD.  Common variants in MS4A4/MS4A6E, CD2AP, CD33 and EPHA1 are associated with late-onset Alzheimer's disease.  Nature Genet 2011, in press.
#     Did not find PMID or PMCID Rosen RF, Ciliax BJ, Wingo TS, Gearing M, Dooyema J, Wingo T, Lah JJ, Ghiso JA, LeVine H, III, Walker LC.  Deficient high-affinity binding of Pittsburgh Compound B in a case of Alzheimer's disease.  Acta Neuropathol 2010; 119:221-233.
#     Did not find PMID or PMCID Xu P, Duong DM, Seyfried NT, Cheng D, Xie Y, Robert J, Rush J, Hochstrasser M, Finley D, and Peng J (2009) Quantitative proteomics reveals the function of unconventional ubiquitin chains in proteasomal degradation. Cell 137:133-145. NIHMSID97944
#     62 entries did not have a PMC or PMID
# 

# I am interested in getting the following attributes:
# AUTHOR LIST
# AUTHOR LOCATION
# Author University
# 

# In[7]:

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


# In[8]:

global_author_list


# Out[8]:

#     {}

# In[9]:

get_metadata_from_PMID(broken_pmid)


# Out[9]:


    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)

    <ipython-input-9-f5331d94acab> in <module>()
    ----> 1 get_metadata_from_PMID(broken_pmid)
    

    NameError: name 'broken_pmid' is not defined


# In[10]:

xml_data.keys()


# Out[10]:


    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)

    <ipython-input-10-fb046b15eb30> in <module>()
    ----> 1 xml_data.keys()
    

    NameError: name 'xml_data' is not defined


# In[13]:

global_author_list = {}
for pmid in PMID_LIST:
    print pmid
    get_metadata_from_PMID(pmid)


# Out[13]:

#     
#     Unable to get abstract for 19342885
#     Unexpected error: <type 'exceptions.KeyError'>
#     24023061
#     21358840
#     Unable to get abstract for 21358840
#     Unexpected error: <type 'exceptions.KeyError'>
#     20409611
#     22431618
#     22926189
#     Data Completed not available?? 22926189
#     Unable to get mesheadings for 22926189
#     21482928
#     21467255
#     unable to process 21467255
#     Unexpected error: <type 'exceptions.KeyError'>
#     22556362
#     unable to process 22556362
#     Unexpected error: <type 'exceptions.KeyError'>
#     23768213
#     225324
#     21917762
#     unable to process 21917762
#     Unexpected error: <type 'exceptions.KeyError'>
#     23301925
#     23301925
#     22126117
#     21577247
#     Unable to get mesheadings for 21577247
#     22265236
#     22678947
#     24128675
#     22110366
#     Unable to get mesheadings for 22110366
#     22883210
#     2236803
#     21530556
#     20935339
#     22024618
#     22906799
#     21998317
#     unable to process 21998317
#     Unexpected error: <type 'exceptions.KeyError'>
#     22718532
#     22621900
#     24305806
#     22288403
#     23360175
#     unable to process 23360175
#     Unexpected error: <type 'exceptions.KeyError'>
#     21554923
#     23460879
#     24174584
#     22313030
#     23150908
#     22028219
#     23878251
#     19835657
#     24162737
#     unable to process 24162737
#     Unexpected error: <type 'exceptions.KeyError'>
#     21131674
#     22633452
#     23791866
#     Data Completed not available?? 23791866
#     Unable to get mesheadings for 23791866
#     21670386
#     unable to process 21670386
#     Unexpected error: <type 'exceptions.KeyError'>
#     21471273
#     unable to process 21471273
#     Unexpected error: <type 'exceptions.KeyError'>
#     23565137
#     unable to process 23565137
#     Unexpected error: <type 'exceptions.KeyError'>
#     21460841
#     21603978
#     23318928
#     22634524
#     23669642
#     21655086
#     23571587
#     unable to process 23571587
#     Unexpected error: <type 'exceptions.KeyError'>
#     23673467
#     unable to process 23673467
#     Unexpected error: <type 'exceptions.KeyError'>
#     21620887
#     24244562
#     Data Completed not available?? 24244562
#     Unable to get mesheadings for 24244562
#     unable to process 24244562
#     Unexpected error: <type 'exceptions.KeyError'>
#     19329226
#     22017494
#     22025277
#     24165455
#     Data Completed not available?? 24165455
#     Unable to get mesheadings for 24165455
#     22927900
#     21855799
#     22416763
#     23602153
#     22157315
#     Unable to get abstract for 22157315
#     Unexpected error: <type 'exceptions.KeyError'>
#     22543846
#     23092715
#     24000778
#     22037496
#     22309832
#     22957617
#     21810649
#     unable to process 21810649
#     Unexpected error: <type 'exceptions.KeyError'>
#     21429865
#     unable to process 21429865
#     Unexpected error: <type 'exceptions.KeyError'>
#     22750520
#     23599928
#     21152911
#     23685628
#     23143602
#     unable to process 23143602
#     Unexpected error: <type 'exceptions.KeyError'>
#     20947215
#     21911656
#     22022397
#     unable to process 22022397
#     Unexpected error: <type 'exceptions.KeyError'>
#     22110158
#     23912899
#     2223185
#     22171532
#     22608086
#     23537733
#     23271330
#     22685416
#     unable to process 22685416
#     Unexpected error: <type 'exceptions.KeyError'>
#     23553836
#     23117489
#     23828492
#     20335454
#     20835371
#     Data Completed not available?? 20835371
#     Unable to get mesheadings for 20835371
#     20884673
#     21714002
#     24256812
#     Data Completed not available?? 24256812
#     Unable to get mesheadings for 24256812
#     unable to process 24256812
#     Unexpected error: <type 'exceptions.KeyError'>
#     21167022
#     19485656
#     20847427
#     19996185
#     unable to process 19996185
#     Unexpected error: <type 'exceptions.KeyError'>
#     20463401
#     20881129
#     21147074
#     19668025
#     19859965
#     20144652
#     19906975
#     19182806
#     24252572
#     Unable to get mesheadings for 24252572
#     unable to process 24252572
#     Unexpected error: <type 'exceptions.KeyError'>
#     20937087
#     Unable to get mesheadings for 20937087
#     23627220
#     Unable to get abstract for 23627220
#     Unexpected error: <type 'exceptions.KeyError'>
#     19279272
#     20369371
#     19342885
#     Unable to get abstract for 19342885
#     Unexpected error: <type 'exceptions.KeyError'>
# 

# In[12]:

from Bio.Entrez import efetch, read
import sys

global_author_list = {}

def get_metadata_from_PMID( pmid ):
    """This function will take an input PMID and parse the attributes I am interested in for the cytoscape plugin...."""
    handle = efetch(db='pubmed', id=pmid, retmode='xml')
    xml_data = read(handle)[0]
    verbose_output = False
    try:
        date_completed = format_ddate( xml_data['MedlineCitation']['DateCompleted'] )
    except:
        print "Data Completed not available??",pmid

    try:
        otherID = xml_data['MedlineCitation']['OtherID']
    except:
        print "Other ID Not availble??",pmid
    try:
        MeshHeadings = xml_data['MedlineCitation']['MeshHeadingList']
    except:
        print "Unable to get mesheadings for",pmid
    
    
    try:
        article = xml_data['MedlineCitation']['Article']
        if verbose_output: print xml_data
        #print date_completed,otherID
        for author in  article['AuthorList']:
            #author_key = { 'LastNAme': author['LastName'], 'Initials': author['Initials'] }
            author_key =    author['LastName'] + ','+  author['Initials'] 
            #print author['LastName'],author['Initials'],author,'MOO'
            if author_key in global_author_list:
                global_author_list[ author_key ] +=1
                #print "adding author"
            else:
                global_author_list[ author_key ] = 1
                #print "I ADDED AN AUTHOR..."
        #return abstract
    except IndexError:
        return None
    except:
        print "unable to process",pmid
        print "Unexpected error:", sys.exc_info()[0]

    try:
        abstract = article['Abstract']['AbstractText'][0]
    except:
        print "Unable to get abstract for",pmid
        print "Unexpected error:", sys.exc_info()[0]
### Gets Med Line Citation 
#MeshHeadings = medline_citation['MeshHeadingList']
#PMID = medline_citation['PMID']
#ArticleInfo = medline_citation['Article']
#for k in medline_citation:
#    print "------",k,"-------"
#    print medline_citation[k]
## DAteCompleted
#MeshHeadingList,OtherID, PMID,KeywordList


# In[14]:

#mesh_list = [x for x in MeshHeadings[0]['QualifierName'] ]
#print ArticleInfo.keys()
#for k in ArticleInfo.keys():
#    print "-----",k,"------------"
#    print ArticleInfo[k]
    


# In[66]:

print my_doc[0].keys()
## each returned element consists of two dictionaries-- pubmeddata and medlinecitatin..
for k in my_doc[0].keys():
    elmt = my_doc[0][k]
    for k1 in elmt.keys():
        print k1
        #,elmt[k1]


# Out[66]:

#     [u'MedlineCitation', u'PubmedData']
#     DateCompleted
#     OtherID
#     DateRevised
#     MeshHeadingList
#     OtherAbstract
#     CommentsCorrectionsList
#     CitationSubset
#     ChemicalList
#     KeywordList
#     DateCreated
#     SpaceFlightMission
#     GeneralNote
#     Article
#     PMID
#     MedlineJournalInfo
#     ArticleIdList
#     PublicationStatus
#     History
# 

# In[23]:

broken_pmid = '22926189'
handle = efetch(db='pubmed', id=broken_pmid, retmode='xml')
xml_data = read(handle)[0]


# In[*]:

get_metadata_from_PMID(broken_pmid)


# In[25]:

xml_data.keys()


# Out[25]:

#     [u'MedlineCitation', u'PubmedData']

# In[65]:

import re
from Bio import Entrez
Entrez.email = "dagutman@gmail.com"     # Always tell NCBI who you are
handle = Entrez.esearch(db="pubmed", term="biopython")
record = Entrez.read(handle)
record["IdList"]


# Out[65]:

#     ['24497503', '24267035', '24194598', '23842806', '23157543', '22909249', '22399473', '21666252', '21210977', '20015970', '19811691', '19773334', '19304878', '18606172', '21585724', '16403221', '16377612', '14871861', '14630660', '12230038']

# In[9]:

import calendar
import Bio
 
from Bio import Entrez
 
# This is for translating abbreviated month names to numbers.
months_rdict = {v: str(k) for k,v in enumerate(calendar.month_abbr)}
 
# Returns a list or its value if there is only one.
list_or_single = lambda l: l*(len(l)>1) or l[0]
 
class PubmedSearcher:
    """Fetches data from Pubmed using the Entrez module from Biopython."""
 
    # There are the fields that we want to fetch, and all of them are single
    # values except grantlist, which is a dictionary (as per Entrez).
    # More fields can easily be added, and all that needs to be done is
    # to add the appropriate extract_ and fetch_ methods below.
    fields = [
        'pmid', 'doi', 'vol', 'pages',
        'year', 'pub_month', 'pub_day',
        'date_pubmed_created', 'date_pubmed_updated',
        'date_accepted', 'date_aheadofprint', 'date_pubmed_history',
        'grantlist' # this is a dict!
    ]
 
    # Entrez normally limits the number of queries to 200, so work with block of 100.
    nblock = 100
 
    def __init__(self, email):
        """Entrez requires and email address."""
        Entrez.email = email
 
    def fetch_xml_round(self, pmid):
        """Tries to fetch and parse the XML for a list of PMIDs, no questions asked."""
        return Entrez.read(Entrez.efetch(db="pubmed", id=pmid, retmode="xml"))
 
    def fetch_xml(self, pmid):
        """This breaks the process up into blocks."""
        self.nrounds = len(pmid) / self.nblock + (len(pmid) % self.nblock > 0)
        if self.nrounds > 1:
            print "Will query in %i rounds with %i articles per round." % (self.nrounds, self.nblock)
            xml_data = []
            for i in range(self.nrounds):
                istart = i * self.nblock
                ifinish = (i+1) * self.nblock
                print "Fetching round %i..." % (i+1)
                xml_data += self.fetch_xml_round(pmid[istart:ifinish])
        else:
            xml_data = fetch_xml_round(pmid)
        return xml_data
 
    def extract_id_factory(idtype):
        def extract_id(self, xml_data):
            """Extract the %s ID from Entrez XML output.""" % idtype
            for id in xml_data['PubmedData']['ArticleIdList']:
                if id.attributes['IdType'].lower() == idtype:
                    return str(id)
        return extract_id
    extract_pmid = extract_id_factory('pubmed')
    extract_doi = extract_id_factory('doi')
 
    def extract_date_factory(datetype):
        def extract_date(self, xml_data):
            """Extract %s date from Entrez XML output.""" % datetype
            for date in xml_data['PubmedData']['History']:
                if date.attributes['PubStatus'].lower() == datetype:
                    return format_ddate(date)
        return extract_date
    extract_date_accepted = extract_date_factory('accepted')
    extract_date_aheadofprint = extract_date_factory('aheadofprint')
    extract_date_pubmed_history = extract_date_factory('pubmed')
 
    # Many fields can be pointed to via an Xpath directly, although we still want
    # to mangle the result in many cases, so the factory needs some tweaking.
    # To make names shorter, the field 'type' argument passed to the factory
    # is prefixed by "xpath_" to get the xpath variable name. Watch out for that!
    xpath_year = ['MedlineCitation', 'Article', 'Journal', 'JournalIssue', 'PubDate', 'Year']
    xpath_pub_month = ['MedlineCitation', 'Article', 'Journal', 'JournalIssue', 'PubDate', 'Month']
    xpath_pub_day = ['MedlineCitation', 'Article', 'Journal', 'JournalIssue', 'PubDate', 'Day']
    xpath_vol = ['MedlineCitation', 'Article', 'Journal', 'JournalIssue', 'Volume']
    xpath_pages = ['MedlineCitation', 'Article', 'Pagination', 'MedlinePgn']
    xpath_date_pubmed_created = ['MedlineCitation', 'DateCreated']
    xpath_date_pubmed_updated = ['MedlineCitation', 'DateRevised']
    def extract_xpath_factory(type, rdict=None, format=None):
        def extract_xpath(self, xml_data):
            try:
                data = xml_data
                for node in getattr(self, 'xpath_'+type):
                    data = data[node]
                if rdict != None:
                    data = rdict[data]
                if format != None:
                    data = format(data)
                return data
            except (KeyError, TypeError):
                return None
        return extract_xpath
    extract_year = extract_xpath_factory('year')
    extract_pub_month = extract_xpath_factory('pub_month', rdict=months_rdict)
    extract_pub_day = extract_xpath_factory('pub_day')
    extract_vol = extract_xpath_factory('vol')
    extract_pages = extract_xpath_factory('pages')
    extract_date_pubmed_created = extract_xpath_factory('date_pubmed_created', format=format_ddate)
    extract_date_pubmed_updated = extract_xpath_factory('date_pubmed_updated', format=format_ddate)
 
    # The grantlist is a bit mroe convoluted, because it is itself a dictionary with several
    # fields, which normally need to go together to by of use.
    xpath_grantlist = ['MedlineCitation', 'Article', 'GrantList']
    def extract_grantlist(self, xml_data):
        try:
            data = xml_data
            for node in self.xpath_grantlist:
                data = data[node]
            fields = {'acronym':'Acronym', 'agency':'Agency', 'country':'Country', 'number':'GrantID'}
            return [{k:d.get(v,None) for k,v in fields.items()} for d in data]
        except (KeyError, TypeError):
            return None
 
    # These are convenience functions that fetch single fields for many PMIDs.
    def fetch_field_factory(type):
        def fetch_field(self, pmid):
            targets = [getattr(self, 'extract_'+type)(parsed) for parsed in self.fetch_xml(pmid)]
            return list_or_single(targets)
        return fetch_field
    fetch_pmid = fetch_field_factory('pmid')
    fetch_doi = fetch_field_factory('doi')
    fetch_year = fetch_field_factory('year')
    fetch_pub_month = fetch_field_factory('pub_month')
    fetch_pub_day = fetch_field_factory('pub_day')
    fetch_vol = fetch_field_factory('vol')
    fetch_pages = fetch_field_factory('pages')
 
    # And this one extracts fetches all the fields defined above for many PMIDs.
    def fetch_all(self, pmid):
        xml_data = self.fetch_xml(pmid)
        all = []
        for parsed in xml_data:
            x = {}
            for f in self.fields:
                x[f] = getattr(self, "extract_"+f)(parsed)
            all.append(x)
        return all

