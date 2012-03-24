# -*- coding: utf-8 -*-
 
import oauth2
import urlparse
import urllib
 
class TumblrClient(object):

    def __init__(self, config):
        self.config = config
        self.base_hostname = config.BASE_HOSTNAME
        self.consumer = oauth2.Consumer(key=config.CONSUMER_KEY, secret=config.CONSUMER_SECRET)

    @property
    def request_token(self):
        client = oauth2.Client(self.consumer)
        resp, content = client.request(self.config.REQUEST_TOKEN_URL + '?' + urllib.urlencode(dict(oauth_callback='http://localhost:4000/')), 'GET')
        return dict(urlparse.parse_qsl(content))

    def get_auth_url(self, request_token):
        return '%s?oauth_token=%s' % (self.config.AUTHORIZE_URL, request_token['oauth_token'])

    def get_access_token(self, request_token, oauth_verifier):
        token = oauth2.Token(request_token['oauth_token'],
                             request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth2.Client(self.consumer, token)
        (response, content) = client.request(self.config.ACCESS_TOKEN_URL, 'POST')
        if response['status'] == '200':
            return dict(urlparse.parse_qsl(content))

    def get_client(self, access_token):
        token = oauth2.Token(key=access_token['oauth_token'],
                             secret=access_token['oauth_token_secret'])
        return oauth2.Client(self.consumer, token)

    def posting(self, posts):
        url = 'http://api.tumblr.com/v2/blog/%s/post' % BASE_HOSTNAME
        client = get_client()
        for post in posts:
            params = {
                'type': 'text',
                'state': 'published',
                'title': post['title'].encode('utf-8'),
                'body': post['body'].encode('utf-8'),
                'tags': post['tags'].encode('utf-8'),
                'date': post['date']}
            resp, content = client.request(url, method='POST', body=urllib.urlencode(params))
            print resp, content

