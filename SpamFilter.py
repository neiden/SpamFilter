import os
import math

word_dict = {}
spam_word_count = {}
ham_word_count = {}
class_dict_temp = {}
class_dict = {}
spam_words = {}
ham_words = {}
    
def train_data():
    rootdir = 'spam-train'

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            text = open(os.path.join(subdir, file))
            for line in text:
                words = line.split()
                for word in words:
                    if word not in word_dict:
                        class_dict_temp[word] = 'H'
                        spam_word_count[word] = 0
                        word_dict[word] = 0
                    word_dict[word] += 1
                    spam_word_count[word] += 1


    rootdir = 'nonspam-train'

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            text = open(os.path.join(subdir, file))
            for line in text:
                words = line.split()
                for word in words:
                    if word not in word_dict:
                        class_dict_temp[word] = 'H'
                        word_dict[word] = 0
                    if word not in ham_word_count:
                        ham_word_count[word] = 0
                    word_dict[word] += 1
                    ham_word_count[word] += 1

    temp_dict = word_dict.copy()
    temp_dict = sorted(temp_dict.items(), key=lambda i: i[1],reverse=True)
    temp_dict = temp_dict[:2500]

    temp_spam_dict = spam_word_count.copy()
    temp_spam_dict = sorted(temp_spam_dict.items(), key=lambda i: i[1],reverse=True)
    temp_spam_dict = temp_spam_dict[:2500]

    temp_ham_dict = ham_word_count.copy()
    temp_ham_dict = sorted(temp_ham_dict.items(), key=lambda i: i[1],reverse=True)
    temp_ham_dict = temp_ham_dict[:2500]

    for pair in temp_dict:
        class_dict[pair[0]] = class_dict_temp[pair[0]]
    for pair in temp_spam_dict:
        spam_words[pair[0]]  = spam_word_count[pair[0]]
    for pair in temp_ham_dict:
        ham_words[pair[0]] = ham_word_count[pair[0]]


    print(class_dict)

    print(spam_words)

    print(ham_words)





def test_data():
    rootdir = 'nonspam-test'

    ham_test_prediction = {}
    test_range = 2500
    contigency = {}
    contigency["TP"] = 0
    contigency["FP"] = 0
    contigency["FN"] = 0
    contigency["TN"] = 0

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            email = open(os.path.join(subdir, file))
            for line in email:
                words = line.split()
                ham_prob = 0
                spam_prob = 0
                for word in words:
                    if word in ham_words:
                        ham_prob += math.log2(ham_word_count[word] / test_range)
                    if word in spam_words:
                        spam_prob += math.log2(spam_word_count[word] / test_range)
                spam_prob *= .5
                ham_prob *= .5
                spam_prob = abs(spam_prob)
                ham_prob = abs(ham_prob)
                #print("spam prob: ", spam_prob , "\tham prob: " , nonspam_prob)
                if spam_prob > ham_prob:
                    ham_test_prediction[os.path.join(subdir, file)] = "S"
                else:
                    ham_test_prediction[os.path.join(subdir, file)] = "H"
            if ham_test_prediction[os.path.join(subdir, file)] == "S":
                contigency['FN'] += 1
            else:
                contigency['TN'] += 1

    print(ham_test_prediction)

    rootdir = 'spam-test'

    spam_test_prediction = {}


    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            email = open(os.path.join(subdir, file))
            for line in email:
                words = line.split()
                ham_prob = 0
                spam_prob = 0
                for word in words:
                    if word in ham_words:
                        ham_prob += math.log2(ham_word_count[word] / test_range)
                    if word in spam_words:
                        spam_prob += math.log2(spam_word_count[word] / test_range)
                spam_prob *= .5
                ham_prob *= .5
                spam_prob = abs(spam_prob)
                ham_prob = abs(ham_prob)
                #print("spam prob: ", spam_prob, "\tham prob: ", ham_prob)
                if spam_prob > ham_prob:
                    spam_test_prediction[os.path.join(subdir, file)] = "S"
                else:
                    spam_test_prediction[os.path.join(subdir, file)] = "H"
            if spam_test_prediction[os.path.join(subdir, file)] == "S":
                contigency['TP'] += 1
            else:
                contigency['FP'] += 1

    precision = contigency["TP"]/(contigency["TP"]+contigency["FP"])
    recall    = contigency["TP"]/(contigency["TP"]+contigency["FN"])
    F         = (2*precision*recall)/(precision + recall)
    print(spam_test_prediction)
    print(contigency)
    print(precision)
    print(recall)
    print(F)



train_data()
test_data()