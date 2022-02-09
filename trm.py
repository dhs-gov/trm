from sentence_transformers import SentenceTransformer, util
import numpy as np
from sklearn.model_selection import learning_curve
from util import xlsx_util
from operator import itemgetter

# Gensim doesn't work because software apps not contained in keyed vectors)
#from gensim.models import KeyedVectors
#from sklearn.metrics.pairwise import cosine_similarity

import spacy
from nltk.corpus import wordnet


class TRM():

    normalized_names_versions = []
    input_names_versions = []
    model = None
    word_vectors = None
    nlp = None

    def __init__(self):
        # Read user configuration
        print(f"init")
        # For Transformers (use multiple models)
        #self.model = SentenceTransformer('all-mpnet-base-v2')
        # Works well!
        #self.model = SentenceTransformer('sentence-transformers/multi-qa-MiniLM-L6-cos-v1')
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        

        # SpaCy
        self.nlp = spacy.load("en_core_web_lg")


    def read_normalized(self, file):
        # Read normalized TRM name and version columns
        print(f'read_normalized')
        self.normalized_names_versions = xlsx_util.get_data(file)
        print(f'Normalized: {self.normalized_names_versions}')

    def read_input(self, file):
        # Read XLSX file of input name and version columns
        print(f'read_input')
        self.input_names_versions = xlsx_util.get_data(file)
        print(f'Input: {self.input_names_versions}')

    def assess_transformer1(self):
        # From https://towardsdatascience.com/semantic-similarity-using-transformers-8f3cb5bf66d6

        for x in self.input_names_versions:
            results = []
            input_name = x[0]
            for y in self.normalized_names_versions:
                norm_name = y[0]
                embedding1 = self.model.encode(input_name, convert_to_tensor=True)
                embedding2 = self.model.encode(norm_name, convert_to_tensor=True)
                
                cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)

                result = [input_name, norm_name, cosine_scores.item()]
                results.append(result)
            # Sort results on descending cosign score
            results = sorted(results, key=itemgetter(2), reverse=True)

            print(f"--- Results for '{input_name}':")
            for z in results:
                print(z)


    def assess_spacy(self):
       for x in self.input_names_versions:
            results = []
            input_name = x[0]
            for y in self.normalized_names_versions:
                norm_name = y[0]
                input_name_tokens = self.nlp(input_name)
                norm_name_tokens = self.nlp(norm_name)
                print(f'input: {input_name}, norm: {norm_name}')
                sim = input_name_tokens.similarity(norm_name_tokens)
                result = [input_name, norm_name, sim]
                results.append(result)
            # Sort results on descending cosign score
            results = sorted(results, key=itemgetter(2), reverse=True)

            print(f"--- Results for '{input_name}':")
            for z in results:
                print(z)


    def assess_nltk(self):

        from itertools import product
        sims = []

        for word1, word2 in product(self.input_names_versions, self.normalized_names_versions):
            syns1 = wordnet.synsets(word1)
            syns2 = wordnet.synsets(word2)
            for sense1, sense2 in product(syns1, syns2):
                d = wordnet.wup_similarity(sense1, sense2)
                sims.append((d, syns1, syns2))

        allsyns1 = set(ss for word in self.input_names_versions for ss in wordnet.synsets(word))
        allsyns2 = set(ss for word in self.normalized_names_versions for ss in wordnet.synsets(word))
        best = max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in 
        product(allsyns1, allsyns2))
        print(best)
#(0.9411764705882353, Synset('command.v.02'), Synset('order.v.01'))


        for x in self.input_names_versions:
            results = []
            input_name = x[0]
            for y in self.normalized_names_versions:
                norm_name = y[0]
                syns1 = wordnet.synsets(input_name)
                syns2 = wordnet.synsets(norm_name)
                norm_name_tokens = self.nlp(norm_name)
                print(f'input: {syns1}, norm: {syns2}')
                d = syns1.wup_similarity(syns2)
                result = [input_name, norm_name, d]
                results.append(result)
            # Sort results on descending cosign score
            results = sorted(results, key=itemgetter(2), reverse=True)

            print(f"--- Results for '{input_name}':")
            for z in results:
                print(z)




