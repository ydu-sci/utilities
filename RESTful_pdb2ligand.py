#Author: duyu
#2016-12-4 21:36:01

import urllib2
import xml.etree.ElementTree as ET
import itertools

def pdb2ligandid_mw(id_pdb):
    ligand_list = []
    url_pdb = 'http://www.rcsb.org/pdb/rest/ligandInfo?structureId='
    #NOT need the prefix
    #prefix_pdb = '{http://www.efamily.org.uk/xml/das/2004/06/17/dasalignment.xsd}'
    file_pdb = urllib2.urlopen(url_pdb+id_pdb)
    try:
        tree_pdb = ET.parse(file_pdb)
    except:
        return False
    for e in list(tree_pdb.iter('ligand')):
        ligandid = e.get('chemicalID')
        ligandmw = e.get('molecularWeight')
        ligand_list.append([ligandid, ligandmw])
    ligand_list.sort()
    return list(ligand_list for ligand_list,_ in itertools.groupby(ligand_list))

pdb_code_list = []
ligandcnt = {}
l2mw = {}
noligand = 0
with open('pdb_code_file.txt') as f:
    for l in f:
        pdb_code_list.append(l.strip())
for p in pdb_code_list:
    ligandlist = pdb2ligandid_mw(p)
    if not ligandlist:
        print p
        noligand += 1
        continue
    for lid, mw in ligandlist:
        if lid in ligandcnt:
            ligandcnt[lid] += 1
        else:
            ligandcnt[lid] = 1
        l2mw[lid] = mw
print noligand
outfile = open('./rank_ligand_count.txt', 'w')
for lid in sorted(ligandcnt, key=ligandcnt.get, reverse=True):
    outfile.write(str(ligandcnt[lid])+' '+str(l2mw[lid])+' '+lid+'\n')
