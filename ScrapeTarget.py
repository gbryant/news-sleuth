from webpage import webpage
import os
import json
import time
from pymongo import MongoClient

client = MongoClient()
db = client.NewsSleuth



def is_item0_in_list_item0(a,b):
    for i in b:
        if i[0]==a[0]:
            return True
    return False


class ScrapeTarget:
    def __init__(self,siteDef):
        self.url=siteDef['url']
        self.name=siteDef['name']
        self.xpathList=siteDef['xpath']
        self.page = webpage()
        self.loader = siteDef['loader']
        self.text = []
        self.collection = db[self.name]

    def is_text_in_db(self,a):
        cursor = self.collection.find({"text": a})
        if cursor.count() == 0:
            return False
        else:
            return True

    def load(self,cached=False):
        if self.loader == "selenium":
            if cached:
                if os.path.exists('page-'+self.name) != True:
                    print(self.name+': fetching page to cache')
                    self.page = webpage(self.url,automator=True)
                    self.page.save('page-'+self.name)
                else:
                    print(self.name+': using cached page')
                    self.page = webpage()
                    self.page.load('page-'+self.name)
            else:
                print(self.name+': fetching page')
                self.page = webpage(self.url,automator=True)
                self.page.save('page-'+self.name)
        else:
            print(self.name+':loader:'+self.loader+' not recognized')

    def runXpaths(self):
        for i in range(0,len(self.xpathList),3):
            results = self.page.xpath(self.xpathList[i])
            for j in results:
                if j.text != None:
                    item = j.text.strip()
                    if item != '':
                        #self.text.append((item,self.xpathList[i+1],j.xpath(self.xpathList[i+2])[0],time.strftime("%I:%M:%S:%P:%F")))
                        self.text.append({'text':item,'type':self.xpathList[i+1],'link':j.xpath(self.xpathList[i+2])[0],'timestamp':time.strftime("%I:%M:%S:%P:%F")})
    def getText(self):
        if os.path.exists('text-'+self.name) != True:
            print(self.name+': no database file present')
            return []
        else:
            with open('text-'+self.name,'r') as file:
                existingText = json.load(file)
            return existingText

    def report(self):
        cursor = self.collection.find({"text": 'Cruz and Trump trade jabs over eligibility issue, NYC values'})
        if cursor.count() == 0:
            print(self.name,':','not found')
        else:
            print(self.name,':','found')

    def updateText(self):
        # for i in self.text:
        #     entry = {'text':i[0],'type':i[1],'link':i[2],'timestamp':i[3]}
        #     self.collection.insert_one(entry)
        # return

        print(self.name+': checking for updates')
        updated=False
        for i in self.text:
            if self.is_text_in_db(i['text'])==False:
                updated=True
                print(self.name+': appending:',i['text'])
                self.collection.insert_one(i)
                #existingText.append(i)
        #if updated:
            #with open('text-'+self.name,'w+') as file:
                #json.dump(existingText,file)