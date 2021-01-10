#___Python 3.8.3____

# STUDENT : TRABZI Mohammed Amine 
# Master 2 Data Science 
# Project : Document similarity 

import random
import math 
import string
import urllib.request
import re
import sys
import time

# Functions :-------------------------------------------------------
def min_hash(doc, perm):
  for d in perm:
    if d in doc: return d
    
def jaccard_similarity(doc1, doc2):  # Jaccard_similarity_function 
  if len(doc1)==0 or len(doc2)==0: return 0.0
  else:
    inter = doc1.intersection(doc2)
    union = doc1.union(doc2)
    return float(len(inter))/float(len(union))

# ------------------------------------------------------------------


#_________________________________Part 0 : _____________________________________________________________________________________________________________________________________

#Read arguments from command line ----------------------------------------------------------------
if len(sys.argv)>=3:
    t1=float(sys.argv[2])
    file_name=sys.argv[1]
    print('Threshold t=%f'%(t1))
    print('file_name is %s'%(file_name))
else:
    print('ERR : argument 2 is missing ! ')
    print('command-line should be as follow: python < program_name > < doc_file > < similarity >')
    sys.exit(2)



# Tune b & r parameters: --------------------------------------- 
b=5 # number of bands
r= round((math.log(1/b))/math.log(t1)) # number of rows per band 
t=math.pow(1/b,1/r)
print('r=%d , b=%d, t=%f'%(r,b,t))



#Open the file :--------------------------------
file= open(file_name,"r")
documents = []

#print('### Print each line of the document :')
for index in file: 
  documents.append(str(index.strip()).lower())
  #print(str(index.strip()).lower() +'\n')


#___________________________________________________________ Part 1. transform the documents into sets of k-shingles_________________________________________________________________________________


clock1=time.time()

k = 5 #k-shingles

offset=k+1
sh_id=0
tot_num_shingles=0

shingle_id={} # for storing shingles and there ids
unique_shingles_list=[] # We store identical shingles without repititions 
matrix=[] # for storing the id of each shingle in all documents in the same order as shigles are ordered
for i in documents:
    line_shingles=[]
    line_compacted=''.join(j for j in i if j.isalnum() ) # remove space between words
   
    for n in range(len(line_compacted)-offset):  # we start shingling the line 
        shingle = line_compacted[n:n + k]
        line_shingles.append(shingle)
    tot_num_shingles+=len(line_shingles) # for each line we measure len(line_shingles) 
                                         # & we add its length to tot_num_shingles
                                         # so that we get at the end the total number of generated shingles
    
    # We need to know unique shingles & shingles for each document to use them later 
    stock_shingle_ids=set()
    for a in line_shingles:
        if a not in shingle_id:
            shingle_id[a]=sh_id
            sh_id+=1
            unique_shingles_list.append(a)
        stock_shingle_ids.add(shingle_id[a])
    matrix.append(stock_shingle_ids)
    
clock2=time.time()
Q1_elapsed_time=clock2-clock1

#---------------------------------------------------------
#printing            
#print ("unique shingles: %d"%len(unique_shingles_list))
#print ("all shingles: %d"%tot_num_shingles)
#print(len(matrix))
#print(matrix)
#print(shingle_id)
#print(jaccard_similarity(matrix[0],matrix[1]))
#---------------------------------------------------------


#___________________________________________________part 2. create the signature matrix, using n min-hash function, as exemplified in Lab__________________________________________________________

clock3=time.time()


n=b*r  # number of min hash functions 
# We generate signature matrix 
permutation_list = list(range(len(unique_shingles_list)))
signature_matrix = []
for i in range(n):
    signature_matrix.append([])
    random.shuffle(permutation_list)
    for doc in matrix:
        minhash = min_hash(doc,permutation_list)
        signature_matrix[i].append(minhash)
        
