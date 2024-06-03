#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 10:28:52 2023

@author: salman
"""

import os
import csv
import openai
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spacy.lang.en import English

path = 'Path to Data File'

#Replace your key with the actual key
openai.api_key = "your key"


def func(value):
    return ''.join(value.splitlines())

def stopwordsremoval(text):
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    filtered_sentence = (" ").join(tokens_without_sw)
    textf = filtered_sentence
    return textf 

def getSentences(text):
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    document = nlp(text)
    return [sent.string.strip() for sent in document.sents]
prompt0="Extract all possible subject-predicate-object triples from the following text and each triple should be in the form of (subject; predicate; object)."
prompt01="Extract subject-predicate-object triples from the following text. Each triple should be in the form of (subject; predicate; object)."
prompt1="Extract subject-predicate-object triples from the following text. Follow the following examples. Each triple should be in the form of (subject; predicate; object). \nText: Mantell was born in Bridgwater, Somerset, and studied at the University of Bath. \nTriples: \\n(Mantell; born in; Bridgwater Somerset),(Mantell; studied at; University of Bath)"
Body = "The text and examples are provided.\nGiven the text, split and rephrase into simple sentence and extract subject-predicate-object triples from the simplified text. Each triple should be in the form of (subject, predicate, object)."
Examples = (
    "Text: Besides CSIRO, Australian National University is located in Canberra.\n"
    "Triplets:\n(Australian National University; located in; Canberra)\n(Australian National University; located beside; CSIRO) \n(CSIRO; located in; Canberra)\n"
    "Text: Mantell was born in Bridgwater, Somerset, and studied at the University of Bath.\n"
    "Triplets:\n(Bridgwater; located in; Somerset)\n(Mantell; born in; Bridgwater Somerset)\n(Mantell; studied at; University of Bath)"
    "Text: Long Yun was an ethnic Yi General, and later Governor of Yunnan, Long Yun was a cousin of Lu Han. \n"
    "Triplets:\n(Long Yun; was; ethnic Yi General)\n(Long Yun; became; Governor of Yunnan)\n(Long Yun; is a cousin of; Lu Han)\n"
)


ANSWER = (
    "Text: {text}\n"
    "Triplets:\n"
)

promptn=f"{prompt0}\n{Examples}"


sim_total=0
with open(path,"r") as f:
    text = csv.reader(f, delimiter=',')
    row=1
    for n in text:
        sent=n[1]
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            #model="gpt4"
            #model="text-davinci-003"
            temperature=0.7,
            messages = [{"role": "user", "content" : f"{prompt01}\n Text: {sent} \nTriples:?"}]
            )
        response = completion['choices'][0]['message']['content']
        simp_out = func(response)
        
        
        print(f"{row} Response:\n {simp_out}")
        row += 1
        output = n[0],simp_out
        
        ## To store output
        with open(path + model+'output.csv', 'a') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(output)
                
#print("Total Simple Sentences: ", sim_total)      
        