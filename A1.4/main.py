import xml.sax as xs
import os
import requests
from urllib.parse import quote,unquote
from xml.dom import minidom
import json
import xmltodict
import xml.etree.ElementTree as ET
import bz2

#A custom content handler to parse the large dataset
class myHandler(xs.ContentHandler):
    #Constructor to define various fields depending on what data we need to extract
    def __init__(self):
        
        self.buffer = ""
        self.documentId = ""
        self.classifications = []
        self.authorIds = []
        self.publicationYear = ""
        self.keywords = []
        self.allData = []
        self.index = 0
        self.counter = 0
        
    #This function is called by the parser object when it identifies a start tag in xml file
    def startElement(self, name, attrs):
        self.buffer= ""
        if name=="zbmath:document_id":
            self._documentId = True
            self.counter += 1
            if self.counter % 1000 == 0:
                print(self.counter)
        if name =="zbmath:publication_year":
            self._publicationYear = True
        if name =="zbmath:author_id":
            self._authorId = True
        if name =="zbmath:classification":
            self._classification = True
        if name =="zbmath:keyword":
            self._keyword = True
            
    #This function is called by the parser object when it identifies a end tag in xml file    
    def endElement(self, name):        
        if name=="zbmath:document_id" and self._documentId ==True:
            self.documentId = self.buffer
        if name=="zbmath:publication_year" and self._publicationYear ==True:
            self.publicationYear = self.buffer
        if name=="zbmath:author_id" and self._authorId ==True:
            self.authorIds.append(self.buffer)
        if name=="zbmath:classification" and self._classification ==True:
            self.classifications.append(self.buffer)
        if name=="zbmath:keyword" and self._keyword ==True:
            self.keywords.append(self.buffer)
        
            
        if name=="zbmath:language":  
            self.allData.append([self.documentId, self.publicationYear, self.authorIds, self.classifications, self.keywords])
            self.authorIds = []
            self.classifications = []
            self.keywords =[] 
                       
    #This function is used to store the content into a buffer variable that needs to be referenced later
    def characters(self, content):
        self.buffer+=content.strip()

    #This function return the data parsed which is added to a List
    def getData(self):
        return self.allData
        
