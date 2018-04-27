from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import dill
import math
from math import log

parse_fields = ['WORK EXPERIENCE', 'EDUCATION', 'SKILLS', 'AWARDS', 'CERTIFICATIONS', 'ADDITIONAL INFORMATION']
companies = ['amazon', 'apple', 'facebook', 'ibm', 'microsoft', 'oracle', 'twitter']

num_category = 7
num_company = 7
train1_size = 100
train2_size = 50
test_size = 50


def my_normalize(m):
    for i in range(num_category):
        for j in range(num_company):
            m[i][j] = m[i][j] + 0.001

    for i in range(num_category):
        sum = 0
        for j in range(num_company):
            sum = sum + m[i][j]
        for j in range(num_company):
            m[i][j] = m[i][j] / sum

    # 	for i in range(num_category):
    # 		minscore = 2
    # 		maxscore = -1
    #
    # 		for j in range(num_company):
    # 			if m[i][j] < minscore:
    # 				minscore = m[i][j]
    # 			if m[i][j] > maxscore:
    # 				maxscore = m[i][j]
    # 		minscore = minscore * 0.8
    # 		maxscore = maxscore + minscore * 0.2
    # 		diff = maxscore - minscore
    # 		if diff == 0:
    # 			return m
    # 		for j in range(num_company):
    # 			m[i][j] = (m[i][j]-minscore)/diff

    return m


def my_col_normalize(m):
    for i in range(num_category):
        for j in range(num_company):
            m[i][j] = m[i][j] + 0.001

    for i in range(num_company):
        sum = 0
        for j in range(num_category):
            sum = sum + m[j][i]
        for j in range(num_category):
            m[j][i] = m[j][i] / sum
    return m


def get_sim_vector(tfidf, tfidf_matrix, doc):
    response = tfidf.transform([doc])
    sim = cosine_similarity(response, tfidf_matrix)
    return sim[0]


def get_class(sim):
    cur_max = -1
    max_index = 0
    for j in range(num_company):
        if sim[j] > cur_max:
            cur_max = sim[j]
            max_index = j
    return max_index


with open('resume_data.pkl', 'rb') as input:
    all_resumes = dill.load(input)

for i in range(num_category):
    for j in range(num_company):
        for d in range(len(all_resumes[i][j])):
            all_resumes[i][j][d] = all_resumes[i][j][d].lower().replace(companies[j], '')



#########################################################################
# the naive TF-IDF
#########################################################################

score_matrix = [[0 for i in range(num_company)] for j in range(num_company)]
correct = 0.0
total = 0.0

train_set = []
for c in range(num_company):
    doc = ''
    for i in range(num_category):
        for d in range(train1_size):
            doc = doc + all_resumes[c][d][i]
    train_set.append(doc)

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)

print "--------- Simple TF-IDF approach----------"
for c in range(num_company):
    #print c
    for d in range(test_size):

        doc = ''

        for i in range(num_category):
            idx = train1_size + train2_size + d
            doc = doc + all_resumes[c][idx][0]

        response = tfidf_vectorizer.transform([doc])
        sim = cosine_similarity(response, tfidf_matrix_train)
        final_score = sim[0]
        print "Cosine similarity", final_score

        # cur_max = -1
        # max_index = 0
        # for j in range(num_company):
        #     if final_score[j] > cur_max:
        #         cur_max = final_score[j]
        #         max_index = j
        # total = total + 1
        # if max_index == c:
        #     correct = correct + 1

# print ""
# print 'Naive tf-idf score: ' + str(correct / total)


##################################################################################
# weighted categorical TF-IDF
##################################################################################
print "------- Weighted TF-IDF----------"
score_matrix = [[0 for i in range(num_company)] for j in range(num_company)]
tfidfs = []
tfidf_trains = []

for i in range(num_category):

    # print 'category:' + str(i)

    train_set = []
    for c in range(num_company):
        doc = ''
        for d in range(train1_size):
            doc = doc + all_resumes[c][d][i]
        train_set.append(doc)

    tfidf_vectorizer = TfidfVectorizer()
    tfidfs.append(tfidf_vectorizer)

    tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)
    tfidf_trains.append(tfidf_matrix_train)

    for c in range(num_company):
        score = 0.0
        for d in range(train2_size):
            idx = train1_size + d
            test_doc = all_resumes[c][idx][i]
            sim = get_sim_vector(tfidf_vectorizer, tfidf_matrix_train, test_doc)
            if get_class(sim) == c:
                score = score + 1
        score = score / train2_size / (1.0 / num_company)
        score_matrix[i][c] = score

score_matrix = my_normalize(score_matrix)
score_matrix = my_col_normalize(score_matrix)
print score_matrix


for i in range(num_category):
    for j in range(num_company):
        round(score_matrix[i][j], 3),
    print ' '

correct = 0
total = 0

for c in range(num_company):

    for d in range(test_size):

        test_matrix = [[0 for i in range(num_company)] for j in range(num_company)]
        for i in range(num_category):
            idx = train1_size + train2_size + d
            test_doc = all_resumes[c][idx][i]
            response = tfidfs[i].transform([test_doc])
            sim = cosine_similarity(response, tfidf_trains[i])
            score = sim[0]
            test_matrix[i] = score
            test_matrix = my_normalize(test_matrix)
        #print test_matrix

        final_score = []
        for j in range(num_company):
            s = 10000000.0
            for i in range(num_category):
                s = s * (0.1 + score_matrix[i][j]) * (0.1 + test_matrix[i][j])
            #  				s = s*(0.3+test_matrix[i][j])
            final_score.append(s)

        cur_max = -1
        max_index = 0
        for j in range(num_company):
            if final_score[j] > cur_max:
                cur_max = final_score[j]
                max_index = j

        total = total + 1
        if max_index == c:
            correct = correct + 1
# print ""
# print 'weighted categorical TF-IDF: ' + str(correct * 1.0 / total)