# -*- coding: utf-8 -*-

from mt2tumblr import parser, tumblr
import urlparse
import urllib
import config

if __name__ == '__main__':
    posts = parser.parse_file(config.PARSE_FILE_PATH)
    for post in posts:
        print post['date'], len(post['body'])
        print ' title:\t', post['title']
        print '  tags:\t', post['tags']
        print

    client = tumblr.TumblrClient(config)
    request_token = client.request_token

    print '----------------'
    print 'open in browser:' + client.get_auth_url(request_token)
    oauth_verifier = raw_input('oauth_verifier:')

    access_token = client.get_access_token(request_token, oauth_verifier)
    tumblr_client = client.get_client(access_token)
    url = 'http://api.tumblr.com/v2/blog/%s/post' % config.BASE_HOSTNAME
    for post in posts:
        params = {
            'type': config.POST_TYPE,
            'state': config.POST_STATE,
            'title': post['title'].encode('utf-8'),
            'body': post['body'].encode('utf-8'),
            'tags': post['tags'].encode('utf-8'),
            'date': post['date']}
        resp, content = tumblr_client.request(url, method='POST', body=urllib.urlencode(params))
        print post['date'], post['title'], content