if __name__ == '__main__':
    #initializing filenames and locations
    problem_filename='problems-big.xml'
    save_path_file = 'solutions-big.xml'
    
    nt_filename='data.nt'
    nt_file= open(nt_filename,'a',encoding='utf-8')
    nt_filepath=os.path.abspath(nt_filename)
    datafile='zbMathOpen_OAIPMH_int.xml.bz2'
    handler = myHandler()
    
    #extracting data from .bz2 file
    with bz2.open(datafile, 'r') as fp:
        fp.read(22)
        xs.parse(fp, handler)
    allData = handler.getData()
    
    #Initializing URLs
    has_author = "http://example.org/hasAuthor"
    has_classification = "http://example.org/hasClassification"
    has_keywords = "http://example.org/hasKeywords"
    published_year = "http://example.org/publishedYear"
    doc_id_url = "https://zbmath.org/?q=an%3A"
    auth_id_url = "https://zbmath.org/authors/?q=ai%3A"
    classification_url = "https://zbmath.org/classification/?q=cc%3A"
    keyword_url = "https://zbmath.org/?q=ut%3A"
    
    blazegraph_localhost = 'http://localhost:9999/'
    query_load = 'blazegraph/namespace/kb/sparql?update= LOAD<file:///'
    query_dropall = 'blazegraph/namespace/kb/sparql?update=DROP ALL'
    query_tail = '&Content-Type=application/sparql-update'
    query_get = 'blazegraph/namespace/kb/sparql?query='
    
    #Clearing blazegraph database
    requests.post(url=blazegraph_localhost+query_dropall)
    
    #Creating Ntriples from the dataset and storing in data.nt file
    for data in allData:
        post_data_pubyear = '<'+doc_id_url+data[0]+'> '+'<'+published_year+'> \"'+data[1]+'\" .\n' 
        nt_file.write(post_data_pubyear)
        for author in data[2]:
            post_data_auth = '<'+doc_id_url+data[0]+'> '+'<'+has_author+'> '+'<'+auth_id_url+author+'> '+'.\n'
            nt_file.write(post_data_auth)
        for classification in data[3]:
            post_data_classfication = '<'+doc_id_url+data[0]+'> '+'<'+has_classification+'> '+'<'+classification_url+classification+'> '+'.\n'
            nt_file.write(post_data_classfication)
        for keyword in data[4]:
            keyword=keyword.replace(" ","+")
            post_data_keyword = '<'+doc_id_url+data[0]+'> '+'<'+has_keywords+'> '+'<'+keyword_url+quote(keyword)+'> '+'.\n'
            nt_file.write(post_data_keyword)
        
        
    nt_file.close()
    #Post reuest to upload Ntriple in blazegraph from data.nt file
    insert_dataURL=blazegraph_localhost+query_load+nt_filepath+'>'+query_tail
    response=requests.post(url=insert_dataURL)
    if response.status_code==200:
        print('Data uploaded to blazegraph')
        os.remove(nt_filepath)
    else:
        print('File not uploaded to Blazegraph. Error Code:',response.status_code)
    
    #parse through problems file via DOM
    doc = minidom.parse(problem_filename)
    problems= doc.getElementsByTagName("Problem")
    where_str = ''
    where_str_xml = ''
    response_coauth = []
    response_msc_int = []
    response_top_keywords = []
    response_top_keywords_count = []
    #creating Elemnet Tree
    solutions = ET.Element('Solutions')

    #Iterating over problems
    for p in problems:
        idn = p.getAttribute("id")
        type = p.getAttribute("type")
        #check if type "coauthors"
        if type == "coauthors":
            author = p.getElementsByTagName("Author")[0]
            auth = author.firstChild.data
            get_co_auth = 'SELECT DISTINCT ?author ' + 'WHERE { ' +'?s <' + has_author + '> <' + quote(auth) + '>. ?s <'+has_author+'> ?author ' 'FILTER(?author!= <'+ quote(auth) + '>).}'
            get_co_auth_xml = 'SELECT DISTINCT ?author ' + 'WHERE { ' +'?s <' + has_author + '> <' + auth + '>. ?s <'+has_author+'> ?author ' 'FILTER(?author!= <'+ auth + '>).}'
            #creating get request with query
            query_get_co_auth = blazegraph_localhost + query_get + get_co_auth
            r1 = requests.get(url=query_get_co_auth)
            if r1.status_code==200:
                content = r1.content
                python_dict = xmltodict.parse(content)
                json_str = json.dumps(python_dict)
                y = json.loads(json_str)
                #extract vlaues from response and updating into element tree
                res = y["sparql"]["results"]
                if res is not None:
                    res = y["sparql"]["results"]["result"]
                    if len(res)==1:
                        res=[res]
                    solution = ET.SubElement(solutions, 'Solution', id=idn)
                    query = ET.SubElement(solution, 'Query')
                    query.text = get_co_auth_xml
                    
                    for r in res:
                        response_coauth.append(r["binding"]["uri"])
                    for i in response_coauth:
                        au = ET.SubElement(solution, 'Author')
                        au.text = i 
            else:
                print(type,"- Error Code: ",r1.status_code)
            response_coauth.clear()
        
        #check if type is "msc-intersection"
        if type == "msc-intersection":
            
            classification = p.getElementsByTagName("Classification")
            str_start='SELECT DISTINCT ?s WHERE { '
            str_end='}'
            count=0
            classificationList=[]
            #loop to add classification filter depending on problem
            for c in range(len(classification)):
                count=count+1
                cl = p.getElementsByTagName("Classification")[c]
                cfn = cl.firstChild.data
                where_str=where_str+'?s <'+has_classification+'> ?o'+str(count)+'. '
                where_str_xml=where_str_xml+'?s <'+has_classification+'> ?o'+str(count)+'. '
                classificationList.append(cfn)
                
            
            for i in range(count):
                where_str=where_str+'FILTER CONTAINS(str(?o'+str(i+1)+'),\"'+quote(classificationList[i])+'\") '
                where_str_xml=where_str_xml+'FILTER CONTAINS(str(?o'+str(i+1)+'),\"'+classificationList[i]+'\") '
            #where_str=where_str[:-6]
            get_msc_intersection=str_start+where_str+str_end
            get_msc_intersection_xml=str_start+where_str_xml+str_end
            where_str = ""
            where_str_xml=""
            # create get request along with query
            query_msc_intersection = blazegraph_localhost + query_get + get_msc_intersection
            r2 = requests.get(query_msc_intersection)
            if r2.status_code==200:
                content = r2.content
                python_dict = xmltodict.parse(content)
                json_str = json.dumps(python_dict)
                y = json.loads(json_str)
                solution = ET.SubElement(solutions, 'Solution', id=idn)
                query = ET.SubElement(solution, 'Query')
                query.text = get_msc_intersection_xml
                #extract claues from reponse and add into element tree
                res = y["sparql"]["results"]
                if res is not None:
                    res = y["sparql"]["results"]["result"]
                    if len(res)==1:
                        res=[res]
                    for r in res:
                        response_msc_int.append(r["binding"]["uri"])
                    for i in response_msc_int:
                        p = ET.SubElement(solution, 'Paper')
                        p.text = i
                        
            else:
                print(type,"- Error Code: ",r2.status_code)
            response_msc_int.clear()
            
        
        #check if type is "top-keywords"
        if type == "top-keywords":
            author = p.getElementsByTagName("Author")[0]
            authr = author.firstChild.data
            befYear = p.getElementsByTagName("BeforeYear")[0]
            by = befYear.firstChild.data
            aftYear = p.getElementsByTagName("AfterYear")[0]
            ay = aftYear.firstChild.data
            get_top_keywords = 'SELECT ?keywords (COUNT(?keywords) as ?oCount) WHERE { ?s <' + has_keywords + '> ?keywords. ?s <' + has_author + '> ?author. ?s <' + published_year + '> ?year. FILTER(xsd:integer(?year)<' + str(by) + ' %26%26 xsd:integer(?year)>'+str(ay)+') FILTER(?author = <' + quote(authr) + '>)} GROUP BY ?keywords ORDER BY desc(?oCount) LIMIT 3'
            get_top_keywords_xml = 'SELECT ?keywords (COUNT(?keywords) as ?oCount) WHERE { ?s <' + has_keywords + '> ?keywords. ?s <' + has_author + '> ?author. ?s <' + published_year + '> ?year. FILTER(xsd:integer(?year)<' + str(by) + ' && xsd:integer(?year)>'+str(ay)+') FILTER(?author = <' + authr + '>)} GROUP BY ?keywords ORDER BY desc(?oCount) LIMIT 3'
            #create get request call with query
            query_top_keywords = blazegraph_localhost + query_get + get_top_keywords
            r3 = requests.get(query_top_keywords)
            if r3.status_code==200:
                content = r3.content
                python_dict = xmltodict.parse(content)
                json_str = json.dumps(python_dict)
                y = json.loads(json_str)
                solution = ET.SubElement(solutions, 'Solution', id=idn)
                query = ET.SubElement(solution, 'Query')
                query.text = get_top_keywords_xml
                #extarct values from response and add in elemnet tree
                res = y["sparql"]["results"]
                count = 0
                if res is not None:
                    res = y["sparql"]["results"]["result"]
                    if len(res)==1:
                        res=[res]
                    for r in res:
                        keywordValue=r["binding"][0]["uri"]
                        splitValue=keywordValue.split('ut%3A')
                        keywordValue=splitValue[0]+'ut%3A'+unquote(splitValue[1])
                        response_top_keywords.append(keywordValue)
                        response_top_keywords_count.append(r["binding"][1]["literal"]["#text"])

                    for i in response_top_keywords:
                        p = ET.SubElement(solution, 'Keyword', count = str(response_top_keywords_count[count]))
                        p.text = i
                        count = count + 1
            else:
                print(type,"- Error Code: ",r3.status_code)
            response_top_keywords.clear()
            response_top_keywords_count.clear()
    
    #Create solution xml from element tree
    solutions = minidom.parseString(ET.tostring(solutions)).toprettyxml(indent = "\t")
    with open(save_path_file, "w") as f:
        f.write(solutions) 