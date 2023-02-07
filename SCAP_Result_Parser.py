#TO DO
#Add Date of Scan
#Basic GUI

#import elementtree and os libraries
import xml.etree.ElementTree as ET
import os

#Define the directory where the XCCDF files are kept and the file keyword to look for
directory = r'[FILE_DIRECTORY]'
keyword = 'XCCDF'  #This can be added to if needed (ie. XCCDF-Results_Windows to only look at Windows files) based on the naming of the XCCDF files in the directory

#Open a text file to write the results to, change the directory and file name as necessary
with open(r'[SAVELOCATION]\SCAPResults.txt', 'w') as output:
    #Loop through all files in the defined directory
    for filename in os.listdir(directory):
        #If the filename contains the defined keyword, process the file.  If not, move to next file
        if keyword in filename:
            #Open results file in read only mode with appropriate encoding for XML
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as infile:
                #Parse the file into an Element tree and locate the root of the tree
                tree = ET.parse(infile)
                root = tree.getroot()

                #locate computer name and stig used in scan.  add to variables
                asset = root.find('.//{http://checklists.nist.gov/xccdf/1.2}target').text
                stig = root.find('.//{http://checklists.nist.gov/xccdf/1.2}benchmark').attrib['href']

                #loop through all rule-results, pull required information
                for i in root.iter('{http://checklists.nist.gov/xccdf/1.2}rule-result'):
                    #pull severity, idref, and pass_fail for each rule
                    severity = i.attrib['severity']
                    idref = i.attrib['idref']
                    pass_fail = i[0].text

                    #build a search string to find the description of the idref number,  ***Id changed in some STIGs to id***
                    idSearch = './/{http://checklists.nist.gov/xccdf/1.2}Rule[@Id="' + idref + '"]'
                    #search the idref number
                    desc = root.find(idSearch)
                    #replace line breaks in description to prevent overflow when importing into Excel
                    desc = desc[1].text.replace("\n","")
                    #create string in csv format using ';' as delimiter
                    outputStr = asset + ";" + stig + ";" + idref + ";" + desc + ";" + severity + ";" + pass_fail + "\n"
                    #write to results file
                    output.write(outputStr)

