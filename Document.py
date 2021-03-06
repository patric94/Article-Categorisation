from pandas import read_csv
import numpy as np
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from nltk.tokenize import wordpunct_tokenize as tokenize
import string as String

stop_word = get_stop_words('english')


class Document:
    def __init__(self, csv_file, start=0, end=-1, test=False):
        self.csv = csv_file
        # Target names as a dictionary
        self.target_names = {
            0: 'Politics',
            1: 'Film',
            2: 'Football',
            3: 'Business',
            4: 'Technology'
        }

        # Target names as a list
        self.target_names_str = [
                'Politics',
                'Film',
                'Football',
                'Business',
                'Technology'
        ]

        self.data = []
        self.target = []
        self.id = []
    
        # Read the csv
        df = read_csv(csv_file, sep='\t')
    
        # We have the option to use only n documents
        # (defined by the start - end index
        if start == 0 and end != -1:
            df = df.head(end)
            self.size = len(df.head(end))
        elif start == 0 and end == -1:
            self.size = len(df)
            pass
        elif start != 0 and end != -1:
            df = df.iloc[start: end]
            self.size = end - start
        elif start != 0 and end == -1:
            df = df.iloc[start: df.size]
            self.size = df.size - start

        a = np.array(df)

    
        if test is False:
            # If this document is not for testing
            # We also save the target of that document
            for i in range(a.shape[0]):
                t = str(a[i][4])
                self.data.append(str(a[i][3]))
                self.id.append(str(a[i][1]))
                if t == 'Politics':
                    self.target.append(0)
                elif t == 'Film':
                    self.target.append(1)
                elif t == 'Football':
                    self.target.append(2)
                elif t == 'Business':
                    self.target.append(3)
                elif t == 'Technology':
                    self.target.append(4)
        else:
            # Otherwise, we only get the data and ID    
            for i in range(a.shape[0]):
                self.data.append(str(a[i][3]))
                self.id.append(str(a[i][1]))

    def get_text(self, target):
        '''
        Get all texts of category <target> as one single string
        '''
        string = ""
        for i in range(len(self.data)):
            if self.target[i] == target:
                string += self.data[i]

        return string

    def get_clean(self, target):
        '''
        Get all texts of category <target> as one single
        *and* remove the stopwords
        '''
        oth_st_words = ['said']
        for oth_word in oth_st_words:
            stop_word.append(oth_word)

        s = self.get_text(target)
        for word in stop_word:
            s = s.replace(' ' + word + ' ', "")
            s = s.replace(',' + word + ' ', "")
            s = s.replace(' ' + word + '.', "")

        return s 
