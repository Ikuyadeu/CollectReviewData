##################
# Author:Toshiki Hirao
# Summary: This code gets metrics from OpenStack, Eclipse, Gerrithub and Libreoffice in Xin's data in MSR2016.
# Usage: 
##################

### Import lib
import sys
import MySQLdb
import numpy
from collections import defaultdict
from Util import ReviewerFunctions
from Class import ReviewerClass
from Util import commentFilterFunctions
import datetime
from dateutil.relativedelta import relativedelta

### Functions
def median(list):
    sorted_list = sorted(list)
    length = len(sorted_list)
    center = length / 2
    if length == 1:
        return sorted_list[0]
    elif length % 2 == 0:
        return sum(sorted_list[center - 1: center + 1]) / 2.0
    else:
        return sorted_list[center]

### Setting agrv
dbName = sys.argv[1]
dbUser = sys.argv[2]
dbPass = sys.argv[3]
botIdFile = sys.argv[4]
FMT = '%Y-%m-%d'

### Init values
datetime_list = defaultdict(lambda: 0)
reviews_list = defaultdict(lambda: None)
botId = []

### Import bot ids from config file
botIdFp = open(botIdFile, "rU")
for row in botIdFp:
    v = row.strip().split(",")
    assert (len(v) == 2)
    botId.append(v[0])

### Connecting DB
cnct = MySQLdb.connect(db = dbName,user = dbUser, passwd = dbPass)
csr = cnct.cursor()

### Setting default values
sql = "SELECT COUNT(*) FROM t_change;"
csr.execute(sql)
NumOfReviews = csr.fetchall()[0][0] # Number Of Qt project's patchsets (70,705)

### Main Execution
# Extract change information from sql
if dbName == "gm_aosp":
    sql = "SELECT id, ch_changeId, ch_status, ch_project, ch_authorAccountId, ch_createdTime \
    FROM t_change \
    WHERE ch_status = 'MERGED'\
    #WHERE ch_status = 'MERGED' OR ch_status = 'ABANDONED' \
    ORDER BY ch_createdTime ASC;"
elif dbName == "gm_qt":
    sql = "SELECT id, ch_changeId, ch_status, ch_project, ch_authorId, ch_createdTime \
    FROM t_change \
    WHERE ch_status = 'MERGED'\
    #WHERE ch_status = 'MERGED' OR ch_status = 'ABANDONED' \
    ORDER BY ch_createdTime ASC;"
else:
    assert(dbName == "gm_openstack" or dbName == "gm_eclipse" or dbName == "gm_libreoffice" or dbName == "gm_gerrithub")
    sql = "SELECT id, ch_changeId, ch_status, ch_project, ch_authorAccountId, ch_createdTime, ch_changeIdNum \
    FROM t_change \
    WHERE ch_status = 'MERGED'\
    #WHERE ch_status = 'MERGED' OR ch_status = 'ABANDONED' \
    ORDER BY ch_createdTime ASC;"
csr.execute(sql)
t_change = csr.fetchall()

# CSV header
print("id,changeId,changeIdNum,status,pattern,discussionLength,numIteration,revLen,numParticipations")
disLenList = []
numIteList = []
for row in t_change:
    id = row[0]
    ch_changeId = row[1]
    ch_status = 0 if row[2] == "MERGED" else  1
    ch_project = row[3]
    ch_patchAuthor = row[4]
    ch_createdTime = row[5]
    if dbName == "gm_aosp" or dbName == "gm_qt":
        ch_changeIdNum = "NA"
    else:
        ch_changeIdNum = row[6]

    # Skipping a bot author patch
    if ch_patchAuthor in botId:
        continue

    # Extract comment from sql
    if dbName == "gm_aosp" or dbName == "gm_qt":
        sql = "SELECT hist_changeId, hist_message, hist_authorId, hist_createdTime, hist_patchSetNum \
        FROM t_history \
        WHERE hist_changeId = '" + str(id) + "' \
        ORDER BY hist_createdTime ASC;"
    else:
        sql = "SELECT hist_changeId, hist_message, hist_authorAccountId, hist_createdTime, hist_patchSetNum \
        FROM t_history \
        WHERE hist_changeId = '" + str(id) + "' \
        ORDER BY hist_createdTime ASC;"
            
    csr.execute(sql)
    t_history = csr.fetchall()
    if len(t_history) < 1:
        continue
    assert(len(t_history) > 0)

    participants_list = [] # The number of participants in the review
    score = 0
    discussionLen = 0
    numIteration = 0
    revLen = 0

    # Iterations: The number of iterations [].
    # Discussion length: The number of non-automated comments [Tsay et al, ICSE2014].

    for row in t_history:
        hist_changeId = row[0]
        hist_message = row[1]
        hist_reviewer = row[2]
        hist_createdTime = row[3] # The time by the last comment (Finally, it should be integration or abandonment comment)
        hist_patchSetNum = row[4]

        # Skipping a bot comment
        if hist_reviewer in botId:
            continue
        # Skipping a build comment
        if commentFilterFunctions.isBuildComment(hist_message) != None:
            continue
        # Measuring 'Discussion length' and '#iterations' that construct our desicion tree.
        if ReviewerFunctions.IsUpdate(hist_message) == None:
            # Counting reviewer comments
            assert(type(ReviewerFunctions.JudgeVoteScore(hist_message)) == int)
            discussionLen = discussionLen + 1
            # Counting participants # The other reviewer sometimes updates the change
            if (hist_reviewer != ch_patchAuthor) and (hist_reviewer not in participants_list) and (hist_reviewer != ""): # hist_reviewer == "" when integrating the change
                participants_list.append(hist_reviewer)

    ### Output
    timediff = hist_createdTime - ch_createdTime
    revLen = int(timediff.total_seconds() / 60 / 60 / 24)
    revExp = 0
    autExp = 0
    pattern = -1
    if (revLen >= 0) and (len(participants_list) > 1):
        reviews_list[int(id)] = str(id)+','+str(ch_changeId)+','+str(ch_changeIdNum)+','+str(ch_status)+','+str(discussionLen)+','+str(hist_patchSetNum)+','+str(revLen)+','+str(len(participants_list))
        disLenList.append(discussionLen)
        numIteList.append(hist_patchSetNum)

### Calculate threshold for discussion length and number of iterations
discussionThreashold = numpy.percentile(disLenList, 75)
iterationThreashold = numpy.percentile(numIteList, 75)
for k in sorted(reviews_list.keys()):
    v = reviews_list[k].strip().split(',')
    if int(v[4]) >= discussionThreashold:
        if int(v[5]) >= iterationThreashold:
            pattern = 0
        else:
            pattern = 1
    else:
        if int(v[5]) >= iterationThreashold:
            pattern = 2
        else:
            pattern = 3
    print v[0]+','+v[1]+','+v[2]+','+v[3]+','+str(pattern)+','+v[4]+','+v[5]+','+v[6]+','+v[7]