##################
# Author:Toshiki Hirao
# Summary: This script finds where the change occured.
# Usage: ./changedLineIdentifier.py gm_openstack 1 1000
##################

### Import lib
import sys
import csv
import datetime
import json
import re
from collections import defaultdict

### Import json file
specificDir = sys.argv[1]
startIdx = int(sys.argv[2])
endIdx = int(sys.argv[3])
resultFilePatch = '../changedLineList_'+str(startIdx)+'_'+str(endIdx)+'.csv'
errorFilePatch = '../changedLineListError_'+str(startIdx)+'_'+str(endIdx)+'.csv'
fResult = open(resultFilePatch, 'w')
fErrorLog = open(errorFilePatch, 'w')

### Main
with open('../gm_openstack.csv', 'rU') as fImport:
    reader = csv.DictReader(fImport, lineterminator='\n')
    for i, rev_file in enumerate(reader, start=1):
        if i < startIdx:
            continue
        if i > endIdx:
            break
        idx = i
        changeFlg = False
        skipFlg = False
        onlyAddedLineNumberList = []
        rev_id = rev_file["rev_id"]
        previousRev_id = rev_file["rev_previousId"]
        f_file_name = rev_file["f_file_name"]
        # The json has like ]}' at the begining.
        fjsonPath = '../revision_files/' + specificDir + '/' + rev_id + '/' + f_file_name + '.json'
        fjson = open(fjsonPath, 'r')
        fjsonEncoded = fjson.read()
        jsonFile = re.sub(r"^\)\]\}\'", "", fjsonEncoded)
        sys.stdout.write("\rFile: %d / %d : start %d, end %d " % (i, endIdx, startIdx, endIdx))
        try:
            jtext = json.loads(jsonFile)
        except :
            fErrorLog.write(str(idx)+','+rev_id+','+f_file_name+","+"Error"+"\n")
            continue
        if "change_type" not in jtext.keys():
            fErrorLog.write(str(idx)+','+rev_id+','+f_file_name+","+"No_change_type"+"\n")
            continue
        if (jtext['change_type'] != 'DELETED'):
            aCount = 0
            bCount = 0
            for c in jtext['content']:
                # 'skip' = there is no change between previous patch set and current patch set
                # 'ab' = a common code that remain between previous patch set and current patch set
                # 'a' = previous codes that were modified in current patch set
                # 'b' = current codes that were modified in current patch set
                startChange = 0
                endChange = 0
                if 'skip' in c.keys():
                    fErrorLog.write(str(idx)+','+rev_id+','+f_file_name+","+"Skip"+"\n")
                    skipFlg = True
                    break
                if 'ab' in c.keys():
                    assert(('a' not in c.keys()) and ('b' not in c.keys()))
                    for l in c['ab']:
                        aCount += 1
                        bCount += 1
                elif 'a' in c.keys():
                    startChange = aCount + 1
                    for l in c['a']:
                        aCount += 1
                    endChange = aCount
                    fResult.write(str(idx)+','+rev_id+','+previousRev_id+','+f_file_name+','+str(startChange)+','+str(endChange)+"\n")
                    changeFlg = True
                elif 'b' in c.keys():
                    onlyAddedLineNumberList.append(aCount)
                    for l in c['b']:
                        bCount += 1
            if (changeFlg != True) and (skipFlg == False):
                if (len(onlyAddedLineNumberList) > 0):
                    for addedLineNumber in onlyAddedLineNumberList:
                        fResult.write(str(idx)+','+rev_id+','+previousRev_id+','+f_file_name+','+str(addedLineNumber)+','+str(addedLineNumber+1)+"\n")
                else:
                    fErrorLog.write(str(idx)+','+rev_id+','+f_file_name+","+"NoChange"+"\n")
        else:
            fErrorLog.write(str(idx)+','+rev_id+','+f_file_name+","+"Delete"+"\n")
            continue
        
