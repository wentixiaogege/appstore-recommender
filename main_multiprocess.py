#!/usr/bin/python2.7
#-*- encoding=utf-8 -*-
import time
import math
import pymongo
import operator
import DataService
import helper

from DataService import DataService
from helper import Helper
from pymongo import MongoClient

from multiprocessing import Process
from multiprocessing import Pool
import os


def calculate_app_top_10(app,user_download_history):
    #get app with all the lists similarity
    
    app_similarity ={}
    for apps in user_download_history:
        similarity = Helper.cosine_similarity([app],apps)
        for listapp in apps:
            if listapp is app:
                continue
            elif app_similarity.has_key(listapp):
                app_similarity[listapp] = app_similarity[listapp] + similarity
            else:
                app_similarity[listapp] = similarity
            
    if not app_similarity.has_key(app):
        return 
    #remove itself
    #app_similarity.pop(app)
    #calculate top10  reverse= true means from bigger to smaller   
    #items() and operator.itemgetter(1) means get list of tuples with key-value pair
    sorted_apps =sorted(app_similarity.items(),key=operator.itemgetter(1),reverse=True)

    top_ten_apps=[]

    i=0
    while i<10:
        #print("top 10 apps "+sorted_apps[i][0]) ## uncommnet for test one app top 10
        top_ten_apps.append(sorted_apps[i][0])
        i+=1

    # add into mongodb appstore
    #DataService.update_app_info({'app_id':app},{'$set':{"'top_10_app":top_ten_apps}})
def calculate_user_top_5(user,all_apps,user_download_list):
    # ways is to calculate all_apps similarity with the user_download_list

    app_similarity={}

    for app in all_apps:
        if app in user_download_list:
            continue
        else:
            #calculate the app similarity with the user download lists
            similarity = Helper.cosine_similarity([app],user_download_list)
            if app_similarity.has_key(app):
                app_similarity[app] = app_similarity[app] + similarity
            else:
                app_similarity[app] = similarity

    #get the top 5
    top_five_apps=[]
    sorted_apps =sorted(app_similarity.items(),key=operator.itemgetter(1),reverse=True)
    i=0
    while i<5:
        #print("top 10 apps "+sorted_apps[i][0]) ## uncommnet for test one app top 10
        top_five_apps.append(sorted_apps[i][0])
        i+=1

    DataService.update_user_info({'user_id':user},{'$set':{"top_5_app":top_five_apps}})

def main():
    try:
        #client = MongoClient("mongodb://mongodb0.example.net:27019")
        client = MongoClient()
        DataService.init(client)
        user_download_history = DataService.retrieve_user_download_history()
        start_time = time.clock();


        app_info = DataService.retrieve_app_info()

        p = Pool(4)
        for app in app_info.keys():
            p.apply_async(calculate_app_top_10, args=(app,user_download_history.values(),))
        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')

        

        # testing all app's top10 
        #for app in app_info.keys():
        #  calculate_app_top_10(app,user_download_history.values())

        #testing all user's top5
        #for user in user_download_history.keys():
        #   calculate_user_top_5(user,app_info.keys(),user_download_history[user])

        end_time = time.clock();

        print('overall using time is %f seconds' % (end_time - start_time))
    except Exception as e:
        print(e)
    finally:
        #
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()