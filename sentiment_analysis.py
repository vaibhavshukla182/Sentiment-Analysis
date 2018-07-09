from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
import string
import math
stopwords=['apple','amazon','positive','phone','comment', 'iphone','u','pune','indore','city','amazons' ,'prime', '7', 'user', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'nor', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just', 'don', 'should', 'now','re', 've','ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn','iphone7','iphone','black','32gb','gb']
plt.ion()
df=pd.read_csv('/Users/vaibhavshukla/Desktop/project2')#to open the file containing the scraped data
df.dropna(inplace=True)
pd.set_option('display.max_colwidth', -1)
def text_process(mess):
    '''mess= [r.encode('ascii', 'ignore') for r in mess]
    mess=str(mess)
    mess=''.join(mess)'''
    nopunc= [a for a in mess if a not in string.punctuation]
    nopunc=''.join(nopunc)
    word= [a for a in nopunc.split( ) if a.lower() not in stopwords]
    return word
df['Comments']=df['Comments'].apply(text_process)#to apply the process of text processing
bag=[]
list_of_comments=[]
for comment in df['Comments']:
    list_of_comments.append(comment)
    for words in comment:
        if words not in bag:
            bag.append(words)#to create a bag containing one copy of all the words 
#print(len(bag))
def freq(words,comment):#to find out the freq of a particular word in a particular sentence
    num=0
    for k in comment:
        if(k==words):
            num=num+1
return num
list_of_bow=[]
list_of_bow_of_each_comment=[]
for comment in df['Comments']:
    list_of_bow_of_each_comment=[comment]
    for words in bag:
        if words not in comment:
            list_of_bow_of_each_comment.append(0)#to create a row with 0 or frequency value of that word with the first column as the comment itself 
        else:
            list_of_bow_of_each_comment.append(freq(words,comment))
    list_of_bow.append(list_of_bow_of_each_comment)#to create a list of list to make a dataframe
a='comment'
bag_with_comments_column=[a]+bag
df_bow=pd.DataFrame(list_of_bow,columns=bag_with_comments_column)
print(df_bow.head(5))
df_bow.to_csv('df_bow')#dataframe of bow
df_tfidf=df_bow
tfidf_value=[]
count=0
for word_for_columns in bag:
    num=0
    for rows in df_bow[word_for_columns]:
        if rows!=0:
            num=num+1#to count the number of comments in which that particular word is occuring  
    a=df['Comments'].count()/num#to calculate total no of comments/number of comments in which a particular word is occuring 
    df_tfidf[word_for_columns] = df_bow[word_for_columns].apply(lambda x: x*math.log10(a))
df_tfidf['positive']=df['positive']
#df_tfidf--the dataframe containing the dfidf values
#print(df_tfidf.head(5))
list_positive=[]
list_negative=[]
df_tfidf.to_csv('df_tfidf')
df_tfidf=pd.read_csv('/Users/vaibhavshukla/Desktop/df_tfidf')
print(df_tfidf.info())
for words in bag:
    sum_positive=0
    sum_negative=0
    for index in df_tfidf['Unnamed: 0']:
        if(df_tfidf['positive'][index]==1.0 ):
            sum_positive=sum_positive+df_tfidf[words][index]
        else:
            sum_negative=sum_negative+df_tfidf[words][index]
    list_positive.append(sum_positive)
    list_negative.append(sum_negative)
list=[]#to make a datframe
list.append(list_positive)
list.append(list_negative)
df_final=pd.DataFrame(list,columns=bag)
df_final.to_csv('df_final')#the final dataframe conatining two rows
sum=0
df_final=pd.read_csv('/Users/vaibhavshukla/Desktop/df_final')
'''with pd.option_context('display.max_rows', 2, 'display.max_columns', 100):
    print(df_final)'''
df_reviews=pd.read_csv('/Users/vaibhavshukla/Desktop/test_project')
counter=0
for comments in df_reviews['Comments']:
    if(counter!=92):
        input_processed=text_process(comments)
        positive_sum=0
        negative_sum=0
        for words in input_processed:
            if words in bag:
                positive_sum=positive_sum+(df_final['words'][0]*freq(words,comments))
                negative_sum=negative_sum+(df_final['words'][1]*freq(words,comments))
        if(positive_sum>=negative_sum):
            value=1
        else:
            value=0
        if(value==df_reviews['positive'][counter]):
            sum=sum+1
        counter=counter+1
    else:
        counter=counter+1
print("Accuracy--",(sum/129)*100,"%","with",counter-1,"test data")






