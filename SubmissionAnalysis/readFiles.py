# Written by Caitlin C Bannan
# Mobley Group, University of California Irvine
# January 2016
# Reads prediction files submitted for the distribution coefficient half of SAMPL5
# Stores all collected data in a dictionary that can be used later

import pickle
import glob
import commands

def parseFile(fileName, comments = '#', keywords = ['predictions:', 'name:','software:', 'method:']):
    """
    Takes in file name and parses for prediction data and other provided information
    Returns two dictionaries 
    data keyed with molecule IDs from the prediction part of the file
    other keyed with the key words containing list of lines from that part of the file
    """
    fN = open(fileName)
    lines = fN.readlines()
    fN.close()
    keyword = ''
    data = {}
    other = {}
    for l in lines:

        # If the line is blank or a comment skip it
        if l.strip() == '':
            continue
        elif l.strip()[0] == comments:
            continue

        # If the line is a new keyword switch to that keyword
        elif l.strip().lower() in keywords:
            keyword = l.strip().lower()
            continue
        #Some of the submissions don't have the : after the keywords...
        elif l.strip().lower()+':' in keywords:
            keyword = l.strip().lower()+':'
            continue
        
        # Line is not a comment, blank or keyword so check the current keyword and behave accordingly
        if keyword == 'predictions:':
            split = l.strip().split(',')
            # get the molecule ID and add the data to the dictionary
            k = split[0].strip().upper() # a few people had SAMPl instead of SAMPL
            data[k] = [float(split[i]) for i in range (1,4)]
        
        # If it's not the prediction section save the info to the 'other' dictionary
        # The other dictionary would basically allow us to store the other information inclded in the prediction files, method names, software used, and methods followed.  
        else:
            # Add the line to the list for that keyword
            if not other.has_key(keyword):
                other[keyword] = []
            other[keyword].append(l.strip())
            
    return data, other

def ParseAllFiles(fileList, numDict = None):
    """
    Takes a list of files and creates a dictionary with information and data
    data is at key 'data' all other information is specified
    """
    Dict = {}
    # Parse file list
    for i,f in enumerate(fileList):
        fileName = f.split('/')[-1]
        Flist = fileName.split('_')
        # submission ID assigned from randomly assigned identifier
        subID = int(Flist[0].strip())
        # Use parseFile method to extract data
        data, Dict[subID] = parseFile(f)
        # Save other information to infoDictionary
        Dict[subID]['data'] = data

    # Return both dictionaries
    return Dict
        
#========================================================================
# Now use methods to parse prediction text files 

# Location of prediction data files:
preDir = "../predictionFiles_byNumber/"

# Parse and save all standard DC results
# Note: Mobley group was the only one to submit standard results...
#StanFiles = glob.glob('%s/*DCStandard-*.txt' % preDir)
#stanData = ParseAllFiles(StanFiles)
#pickle.dump(stanData, open('../DataFiles/StandardPredictions.p','wb'))

# Parse results for all regular DC predictions
RegFiles = glob.glob('%s/*.txt' % preDir)
regData = ParseAllFiles(RegFiles)

# ====================================================================
# Add user information to dictionary from SAMPL5_users.csv 
# This file has been edited by hand to guarentee 
# only DC prediction information is included
# and one organization name was edited to remove commas

UserInfoFile = "SAMPL5_submissionList.txt"
f = open(UserInfoFile)
lines = f.readlines()
f.close()

# Where I want a copy of these stored. 
SIdirectory = "~/Google\ Drive/Research/SAMPL/predictionFiles/"
for l in lines[1:]: # Skip header line in file
    # strip information
    info = [s.strip() for s in l.split(',')]
    key = int(info[0])

    # Added data about entry to dictionary entry
    regData[key]['firstName'] = info[1]
    regData[key]['lastName'] = info[2]
    regData[key]['Organization'] = info[3]

pickle.dump(regData, open('../DataFiles/predictions.p','wb'))
