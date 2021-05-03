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

    stopword_list = []
    for line in stopwords_line:
        stripped_word = line.rstrip("\n")
        #add the stop word to list
        stopword_list.append(stripped_word)
    #print(stopword_list)
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
                
                #Using the finditer to implement the regex. Finds the start of each word that fits and end. adds it to tokenization list
                for word in re.finditer(token_regex,newText):
                    begin = word.start()
                    end = word.end()
                    text_seperated = newText[begin:end]
                    tokenization_list.append(text_seperated)
                # if word in removing_punc:
                    #    text = text.replace(word , "")
                #t = token_regex.sub('',text)
                #cleaned_Text = t.split()

                #the for loop stops each line and only grabs the word.
                
                #for words in stopword_list:
                #    if words in tokenization_list:
                #        tokenization_list.remove(words)
                
                #makes a new tokenization list which compares the stopwords with the old tokenization list and removes stop words
                tokenization_list = [i for i in tokenization_list if i not in stopword_list]
                
                term_id_list = []
                position_count_list = []
                position_count = 1
                #makes a term id list by encoding it into binary of each word is the term_id
                for words_stop in tokenization_list:
                    term_id_list.append(words_stop.encode())
                    position_count_list.append(position_count)
                    position_count = position_count +1

                #for loop that runs from 0 to the size of the tokenization list
                for i in range(0,len(tokenization_list)):
                    #checks if the key which is a word is in the dictionary already. if it is then it appends the termid , doc id and position of the word
                    if(tokenization_list[i] in tuple_dictionary):
                        tuple_dictionary[tokenization_list[i]].append((term_id_list[i],doc_id_occurence,position_count_list[i]))
                    elif(tokenization_list[i] not in tuple_dictionary):
                        #if its not then it adds the key with its first value which is the term id , doc id and position of the word
                        tuple_dictionary[tokenization_list[i]] = [(term_id_list[i],doc_id_occurence,position_count_list[i])]

                #same as the loop above excepts adds the doc_id and number of words in the document
                if(docno in doc_dictionary):
                    doc_dictionary[docno].append((doc_id_occurence,position_count_list[-1]))
                else:
                    #checks if the list is empty
                    if position_count_list:
                        #adds the first key with values
                        doc_dictionary[docno] = [(doc_id_occurence,position_count_list[-1])]
                

                
        #print(stopword_list)
        #print(term_id_list)
                doc_id_occurence = doc_id_occurence +1
    #print(doc_dictionary[command])

    #if the command has --doc at position one then it will run
    if("--doc" == command[1]):
        #command is broken down into a list of command that was inputted EX: [".\read_index.py", "--term", "human", "--doc", "AP890321-0001"]
        #print command at 2 which should be the DOCNAME
        print("Listing for document: ",command[2])

        #runs a loop that checks each value in the certain key and returns DOC in the tuple and the total position in the tuple
        for docid in doc_dictionary[command[2]]:
            print("DOCID: ",docid[0])
            print("Total Terms: ", docid[1])

    #same as above except it checks if -- doc is not in the command
    if("--term" == command[1] and "--doc" not in command):
        #prints the listings for term in the tuple
        print("listing for term: ", command[2])
        #list for the first value in the tuple waste of memory and time ... i know
        first_value = []
        for tuple_shows in tuple_dictionary[command[2]]:
            first_value.append(tuple_shows[0])
        
        #Term ID which is the first value in the list
        print("TERMID:" ,first_value[0])
        #checks the length of the values in the tuple to check the total amount of times the word is used
        print("Total:" ,len(tuple_dictionary[command[2]]))
        #counter that starts at 0 and increments and the list Doc_count_terms checks if the doc id is already in the list
        counter2 = 0
        Doc_cont_terms = []
        for tuple_shown in tuple_dictionary[command[2]]:
            #if doc id is not in the tuple then it increments and adds it else it goes to the next one (term id, doc id , position)
            if tuple_shown[1] not in Doc_cont_terms:
                counter2 += 1
                Doc_cont_terms.append(tuple_shown[1])
        print("Number of documents containing term: " ,counter2)

    #same as above but chekcs if --doc is in the command    
    if("--term" == command[1] and "--doc" in command ):
        #command[2] is the term being used and command[4] is the document
        print("Inverted list for term:", command[2])
        print("In document: " , command[4])
        first_value2 = []
        term_freq_count = 0
        #checks for the doc id number to be used later in the for loop
        for docid in doc_dictionary[command[4]]:
            doc_id_number = docid[0]
            #print(doc_id_number)
        position_intuple = []

    
        for tuple_shown in tuple_dictionary[command[2]]:
            #print(tuple_shown[1])
            #if the value tuple has the doc id then it increments
            if (tuple_shown[1]  == doc_id_number):
                term_freq_count += 1
                #it also adds the position of the word to the position_tuple list
                position_intuple.append(tuple_shown[2])
            #shows the term id and puts it in the list of first value
            first_value2.append(tuple_shown[0])    
        print("TERMID:" ,first_value2[0])
        print("DOCID: ",doc_id_number)
        print("Term frequency in document: ", term_freq_count)
        print("Positions: ", position_intuple)
        #finally outputs   
            
            # step 3 - build index
            