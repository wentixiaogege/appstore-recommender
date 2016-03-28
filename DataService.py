#!/usr/bin/python2.7
#-*- encoding=utf-8 -*-

class DataService(object):

    @classmethod
    def init(cls,client):
        cls.appstore = client.appstore
        cls.app_info = client.appstore.app_info
        cls.user_info = client.appstore.user_info
        cls.user_download_history = client.appstore.user_download_history


    @classmethod
    def retrieve_user_download_history(cls,filter_dict={}):
        
        cursor = cls.user_download_history.find(filter_dict)
        result = {}
        for document in cursor:
            result[document['user_id']] = document['download_history']
        return result

    @classmethod
    def retrieve_app_info(cls,filter_dict={}):

        cursor = cls.app_info.find(filter_dict)
        result = {}
        for document in cursor:
            result[document['app_id']] = {'title':document['title']}

        return result

    @classmethod
    def update_app_info(cls,filter_dict,update):

        cls.app_info.update_one(filter_dict,update)

    @classmethod
    def retrieve_user_info(cls,filter_dict={}):

        cursor = cls.user_download_history.find(filter_dict)
        result = []
        for document in cursor:
            result.append(document['user_id'])

        return result
    @classmethod
    def update_user_info(cls,filter_dict,update):

        cls.user_info.update_one(filter_dict,update,upsert=True)