clock4=time.time()
Q2_elapsed_time=clock4-clock3
#-------------------------------------------------------------------
#printing
#print(signature_matrix) 
#print(len(signature_matrix[199]))
#print('signature_matrix[%d][%d]=%d'%(0,0,signature_matrix[0][0]))
#print('signature_matrix[%d][%d]=%d'%(1,0,signature_matrix[0][1]))
#print('signature_matrix[%d][%d]=%d'%(2,0,signature_matrix[1][0]))
#print('signature_matrix[%d][%d]=%d'%(3,0,signature_matrix[1][1]))
#print('signature_matrix[%d][%d]=%d'%(4,0,signature_matrix[2][0]))
#print('signature_matrix[%d][%d]=%d'%(5,0,signature_matrix[2][0]))
#--------------------------------------------------------------------


#______________________________part 3. use Locality Sensitive Hashing, by carefully choosing the threshold to minimize the number of candidate document pairs _________________________________________
                                                                                    
clock5=time.time()

# 3.1. create string repr. for each document, containing the signature 

vect=[] # matrix of size :  b x number-of-docs

for k in range(b): 
    x=k*r # using x is important to create bands
    vect.append([])
    for j in range(len(matrix)): #  len(matrix) = number of docs
            string=[]
            for i in range(r):
                string.append(signature_matrix[i+(x)][j])
            shot_string=''.join(map(str,string))
            vect[k].append(shot_string)
#print('->number of bands : len(vect)= %d'%(len(vect))) 


# 3.2. create dictionary ___ example: d = { '1-3-3':[d1,d2], '1-1-2':[d3] }      

number_portions=len(matrix)*len(vect)
#print('#number_portions(#bands x #docs)=%d'%(number_portions))
#print(hash(vect[0][0])%number_portions)

vect1=[]
bucket_size=number_portions*1000
for i in range(bucket_size):
    vect1.append([])
    
for i in range(b):
    for j in range(len(matrix)):
        index=hash(vect[i][j])%(bucket_size)
        if j not in vect1[index]:
            vect1[index].append(j)
        else:
            continue
#print('->len(vect1)=%d'%(len(vect1)))

vect2=[]
#vect3=[]
count_pairs=0
for i in range(len(vect1)):
    if len(vect1[i])>=2:
        a=len(vect1[i])
        vect2.append(vect1[i])
        if a==2:
          count_pairs+=1
        else:
          count_pairs+=a*(a-1)-a
        
print('\n')      
print('->len(vect2)=%d'%(len(vect2)))     
print('-> print vect2')
print(vect2)
print('counted_pairs =%d'%(count_pairs))      
print('\n')

clock6=time.time()
Q3_elapsed_time=clock6-clock5

#_____________________________________ part 4. compute the true Jaccard similarity for the document pairs, and output them if above the thresh-old____________________________________________________

clock7=time.time()

print('Count true jaccard similarity between candidate pairs') 
print('\n')
count_truePos_pairs=0
for i in range(len(vect2)):
    for j in range(len(vect2[i])):
        for k in range(len(vect2[i])):
            if j !=k:
                j_sim = jaccard_similarity(matrix[vect2[i][j]],matrix[vect2[i][k]])
                if j_sim>t:
                    count_truePos_pairs+=1
                    print ('doc%d-doc%d jaccard-sym %f'%(vect2[i][j],vect2[i][k],j_sim))
                else:
                    continue
clock8=time.time()  
Q4_elapsed_time=clock8-clock7   
print('\n')
print('# true positive = %d'%(count_truePos_pairs/2))  
print('# false positive = %d'%(count_pairs-count_truePos_pairs/2))  
print('Pourcentage of TP = %f pourcent' %(100*(count_truePos_pairs/2)/(count_pairs))) 
print('Pourcentage of FP = %f pourcent' %(100*((count_pairs-count_truePos_pairs/2))/(count_pairs)))
#___________________________________________________________________________________________________________________________________________________________________________

# print measumed running time: 
print('\n')
print('Time measurements:')
print('******************')
print('Elapsed time to transform documents into sets of k-shingles = %f'%(Q1_elapsed_time))
print('Elapsed time to create the signature matrix = %f'%(Q2_elapsed_time))
print('Elapsed time to use Locality Sensitive Hashing = %f'%(Q3_elapsed_time))
print('Elapsed time to compute the true Jaccard similarity for the document pairs = %f'%(Q4_elapsed_time))
print('Total time = %f'%(Q1_elapsed_time+Q2_elapsed_time+Q3_elapsed_time+Q4_elapsed_time))
