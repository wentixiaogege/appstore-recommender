this is the recommender project using python2.7: basic idea is that 
based on the user download history and user installed apps ,you can get 
  top10 recommending apps for every app
  top10 recommending apps for every user

steps:
    install  python2.7
    install  mongo db
    install  pymongo

## get app's top 10 recommending apps
1.edit /etc/profile setting evn if needed
2.service mongod start for starting the mongodb service on default post
  2.0 create database and collections 
  2.1 import the test json data
      
      data hierarchy database/collection/document:w:
      mongoimport --db appstore --collection app_info --drop --file app_info.json 
      mongoimport --db appstore --collection user_download_history --drop --file user_download_history.json
      remove a collection: db.getCollection("_registration").drop()
                           db.collectionname.drop()

3. ways to calculate the top10 for every app
    using  similarity between a1 to all other apps 

4. store the top10 into mongo 
    DataService.update_app_info({'app_id':app},{'$set':{"'top_5_app":top_ten_apps}})
5. check 
    db.app_info.find({"app_id":"C10107104"}).pretty()

## get user's top 5 recommending apps
db.user_info.update({"user_id":"1"},{'$set':{"top_5_apps":"fdsafdsa"}},{upsert:true})



## without optimize yet
### getting app's top 10
overall using time is 44.227575 seconds
### getting user's top 5
overall using time is 27.130482 seconds

#Optimize
 1.methods updates 
    logic level
 2.framework updates 
    multi-thread : thread threading (cause using Cpython as a interpreter which has a GIL lock for threads within a process )因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。
    multi-process: will be a good solution here if using Cpython
##using multiprocess
All subprocesses done.
overall using time is 165.589536 seconds
## using multithreading
overall using time is 83.349423 seconds

## using concurrent
sudo pip install futures
     ProcessPoolExecutor
     overall using time is 151.707311 seconds
     ThreadPoolExecutor
     overall using time is 84.498609 seconds




