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
         'info':"Idly indulging in baseless paranormal activities with the Occult Club, high schooler Yuuji Itadori spends his days at either the clubroom or the hospital, where he visits his bedridden grandfather. However, this leisurely lifestyle soon takes a turn for the strange when he unknowingly encounters a cursed item. Triggering a chain of supernatural occurrences, Yuuji finds himself suddenly thrust into the world of Curses—dreadful beings formed from human malice and negativity—after swallowing the said item, revealed to be a finger belonging to the demon Sukuna Ryoumen, the 'King of Curses'.",
         'rating': 5,
         'img':'images/jks.png'},
        {'title':'Nomad: Megalo Box 2',
         'url':'http://www.greenteapress.com/thinkpython/',
         'views':59,
         'info':"Megalo Box is an advanced form of boxing where competitors wear metal frames called Gear. When the first ever Megalonia tournament took place, 'Gearless' Joe became its champion and known to all as a legendary fighter. However, soon after, he lost an exhibition match against the second champion and vanished from the public eye.",
         'rating': 5,
         'img':'images/nomad.png'},
        {'title':'Kobayashi-san Chi no Maid Dragon S',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views':95,
         'info':"As Tooru continues on her quest to become the greatest maid and Kanna Kamui fully immerses in her life as an elementary school student, there is not a dull day in the Kobayashi household with mischief being a daily staple. On one such day, however, a massive landslide is spotted on the hill where Kobayashi and Tooru first met—a clear display of a dragon's might. When none of the dragons they know claim responsibility, the perpetrator herself descends from the skies: Ilulu, the radical Chaos Dragon with monstrous power rivaling that of Tooru.",
         'rating': 3,
         'img':'images/drgm.png'},
         {'title':'SSSS.Dynazenon',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views':95,
         'info':"One day after school, first-year high school student Yomogi Asanaka comes across a starving man under a bridge. Introducing himself as Gauma, the strange drifter informs Yomogi that he is a 'kaiju user,' a person who deals with the 'kaiju'—monsters who bring harm to the city and its citizens.",
         'rating': 4,
         'img':'images/ssss.png'} ]

    Comics_pages = [
        {'title':'One Piece',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views':29,
         'info':"One Piece is the highest selling manga series of all time, with over 480 million copies in circulation as of February 2021. Volume 67 of the series currently holds the record for highest first print run of any manga (including books) of all time in Japan, with 4.05 million in 2012. The series was a finalist for the Tezuka Osamu Cultural Prize three times in a row from 2000 to 2002. In 2012, it won the 41st Japan Cartoonists Association Award Grand Prize, alongside Kimuchi Yokoyama's Neko Darake.",
         'rating': 5,
         'img':'images/op.png'},
        {'title':'One Punch-Man',
         'url':'http://www.djangorocks.com/',
         'views':51,
         'info':"One Punch-Man is the manga remake of the original web comic by ONE. In 2014, the series was nominated for the 7th annual Manga Taishou Award and was ranked 7th place.",
         'rating': 4,
         'img':'images/opm.png'},
        {'title':'Fullmetal Alchemist',
         'url':'http://www.tangowithdjango.com/',
         'views':71,
         'info':"Alchemists are knowledgeable and naturally talented individuals who can manipulate and modify matter due to their art. Yet despite the wide range of possibilities, alchemy is not as all-powerful as most would believe. Human transmutation is strictly forbidden, and whoever attempts it risks severe consequences. Even so, siblings Edward and Alphonse Elric decide to ignore this great taboo and bring their mother back to life. Unfortunately, not only do they fail in resurrecting her, they also pay an extremely high price for their arrogance: Edward loses his left leg and Alphonse his entire body. Furthermore, Edward also gives up his right arm in order to seal his brother's soul into a suit of armor.",
         'rating': 3,
         'img':'images/fa.png'} ]

    Games_pages = [
        {'title':'Dead Cells',
         'url':'http://bottlepy.org/docs/dev/',
         'views':44,
         'info':"Dead Cells is a rogue-lite, metroidvania action-platformer. You'll explore a sprawling, ever-changing castle... assuming you’re able to fight your way past its keepers in 2D souls-lite combat. No checkpoints. Kill, die, learn, repeat.",
         'rating': 5,
         'img':'images/dc.png'},
        {'title':'Monster Hunter: World',
         'url':'http://flask.pocoo.org',
         'views':67,
         'info':"In Monster Hunter: World you assume the role of a hunter venturing to a new continent where you track down and slay ferocious beasts in heart-pounding battles. This new land and its diverse inhabitants play a critical role in each quest as you strategically use the surrounding environment including terrain, vegetation and wildlife to your advantage in battle or become hindered by the hazards they present. As a hunter, you must use your cunning and expertise to track and maneuver your targets throughout the intense, evolving battles. [Capcom]",
         'rating': 5,
         'img':'images/mhw.png'} ]

    cats = {'Anime': {'pages': Anime_pages,'views':128,'likes':64, 'info':'View the most popular animations','img':'images/anime.png'},
            'Comics': {'pages': Comics_pages,'views':64,'likes':32, 'info':'View the most popular comics','img':'images/comic.png'},
            'Games': {'pages': Games_pages,'views':32,'likes':16, 'info':'View the most popular games','img':'images/game.png'} }
    
# If you want to add more categories or pages,
# add them to the dictionaries above.

# The code below goes through the cats dictionary, then adds each category,
# and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data['views'],cat_data['likes'],cat_data['info'],cat_data['img'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'],p['views'],p['img'],p['info'],p['rating'])

# Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views, img,info,rating):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.info = info
    p.img=img
    p.rating = rating
    p.save()
    return p

def add_cat(name,views,likes,info,img):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.info = info
    c.img = img
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()