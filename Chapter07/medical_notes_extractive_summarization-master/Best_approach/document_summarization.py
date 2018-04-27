# -*- coding: utf-8 -*-
"""
Created on Sun Sep 04 15:24:26 2016

@author: DIP
"""

from normalization import normalize_corpus, parse_document
from utils import build_feature_matrix, low_rank_svd
import numpy as np


toy_text = """
Elephants are large mammals of the family Elephantidae 
and the order Proboscidea. Two species are traditionally recognised, 
the African elephant and the Asian elephant. Elephants are scattered 
throughout sub-Saharan Africa, South Asia, and Southeast Asia. Male 
African elephants are the largest extant terrestrial animals. All 
elephants have a long trunk used for many purposes, 
particularly breathing, lifting water and grasping objects. Their 
incisors grow into tusks, which can serve as weapons and as tools 
for moving objects and digging. Elephants' large ear flaps help 
to control their body temperature. Their pillar-like legs can 
carry their great weight. African elephants have larger ears 
and concave backs while Asian elephants have smaller ears 
and convex or level backs.  
"""


from gensim.summarization import summarize, keywords

def text_summarization_gensim(text, summary_ratio=0.5):
    
    summary = summarize(text, split=True, ratio=summary_ratio)
    for sentence in summary:
        print sentence

docs = parse_document(toy_text)
text = ' '.join(docs)
text_summarization_gensim(text, summary_ratio=0.4)


    
sentences = parse_document(toy_text)
norm_sentences = normalize_corpus(sentences,lemmatize=False) 

total_sentences = len(norm_sentences)
print 'Total Sentences in Document:', total_sentences   



num_sentences = 3
num_topics = 1

vec, dt_matrix = build_feature_matrix(sentences, 
                                      feature_type='frequency')

td_matrix = dt_matrix.transpose()
td_matrix = td_matrix.multiply(td_matrix > 0)

u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)  
                                         
sv_threshold = 0.5
min_sigma_value = max(s) * sv_threshold
s[s < min_sigma_value] = 0

salience_scores = np.sqrt(np.dot(np.square(s), np.square(vt)))
print np.round(salience_scores, 2)

top_sentence_indices = salience_scores.argsort()[-num_sentences:][::-1]
top_sentence_indices.sort()
print top_sentence_indices

for index in top_sentence_indices:
    print sentences[index]
    
    
def lsa_text_summarizer(documents, num_sentences=2,
                        num_topics=2, feature_type='frequency',
                        sv_threshold=0.5):
                            
    vec, dt_matrix = build_feature_matrix(documents, 
                                          feature_type=feature_type)

    td_matrix = dt_matrix.transpose()
    td_matrix = td_matrix.multiply(td_matrix > 0)

    u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)  
    min_sigma_value = max(s) * sv_threshold
    s[s < min_sigma_value] = 0
    
    salience_scores = np.sqrt(np.dot(np.square(s), np.square(vt)))
    top_sentence_indices = salience_scores.argsort()[-num_sentences:][::-1]
    top_sentence_indices.sort()
    
    for index in top_sentence_indices:
        print sentences[index]
    
    
    

import networkx

num_sentences = 3
vec, dt_matrix = build_feature_matrix(norm_sentences, 
                                      feature_type='tfidf')
similarity_matrix = (dt_matrix * dt_matrix.T)
print np.round(similarity_matrix.todense(), 2)

similarity_graph = networkx.from_scipy_sparse_matrix(similarity_matrix)

networkx.draw_networkx(similarity_graph)

scores = networkx.pagerank(similarity_graph)

ranked_sentences = sorted(((score, index) 
                            for index, score 
                            in scores.items()), 
                          reverse=True)
ranked_sentences

top_sentence_indices = [ranked_sentences[index][1] 
                        for index in range(num_sentences)]
top_sentence_indices.sort()
print top_sentence_indices

for index in top_sentence_indices:
    print sentences[index]
    

def textrank_text_summarizer(documents, num_sentences=2,
                             feature_type='frequency'):
    
    vec, dt_matrix = build_feature_matrix(norm_sentences, 
                                      feature_type='tfidf')
    similarity_matrix = (dt_matrix * dt_matrix.T)
        
    similarity_graph = networkx.from_scipy_sparse_matrix(similarity_matrix)
    scores = networkx.pagerank(similarity_graph)   
    
    ranked_sentences = sorted(((score, index) 
                                for index, score 
                                in scores.items()), 
                              reverse=True)

    top_sentence_indices = [ranked_sentences[index][1] 
                            for index in range(num_sentences)]
    top_sentence_indices.sort()
    
    for index in top_sentence_indices:
        print sentences[index]                             
    

