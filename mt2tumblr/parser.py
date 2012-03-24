#coding: utf-8

import re
import time
import datetime

def jst2gmt(date_str): 
    t = time.strptime(date_str, '%m/%d/%Y %H:%M:%S %p')
    gmt = datetime.datetime.fromtimestamp(time.mktime(t) - (9 * 60 * 60))
    return gmt.strftime('%Y-%m-%d %H:%M:%S GMT')

def parse_post(lines):
    header_names = {
        'DATE'     : 'date',
        'BASENAME' : 'slug',
        'TITLE'    : 'title',
        'CATEGORY' : 'tags',
    }
    exp = re.compile('^([^:]+): (.+)$')
    postdata = {'tags':[]}
    elements = lines.split('-----\n')
    if len(elements) < 2:
        return None
    headers = elements[0]
    body = elements[1]
    for line in headers.splitlines():
        matched = exp.search(line)
        if matched:
            (k, v) = matched.groups()
            if k in header_names.keys():
                if k == 'CATEGORY':
                    postdata[header_names[k]].append(v.decode('utf-8'))
                else:
                    if k == 'DATE':
                        v = jst2gmt(v)
                    if k == 'TITLE':
                        v = v.decode('utf-8')
                    postdata[header_names[k]] = v
    postdata['tags'] = u','.join(postdata['tags'])
    postdata['body'] = u'\n'.join([ s.strip().decode('utf-8') for s in body.splitlines()[2:]])
    return postdata

def parse_file(filename):
    posts = []
    with open(filename, 'r') as file:
        buffers = []
        for line in file.readlines():
            if line == '--------\n':
                post = parse_post('\n'.join(buffers))
                if post:
                    posts.append( post )
                    buffers = []
            else:
                buffers.append(line)
        if len(buffers):
            post = parse_post('\n'.join(buffers))
            if post:
                posts.append( parse_post('\n'.join(buffers)) )
    return posts

