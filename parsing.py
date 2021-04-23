import re
import os
import zipfile

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)
token_regex = re.compile("\w+([\,\.]\w+)*")
#removing_punc = '''``!()[];:'",<>@#$%^&*_~'''
stopwords_file = open('stopwords.txt', 'r')
stopwords_line = stopwords_file.readlines()

with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()
    

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
            tokenization_list = []
            text.replace('_','')
            #removing 
            for word in re.finditer(token_regex,text):
                begin = word.start()
                end = word.end()
                text_seperated = text[begin:end]
                tokenization_list.append(text_seperated)
               # if word in removing_punc:
                #    text = text.replace(word , "")
            #t = token_regex.sub('',text)
            #cleaned_Text = t.split()
            stopword_list = []
            for line in stopwords_line:
                stripped_word = line.rstrip("\n")
                stopword_list.append(stripped_word)
            
            #for words in stopword_list:
            #    if words in tokenization_list:
            #        tokenization_list.remove(words)
            tokenization_list = [i for i in tokenization_list if i not in stopword_list]
            #tokenization_list.remove('_')

            
    #print(stopword_list)
    print(tokenization_list)

            #print(tokenization_list)
            # step 2 - create tokens 
            # step 3 - build index
            