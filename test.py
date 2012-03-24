# -*- coding: utf-8 -*-
import config
import urllib
import urlparse
import oauth2
import mt2tumblr
from mt2tumblr import parser
from mt2tumblr import tumblr

import unittest

class TestParser(unittest.TestCase):
    def test_parse_post(self):
        post_str = """
AUTHOR: restartr
TITLE: テスト投稿2
STATUS: Publish
ALLOW COMMENTS: 1
CONVERT BREAKS: 1
ALLOW PINGS: 1
DATE: 03/20/2012 21:29:10 PM
CATEGORY: test
CATEGORY: scala
-----
BODY:

		<div class="section">
			<p>テスト</p>
			<p>ScalaとPython。</p>
		</div>

"""
        post = parser.parse_post(post_str)
        print post
        if post:
            self.assertTrue( 'title' in post.keys() )
            self.assertTrue( 'date' in post.keys() )
            self.assertTrue( 'body' in post.keys() )
            self.assertTrue( 'tags' in post.keys() )
            self.assertTrue( post['tags'], list )

    def test_parse_file(self):
        posts = parser.parse_file('./resources/sample_mt.txt')
        for post in posts:
            self.assertTrue(isinstance(post, dict))

class TestTumblrClient(unittest.TestCase):
    def setUp(self):
        self.client = tumblr.TumblrClient(config)

    def test_request_token(self):
        request_token = self.client.request_token
        self.assertTrue( 'oauth_token' in request_token )
        self.assertTrue( 'oauth_token_secret' in request_token )
        self.assertTrue( 'oauth_callback_confirmed' in request_token )

    def test_get_auth_url(self):
        request_token = self.client.request_token
        url = self.client.get_auth_url(request_token)
        self.assertTrue( url.startswith('http://www.tumblr.com/oauth/authorize?oauth_token=') )

    def test_access_token(self):
        """
        comment out if you don't want to run this test
        """
        request_token = self.client.request_token
        print '----------------'
        print 'open in browser:' + self.client.get_auth_url(request_token)
        oauth_verifier = raw_input('oauth_verifier:')
        access_token = self.client.get_access_token(request_token, oauth_verifier)
        client = self.client.get_client(access_token)
        self.assertTrue( isinstance(client, oauth2.Client) )

    def test_post(self):
        """
        comment out if you don't want to run this test
        """
        request_token = self.client.request_token
        print '----------------'
        print 'open in browser:' + self.client.get_auth_url(request_token)
        oauth_verifier = raw_input('oauth_verifier:')
        access_token = self.client.get_access_token(request_token, oauth_verifier)
        client = self.client.get_client(access_token)
        url = 'http://api.tumblr.com/v2/blog/%s/post' % config.BASE_HOSTNAME
        postdata = {'type' : 'text',
                    'state' : 'draft',
                    'title' : 'test post',
                    'body' : u'happy new year!!!',
                    'date' : '2012-01-01 00:00:00 GMT'}
        (response, content)= client.request(url, method='POST', body=urllib.urlencode(postdata))
        self.assertEqual( response['status'], '200' )

if __name__ == '__main__':
    config.PARSE_FILE_PATH='./resources/sample_mt.txt'
    config.POST_STATE = 'draft'

    unittest.main()

