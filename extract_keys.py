import os
import re
import nltk
import datetime
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import seaborn as sns


class Extractor:
    def __init__(self, path=None):
        if path:
            self.feedbacks = pd.read_csv(path)
        else:
            self.feedbacks = pd.read_csv('static/data/feedbacks.csv')
        self.stop_words = set(stopwords.words("english"))
        
    def refresh(self,):
        self.feedbacks = pd.read_csv('static/data/feedbacks.csv')

    def set_city(self, city):
        self.city = city

    def get_wordnet_pos(self, word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN)

    def get_top_n_words(self, corpus, n=None):
        vec = CountVectorizer().fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in      
                        vec.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], 
                            reverse=True)
        return words_freq[:n]

    def get_top_n2_words(self, corpus, n=None):
        vec1 = CountVectorizer(ngram_range=(2,2),  
                max_features=2000).fit(corpus)
        bag_of_words = vec1.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in     
                        vec1.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
        return words_freq[:n]

    def get_top_n3_words(self, corpus, n=None):
        vec1 = CountVectorizer(ngram_range=(3,3), 
                max_features=2000).fit(corpus)
        bag_of_words = vec1.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in     
                        vec1.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
        return words_freq[:n]

    def get_top_n4_words(self, corpus, n=None):
        vec1 = CountVectorizer(ngram_range=(4,4), 
                max_features=2000).fit(corpus)
        bag_of_words = vec1.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in     
                        vec1.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], 
                    reverse=True)
        return words_freq[:n]

    def range_bound(self, type):
        end = datetime.date.today() + datetime.timedelta(days=1)
        if type=='month':
            start = end - datetime.timedelta(days=30)
        elif type=='week':
            start = end - datetime.timedelta(days=7)
        else:
            start = end - datetime.timedelta(days=1)

        subset = self.feedbacks.loc[(self.feedbacks.Date>=str(start)) & (self.feedbacks.Date<str(end))]
        return subset.reset_index(drop=True)

    def clean(self, datacol='content', typ='month'):
        dataset = self.range_bound(typ)
        corpus = []
        dataset['word_count'] = dataset[datacol].apply(lambda x: len(str(x).split(" ")))
        ds_count = len(dataset.word_count)
        for i in range(0, ds_count):
            # Remove punctuation
            text = re.sub('[^a-zA-Z]', ' ', str(dataset[datacol][i]))
    
            # Convert to lowercase
            text = text.lower()
    
            # Remove tags
            text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
    
            # Remove special characters and digits
            text=re.sub("(\\d|\\W)+"," ",text)
    
            # Convert to list from string
            text = text.split()
    
            # Lemmatisation
            lem = WordNetLemmatizer()

            text = [lem.lemmatize(word, self.get_wordnet_pos(word)) for word in text if not word in  
                    self.stop_words] 
            text = " ".join(text)
            corpus.append(text)

        return corpus

    # Convert most freq words to dataframe for plotting bar plot, save as CSV
    def single_imp(self, corpus, city=None):
        if city:
            self.set_city(city)
        top_words = self.get_top_n_words(corpus, n=20)
        top_df = pd.DataFrame(top_words)
        top_df.columns=["Keyword", "Frequency"]
        # Barplot of most freq words
        sns.set(rc={'figure.figsize':(13,8)})
        g = sns.barplot(x="Keyword", y="Frequency", data=top_df, palette="mako")
        g.set_xticklabels(g.get_xticklabels(), rotation=45)
        g.figure.savefig(os.path.join('static', 'img', self.city, 'feedbacks', "keywords.png"), bbox_inches = "tight")
        g.figure.clf()

        return top_df.values.tolist()


    def double_imp(self, corpus, city=None):
        if city:
            self.set_city(city)
        top2_words = self.get_top_n2_words(corpus, n=20)
        top2_df = pd.DataFrame(top2_words)
        top2_df.columns=["Bi-gram", "Frequency"]

        # Barplot of most freq Bi-grams
        sns.set(rc={'figure.figsize':(13,8)})
        h=sns.barplot(x="Bi-gram", y="Frequency", data=top2_df, palette="mako")
        h.set_xticklabels(h.get_xticklabels(), rotation=75)
        h.figure.savefig(os.path.join('static', 'img', self.city, 'feedbacks', "bi-gram.png"), bbox_inches = "tight")
        h.figure.clf()

        return top2_df.values.tolist()

    def triple_imp(self, corpus, city=None):
        if city:
            self.set_city(city)
        top3_words = self.get_top_n3_words(corpus, n=20)
        top3_df = pd.DataFrame(top3_words)
        top3_df.columns=["Tri-gram", "Frequency"]

        # Barplot of most freq Tri-grams
        sns.set(rc={'figure.figsize':(13,8)})
        j=sns.barplot(x="Tri-gram", y="Frequency", data=top3_df, palette="mako")
        j.set_xticklabels(j.get_xticklabels(), rotation=75)
        j.figure.savefig(os.path.join('static', 'img', self.city, 'feedbacks', "tri-gram.png"), bbox_inches = "tight")
        j.figure.clf()

        return top3_df.values.tolist()

    def four_imp(self, corpus, city=None):
        if city:
            self.set_city(city)
        top4_words = self.get_top_n4_words(corpus, n=20)
        top4_df = pd.DataFrame(top4_words)
        top4_df.columns=["Quad-gram", "Frequency"]

        # Barplot of most freq Quad-grams
        sns.set(rc={'figure.figsize':(13,8)})
        j=sns.barplot(x="Quad-gram", y="Frequency", data=top4_df, palette="mako")
        j.set_xticklabels(j.get_xticklabels(), rotation=75)
        j.figure.savefig(os.path.join('static', 'img', self.city, 'feedbacks', 'quad-gram.png'), bbox_inches = "tight")
        j.figure.clf()

        return top4_df.values.tolist()