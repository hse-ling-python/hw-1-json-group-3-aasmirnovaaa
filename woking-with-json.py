import json
import urllib.request
uri = "https://raw.githubusercontent.com/aasmirnovaaa/Devoirs/master/hw_3_twitter.json"
response = urllib.request.urlopen(uri)
text = response.read().decode('utf-8')
tweets = text.splitlines()
tweet_jsons = []
for tweet in tweets:
    tweet_json = json.loads(tweet)
    tweet_jsons.append(tweet_json)

# Сколько твитов в наборе
print("tweets count = ",len(tweets))

# Какой процент твитов составляют удаленные записи? (помеченные как deleted)
def deleted_filter(tweet_json):
    if 'delete' not in tweet_json:
        return False
    else:
        return True
deleted_tweets = filter(deleted_filter,tweet_jsons)
deleted_tweets_count = len(list(deleted_tweets))
deleted_tweets_percent = int(deleted_tweets_count * 100 / len(tweets))
print("deleted tweets count = ",deleted_tweets_count)
print("deleted tweets percent = ",deleted_tweets_percent )

# Какие самые популярные языки твитов?
languages = {}
for tweet_json in tweet_jsons:
    if 'lang' in tweet_json:
        if tweet_json['lang'] in languages:
            languages[tweet_json['lang']] += 1
        else:
            languages.update({tweet_json['lang']:1})
print("TOP 10 languages:")
import operator
sorted_languages = sorted(languages.items(),key = operator.itemgetter(1),reverse=True)
for sl in sorted_languages[:10]:
    print(sl[0], " : ",sl[1])

# Есть ли твиты от одного и того же пользователя? Если да, то сколько таких пользователей?
user_tweet_counts = {}
for tweet_json in tweet_jsons:
    if 'user' in tweet_json:
        usr_id = tweet_json['user']['id']
        if usr_id in user_tweet_counts:
            user_tweet_counts[usr_id] += 1
        else:
            user_tweet_counts.update({usr_id:1})
active_user_count = 0
for (key,value) in user_tweet_counts.items():
    if value >= 2:
        active_user_count += 1
print("Users that wrote 2 or more posts: ", active_user_count)

# Топ-20 хэштегов (для них есть специальное поле)
hashtag_counts = {}
for tweet_json in tweet_jsons:
    if 'entities' in tweet_json:
        entities = tweet_json['entities']
        if 'hashtags' in entities:
            hashtags = entities['hashtags']
            for hashtag in hashtags:
                hashtag_text = hashtag['text']
                if hashtag_text in hashtag_counts:
                    hashtag_counts[hashtag_text] += 1
                else:
                    hashtag_counts.update({hashtag_text:1})
print("TOP 10 hashtags:")
sorted_hashtag_counts = sorted(hashtag_counts.items(),key = operator.itemgetter(1),reverse=True)
for shc in sorted_hashtag_counts[:20]:
    print(shc[0], " : ",shc[1])