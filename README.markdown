Import the MovableType formated data to Tumblr
====

Setup
----

Install  requirements

    pip oauth2

Register application

  * access tumblr oauth page. ( http://www.tumblr.com/oauth/apps )
  * register application
  * copy consumer_key and consumer_secret.

Write your consumer_key and consumer_secret to config.py 

    CONSUMER_KEY = '<consumer_key>'
    CONSUMER_SECRET = '<consumer_secret>'
    BASE_HOSTNAME = '<your_tumblr_url>' # like '<your-id>.tumblr.com'


Put your movable type format file to "resources" directory, and edit config.py

    PARSE_FILE_PATH = 'path/to/movable_type_data.txt'

If you want to public post, change config as following.

    POST_STATE = 'publish'
    

Usage
----

    python ./run.py

And show as following

    open in browser:http://www.tumblr.com/oauth/authorize?oauth_token={OAUTH_TOKEN}
    oauth_verifier:

Access this url, and redirect the access.

Copy the oauth_verifier included in the redirected page url.

Paste it, and start to import.


