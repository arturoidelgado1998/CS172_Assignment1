import re
import os
import zipfile

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)
token_regex = re.compile("(?:\w+)(?:\.?\w+)*", re.DOTALL)

with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()

with open("stopwords.txt","r") as f:
    stopwords = f.split("\n")
    

# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
    
for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")

            # step 1 - lower-case words, remove punctuation, remove stop-words, etc.
            text = text.lower()

            #for word in text:
            #    if word in regex:
            #        text = text.replace(word , "")

            #This snippet is from Jorge
            text = re.findall(token_regex, text)

            #commented the rest out
            #text = text.replace("_","")
            #text = text.replace("`","")
            #t = token_regex.split(text)
            #t =text.split()
            #print(t)
            #for words in t:
            #    if stopwords == words:
            #        t =t.remove(words)
            print(t)

            # step 2 - create tokens 
            # step 3 - build index
            