from nltk.corpus import treebank
from nltk import Nonterminal
from nltk.parse import ViterbiParser
from nltk.grammar import induce_pcfg
from nltk import Tree

dataset_size = len(treebank.parsed_sents())
split_size = int(dataset_size * 0.97)
# learning_set = treebank.parsed_sents()[:split_size]  #100%
# learning_set = treebank.parsed_sents()[:int(split_size*0.7)] #70%
# learning_set = treebank.parsed_sents()[:int(split_size*0.5)] #50%
learning_set = treebank.parsed_sents()[:int(split_size*0.1)] #10%
test_set = treebank.parsed_sents()[split_size:]
print("Dataset Size : " + str(dataset_size))
print("Learning Set : " + str(len(learning_set)) + " of " + str(split_size))
print("Test Set     : " + str(len(test_set)))

sents = treebank.sents()
raw_test_set = [sents[i] for i in range(split_size, dataset_size)]
raw_train_set = [sents[i] for i in range(0, split_size)]

tbank_productions = []

for sent in learning_set:
    sent.collapse_unary()
    # Transform ke dalam bentuk CNF
    sent.chomsky_normal_form()
    for production in sent.productions():
        tbank_productions.append(production)

for word, tag in treebank.tagged_words():
    t = Tree.fromstring("(" + tag + " " + word + ")")
    for production in t.productions():
        tbank_productions.append(production)

tbank_grammar = induce_pcfg(Nonterminal('S'), tbank_productions)

parser = ViterbiParser(tbank_grammar)

def ExactMatch():
    sama_train = 0
    sama_test = 0
    # test dengan 10 data latih pertama
    for index in range(0, 10):
        if parser.parse(raw_train_set[index]) == learning_set[index]:
            sama_train += 1
    # test dengan 10 data test pertama
    for index in range(0, 10):
        if parser.parse(raw_test_set[index]) == test_set[index]:
            sama_test += 1
    return sama_train, sama_test

e_train, e_test = ExactMatch()
print("Exact match untuk 10 data train pertama = " + str(e_train))
print("Exact match untuk 10 data test pertama = " + str(e_test))

def Precision(sama_train,sama_test):
    prec_train = sama_train/len(raw_train_set)
    prec_test = sama_test/len(raw_test_set)
    return prec_train,prec_test

p_train,p_test = Precision(e_train,e_test)
print("Precision untuk data train = " + str(p_train) + "% dan untuk data test = "+ str(p_test) + "%")

def Recall(sama_train,sama_test):
    rec_train = sama_train/len(learning_set)
    rec_test = sama_test/len(test_set)
    return rec_train,rec_test

r_train,r_test = Recall(e_train,e_test)
print("Recall untuk data train = " + str(r_train) + "% dan untuk data test = "+ str(r_test) + "%")

# def Precision_Train(cek):
#     sama_train = 0.0
#     jumlah = 0.0
#     for i in parser.parse(raw_train_set[cek]):
#         for j in learning_set[cek]:
#             if i==j:
#                 sama_train += 1
#         jumlah += 1
#     return "Presicion untuk data training ke-" + str(cek) + " = " + str(sama_train / jumlah)
#
# def Precision_Test(cek):
#     sama_test = 0.0
#     jumlah = 0.0
#     for i in parser.parse(raw_test_set[cek]):
#         for j in test_set[cek]:
#             if i==j:
#                 sama_test += 1
#         jumlah += 1
#     return "Presicion untuk data testing ke-" + str(cek) + " = " + str(sama_test / jumlah)
#
# def Recall_Train(cek):
#     sama_train = 0.0
#     jumlah = 0.0
#     for i in learning_set[cek]:
#         for j in parser.parse(raw_train_set[cek]):
#             if i==j:
#                 sama_train += 1
#         jumlah += 1
#     return "Recall untuk data training ke-" + str(cek) + " = " + str(sama_train / jumlah)
#
# def Recall_Test(cek):
#     sama_test = 0.0
#     jumlah = 0.0
#     for i in test_set[cek]:
#         for j in parser.parse(raw_test_set[cek]):
#             if i==j:
#                 sama_test += 1
#         jumlah += 1
#     return "Recall untuk data testing ke-" + str(cek) + " = " + str(sama_test / jumlah)
#
# for cek in range(0, 10):
#     print Precision_Train(cek)
#     print Recall_Train(cek)
#
# for cek in range(0,10):
#     print Precision_Test(cek)
#     print Recall_Test(cek)