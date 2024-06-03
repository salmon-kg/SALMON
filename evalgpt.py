#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 23:45:28 2023

@author: salman
"""

import os
import nltk
import string
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
from spacy.lang.en import English
import csv

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

path = 'Path to data file'


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    return tokens


def jaccard_similarity(a, b):
    
    tokens_a = [token.lower().strip(string.punctuation) for token in tokenize(a)] #\
                    #if token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in tokenize(b)] #\
                    #if token.lower().strip(string.punctuation) not in stopwords]

    ratio = len(set(tokens_a).intersection(tokens_b)) / float(len(set(tokens_a).union(tokens_b)))
    #print('Similarity:',ratio)
    return (ratio)


def cosine_simialarity(a, b):
    
    l1 =[]
    l2 =[]

    tokens_a = [token.lower().strip(string.punctuation) for token in tokenize(a)] #\
                    #if token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in tokenize(b)]# \
                    #if token.lower().strip(string.punctuation) not in stopwords]
    
    rvector = set(tokens_a).union(tokens_b)
    for w in rvector:
        if w in tokens_a: l1.append(1) # create a vector
        else: l1.append(0)
        if w in tokens_b: l2.append(1)
        else: l2.append(0)
    
    c = 0
    for i in range(len(rvector)):
        c+= l1[i]*l2[i]
        
    x = float((sum(l1)*sum(l2))**0.5)
    
    if x!=0:
        cosine = c/x
    else:
        cosine = 0
    #print("similarity: ", cosine)

    return (cosine)
grt=0
gptt=0

tcos=0
tjac=0
tcosa=0
tjaca=0
tcosp=0
tjacp=0
totalCos=0
totalJac=0

with open(path,"r") as f:
    #data = f.readlines()
    csv_readerx = csv.reader(f, delimiter=',')
    num=0
    for n in csv_readerx:    
        i=0
        x=n[ground-truth]
        y=n[extracted]
        c=0
        j=0
        i=1
        if y:
            GT=x.split(',')
            T=y.split(',')
            #print(T)
            
            for a in T:   
                #cs=0.8
                #js=0.8
                for b in GT:
                    Csim = cosine_simialarity(a,b)
                    #if Csim>cs:
                        #Csim=1
                
                    
                    Jsim = jaccard_similarity(a,b)
                    #if Jsim>js:
                        #Jsim=1
                        
                # # AMNESTY        
                # if js>0.8:
                #       js=1    
                # # # PENALTY   
                # if js<0.5:
                #     js=0
           
                  
                # # # AMNESTY    
                # if cs>0.8:
                #       cs=1  
                # # # PENALTY    
                # if cs<0.5:
                #     cs=0
                
                
                c+=Csim
                j+=Jsim
          
        k = len(GT)
        l= len(T)
        #print(k,"vs",l)
        mn = max(k,l)
        grt+=k
        gptt+=l
        cos = c/l
        jac = j/mn

            
        output=cos,jac    
        totalCos+=cos
        totalJac+=jac
        num+=1
        #print("Cosine Similarity For Paragraph ",num,":",cos)
        #print("Jaccard Similarity For Paragraph ",num,":",jac)
     
        
# print("######################################")
# print("GPT-3.5-Turbo 0-Shot Complex")
# print("######################################")
# #print("Total Cosine Similarity:",totalCos)
# #print("Total Jaccard Similarity:",totalJac)
# print("Total Cosine Similarity:",(totalCos/720)*100,"%")
# print("Total Jaccard Similarity",":",(totalJac/720)*100,"%")
# print("######################################")

print("G-TRUTH TRIPLES:",grt)
print("Identified Triples:",gptt)
# print("######################################") 

M=max(grt,gptt)
N=min(grt,gptt)

R = N/M*100
P = (totalCos/100)*100
Fscore = 2*(P*R)/(P+R)

print("######################################")
print("GPT3.5-S Penalty free Precision 0-Shot")

print("Precison = ", round(P,2))
print("Recall = ", round(R,2))
print("F-Measure = ", round(Fscore,2))
print("######################################")


#### Test Scenario ############
      
# GT = ["ANU, Located in, Canberra Australia","ANU, Location, Canberra"]
# T = ["ANU, Located in, Canberra Australia", "ANU, is in, Australia"]

# # Csim = cosine_simialarity(GT,T)
# # print("Cosine Similarity:",Csim)

# # Jsim = jaccard_similarity(GT,T)
# # print("Jaccard Similarity:",Jsim)
# c=0
# j=0
# i=1
# for x in T:   
#     cs=0
#     js=0
#     for y in GT:
#         Csim = cosine_simialarity(x,y)
#         if Csim>cs:
#             cs=Csim
    
        
#         Jsim = jaccard_similarity(x,y)
#         if Jsim>js:
#             js=Jsim
        
        
#     print("Cosine Similarity for Triple",i,":",cs)
#     print("Jaccard Similarity for Triple",i,":",js)    
       
#     j+=js
#     c+=cs    
#     i+=1
    
# k = len(T)
# l= len(GT)
# print(k,"vs",l)
# n = max(k,l)

# print("Total Cosine Similarity:",c/n)
# print("Total Jaccard Similarity:",j/n)