import re
import os
import zipfile

def result(command):# Regular expressions to extract data from the corpus
    doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
    docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
    text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)
    token_regex = re.compile("\w+([\,\.]\w+)*")
    #removing_punc = '''``!()[];:'",<>@#$%^&*_~'''

    tuple_dictionary = {}
    doc_dictionary = {}
    #opening and reading the files with stop words
    stopwords_file = open('stopwords.txt', 'r')
    stopwords_line = stopwords_file.readlines()

    #dictionary where all of the tuple will be kept by category

    doc_id_occurence = 1
    term_id = 0
    with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
        zip_ref.extractall()
        

    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
        
    for file in allfiles[0:]:
        with open(file, 'r', encoding='ISO-8859-1') as f:
            filedata = f.read()
            result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

            for document in result[0:]:
                # Retrieve contents of DOCNO tag
                docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
                #print(docno)
                # Retrieve contents of TEXT tag
                text = "".join(re.findall(text_regex, document))\
                        .replace("<TEXT>", "").replace("</TEXT>", "")\
                        .replace("\n", " ")
                        

                # step 1 - lower-case words, remove punctuation, remove stop-words, etc.
                text = text.lower()
                tokenization_list = []
                #removes the underscore here
                newText = text.replace("_"," ")
                
                #removing 
                for word in re.finditer(token_regex,newText):
                    begin = word.start()
                    end = word.end()
                    text_seperated = newText[begin:end]
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
                term_id_list = []
                position_count_list = []
                position_count = 1
                for words_stop in tokenization_list:
                    term_id_list.append(words_stop.encode())
                    position_count = position_count +1
                    position_count_list.append(position_count)

                for i in range(0,len(tokenization_list)):
                    if(tokenization_list[i] in tuple_dictionary):
                        tuple_dictionary[tokenization_list[i]].append((term_id_list[i],doc_id_occurence,position_count_list[i]))
                    elif(tokenization_list[i] not in tuple_dictionary):
                        tuple_dictionary[tokenization_list[i]] = [(term_id_list[i],doc_id_occurence,position_count_list[i])]

                if(docno in doc_dictionary):
                    doc_dictionary[docno].append((doc_id_occurence,position_count_list[-1]))
                
                else:
                    if position_count_list:
                        #print(position_count_list)
                        doc_dictionary[docno] = [(doc_id_occurence,position_count_list[-1])]
                

                
        #print(stopword_list)
        #print(term_id_list)
                doc_id_occurence = doc_id_occurence +1
    #print(doc_dictionary[command])
    print("Listing for document: ",command)
    for docid in doc_dictionary[command]:
        print("DOCID: ",docid[0])
        print("Total Terms: ", docid[1])

    #print(tuple_dictionary[command])
    #print("Total:" ,len(tuple_dictionary['command']))
    #counter2 = 0
    #for tuple_shown in tuple_dictionary['state']:
    #    if tuple_shown[1] == counter2:
    #        counter2 = counter2 +1
        

    #print(counter2)
        


            
            # step 3 - build index
            