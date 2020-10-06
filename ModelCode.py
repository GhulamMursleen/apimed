


import pandas as pd
import numpy as np
from pandas import DataFrame
import collections
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pickle
from fuzzywuzzy import fuzz

from fuzzywuzzy import process

class Model:
    # In[2]:
    
    
    def readdataframe(self,filename):
        return pd.read_csv (filename)
    def savedataframe(self,filename,df):
        df.to_csv(filename,index=False)
        return
    
    
    # In[3]:
    
    
    def checknoofcolms(self,df):
        # define an empty list
        columns = []
        # open file and read the content in a list
        with open('Data/columnnames.txt', 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                currentPlace = line[:-1]
    
                # add item to the list
                columns.append(currentPlace)
        #print(len(columns),columns)
        colms=df.columns.tolist()
        if (len(columns)==len(colms)):
            return True,"same"
        else:
            return False, "Not equal colomns"
    def checksamenamecolumns(self,df):
        # define an empty list
        columns = []
        # open file and read the content in a list
        with open('Data/columnnames.txt', 'r') as filehandle:
            for line in filehandle:
                # remove linebreak which is the last character of the string
                currentPlace = line[:-1]
    
                # add item to the list
                columns.append(currentPlace)
        colms=df.columns.tolist()
        return collections.Counter(colms) == collections.Counter(columns)
    def validFile(self,filename):
        filename="./Data/Data.csv";
        df=self.readdataframe(filename)
        if self.checknoofcolms(df):
            if self.checksamenamecolumns(df):
                return True,"validfile"
                
            else:
                return False,"CSV Files columns names are not same"
                
        else:
            return False,"No of columns not equal Like before"
    
    
    # In[4]:
    
    
    def append(self):
        
        filename1="Data/append.csv";
        filename2="Data/Data.csv";
        flag,output=self.validFile(filename1)
        if flag:
            df1=self.readdataframe(filename1)
            df2=self.readdataframe(filename2)
            df1=df1.append(df2)
            df1=df1.drop_duplicates()
            self.savedataframe(filename2,df1)#change filename with filename 2
            return "Successful Append"
        else:
            return output
    #response=append()
    
    #response
    
    
    # In[5]:
    
    
    def replace(self):
        filename1="./Data/append.csv";
        filename2="./Data/Data.csv";
        flag,output=self.validFile(filename1)
        if flag:
            df1=self.readdataframe(filename1)
            df1=df1.drop_duplicates()
            self.savedataframe(filename2,df1)#change filename with filename2
            return "Successful Replace File"
        else:
            return output
    #response=replace()
    #response
    
    
    # In[9]:
    
    
    
    def preprocess(self,df):
        df=df.drop(['Timestamp','Write any anonymous name (No need to provide your real name)'], axis = 1)
        columnnames=['A','B','C','D','E','F','G','H','I','J','K','L','O']
        df.columns=columnnames
        df2=df.copy(deep=True)
        df2=df2.drop(['O'], axis = 1)
        
        Row_list =[]
        for index, rows in df2.iterrows(): 
            rows=rows.tolist()
            for i in range(0, len(rows)): 
                rows[i] = str(rows[i])
            #print(type(rows),rows)
            # append the list to the final list 
            Row_list.append(" ".join(rows))
    
        # Print the list 
        
        #print(Row_list)
        dfnew = DataFrame (Row_list,columns=['text'])
        dfnew['out']=df['O'].copy()
        self.savedataframe("Data/fuzzy.csv",dfnew)
        
        Preprocesscols=['B','C','D','E','F','G','H','I','J','K','L']
        uniquedict={}
        import csv

        with open('Data/inputforms.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for x in Preprocesscols:
                #print(df[x].unique())
                    
                    writer.writerow(df[x].unique())
                    uniquedict.update({x:(df[x].unique())})
                    
        
        with open('Data/uniquecols.txt', 'wb') as handle:
          pickle.dump(uniquedict, handle)
        keys=list(uniquedict.keys())
        for col in keys:
            df[col] = pd.factorize(df[col])[0]
        aa = np.array(df['O'].values.tolist())
        #print(type(aa))
        a=np.where(aa <= 25, 0, aa).tolist()
        a=np.array(a)
        a=np.where((a > 25) & (a<=50), 1, a).tolist()
        a=np.array(a)
        a=np.where((a > 50) & (a<=75), 2, a).tolist()
        a=np.array(a)
        a=np.where((a >75) & (a<=100), 3, a).tolist()
        #print(aa,"\n",a)
        df['O'] = DataFrame (a,columns=['O'])
        return df
    
    
    # In[11]:
    
    
    def train(self):
        filename="Data/Data.csv";
        df=self.readdataframe(filename)
        df=self.preprocess(df)
        X = df.drop('O', axis=1)
        Y = df['O']
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)
        svclassifier = SVC(kernel='linear',probability=True)
        svclassifier.fit(X_train, y_train)
        filename = 'Data/finalized_model.sav'
        pickle.dump(svclassifier, open(filename, 'wb'))
        return "Trained Successfully"
    #print(train())
    
    
    # In[47]:
    
    
    #lit=["name","age","gender","climate condition","any prescribed medicine","composition of medicine","type of medicine","any health issue","food restrictions","food you feel alergic","any particular allergy towards medicine",'Any symptoms','family disease']
    
    #print(len(lit))
     #lit=["name","age","gender","climate condition","any prescribed medicine","composition of medicine","type of medicine","any health issue","food restrictions","food you feel alergic","any particular allergy towards medicine",'Any symptoms','family disease']
    
    #print(len(lit))
    def predict(self,lst):
        lst[1]=float(lst[1])
        lstsave=lst.copy()
        
        lst.pop(0)
        rows=lst
        for i in range(0, len(rows)): 
                rows[i] = str(rows[i])
        lstjoin=" ".join(rows) 
        df = self.readdataframe("Data/fuzzy.csv")
        text=df['text'].tolist()
        out=df['out'].tolist()
        results=process.extract(lstjoin, text, scorer=fuzz.token_sort_ratio)
        Match=results[0][0]
        score=results[0][1]
        if score <75:
            readuniquedict={}
            with open('Data/uniquecols.txt', 'rb') as handle:
              readuniquedict = pickle.loads(handle.read())
            readuniquedict
            preprocessedlst=[]
            keys=readuniquedict.keys()
            i=0
            for x in lst:
                if i!=0:
                    #print(chr(i+65),x,len(lst))
                    key=chr(i+65)
                    keylist=readuniquedict[key].tolist()
                    if x in keylist:
                        preprocessedlst.append(keylist.index(x))
                    else:
                        preprocessedlst.append(-1)
                else:
                    preprocessedlst.append(x)
                i=i+1
    
    
            # load the model from disk
            filename = 'Data/finalized_model.sav'
            loaded_model = pickle.load(open(filename, 'rb'))
            #lst = pd.DataFrame([preprocessedlst], columns = ['A','B','C','D','E','F','G','H','I','J','K','L']) 
            preprocessedlst=np.array(preprocessedlst)
            preprocessedlst=preprocessedlst.reshape(1, -1)
            y_pred = loaded_model.predict(preprocessedlst)
    
            #print(loaded_model.predict_proba(preprocessedlst))
            res=((y_pred[0]+1)*25)*max(loaded_model.predict_proba(preprocessedlst)[0])
            df=self.readdataframe('Data/input.csv')
            lstsave.insert(0, 0)
            lstsave.append(res)
            df2 = (pd.DataFrame(lstsave)).T
            df2.columns=df.columns
            df=df.append(df2, ignore_index=True)
            self.savedataframe('Data/input.csv',df)
            return res
        else:
            return out[text.index(results[0][0])]
    #lst=["Satanjib Das","17","Male","Humid subtropical","Rablet-20","Rabeprezol Sodium I.P :- 20MG", "Tablet/ Capsule","Don't know","nan","Mutton","nan","nan","nan"]
    
    #res=predict(lst)
    #print (res)
    
    
    # In[49]:
    
    # In[49]:
    
    
    def formdata(self): #lit=["name","age","gender","climate condition","any prescribed medicine","composition of medicine","type of medicine","any health issue","food restrictions","food you feel alergic","any particular allergy towards medicine",'Any symptoms','family disease']
        readuniquedict={}
        with open('Data/uniquecols.txt', 'rb') as handle:
              readuniquedict = pickle.loads(handle.read())
        return readuniquedict
    #print (formdata())
    
    def __init__(self):
        print("Start Model")



