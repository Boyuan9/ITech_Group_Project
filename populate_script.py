import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page

def populate():
# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories.
# This might seem a little bit confusing, but it allows us to iterate
# through each data structure, and add the data to our models.

    Anime_pages = [
        {'title': 'Jujutsu Kaisen',
         'url':'http://docs.python.org/3/tutorial/',
         'views':99,
         'img':'images/jks.png'},
        {'title':'Nomad: Megalo Box 2',
         'url':'http://www.greenteapress.com/thinkpython/',
         'views':59,
         'img':'images/nomad.png'},
        {'title':'Kobayashi-san Chi no Maid Dragon S',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views':95,
         'img':'images/drgm.png'},
         {'title':'SSSS.Dynazenon',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views':95,
         'img':'images/ssss.png'} ]

    Comics_pages = [
        {'title':'One Piece',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views':29,
         'img':'images/op.png'},
        {'title':'One Punch-Man',
         'url':'http://www.djangorocks.com/',
         'views':51,
         'img':'images/opm.png'},
        {'title':'Fullmetal Alchemist',
         'url':'http://www.tangowithdjango.com/',
         'views':71,
         'img':'images/fa.png'} ]

    Games_pages = [
        {'title':'Dead Cells',
         'url':'http://bottlepy.org/docs/dev/',
         'views':44,
         'img':'images/dc.png'},
        {'title':'Monster Hunter: World',
         'url':'http://flask.pocoo.org',
         'views':67,
         'img':'images/mhw.png'} ]

    cats = {'Anime': {'pages': Anime_pages,'views':128,'likes':64},
            'Comics': {'pages': Comics_pages,'views':64,'likes':32},
            'Games': {'pages': Games_pages,'views':32,'likes':16} }
    
# If you want to add more categories or pages,
# add them to the dictionaries above.

# The code below goes through the cats dictionary, then adds each category,
# and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['views'],cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'],p['views'],p['img'])

# Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views, img):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.img=img
    p.save()
    return p

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()