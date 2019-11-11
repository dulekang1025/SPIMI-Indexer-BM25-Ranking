import math
import json
class BM25:
    bm25_params = {}
    doc_num = 0
    doc_len = {}
    doc_avg_len = 0.0
    k = 1.2
    b = 0.75
    def __init__(self):
        with open("/Users/lekangdu/Desktop/SPIMI/DISK/bm25_params.txt") as f:
            self.bm25_params = json.load(f)
            self.doc_num = self.bm25_params["doc_num"]
            self.doc_len = self.bm25_params["doc_len"]
            self.doc_avg_len = self.bm25_params["doc_avg_len"]

            print("1, " + str(self.doc_num))
            print("2, " + str(self.doc_len))
            print("3, " + str(self.doc_avg_len))
    def compute_score(self,res):
        score = 0
        for k,v in res.items():
            tf = v[0]
            df = v[1]
            doc_id = v[2]
        #     print(k,end="")
        #     print(" - ",end="")
        #     print(str(v[0]) + " " + str(v[1]) + " " +str(v[2]))
# bm25_score += (math.log(num_documents / doc_freq))*(((k1 + 1) * term_freq) / (k1 * ((1-b) + b * (doc_len[doc_id] / avg_len)) + term_freq))
            idf = math.log(self.doc_num / df)
            upper = (self.k + 1) * tf
            bottom = k * ((1 - self.b) + self.b * (self.doc_len[doc_id] / self.doc_avg_len)) + tf
            score += idf * (upper / bottom)
        return score

        # print()