Twitter Photos
==============
Twitter Photos is a command-line tool to get photos from Twitter accounts.

Requirements
------------

* python-twitter
* requests
* urllib3

Installation
------------

You can install the package with pip::

  $ pip install twitter-photos

Or, you can download a source distribution and install with these commands::

  $ python setup.py install

Setup
-----

Create a config file at ~/.twphotos specifying your Twitter credentials::

    [credentials]
    consumer_key = your_consumer_key
    consumer_secret = your_consumer_secret
    access_token_key = your_access_token_key
    access_token_secret = your_access_token_secret


Usage
-----
The simplest usage is to run "twphotos" from command-line without any options. This will download all photos from the current authenticated user (you)::

    $ twphotos

Download all photos from an existing user other yourself with ``-u`` option followed by username::

    $ twphotos -u wired

Download `n` most recent photos from a user using ``-n`` followed by number::

    $ twphotos -u wired -n 20

Download photos to a directory other than the current one::

    $ twphotos -u wired -o /path/to/dir

Enable "incremental download" to download the new photos since the last downloads with ``-i``::

    $ twphotos -u wired -i

Enable "parallel download" to speedup the downloads using the ``-r`` switch::

    $ twphotos -u wired -r

Print username, tweet ids, and URLs instead of downloading them with ``-p`` switch::

    $ twphotos -u wired -p

You can retrieve only the URLs with ``cut`` command::

    $ twphotos -u wired -p | cut -d ' ' -f3

Command-line Options
~~~~~~~~~~~~~~~~~~~~
The "soundmeter" command accepts the following options:

  -u USER, --user USER  user account
  -l LIST_SLUG, --list LIST_SLUG
                        list slug with --user as list owner
  -o OUTDIR, --outdir OUTDIR
                        output directory
  -p, --print           print media urls and tweet ids instead of download
  -r, --parallel        enable parallel download
  -n NUM, --num NUM     number of most recent photos to download
  -i, --increment       download only new photos since last download
