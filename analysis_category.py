# -*- coding: utf-8 -*-
import pyquery
import pymongo
import datetime
import os
import sys

from pyquery import PyQuery as pq

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

client = pymongo.MongoClient(host="127.0.0.1", port=27017)
# Connect Database
db = client.beauty
# Use collection
collection = db['4493_category']
category = collection.find({""})


Get_Category_withtotal()
