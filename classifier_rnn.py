import os

import numpy as np
import torch
import MeCab

from gensim.models import word2vec

from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

class NarouRNN:
    def __init__(self):
        # self.rubyFile = "ruby.txt"
        self.rubyFile = "rdup.txt"
        self.middleFile = "middle.txt"
        self.words, self.ruby = Narou.load(self.rubyFile)
        self.m = MeCab.Tagger("-Ochasen")

        # self.wv_model = Narou.char2vec(self.words, self.middleFile)
        self.wv_model = Narou.word2vec(self.words, self.middleFile, self.m)

        self.middleWords = Narou.loadMiddle(self.middleFile)
        self.X_train = np.array([np.sum([self.wv_model[word] for word in words], axis=0) for words in self.middleWords])
        self.Y_train = np.array(self.ruby)

        self.model = self.fit()

    def loadMiddle(middleFile):
        middleWords = []
        with open(middleFile) as f:
            for sentences in f.read().split("\n"):
                middleWords.append([])
                for word in sentences.split(" "):
                    if word != '':
                        middleWords[-1].append(word)

        middleWords = filter(lambda x:x != [], middleWords)
        return middleWords

    def load(rubyFile):
        words = None
        ruby = None
        with open(rubyFile) as f:
            data = f.read().split("\n")[0:-2]
            word = [d.split(":")[0] for d in data]
            ruby = [d.split(":")[1] for d in data]
        return word, ruby


    def char2vec(words, middleFile):
        with open(middleFile, "w") as f:
            for w in words:
                print(" ".join(list(w)), file=f)

        sentences = word2vec.LineSentence(middleFile)
        return word2vec.Word2Vec(sentences,sg=1,size=30,min_count=1,window=2,hs=1,negative=0)

    def word2vec(sentences, middleFile, m):
        # m = MeCab.Tagger("-Ochasen")
        with open(middleFile, "w") as f:
            for sentence in sentences:
                for word in m.parse(sentence).split("\n"):
                    w = word.split("\t")[0]
                    if w != 'EOS' and w != '':
                        print(w, end=' ', file=f)
                print(file=f)

        sentences = word2vec.LineSentence(middleFile)
        return word2vec.Word2Vec(sentences,sg=1,size=30,min_count=1,window=2,hs=1,negative=0)

    def fit(self):
        # model = SVC()
        model = KNeighborsClassifier(1)
        # model = LDA()
        # print("fitting")
        model.fit(self.X_train, self.Y_train)
        # print("fitted")

        return model

    def classification(self, sentences):
        print(sentences)

        X_test = np.zeros((len(sentences), self.X_train.shape[1]))
        for i,words in enumerate(sentences):
            for mwords in self.m.parse(words).split("\n"):
                word = mwords.split("\t")[0]
                if word != 'EOS' and word != '':
                    X_test[i] += self.wv_model[word]

        pred = self.model.predict(X_test)
        print(pred)


if __name__ == '__main__':
    n = NarouRNN()
    n.classification(["暗黒", "暗黒物質", "地球", "回復", "友達", "戦乙女"])
