# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = T("See yourself in the world's eyes!")

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Radu Ioan fericean'
response.meta.description = 'The place to see how beautiful you are'
response.meta.keywords = 'beauty, miss, mister, contest'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

response.menu = [
    (T('Home'), False, URL('default','index'), [])
    ]
