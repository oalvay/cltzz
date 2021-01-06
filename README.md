# TTDS CW3

⚠️always `git pull` before you start to work, and `git push` after your work⚠️  

A guide to use git if you are not familar with it: [git novice](http://swcarpentry.github.io/git-novice/)


**topic**: song search based on lyrics

## Details

### Contents

The repository is currenctly splited into four parts (can be extented if needed):

name|function
---|---
`crawler`| collect data from internet
`engine`| preprocess data and bulid search engine that receive quries and return a ranking of songs
`webapp`| build a web application using the data and search engine
`report`| write report

### Data

Since github does not support large size file (>100MB), please download the dataset from [this private kaggle link](http://www.kaggle.com/dataset/991400034c35e93ff75a6255470ea5a7ce796409259539c9b996da553b8dccba) and move the `.csv` files under the `engine` directory.

### Current Planning 

#### stage 1 (completed)

+ build a demo web crawler (requests 1000 time)
+ write templates for front-page and search results.

#### stage 2 (completed)

+ build the full crawler
+ scraping the first one-million songs

#### stage 3 (on going)

+ build search engine
+ scraping all songs (6 millions)
 
---

## Team members

Name | github id | email
---|---|---
Siyue Chen | CindySakura | s2070782@ed.ac.uk
Yang Lin | oalvay | s2041499@ed.ac.uk
Zhendong Tian | 7818207 | s1702583@ed.ac.uk
Zhuocheng Zhen | WhatsTheYouth | s2085935@ed.ac.uk
Yongchang Zhu | relic-dyebt | s2133997@ed.ac.uk
