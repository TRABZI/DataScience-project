University of Paris Saclay
Master 2 Data Science

Programming Project
Document Similarity

Course:
Algorithms for Data Science

by:
mohammed amine TRABZI

Overview:
*********
The objective of this project is to be able to implement a system for document similarity evaluation,
using the techiniques of shingling and Min-Hash and Locality Sensitive Hashing. The documents we
are going to use are available in the following link : https://www.lri.fr/~maniu/tweets.txt . We
assume that each line in file tweets.txt is considered as document, for example line zero is
considered as document zero , line two is document two , and so on ...etc.
To realize this project, we will implement a python code having command line that takes : (1)_the
name of the file containing the documents, (2)_the similarity threshold in [0, 1], so that the
command line is: ./ < program_name > < doc_file > < similarity > .
The code output will be the pairs of documents that have a Jaccard similarity above the predefined
threshold, followed by their true similarity number.


Code execution :
****************

python code.py argument1 argument2

the argument should be in [0 1]

			Example:
			********
			python code.py tweets.txt 0.55
