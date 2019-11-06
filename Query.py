import ast
import collections
from itertools import chain

from os import listdir

import nltk


class Query:
    index_path = '/Users/lekangdu/Desktop/SPIMI/Index/'
    index_files = []
    index = {}
    def readIndex(self):
        spimi_index = collections.OrderedDict()
        files = listdir(self.index_path)
        for i in files:
            self.index_files.append(self.index_path + '/' + i)
        file_handles = [open(f) for f in self.index_files]
        for f in file_handles:
            line = f.readline()
            while line != '':
                term = line.split(':')[0]
                pl = line.split(':')[1]
                posting_list = ast.literal_eval(pl)
                if term not in self.index:
                    self.index[term] = posting_list
                else:
                    self.index[term].extend(posting_list)
                line = f.readline()

    def startQyery(self):
        while True:
            count = 0
            query = input("Input query: (/N to quit)")
            flag = ""
            terms = []
            if self.findWord(query) == "or":
                flag = "OR"        # Multiple keyword OR query
            elif self.findWord(query) == "and":
                flag = "AND"       # Multiple keyword AND query
            elif query == "/N":
                break
            else:
                flag = "NONE"      # Single keyword query

        #     processing query

        #     get posting list
            terms = self.getTerms(query)
            pls = self.getPostingList(terms)
            if flag == "NONE":
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No result.")
                    continue
                for t in terms:
                    print(t + ":",end="")
                    print(sorted(self.index[t]))
            elif flag == "OR":
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No result.")
                    continue
                res = list(set.union(*map(set, pls)))
                print(sorted(res))

            else: # and
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No result.")
                    continue
                res = []
                temp = []
                new_pls = []
                for i in pls:
                    if i != []:
                        new_pls.append(i)
                for i in pls:
                    temp = i
                for i in new_pls:
                    temp = set(i).intersection(temp)
                res = temp
                print(sorted(res))
                if len(res) == 0:
                        print("No intersection result.")
                        continue


    def findWord(self,query):
        temp = query.lower()
        if "or" in temp:
            return "or"
        elif "and" in temp:
            return "and"
        else:
            return "none"

    def getTerms(self,query):
        temp = query.lower()
        terms = []
        if "or" in temp:
            temp_terms = temp.split(" or ")
            terms = temp_terms
        elif "and" in temp:
            temp_terms = temp.split(" and ")
            terms = temp_terms
        else:
            terms.append(query)
        # stemming
        stemmer = nltk.PorterStemmer()
        terms = [stemmer.stem(j) for j in terms]
        print(terms)
        return terms

    def getPostingList(self, terms):
        res = [[]]
        for term in terms:
            if term in self.index:
                res.append(self.index[term])
        return res

    def intersection(self,l1,l2):
        temp = set(l2)
        l = [v for v in l1 if v in temp]
        return l

