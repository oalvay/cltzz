# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 02:37:31 2020

@author: 78182
"""

import os.path
from os import path
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
from fp.fp import FreeProxy
import requests
class Crawler:
    def __init__(self):
        self.list_of_websites = ['azlyrics.com']
        self.print_info()
        
    def print_info(self):
        print('Directory for crawled lyrics {} \n'.format(os.path.realpath('..')))
        print('Crawling from {} \n'.format(self.list_of_websites))
        for w in self.list_of_websites:
            if(path.exists(os.path.realpath('..')+'\\{}'.format(w+'.csv'))):
                print(w + 'is crawled \n')
            else:
                print(w + 'is not yet crawled, started crawling \n')
                self.start_crawling(w)
    
    def start_crawling(self,website):
        if(website == 'azlyrics.com'):
            
            print('start crawling from {}'.format(website))
            author_song_lyrics_dict = {}
            
            appendix = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','19']
            proxy = FreeProxy(country_id=['UK'],rand=True).get()
            for appen in tqdm(appendix,desc='downloading author categories by initial'):
                url = 'http://'+website+'/'+appen+'.html'
                
                req = Request(url,headers = { 'User-Agent' : 'Mozilla/5.0' },proxy=proxy)
                soup = BeautifulSoup(req.text, "lxml")
                author_hrefs = soup.find_all("div",{'class':'col-sm-6 text-center artist-col'})
                hrefs_list = []
                for href in author_hrefs:
                   hrefs_list =  hrefs_list + href.find_all('a')
                  
                links_list = []
                author_list =[]
                for h in hrefs_list:
                    links_list.append(h.get('href'))
                    author_list.append(h.text)

                for author,link in zip(author_list,links_list):
                    proxy = FreeProxy(country_id=['UK'],rand=True).get()
                    author_url = 'http://'+website+'/'+link
                    req = Request(author_url,headers = { 'User-Agent' : 'Mozilla/5.0'},proxy=proxy)
                    soup = BeautifulSoup(req.text, "lxml")
                    song_hrefs = soup.find_all("div",{'class':'listalbum-item'})
                    song_titles = []
                    song_lyrics = []
                    proxy = FreeProxy(country_id=['UK'],rand=True).get()
                    for h in song_hrefs:
                        song_titles.append(h.text)
                        lyric_link = 'http://'+website + h.find('a')['href'][2:]
                        req = Request(lyric_link,headers = { 'User-Agent' : 'Mozilla/5.0'},proxy= proxy)
                        soup = BeautifulSoup(req.text, "lxml")
                        lyrics = soup.find_all("div",class_=None)[1]
                        lyrics_contents = lyrics.contents[2:]
                        song_lyrics.append(lyrics_contents)
                    for s,l in zip(song_titles,song_lyrics):
                        author_song_lyrics_dict[(author,s)] = l