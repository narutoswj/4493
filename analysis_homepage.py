# -*- coding: utf-8 -*-
import pyquery
import pymongo
import datetime
import os
import sys

print sys.getdefaultencoding()

def Get_Category():
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    # Connect Database
    db = client.beauty
    # Use collection
    collection = db['4493_category']
    category = collection.find({})
    client.close()
    return category

def Get_Category_withtotal():
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    # Connect Database
    db = client.beauty
    # Use collection
    collection = db['4493_category']
    category = Get_Category()
    for cat in category:
        first_page = cat['url']
        print first_page
        try:
            total_images = pq(first_page)('.interestline')('span:first').html()
            if not total_images == None:
                collection.update({"_id": cat["_id"]}, {"$set": {"total_images": total_images}})
        except Exception, e:
            print e
    client.close()

homepage = 'http://www.4493.com'
directory = 'D:/Image/4493/'
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
# Connect Database
db = client.beauty

# Use collection
collection = db['4493_category']

from pyquery import PyQuery as pq
nav_list = pq(homepage)('.topulnav')('li')
for item in nav_list:
    first_level = pq(item)('a:first')
    #print first_level
    second_level = pq(item)('.childnav').html()
    if not(second_level == None):
        second_level_detail = pq(second_level)('p')
        for level_two_item in second_level_detail:
            #print pq(level_two_item).html()
            if (pq(level_two_item)('a').attr('href').__contains__('http')):
                path = first_level.text() + '/' + pq(level_two_item)('a').text()
                url = pq(level_two_item)('a').attr('href')
                print 'path: ' + path
                print 'url: ' + url
            else:
                path = first_level.text() + '/' + pq(level_two_item)('a').text()
                url = homepage + pq(level_two_item)('a').attr('href')
                print 'path: ' + path
                print 'url: ' + url
                if collection.find({"url":url}).count() == 0:
                    collection.insert({"url":url,"path":path})
                if not (os.path.exists(directory+path)):
                    os.makedirs(directory+path)
    else:
        path = first_level.text()
        if (first_level.attr('href').__contains__('http')):
            url = first_level.attr('href')
        else:
            url = homepage + first_level.attr('href')
        print 'path: ' + path
        print 'url: ' + url
        if collection.find({"url": url}).count() == 0:
            collection.insert({"url": url, "path": path})
        if not (os.path.exists(directory + path)):
            os.makedirs(directory + path)

Get_Category_withtotal()
category = collection.find({"total_images":{"$ne":None}})
for cat in category:
    collection.update({"_id": cat["_id"]}, {"$set": {"total_images": int(cat["total_images"].encode('utf-8').__str__().split('：')[2])}})
    collection.update({"_id": cat["_id"]}, {"$set": {"page": int(cat["total_images"].encode('utf-8').__str__().split('：')[2])/30 + 1}})