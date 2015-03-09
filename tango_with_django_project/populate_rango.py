import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    python_cat = add_cat('Python',128,64)

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        url="http://docs.python.org/2/tutorial/",views=10)

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        url="http://www.greenteapress.com/thinkpython/",views=15)

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        url="http://www.korokithakis.net/tutorials/python/",views=20)

    django_cat = add_cat("Django",64,32)

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/"
		views=30)

    add_page(cat=django_cat,
        title="Django Rocks",
        url="http://www.djangorocks.com/",views=14)

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/",views=18)

    frame_cat = add_cat("Other Frameworks",32,16)

    add_page(cat=frame_cat,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/",views=30)

    add_page(cat=frame_cat,
        title="Flask",
        url="http://flask.pocoo.org",views=40)

    My_cat = add_cat("Rajeevan",100,100)

    add_page(cat=My_cat,
        title="GitHub",
        url="https://github.com/2080123V/tangowithdjango.git"
		,views=35)
    add_page(cat=My_cat,
        title="PythonAnywhere",
        url="https://www.pythonanywhere.com/user/2080123V/consoles",
		views=27)

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]
    return p

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()