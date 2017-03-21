'''
Download Treebank Sample Dataset :
	>>nltk.download()
	Klik Tab Corpora -->treebank --> Download

Info lengkap tentang command terkait treebank : http://www.nltk.org/howto/corpus.html,
di bagian Parsed Corpora

Eksekusi perintah di bawah ini SATU PER SATU
'''

from nltk.corpus import treebank
from nltk import PCFG
from nltk import CFG
from nltk import Nonterminal
from nltk.parse import ViterbiParser
from nltk.grammar import induce_pcfg
from nltk import Tree
import sys, time


#Melihat list dokumen id yang ada pada dataset treebank
print(treebank.fileids())
len(treebank.fileids())

#Setiap file mengandung jumlah kalimat yang berbeda-beda
len(treebank.parsed_sents('wsj_0001.mrg'))
len(treebank.parsed_sents('wsj_0010.mrg'))

#Melihat token/word pada dokumen
print(treebank.words('wsj_0003.mrg'))

#Melihat parsed tree pada kalimat pertama (index 0) di dokumen wsj_0003
print(treebank.parsed_sents('wsj_0003.mrg')[0])

#Visualize treebank
treebank.parsed_sents('wsj_0003.mrg')[0].draw()

#treebank.parsed_sents() mengandung semua kalimat dari semua file
len(treebank.parsed_sents())
print(treebank.parsed_sents()[0])

#List grammar yang ada pada kalimat pertama
treebank.parsed_sents()[0].productions()


#Jika ingin bermain2 dengan PCFG, bisa membangun grammar pcfg dari text
#Cara untuk membangun grammar PCFG dari list production
toy_pcfg = PCFG.fromstring("""
    S -> NP VP [1.0]
    NP -> Det N [0.5] | NP PP [0.25] | 'John' [0.1] | 'I' [0.15]
    Det -> 'the' [0.8] | 'my' [0.2]
    N -> 'man' [0.5] | 'telescope' [0.5]
    VP -> VP PP [0.1] | V NP [0.7] | V [0.2]
    V -> 'ate' [0.35] | 'saw' [0.65]
    PP -> P NP [1.0]
    P -> 'with' [0.61] | 'under' [0.39]
    """)





#Split datase menjadi 97% data training dan 3% data testing
dataset_size = len(treebank.parsed_sents())
split_size = int(dataset_size * 0.97)
learning_set = treebank.parsed_sents()[:split_size]
test_set = treebank.parsed_sents()[split_size:]

#Test set saat ini masih merupakan parsed sentence (bentuk tree). 
#Untuk itu yang diperlukan adalah raw formatnya. Raw format ada di treebank.sents()
sents = treebank.sents()
raw_test_set = [sents[i] for i in range(split_size,dataset_size)]


#EXTRACTING THE GRAMMARS out of the learning_set
#Semua grammars yang ada pada learning_set akan disimpan pada tbank_productions
tbank_productions = []

for sent in learning_set:
	sent.collapse_unary()
	#Transform ke dalam bentuk CNF
	sent.chomsky_normal_form()
	for production in sent.productions():
		tbank_productions.append(production)


# supaya tidak ada permasalahan unknown token/word, kita tambahkan semua lexical(termasuk)
#yang di test_set
for word, tag in treebank.tagged_words():
	t = Tree.fromstring("("+ tag + " " + word  +")")
	for production in t.productions():
		tbank_productions.append(production)

print tbank_productions[2]

#Secara otomatis membangun grammar (terutama menghitung probability rule) 
#dari list production rule tbank_productions
tbank_grammar = induce_pcfg(Nonterminal('S'), tbank_productions)

print tbank_grammar

#PARSING
parser = ViterbiParser(tbank_grammar)
s = time.time()
#parsing untuk raw data latih kedua
for t in parser.parse(raw_test_set[1]):
	print(t)

#hitung waktu parsing
s = time.time()-s



#gold standard dari dataset kedua
print test_set[1]

'''Tugas anda adalah membangun fungsi untuk mengukur akurasi dari parser 
yang telah dibangun. Akurasi terdiri dari 2 macam, yaitu exact match, 
dan partial match (rata-rata recall dan precision). Cari sendiri bagaimana
menghitung recall dan precision untuk parsing dari referensi yang valid.

Setelah dibangun fungsi untuk menghitung 2 jenis akurasi tersebut, 
lakukan skenario di bawah ini :

1. Latih dengan data latih 100%, test dengan 10 data latih pertama, dan test dengan 10 data test pertama
2. Latih dengan data latih 70%, test dengan 10 data latih pertama, dan test dengan 10 data test pertama
3. Latih dengan data latih 50%, test dengan 10 data latih pertama, dan test dengan 10 data test pertama
4. Latih dengan data latih 10%, test dengan 10 data latih pertama, dan test dengan 10 data test pertama
5. Latih dengan data latih 100%, dan lakuka


PENTING !!!
Semua persentase di atas adalah dari total data latih yg 97% di awal. Jadi untuk yang 
100%, artinya semua data latih yang 97%. Untuk yang 50%, artinya 50% dari data latih 
yang 97% tersebut. Sisa data latih di diamkan saja, sementara data testingnya adalah tetap
yaitu yang 10 kalimat pertama dari 3% di awal.

Lakukan pengamatan terhadap hasil, dan berikan kesimpulan
'''