
import from movable type data to tumblr
====

setup
----
* install  requirements

> pip oauth2

* register application

  * access [http://www.tumblr.com/oauth/apps].
  * register application
  * copy consumer_key and consumer_secret.

* write your consumer_key and consumer_secret to config.py 

> CONSUMER_KEY = '<consumer_key>'
> CONSUMER_SECRET = '<consumer_secret>'
> BASE_HOSTNAME = '<your_tumblr_url>'

usage
----

> python ./run.py

 