DOCUMENT = """
The Elder Scrolls V: Skyrim is an open world action role-playing video game 
developed by Bethesda Game Studios and published by Bethesda Softworks. 
It is the fifth installment in The Elder Scrolls series, following 
The Elder Scrolls IV: Oblivion. Skyrim's main story revolves around 
the player character and their effort to defeat Alduin the World-Eater, 
a dragon who is prophesied to destroy the world. 
The game is set two hundred years after the events of Oblivion 
and takes place in the fictional province of Skyrim. The player completes quests 
and develops the character by improving skills. 
Skyrim continues the open world tradition of its predecessors by allowing the 
player to travel anywhere in the game world at any time, and to 
ignore or postpone the main storyline indefinitely. The player may freely roam 
over the land of Skyrim, which is an open world environment consisting 
of wilderness expanses, dungeons, cities, towns, fortresses and villages. 
Players may navigate the game world more quickly by riding horses, 
or by utilizing a fast-travel system which allows them to warp to previously 
Players have the option to develop their character. At the beginning of the game, 
players create their character by selecting one of several races, 
including humans, orcs, elves and anthropomorphic cat or lizard-like creatures, 
and then customizing their character's appearance.discovered locations. Over the 
course of the game, players improve their character's skills, which are numerical 
representations of their ability in certain areas. There are eighteen skills 
divided evenly among the three schools of combat, magic, and stealth. 
Skyrim is the first entry in The Elder Scrolls to include Dragons in the game's 
wilderness. Like other creatures, Dragons are generated randomly in the world 
and will engage in combat. 
"""

DOCUMENT_1 = """

The patient is an 86-year-old female admitted for evaluation of abdominal pain and bloody stools. The patient has colitis and also diverticulitis, undergoing treatment.
During the hospitalization, the patient complains of shortness of breath, which is worsening. The patient underwent an echocardiogram, which shows severe mitral regurgitation and also large pleural effusion.
This consultation is for further evaluation in this regard. As per the patient, she is an 86-year-old female, has limited activity level.
She has been having shortness of breath for many years. She also was told that she has a heart murmur, which was not followed through on a regular basis.

"""

DOCUMENT_2 = """ The patient is a very pleasant 41-year-old white female that is known to me previously from our work at the Pain Management Clinic, as well as from my residency training program, San Francisco. We have worked collaboratively for many years at the Pain Management Clinic and with her departure there, she has asked to establish with me for clinic pain management at my office. She reports moderate to severe pain related to a complicated past medical history. In essence, she was seen at a very young age at the clinic for bilateral knee and hip pain and diagnosed with bursitis at age 23. She was given nonsteroidals at that time, which did help with this discomfort. With time, however, this became inadequate and she was seen later in San Francisco in her mid 30s by Dr. V, an orthopedist who diagnosed retroverted hips at Hospital. She was referred for rehabilitation and strengthening. Most of this was focused on her SI joints. At that time, although she had complained of foot discomfort, she was not treated for it. This was in 1993 after which she and her new husband moved to the Boston area, where she lived from 1995-1996. She was seen at the Pain Center by Dr. R with similar complaints of hip and knee pain. She was seen by rheumatologists there and diagnosed with osteoarthritis as well as osteophytosis of the back. Medications at that time were salicylate and Ultram.

When she returned to Portland in 1996, she was then working for Dr. B. She was referred to a podiatrist by her local doctor who found several fractured sesamoid bones in her both feet, but this was later found not to be the case. Subsequently, nuclear bone scans revealed osteoarthritis. Orthotics were provided. She was given Paxil and Tramadol and subsequently developed an unfortunate side effect of grand mal seizure. During this workup of her seizure, imaging studies revealed a pericardial fluid-filled cyst adhered to her ventricle. She has been advised not to undergo any corrective or reparative surgery as well as to limit her activities since. She currently does not have an established cardiologist having just changed insurance plans. She is establishing care with Dr. S, of Rheumatology for her ongoing care. Up until today, her pain medications were being written by Dr. Y prior to establishing with Dr. L.

Pain management in town had been first provided by the office of Dr. F. Under his care, followup MRIs were done which showed ongoing degenerative disc disease, joint disease, and facet arthropathy in addition to previously described sacroiliitis. A number of medications were attempted there, including fentanyl patches with Flonase from 25 mcg titrated upwards to 50 mcg, but this caused oversedation. She then transferred her care to Ab Cd, FNP under the direction of Dr. K. Her care there was satisfactory, but because of her work schedule, the patient found this burdensome as well as the guidelines set forth in terms of monthly meetings and routine urine screens. Because of a previous commitment, she was unable to make one unscheduled request to their office in order to produce a random urine screen and was therefore discharged.
"""

sentences = parse_document(DOCUMENT_1)
norm_sentences = normalize_corpus(sentences,lemmatize=True) 
print "Total Sentences:", len(norm_sentences)

print ("\n---------lsa summarization for document 1--------")
lsa_text_summarizer(norm_sentences, num_sentences=4,
                    num_topics=2, feature_type='frequency',
                    sv_threshold=0.5)

print ("---------text-rank summarization for document 1--------\n")
textrank_text_summarizer(norm_sentences, num_sentences=4,
                         feature_type='tfidf')

sentences = parse_document(DOCUMENT_2)
norm_sentences = normalize_corpus(sentences,lemmatize=True)
print "Total Sentences:", len(norm_sentences)

print ("\n---------lsa summarization for document 2--------")
lsa_text_summarizer(norm_sentences, num_sentences=4,
                    num_topics=2, feature_type='frequency',
                    sv_threshold=0.5)

print ("---------text-rank summarization for document 2--------\n")
textrank_text_summarizer(norm_sentences, num_sentences=4,
                         feature_type='tfidf')