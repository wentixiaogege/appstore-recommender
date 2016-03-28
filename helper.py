#!/usr/bin/python2.7
#-*- encoding=utf-8 -*-
import math

class Helper(object):

    @classmethod
    def cosine_similarity(cls,app_list_1,app_list_2):
        match = cls.__count_match(app_list_1,app_list_2)
        return float(match / math.sqrt(len(app_list_1)*len(app_list_2)))

    @classmethod
    def __count_match(cls,list1,list2):
        count =0
        for element in list1:
            if element in list2:
                count +=1;

        return count



