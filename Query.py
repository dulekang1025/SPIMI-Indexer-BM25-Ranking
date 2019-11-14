import ast
import collections
import string
import json
from os import listdir
from BM25 import BM25
import nltk

class Query:
    """
    This class is to do the query part of spimi
    """
    index_path = '/Users/lekangdu/Downloads/40051703-A2/SPIMI-BM25/Index'
    index_files = []
    index = {}
    bm25_params = {}
    doc_num = 0
    doc_len = {}
    doc_avg_len = 0.0

    def __init__ (self):
        """
        open bm25_params.txt and get params of BM25
        """
        with open("/Users/lekangdu/Downloads/40051703-A2/SPIMI-BM25/DISK/bm25_params.txt") as f:
            self.bm25_params = json.load(f)
            self.doc_num = self.bm25_params["doc_num"]
            self.doc_len = self.bm25_params["doc_len"]
            self.doc_avg_len = int(self.bm25_params["doc_avg_len"])

    def readIndex(self):
        """
        This function is to read index
        """
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

    def read_index (self):
        """
        This function is to read index
        """
        files = listdir(self.index_path)
        for i in files:
            self.index_files.append(self.index_path + '/' + i)
        file_handles = [open(f) for f in self.index_files]
        for f in file_handles:
            block = json.load(f)
            for k, v in block.items():
                if not k in self.index:
                    self.index[k] = v
                else:
                    self.index[k].update(v)
    # ranking search
    def start_query_with_ranking(self):
        """
        This fucntion is to do the ranking search
        """
        bm25 = BM25()
        while True:
            rank_score = {}   # for the bm25 ranking score
            count = 0
            query = input("Input query: (/N to quit)")
            flag = ""
            terms = []
            if self.findWord(query) == "or":
                flag = "OR"  # Multiple keyword OR query
            elif self.findWord(query) == "and":
                flag = "AND"  # Multiple keyword AND query
            elif query == "/N":
                break
            else:
                flag = "NONE"  # Single keyword query
            # start search
            terms = self.getTerms_without_compression(query)
            pls = self.get_posting_list(terms)
            if flag == "NONE":
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
                    continue
                doc_freq = len(pls)
                res = {}
                t_list = pls.keys() # get the flatted pls list
                for doc_id in t_list:
                    for t in terms: # compute each term's tf
                        res[t] = []
                        if doc_id in self.index[t]:
                            tf = self.index[t][doc_id]
                        else:
                            tf = 0
                        res[t].append(tf) # {term : [tf, df, doc_id]}
                        res[t].append(doc_freq)
                        res[t].append(doc_id)
                    # compute bm25 score for this doc_id
                    rank_score[doc_id] = bm25.compute_score(res)
            elif flag == "OR":
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
                    continue
                res = {}
                t_list = []
                for t in terms: # get the flatted pls list
                    if t in self.index:
                        keys = self.index[t].keys()
                        for k in keys:
                            if not k in t_list:
                                t_list.append(k)
                doc_freq = len(t_list)

                for doc_id in t_list:
                    for t in terms: # compute each term's tf
                        if t in self.index:
                            res[t] = []
                            if doc_id in self.index[t]:
                                tf = self.index[t][doc_id]
                            else:
                                tf = 0
                            res[t].append(tf) # {term : [tf, df, doc_id]}
                            res[t].append(doc_freq)
                            res[t].append(doc_id)
                    # compute bm25 score for this doc_id
                    rank_score[doc_id] = bm25.compute_score(res)
                self.show_rank_doc(rank_score)
                rank_score = {}
            else:  # and
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
                    continue
                temp_list = []
                res = {}
                t_list = []
                for t in terms: # get the flatted pls list
                    keys = self.index[t].keys()
                    for k in keys:
                        if not k in temp_list:
                            temp_list.append(k)
                        else:
                            t_list.append(k)
                doc_freq = len(t_list)

                for doc_id in t_list:
                    for t in terms:  # compute each term's tf
                        res[t] = []
                        if doc_id in self.index[t]:
                            tf = self.index[t][doc_id]
                        else:
                            tf = 0
                        res[t].append(tf)  # {term : [tf, df, doc_id]}
                        res[t].append(doc_freq)
                        res[t].append(doc_id)
                    # compute bm25 score for this doc_id
                    rank_score[doc_id] = bm25.compute_score(res)
    # boolean retrivial, using compressed data
    def startQyery(self):
        """
        This fucntion is to do the boolean search
        """
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
                    print("No testing_results.")
                    continue
                for t in terms:
                    print(t + ":",end="")
                    print(sorted(self.index[t]))
            elif flag == "OR":
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
                    continue
                res = list(set.union(*map(set, pls)))
                print(sorted(res))

            else: # and
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
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
                        print("No intersection testing_results.")
                        continue

    # boolean retrivial, using un-compressed data
    def startQyeryWithOutCompression(self):
        """
        This fucntion is to do the boolean search
        using un-compressed data
        """
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
            terms = self.getTerms_without_compression(query)
            pls = self.getPostingList(terms)
            if flag == "NONE":
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
                    continue
                for t in terms:
                    print(t + ":",end="")
                    print(sorted(self.index[t]))
            elif flag == "OR":
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
                    continue
                res = list(set.union(*map(set, pls)))
                print(sorted(res))

            else: # and
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
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
                        print("No intersection testing_results.")
                        continue


    def findWord(self,query):
        """
        This function is to find "or" "and"
        :param query: query
        :return: keyword
        """
        temp = query.lower()
        if "or" in temp:
            return "or"
        elif "and" in temp:
            return "and"
        else:
            return "none"

    def getTerms(self,query):
        """
        This function is to get terms of a query
        :param query: query
        :return: list of terms
        """
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

    def getTerms_without_compression(self,query):
        """
        This function is to get terms of a query without compression
        :param query: query
        :return: list of terms
        """
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
        terms = [j for j in terms if not ':' in j]
        terms = [j for j in terms if not "''" in j]
        terms = [j for j in terms if not '&' in j]
        terms = [j for j in terms if not j.isdigit()]
        terms = [j for j in terms if not j in string.punctuation]
        stop_words = set(nltk.corpus.stopwords.words('english'))
        terms = [j for j in terms if not j in stop_words]
        # stemming
        stemmer = nltk.PorterStemmer()
        terms = [stemmer.stem(j) for j in terms]
        print(terms)
        return terms

    def getPostingList(self, terms):
        """
        This function is to get terms' posting list
        :param terms: list of terms
        :return: list of posting lists
        """
        res = [[]]
        for term in terms:
            if term in self.index:
                res.append(self.index[term])
        return res
    def get_posting_list(self, terms):
        """
        This function is to get terms' posting list
        :param terms: list of terms
        :return: list of posting lists
        """
        res = {}
        for term in terms:
            res.update(self.index[term])
        return res

    def intersection(self,l1,l2):
        """
        This fucntion is to do list intersection
        :param l1: posting list 1
        :param l2: posting list 2
        :return: intersection list
        """
        temp = set(l2)
        l = [v for v in l1 if v in temp]
        return l

    def show_rank_doc(self,res,matches,total_tf):
        """
        This fucntion is to show the ranking results
        :param res: result of ranking
        :param matches: dictionary of matches
        :param total_tf: dictionary of total tf
        """
        count = 0
        sorted_x = sorted(res.items(), key=lambda kv: kv[1], reverse=True)
        print("{:<8}  {:<8}  {:<8} {:<12} {:<8}".format("docID", "RSVd","Matches","Doc Length","total_tf"))
        for i in sorted_x:
            count += 1
            print("{:<8}  {:<8}  {:<8} {:<12} {:<8}".format(i[0], i[1],matches[i[0]],self.doc_len[i[0]],total_tf[i[0]]))

    def get_terms_for_ranking(self,query):
        """
        This function is to get terms of a query
        :param query: query
        :return: list of terms
        """
        temp = query.lower()
        terms = temp.split(" ")
        terms = [j for j in terms if not ':' in j]
        terms = [j for j in terms if not "''" in j]
        terms = [j for j in terms if not '&' in j]
        terms = [j for j in terms if not j.isdigit()]
        terms = [j for j in terms if not j in string.punctuation]
        stop_words = set(nltk.corpus.stopwords.words('english'))
        terms = [j for j in terms if not j in stop_words]

        # stemming
        # stemmer = nltk.PorterStemmer()
        # terms = [stemmer.stem(j) for j in terms]

        # lemmatizer
        lemmatizer = nltk.stem.WordNetLemmatizer()
        terms = [lemmatizer.lemmatize(j) for j in terms]

        terms = [j for j in terms if j in self.index]
        print(terms)
        return terms

    def ranking_query(self):
        """
        This fucntion is to do the BM25 ranking search
        """
        bm25 = BM25()
        while True:
            rank_score = {}  # for the bm25 ranking score
            count = 0
            query = input("Input query: (/N to quit)")
            # start search
            terms = self.get_terms_for_ranking(query)
            pls = self.get_posting_list(terms)
            if len(terms) == 1:
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
                    continue
                doc_freq = len(pls)
                res = {}
                t_list = pls.keys() # get the flatted pls list
                for doc_id in t_list:
                    for t in terms: # compute each term's tf
                        res[t] = []
                        if doc_id in self.index[t]:
                            tf = self.index[t][doc_id]
                        else:
                            tf = 0
                        res[t].append(tf) # {term : [tf, df, doc_id]}
                        res[t].append(doc_freq)
                        res[t].append(doc_id)
                        print("~~ "+str(tf) +" "+ str(doc_freq) +" "+ str(doc_id))
                    # compute bm25 score for this doc_id
                    rank_score[doc_id] = bm25.compute_score(res)
                self.show_rank_doc(rank_score)
                rank_score = {}
            else:
                for t in pls:
                    if len(t) != 0:
                        count += 1
                if count == 0:
                    print("No testing_results.")
                    continue
                res = {}
                t_list = []
                for t in terms: # get the flatted pls list
                    if t in self.index:
                        keys = self.index[t].keys()
                        for k in keys:
                            if not k in t_list:
                                t_list.append(k)
                doc_freq = len(t_list)
                matches = {}
                total_tf = {}
                for doc_id in t_list:
                    matches[doc_id] = 0
                    total_tf[doc_id] = 0
                    for t in terms: # compute each term's tf
                        if t in self.index:
                            res[t] = []
                            if doc_id in self.index[t]:
                                tf = self.index[t][doc_id]
                                matches[doc_id] += 1
                                total_tf[doc_id] += tf
                            else:
                                tf = 0
                            res[t].append(tf) # {term : [tf, df, doc_id]}
                            res[t].append(doc_freq)
                            res[t].append(doc_id)
                    # compute bm25 score for this doc_id
                    rank_score[doc_id] = bm25.compute_score(res)

                self.show_rank_doc(rank_score,matches,total_tf)
                rank_score = {}



