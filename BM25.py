import math
import json
class BM25:
    """
    This class is to do the BM25 score for a document
    """
    bm25_params = {}
    doc_num = 0
    doc_len = {}
    doc_avg_len = 0.0
    k1 = 1.2
    b = 0.75
    def __init__(self):
        """
        open bm25_params.txt and get params of BM25
        """
        with open("/Users/lekangdu/Downloads/40051703-A2/SPIMI-BM25/DISK/bm25_params.txt") as f:
            self.bm25_params = json.load(f)
            self.doc_num = self.bm25_params["doc_num"]
            self.doc_len = self.bm25_params["doc_len"]
            self.doc_avg_len = int(self.bm25_params["doc_avg_len"])

            print("1, " + str(self.doc_num))
            print("2, " + str(self.doc_len))
            print("3, " + str(self.doc_avg_len))
    def compute_score(self,res):
        """
        This fucntion is to compute the BM25 score
        :param res: A document's all params to compute the BM25 score
        :return: BM25 score of current document
        """
        score = 0
        for k,v in res.items():
            tf = v[0]
            df = v[1]
            doc_id = v[2]
            idf = float(math.log(self.doc_num / df))
            upper = (self.k1 + 1) * tf
            bottom = self.k1 * ((1 - self.b) + self.b * (self.doc_len[doc_id] / self.doc_avg_len)) + tf
            score += idf * (upper / bottom)
        return round(score,3)
