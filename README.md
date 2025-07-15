# eBirders PT

eBirders PT is a Django-based web site that publishes data from eBird Portugal 
in a birder-friendly form.

## Overview

The Cornell Laboratory of Ornithology in Ithaca, New York runs the eBird database
which collects observations of birds from all over the world. The eBird web [site](https://ebird.org)
is great, but the information of most interest to birders is not always easy to 
find. eBirders PT uses the eBird [API](https://documenter.getpostman.com/view/664302/S1ENwy59) to publish the observations submitted
for Portugal so everyone can easily find out what has been seen in the different
regions of the country, and where are the best places to go birding.

Apart from the translations, the site is not specific to Portugal, and can be used
for any country or region. The site is a regular Django web site, so it is easy to 
adapt, to add or remove features, as you see fit.

## Getting Started

To get started, you will need to [sign up](https://secure.birds.cornell.edu/identity/account/create) 
for an eBird account, if you don't already have one and [register](https://ebird.org/data/download) to get an 
API key. Make sure you read and understand the [Terms of use](https://www.birds.cornell.edu/home/ebird-api-terms-of-use/), and remember 
bandwidth and servers cost money, so don't abuse the service.

Next, get a copy of the repository:

    git clone https://git.sr.ht/~smackay/ebirders-pt
    cd ebirders-pt

Create the virtual environment:

    uv venv

Activate it:

    source .venv/bin/activate

Install the requirements:

    uv sync

Create a copy of the .env.example file and add your API key and map the 
languages of your site to the locales used by eBird for species names:

    cp .env.example .env

For example:

    EBIRD_API_KEY=<my api key>
    EBIRD_LOCALES="{"en":"en_HBW","fr":"fr_CA"}"

This Canadian site serves pages in English and French, with the common names
of species in the English-language version taken from the Handbook of Birds
of the World.

Be sure to also change the CACHE_URL and DATABASE_URL entries to match your 
setup. The site is developed and tested with PostgreSQL, but it should also
work with SQLite, however, you will need to install it with the JSON1 extension.

Run the database migrations:

    python manage.py migrate

Create an admin user:

    python manage.py createsuperuser

Now, download data from the API:

    python manage.py add_checklists --days 2 US-NY-109

This loads all the checklists, submitted in the past two days by birders
in Tompkins County, New York, where the Cornell Lab is based. You can use
any location code used by eBird, whether it's for a country, state/region,
or county. Remember, read the [Terms of use](https://www.birds.cornell.edu/home/ebird-api-terms-of-use/).

It's time to start the server:

    python manage.py runserver

Finally, visit the home page to view the checklists:

    http://localhost:8000/

## Production Sites
Web sites using this project:

* https://www.ebirders.pt

## Project Information

* Issues: https://todo.sr.ht/~smackay/ebirders-pt
* Repository: https://git.sr.ht/~smackay/ebirders-pt
* Announcements: https://lists.sr.ht/~smackay/ebirders-announce
* Discussions: https://lists.sr.ht/~smackay/ebirders-discuss
* Development: https://lists.sr.ht/~smackay/ebirders-devel

The app is tested on Python 3.8+, and officially supports Django 4.2, 5.0 and 5.1.

eBirders PT is released under the terms of the [MIT](https://opensource.org/licenses/MIT) license.
