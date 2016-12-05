#Author: duyu
#2016-12-4 21:36:01

import urllib2
import xml.etree.ElementTree as ET

def pdb2uniprotIdSet(id_pdb):
    uniprotId_list = []
    url_pdb = 'http://www.rcsb.org/pdb/rest/das/pdb_uniprot_mapping/alignment?query='
    prefix_pdb = '{http://www.efamily.org.uk/xml/das/2004/06/17/dasalignment.xsd}'
    file_pdb = urllib2.urlopen(url_pdb+id_pdb)
    try:
        tree_pdb = ET.parse(file_pdb)
    except:
        return False
    for e in list(tree_pdb.iter(prefix_pdb+'alignObject')):
        type = e.get('type')
        if type == 'PROTEIN':
            uniprotId_list.append(e.get('dbAccessionId'))
    return set(uniprotId_list)

def uniprotId2fullName(id_uniprot):
    url_uniprot = 'http://www.uniprot.org/uniprot/'
    prefix_uniprot = '{http://uniprot.org/uniprot}'
    file_uniprot = urllib2.urlopen(url_uniprot+id_uniprot+'.xml')
    try:
        tree_uniprot = ET.parse(file_uniprot)
    except:
        print id_uniprot
        return False
    full_name = list(tree_uniprot.iter(prefix_uniprot+'fullName'))[0].text
    return full_name

pdb_code_list = []
uid2fullName = {}
uidcnt = {}
nouid = 0
with open('pdb_code_file.txt') as f:
    for l in f:
        pdb_code_list.append(l.strip())
for p in pdb_code_list:
    uidlist = pdb2uniprotIdSet(p)
    if not uidlist:
        nouid += 1
        continue
    for uid in uidlist:
        fullName = uniprotId2fullName(uid)
        if not fullName:
            uid2fullName[uid] = 'None'
        else:
            uid2fullName[uid] = uniprotId2fullName(uid)
        if uid in uidcnt:
            uidcnt[uid] += 1
        else:
            uidcnt[uid] = 1
print nouid
outfile = open('./rank_protein_count.txt', 'w')
for uid in sorted(uidcnt, key=uidcnt.get, reverse=True):
    outfile.write(str(uidcnt[uid])+' - '+uid+' - '+uid2fullName[uid]+'\n')
