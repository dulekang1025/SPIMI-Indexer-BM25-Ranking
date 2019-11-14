from os import listdir
import string
import nltk
import json
from collections import OrderedDict
nltk.download('punkt')
nltk.download('stopwords')


class Spimi_Inverter:
    """
    This class is to do the invert part of spimi
    """

    Src_Files_Path = '/Users/lekangdu/Downloads/40051703-A2/SPIMI-BM25/documents'
    Src_Files = []
    BlockSize = 500
    BlockFilesNumber = 0
    Dictionary = {}
    PostingList = {}
    Sorted_PostingList = {}
    doc_length = {}
    corpus_total_length = 0
    Count_doc = 0

    def GetAllFiles(self):
        """
        This fucntion is to get all the src files
        """
        files = listdir(self.Src_Files_Path)
        for file in files:
            if str(file).find("reut2") != -1:
                self.Src_Files.append(file)
                # print(str(file))

    def SplitIntoDoc(self):
        """
        This function is to inverting the document
        :return:
        """
        Doc_begin = False
        Body_begin = False
        Title_begin = False
        count_test = 0

        for file in self.Src_Files:
            with open(self.Src_Files_Path +'/'+ str(file), errors='ignore') as f:
                body = ""
                docID = ""
                for line in f:
                    if Doc_begin and Body_begin:
                        if line.find("</BODY>") == -1:
                            body += line
                        else:
                            self.Dictionary[docID] = body
                            docID = 0
                            body = ""
                            Body_begin = False
                        if line.find("</REUTERS") != -1:
                            Doc_begin = False
                    else:
                        p = line.find("<REUTERS")
                        if p != -1:
                            Doc_begin = True
                            # get newID
                            q = line.find("NEWID")
                            if(q != -1):
                                self.Count_doc += 1
                                temp = int(line[q + 7: len(line) - 3])
                            docID = temp
                        # find <TITLE>
                        if line.find("<TITLE>") != -1:
                            begin_pos = line.find("<TITLE>") + 7
                            end_pos = len(line) - 1
                            if line.find("</TITLE>") != -1:
                                end_pos = line.find("</TITLE>")
                                title = line[begin_pos : end_pos]
                                body += title
                        # find <BODY>
                        if line.find("<BODY>") != -1:
                            Body_begin = True
                            body += line[line.find("<BODY>") + 6: len(line) - 1] + '\n'
                        else:
                            continue
        print(self.Count_doc)
        print(len(self.Dictionary))
    # Tokenize, stemming and remove Stopwords
    def processDocumentWithCompression(self):
        """
        This fucntion is to process Document With Compression
        """
        counter = 0
        no = 0
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for docID in self.Dictionary:
            counter += 1
            no += 1
            # token
            tokens = nltk.word_tokenize(self.Dictionary[docID])
            # lower case
            tokens = [j.lower() for j in tokens]
            # print(tokens)
            # stop words
            tokens = [j for j in tokens if not j in stop_words]
            # Stupid method.... Will change it later...
            tokens = [j for j in tokens if not j in [',','+','-','.','?','!','\'\'','\'','$','^','~',':',';','"'
                                                     '{','}','&','(',')','@','*','>','<','#',"''",'``','...','..'
                                                     ,'[',']','|','','=','_','%']]
            tokens = [j for j in tokens if not j in ['1','2','3','4','5','6','7','8','9','0']]
            tokens = [j for j in tokens if not '1' in j]
            tokens = [j for j in tokens if not '2' in j]
            tokens = [j for j in tokens if not '3' in j]
            tokens = [j for j in tokens if not '4' in j]
            tokens = [j for j in tokens if not '5' in j]
            tokens = [j for j in tokens if not '6' in j]
            tokens = [j for j in tokens if not '7' in j]
            tokens = [j for j in tokens if not '8' in j]
            tokens = [j for j in tokens if not '9' in j]
            tokens = [j for j in tokens if not '0' in j]
            # tokens = [j for j in tokens if not '-' in j]
            tokens = [j for j in tokens if not '.' in j]
            tokens = [j for j in tokens if not 'th' in j]
            tokens = [j for j in tokens if not '..' in j]
            tokens = [j for j in tokens if not '+' in j]
            tokens = [j for j in tokens if not '\'' in j]
            tokens = [j for j in tokens if not '/' in j]
            tokens = [j for j in tokens if not ',' in j]
            tokens = [j for j in tokens if not '&' in j]
            tokens = [j for j in tokens if not '*' in j]
            tokens = [j for j in tokens if not '^' in j]
            tokens = [j for j in tokens if not '%' in j]
            tokens = [j for j in tokens if not '&' in j]
            tokens = [j for j in tokens if not '@' in j]
            tokens = [j for j in tokens if not '#' in j]
            tokens = [j for j in tokens if not '{' in j]
            tokens = [j for j in tokens if not '}' in j]

            # numbers
            tokens = [j for j in tokens if not j.isdigit()]
            tokens = [j for j in tokens if not j.isnumeric()]
            tokens = [j for j in tokens if not self.isFloat(j)]

            # stemming
            stemmer = nltk.PorterStemmer()
            tokens = [stemmer.stem(j) for j in tokens]



            # ------------------------------------------------------------
            tokens = [j for j in tokens if not j in [',', '+', '.', '?', '!', '\'\'', '\'', '-', '$', '^', '~', ':', ';', '"'
                              '{', '}', '&','(', ')', '@', '*', '>', '<', '#', "''", '``', '...', '..'
                          , '[', ']', '|', '', '=', '_', '%']]
            tokens = [j for j in tokens if not '.' in j]
            tokens = [j for j in tokens if not 'th' in j]
            tokens = [j for j in tokens if not '..' in j]
            tokens = [j for j in tokens if not '+' in j]
            tokens = [j for j in tokens if not '\'' in j]
            tokens = [j for j in tokens if not '/' in j]
            tokens = [j for j in tokens if not ',' in j]
            tokens = [j for j in tokens if not '&' in j]
            tokens = [j for j in tokens if not '*' in j]
            tokens = [j for j in tokens if not '^' in j]
            tokens = [j for j in tokens if not '%' in j]
            tokens = [j for j in tokens if not '&' in j]
            tokens = [j for j in tokens if not '@' in j]
            tokens = [j for j in tokens if not '#' in j]
            tokens = [j for j in tokens if not '{' in j]
            tokens = [j for j in tokens if not '}' in j]

            # create posting list
            for token in tokens:
                self.createPostingList(token,docID)

            # write to blocks

            if counter >= 500 or no == len(self.Dictionary) - 1:
                self.Sorted_PostingList = sorted(self.PostingList)
                self.writeToBlock()
                self.PostingList.clear()
                self.Sorted_PostingList.clear()
                counter = 0

    def processWithoutCompression(self):
        """
        This fucntion is to process Document Without Compression
        """
        counter = 0
        no = 0
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for docID in self.Dictionary:
            counter += 1
            no += 1
            # token
            tokens = nltk.word_tokenize(self.Dictionary[docID])
            tokens = [j for j in tokens if not ':' in j]
            tokens = [j for j in tokens if not j in string.punctuation]
            tokens = [j for j in tokens if not '&' in j]
            tokens = [j for j in tokens if not "''" in j]

            # add doc_length
            self.doc_length[docID] = len(tokens)
            self.corpus_total_length += len(tokens)

            tokens = [j for j in tokens if not j.isdigit()]
            tokens = [j.lower() for j in tokens]
            stop_words = set(nltk.corpus.stopwords.words('english'))
            tokens = [j for j in tokens if not j in stop_words]

            # stemming
            # stemmer = nltk.PorterStemmer()
            # tokens = [stemmer.stem(j) for j in tokens]

            # lemmatizer
            lemmatizer = nltk.stem.WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(j) for j in tokens]


            # create posting list
            for token in tokens:
                self.createPostingList(token, docID)

            # write to blocks

            if counter >= 500 or no == len(self.Dictionary) - 1:
                self.Sorted_PostingList = sorted(self.PostingList)
                self.writeToBlock()
                self.PostingList.clear()
                self.Sorted_PostingList.clear()
                counter = 0

        # write doc_number, doc_len, doc_avg_len into file
        self.wrtie_bm25_params()

    # write doc_number, doc_len, doc_avg_len into file
    def wrtie_bm25_params(self):
        """
        This function is to save BM25 parameters
        """
        total = {}
        total["doc_num"] = self.Count_doc
        total["doc_len"] = self.doc_length
        doc_avg_len = self.corpus_total_length / self.Count_doc
        total["doc_avg_len"] = doc_avg_len

        with open('/Users/lekangdu/Downloads/40051703-A2/SPIMI-BM25/DISK/bm25_params.txt', 'w') as f:
            json.dump(total,f)



    # create posting list
    def createPostingList(self,token,docID):
        """
        This fucntion is to create Posting List
        :param token: list of tokens
        :param docID: doc id
        """
        if token not in self.PostingList:
            self.PostingList[token] = {docID : 1}
        else:
            if docID not in self.PostingList[token]:
                self.PostingList[token].update({docID : 1})
            else:
                self.PostingList[token][docID] += 1

    # test posting list
    def testPostingList(self):
        """
        test Posting List
]        """
        for i in self.PostingList:
            print(i + ' ',end="")
            for j in self.PostingList[i]:
                print(str(j) + ', ',end="")
            print()
    # write dictionary to file
    def writeToBlock(self):
        """
        This fucntion is to write index into block files
        """
        sorted_dictionary = OrderedDict()
        with open('/Users/lekangdu/Downloads/40051703-A2/SPIMI-BM25/DISK/Block' + str(self.BlockFilesNumber) + '.txt', 'w') as f:
            for i in self.Sorted_PostingList:
                sorted_dictionary[i] = self.PostingList[i]
            json.dump(sorted_dictionary,f)
            self.BlockFilesNumber += 1

    # check float
    def isFloat(self,v):
        """
        This fucntion is to find the dot
        :param v: value
        :return: t or f
        """
        if v.count('.') == 1:
            if v.replace('.','').isdigit:
                return True
        return False
