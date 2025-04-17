# eBird Pages

eBird Pages is a Django-based web site that publishes data from eBird in a birder
friendly form.

## Overview

The Cornell Laboratory of Ornithology in Ithaca, New York runs the eBird database
which collects observations of birds from all over the world. The eBird web [site](https://ebird.org)
is great, but the information of most interest to birders is not always easy to 
find. eBird Pages uses the eBird [API](https://documenter.getpostman.com/view/664302/S1ENwy59) to publish observations, checklist,
and interesting statistics so you can find out what's been seen in your part of 
the world, where are the best places to go birding, and who are the eBirders 
finding the most interesting birds.

## Getting Started

To get started, you will need to [sign up](https://secure.birds.cornell.edu/identity/account/create) for an eBird account, if you don't 
already have one and [register](https://ebird.org/data/download) to get an API key. Make sure you read and 
understand the [Terms of use](https://www.birds.cornell.edu/home/ebird-api-terms-of-use/), and remember bandwidth and servers cost money, 
so don't abuse the service.

Next, get a copy of the repository:

    git clone https://git.sr.ht/~smackay/ebird-pages
    cd ebird-pages

Create the virtual environment:

    uv venv

Activate it:

    source venv/bin/activate

Install the requirements:

    uv sync

Run the database migrations:

    python manage.py migrate

Create an admin user:

    python manage.py createsuperuser

Create a copy of the .env.example file and add your API key:

    cp .env.example .env

For example:

    EBIRD_API_KEY=<my api key>

Now, download data from the API:

    python manage.py load_api new 2 US-NY-109

This loads all the checklists, submitted in the past two days by birders
in Tompkins County, New York, where the Cornell Lab is based. You can use
any location code used by eBird, whether it's for a country, state/region,
or county. Remember, read the [Terms of use](https://www.birds.cornell.edu/home/ebird-api-terms-of-use/).

It's time to start the server:

    python manage.py runserver

Finally, visit the home page to view the checklists:

    http://localhost:8000/

This project gives you a basic web site, which is reasonably well documented.
The source code will be simple to adapt if you are familiar with Django at any
skill level. The rest is up to you.

To see a real site, developed using this code-base, please visit, https://www.ebirders.pt

## Project Information

* Issues: https://todo.sr.ht/~smackay/ebird-pages
* Repository: https://git.sr.ht/~smackay/ebird-pages
* Announcements: https://lists.sr.ht/~smackay/ebirders-announce
* Discussions: https://lists.sr.ht/~smackay/ebirders-discuss
* Development: https://lists.sr.ht/~smackay/ebirders-devel

The app is tested on Python 3.8+, and officially supports Django 4.2, 5.0 and 5.1.

eBird Pages is released under the terms of the [MIT](https://opensource.org/licenses/MIT) license.

## Related Projects

* ebird-checklists: https://todo.sr.ht/~smackay/ebird-checklists - the core project
  one which eBird Pages is based. It contains all the code you need to set up a feed
  from the eBird API and load it into a database.

* ebird-notebooks: https://todo.sr.ht/~smackay/ebird-notebooks - a set of Jupyter 
  Notebooks that you can used to analyse data form the eBird API or the eBird Basic
  Dataset.

* ebird-api: https://todo.sr.ht/~smackay/ebird-api - a python library that you can
  use to download data from the eBird API.

* ebird-scrapers: https://todo.sr.ht/~smackay/ebird-scrapers - not everything is available
  from the eBird API. eBird Scrapers is library for extracting information from pages
  on the eBird web site.
