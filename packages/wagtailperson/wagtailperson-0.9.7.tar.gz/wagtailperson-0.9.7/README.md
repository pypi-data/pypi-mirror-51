Wagtail Person
==============

Add a person and a persons index pages to Wagtail as well as a person
block for StreamFields. This app provide a basic CSS and templates, feel
free to customize it.


Install
-------

Simply install it from pypi.org:

``` {.bash}
pip install wagtailperson
```

Add this app to django installed app in your settings.py:

``` {.python}
INSTALLED_APPS = [
    # …
    'wagtailperson',
    # …
    ]
```

Then, finally, apply migration scripts:

``` {.bash}
./manage.py migrate wagtailperson
```


Use
---

This application provide 2 pages models:

-   A person page: Represent someone, can be used mostly everywhere in
    the pages tree
-   A person index page: A root page for persons pages, it list each of
    person it had as children pages and can only have person pages as
    children

The person index page can be useful to group persons, globally or per
group.

A person page got multiple fields:
-   Name
-   Picture
-   Titles
-   Introduction
-   Abstract
-   Extra informations

This application also provide a person block for StreamField at
`wagtailperson.blocks.PersonBlock`. Feel free to use it on your models
StreamField.


Development
-----------

The source code repository provide a full Django project, so you can
easily work with wagtailperson for testing you modifications.

Simply use these two steps in the source code working directory:

``` {.bash}
./manage.py migrate
./manage.py runserver
```


Licence
-------

LGPLv3


Author
------

Sébastien Gendre \<seb\@k-7.ch\>
