from os import listdir
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')


class Spimi_Inverter:

    Src_Files_Path = '/Users/lekangdu/Desktop/SPIMI/documents'
    Src_Files = []
    BlockSize = 500
    BlockFilesNumber = 0
    Dictionary = {}
    PostingList = {}
    Sorted_PostingList = {}

    def GetAllFiles(self):
        files = listdir(self.Src_Files_Path)
        for file in files:
            if str(file).find("reut2") != -1:
                self.Src_Files.append(file)
                # print(str(file))

    def SplitIntoDoc(self):
        Count_doc = 0
        Doc_begin = False
        Body_begin = False
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
                            #  Test
                            # print(str(docID) + " : " + body)
                            docID = 0
                            body = ""
                            Body_begin = False

                            # if Count_doc >= 500:
                            #     self.writeToBlock(Dictionary)
                            #     Dictionary.clear()
                            #     Count_doc = 0
                            #     count_test += 1
                            #     print(count_test)
                        if line.find("</REUTERS") != -1:
                            Doc_begin = False
                    else:
                        p = line.find("<REUTERS")
                        if p != -1:
                            Doc_begin = True
                            # get newID
                            q = line.find("NEWID")
                            if(q != -1):
                                Count_doc += 1
                                temp = int(line[q + 7: len(line) - 3])
                            docID = temp
                            # print("docID : " + str(temp))
                        # find <BODY>
                        if line.find("<BODY>") != -1:
                            Body_begin = True
                            body = line[line.find("<BODY>") + 6: len(line) - 1] + '\n'
                        else:
                            continue
        print(Count_doc)
        print(len(self.Dictionary))
    # Tokenize, stemming and remove Stopwords
    def processDocumentWithCompression(self):
        counter = 0
        no = 0
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for docID in self.Dictionary:
            counter += 1
            no += 1
            # token
            tokens = nltk.word_tokenize(self.Dictionary[docID])
            # print("counter " + str(counter))
            # print(docID)
            # print(tokens)
            # ------------------------------------------------------------
            # lower case
            tokens = [j.lower() for j in tokens]
            # print(tokens)

            # stop words
            tokens = [j for j in tokens if not j in stop_words]
            # print(tokens)
            # , . ? ! ...
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




            # print(tokens)
            # numbers
            tokens = [j for j in tokens if not j.isdigit()]
            tokens = [j for j in tokens if not j.isnumeric()]
            # tokens = [j for j in tokens if not j.isalnum()]
            tokens = [j for j in tokens if not self.isFloat(j)]


            # print(tokens)
            # stemming
            stemmer = nltk.PorterStemmer()
            tokens = [stemmer.stem(j) for j in tokens]

            # ------------------------------------------------------------
            tokens = [j for j in tokens if not j in [',', '+', '.', '?', '!', '\'\'', '\'', '-', '$', '^', '~', ':', ';', '"'
                              '{', '}', '&','(', ')', '@', '*', '>', '<', '#', "''", '``', '...', '..'
                          , '[', ']', '|', '', '=', '_', '%']]
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
        counter = 0
        no = 0
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for docID in self.Dictionary:
            counter += 1
            no += 1
            # token
            tokens = nltk.word_tokenize(self.Dictionary[docID])
            tokens = [j for j in tokens if not ':' in j]
            tokens = [j.lower() for j in tokens]

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

    # create posting list
    def createPostingList(self,token,docID):
        if token not in self.PostingList:
            self.PostingList[token] = [docID]
        else:
            if docID not in self.PostingList[token]:
                self.PostingList[token].append(docID)

    # test posting list
    def testPostingList(self):
        for i in self.PostingList:
            print(i + ' ',end="")
            for j in self.PostingList[i]:
                print(str(j) + ', ',end="")
            print()
    # write dictionary to file
    def writeToBlock(self):
        with open('/Users/lekangdu/Desktop/SPIMI/DISK/Block' + str(self.BlockFilesNumber) + '.txt', 'a+') as f:
            for i in self.Sorted_PostingList:
                f.write(str(i) + ':' + str(self.PostingList[i]) + '\n')
            self.BlockFilesNumber += 1

    # check float
    def isFloat(self,v):
        if v.count('.') == 1:
            if v.replace('.','').isdigit:
                return True
        return False