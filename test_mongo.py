from pymongo import Connection
#connection = Connection()

connection = Connection('localhost', 27017)
db = connection['test']
collection = db['test-collection']

import datetime
post = {"author": "Mike",
        "text": "My first blog post!sdsdsdsdqw",
        "tags": ["mongodb", "python", "pymongo"],
        "sasdasdasdate": datetime.datetime.utcnow()}

posts = db.posts
for x in range(1, 10):
    post = {"author": "Mike%s" % x,
            "text": "My first blog post!sdsdsdsdqw",
            "tags": ["mongodb", "python", "pymongo"],
            "sasdasdasdate": datetime.datetime.utcnow()}
    
    posts.insert(post)
    print x
    

print db.collection_names()
print posts

print posts.find_one({"author": "Mike2"})


test_data = db.test_data
test_data.insert({'user': 1})
print test_data

## pull from twitter
#
#figure_out_unique
#
#twistter_name 
#
## count word repeat
#
## put database
#
## login
#keyword = {"alice": 1, "bob": 2, "carol": 3}
#
## 
#test_data.insert(keyword)
#
#
#
#promotor sign up 
#    search all promotors tweets for unique words
#        insert unique word count into local db {rap: 5; cool: 3, dumb: 10}
#    create new socket to new promotors twitter
#        update/insert unique words count via socket into local db
#
#client
#    "i want to promote my new hair gel"
#    performs search for "hair gel" and selects budget
#        performs concurrent web search for related terms {search: hair {style:20; beiber: 5}}
#    searches local db for keyword hits {local db search: {hair; gel}; web search: {style; beiber}}
#        (backend)   
#            finds users with best match for keywords and budget
#    show results with num tweets
#        Reach 100 users for $2 
#            (backend)
#                find possible matches (in this case 3 promotors meet 100 follower criteria)
#                    3 promotors {promotor: 1 {followers: 25}, promotor: 2 {followers: 50}, promotor: 3 {followers: 25}}    
#                        each follower of promotor is verified for authenticity
#        Reach 500 tweeters for $10 " "
#        Reach 10000 tweeters for $50 " "
#    
#    clients selects campaign
#        Provide your own copy {semi-instant tweet}
#        Have promotor write tweet
