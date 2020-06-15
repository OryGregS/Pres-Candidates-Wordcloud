#!/usr/bin/env python
# coding: utf-8

# In[108]:


import numpy as np
import matplotlib.pyplot as plt
import re
from twython import Twython
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
from nltk.corpus import stopwords
from IPython.display import Image as im
nltk.download('stopwords')


# In[109]:


# Sign up for a twitter dev account, create an app, and replace these values with your app's key & secret key
APP_KEY = "0dSpIRLbTyvQKRvSmnIhAocIV"
APP_SECRET = "4EMoXNG1Yia7CpIILLunjsWaPhZ3iJUPHvGdI0p28ci7WpSh4h"
twitter = Twython(APP_KEY, APP_SECRET)


# In[105]:


words_to_remove = set()
with open("2020PresWords/commonwords_all.txt", "r") as f:
    for line in f:
        words_to_remove.add(line.strip())


# In[118]:


twitterUserNames = ["realDonaldTrump", "JoeBiden"]
for user_name in twitterUserNames:
    
    #Get timeline 
    user_timeline=twitter.get_user_timeline(screen_name=user_name, tweet_mode="extended", count=1) 
    
    #get most recent id
    last_id = user_timeline[0]['id']-1
    for i in range(128):
        batch = twitter.get_user_timeline(screen_name=user_name,count=200, max_id=last_id, tweet_mode="extended", include_rts=False)
        user_timeline.extend(batch)
        last_id = user_timeline[-1]['id'] - 1
        
    raw_tweets = []
    for tweets in user_timeline:
        raw_tweets.append(tweets['full_text'])
        
    raw_string = ''.join(raw_tweets)
    no_links = re.sub(r'http\S+', '', raw_string)
    no_unicode = re.sub(r"\\[a-z][a-z]?[0-9]+", '', no_links)
    no_special_characters = re.sub('[^A-Za-z0-9\\- ]+', '', no_unicode)
    words = no_special_characters.split(" ")
        
    words = [w for w in words if len(w) > 2]  # ignore a, an, be, ...
    words = [w.lower() for w in words]
    words = [w for w in words if w not in words_to_remove]
    
    imgFilePath = '2020PresWords/americanFlag.jpg'
    mask = np.array(Image.open(imgFilePath))
    wc = WordCloud(stopwords=words_to_remove, mask = mask, background_color="black", max_words=1000)
    clean_string = ','.join(words)
    wc.generate(clean_string)
    
    f = plt.figure(figsize=(50,50))
    plt.imshow(wc, interpolation='bilinear')
    plt.title('Twitter Generated WordCloud for @' + user_name, size=40)
    plt.axis("off")
    plt.savefig('2020PresWords/' + user_name + '_words.png')
    plt.show()


# In[117]:


wc = WordCloud(stopwords=words_to_remove, mask = mask, background_color="black", max_words=1000)
clean_string = ','.join(words)
wc.generate(clean_string)

f = plt.figure(figsize=(50,50))
plt.imshow(wc, interpolation='bilinear')
plt.title('Twitter Generated WordCloud for @' + user_name, size=40)
plt.axis("off")
plt.show()


# In[ ]:




