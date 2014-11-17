import pytumblr
import datetime
import os
import configparser


def make_client():
    config = configparser.ConfigParser()
    config.read('creds.ini')
    consumer_key = config['oauth']['consumer_key']
    consumer_secret = config['oauth']['consumer_secret']
    oauth_token = config['oauth']['oauth_token']
    oauth_secret = config['oauth']['oauth_secret']
    return pytumblr.TumblrRestClient(
        consumer_key, 
        consumer_secret,
        oauth_token,
        oauth_secret,
    )

def getAllPosts (client, blog):
    offset = 0
    while True:
        post_response = client.posts(blog, limit=20, offset=offset, filter="text", type="text")
        if len(post_response.get('posts')) is 0:
            return

        for posts in post_response['posts']:
            yield posts

        offset += 20

def any_keyword_in(keywords, string):
    for keyword in keywords:
        if keyword in string:
            return True
    return False

def search(keywords, client, tumblr_url, write_to_datefile=False):
    if not isinstance(keywords, list):
        raise Exception("search keywords must be a list")

    for post in getAllPosts(client, tumblr_url):
        body = post.get('body', "not text").encode("utf-8")
        # think this is right
        timestamp = post.get('timestamp')
        if timestamp:
            post_date = datetime.datetime.fromtimestamp(timestamp).strftime('%F')
            # append date we're on to this file to get an idea of progress/time left
            if write_to_datefile:
                # optionally write the date of current post to a file
                with open('dateSearchIsOn', 'a') as f:
                    f.write(post_date + "\n")

         # if any(['blueball' in lbody, 'blue ball' in lbody, 'dear white people' in lbody]):
        if any_keyword_in(keywords, body.lower()):
            print post.get('post_url')
            print body

def main():
    client = make_client()
    search(["fast"], client, "pythonsweetness.tumblr.com")

if __name__ == "__main__":
    main()
