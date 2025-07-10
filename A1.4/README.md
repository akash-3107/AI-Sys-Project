# Repository for ss23.1.4/team197
This is the repository for you solution. You can modify this README file any way you see fit.

**Topic:** SS23 Assignment 1.4: Query Math Data

[Members: Akash Tambe, Prashansa Priyadarshini]

We implemented a solution for translating a large dataset about mathematical publications into RDF triples and subsequently into a triplestore ( in this case, blazegraph). Then we run certain queries to find answer a set of questions.


Filename : main.py

Approach:

1. class myHandler(ContentHandler) : A custom content handler to parse the large dataset 
    1. __init__(): Constructor to define various fields depending on what data we need to extract
    2. startElement(self, name, attrs): This function is called by the parser object when it identifies a start tag in xml file
    3. endElement(self, name): This function is called by the parser object when it identifies a end tag in xml file
    4. characters(self, content): This function is used to store the content into a buffer variable that needs to be referenced later
    5. getData(self): This function return the data parsed which is added to a List

2. main():
    1. Initially we parse the file with the help of class customer content handler defined earlier
    2. Get the data parsed into a List according to our requirements
    3. Generate RDF triples from the extracted data
    4. Generate a file which contains all the data (Extension = .nt)
    5. LOAD this data file to blazegraph(triplestore) with a POST request
    6. Parse the problem file with help of minidom
    7. Depending upon the problem type, build the query
    8. Execute that query on blazegraph with the help of a GET request
    9. Parse the response we receive from GET request
    10. Get the required data and create a DOM object holding your XML data
    11. Write this DOM object data to a file and name it as a solution file

More points regarding approach: (Pros and Cons)

1. Creation of algorithm and debugging was easier with smaller dataset whereas a bottleneck was observed while processing the big dataset.
2. The idea of using sax parser for big dataset worked in our advantage as processing of each record one by one was possible. 
3. Regarding the processing of querry xml file, we previously started using dataframe which didnt quite work for us. Later we switched to list of lists which made it much simpler and easier.
4. Uploading RDF triples to blazegraph was also a little tricky. We found it easier to create a .nt file containing all the N-triples from the dataset and then uploading them to the blazegraph all together with post request. 
5. We also used postman to create/modify the API reqest to trigger blazegraph rather than directly triggering it via python. This helped us in debugging the API call.


To run:
1. Go to the directory which has main.py file and run it.

Modules used while solving the assignment :
1. xml.sax
2. os
3. requests
4. urllib.parse
5. xml.dom
6. json
7. xmltodict
8. xml.etree.ElementTree
9. bz2


PS:
For Problem type: msc-intersection, with the big dataset, with our query its taking way to long to generate the soutions and that is why it is also missing from solutions-big.xml file as well. Although this same querry is giving very accurate solutions for the smaller dataset with the same problem type. (As discussed the reason might be with the use of 'FILTER' in our querry. We discussed this point already with you and you mentioned that we don not need to make the querry any more efficient.)
