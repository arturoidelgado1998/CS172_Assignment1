# CS172 Assignment 1 - Tokenization

## Arturo Delgado, SID: 862099387
## Mario Aguirre, SID: 862079802

This is part one of a multiple part project of a basic information retrieval system. The language used for the program is Python.

The file, *parsing.py*, contains the majority of code. First we use a regex to remove puncuation and handle white-space in order to tokenize words from a list of documents.
A *stopword.txt* was provided with a list of stop words that are either removed or ignored from the index. In order to handle our tokenization we create a tuple dictionary function and a document dictionary function where all the tuples are kept by category. 
We are provided with code that retireves all the names of the files that are needed to be indexed in the current dictionary.

In the first step we lower-case the words, remove the puncuation, and stop-words and anything irrevalent in our search. Here we create a tokenized list of the cleaned-up word list and iterate through then and add them into the tuple dictionary. 

The second step we create the index of our total occurence of each term and their corresponding document ID. Each term, its info and document's ID are mapped and printed when their command is entered. The third step prints the inverted index of each term, document and its position in each file.

To run the program for example use: 

`py .\read_index.py --term human --doc AP890321-0001`

This will bring up the inverted list for the term 'human', the document in which it appears in this case 'AP890321-0001', the TERMID 'human', the DOCID: 19049, ther term frequency in the document, and the positions of the term.

