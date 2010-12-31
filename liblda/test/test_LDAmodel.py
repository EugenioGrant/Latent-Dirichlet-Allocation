
import os, sys
from gensim import corpora
from liblda.low2corpus import Low2Corpus

# assume it has been done -- so i can do interactive
#from liblda.LDAmodel import LdaModel


"Setup for debugging and testing"

testdir = os.path.realpath(os.path.join(os.path.dirname(__file__)))
print "Working in testdir " + testdir


# SETUP TEST CORPORA
# #######WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

# a simple corpus with 9 docs and 29 words
tcorpus = corpora.MmCorpus(os.path.join(testdir, "test_corpus.mm") )

# a fatter corpus with 19M nnz, 1M vocabulary and 6M super-short docs
INFILE="ukwac-uniqmultiwordterms.SAMPLE.txt"        # 6M docs, one doc per line
VOCABFILE="ukwac-vocabulary.SAMPLE.txt"             # 1M vocab (unique words in INFILE)
infilename = os.path.join(testdir, INFILE)
vfilename =  os.path.join(testdir, VOCABFILE)

tcorpus2 = Low2Corpus(infilename)
tcorpus2.buildVocabs(vfilename)


print "#"*60
print "Now you should import LdaModel from liblda.LDAmodel as "
print "from liblda.LDAmodel import LdaModel"
print "lda = LdaModel( numT=3, corpus=tcorpus) "

print "Currently loaded to test corpora: "
print "   1. tcorpus  "
print tcorpus
print "   2. tcorpus2 "
print tcorpus2

print "shoudl always run"
print "    reload(liblda.LDAmodel); from liblda.LDAmodel import LdaModel; lda = LdaModel( numT=3, corpus=...)"
print "every time you change the code"



import operator

def show_top(phi, num=20, corpus=None):

    numT,numTerms = phi.shape

    topics = []

    for t in range(numT):

        pw_gt = phi[t,:]
        topwords = sorted(enumerate(pw_gt), key=operator.itemgetter(1), reverse=True)
        words = [corpus.id2word[id] for id,prb in topwords[0:num] ]
        topics.append(words)

    return topics

