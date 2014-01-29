# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
import atexit
import os
import sys
# Import .settings before twitter due to local development of python-twitter
from .settings import (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
                       ACCESS_TOKEN_SECRET, COUNT_PER_GET, MEDIA_SIZES)
from .utils import download, create_directory
from .command import parse_args
import twitter


class TwitterPhotos(object):
    def __init__(self, user=None, list_slug=None, outdir=None, num=None):
        """
        :param user: The screen_name of the user whom to return results for
        :param list_slug: The slug identifying the list owned by the `user`
        :param outdir: The output directory (absolute path)
        :param num: Number of most recent photos to download from each
            related user
        """
        self.user = user
        self.list_slug = list_slug
        self.outdir = outdir
        self.num = num
        self.api = twitter.Api(consumer_key=CONSUMER_KEY,
                               consumer_secret=CONSUMER_SECRET,
                               access_token_key=ACCESS_TOKEN,
                               access_token_secret=ACCESS_TOKEN_SECRET)
        self.photos = {}
        self._downloaded = 0
        self._total = 0

    def get(self, count=None, since_id=None):
        """
        Get all photos from the user or members of the list
        :param count: Number of tweets to try and retrieve. If None, return
            all photos since `since_id`
        :param since_id: An integer specifying the oldest id
        """
        print('Retrieving photos from Twitter API...')
        self.auth_user = self.verify_credentials().screen_name
        for user in self.users:
            photos = self.load(user=user,
                               count=count,
                               since_id=since_id)
            self.photos[user] = photos[:self.num]
            self._total += len(self.photos[user])
        return self.photos

    def load(self, user=None, count=None, max_id=None,
             since_id=None, photos=[]):
        statuses = self.api.GetUserTimeline(screen_name=user,
                                            count=count or COUNT_PER_GET,
                                            max_id=max_id,
                                            since_id=since_id,
                                            exclude_replies=True)
        if statuses:
            min_id = statuses[-1].id

        fetched_photos = [
            (s.media[0]['id'],
             s.media[0]['media_url']) for s in statuses
            if s.media and s.media[0]['type'] == 'photo'
        ]

        if statuses and count is None:
            return self.load(count=None,
                             max_id=min_id - 1,
                             since_id=since_id,
                             photos=photos + fetched_photos)
        else:
            return photos + fetched_photos

    def download(self, size=None):
        if size is None:
            size = 'large'
        if size not in MEDIA_SIZES:
            raise Exception('Invalid media size %s' % size)
        for user in self.photos:
            d = os.path.join(self.outdir or '', user)
            # Create intermediate directory
            create_directory(d)
            for photo in self.photos[user]:
                media_url = photo[1]
                self._print_progress(user, media_url)
                download(media_url, size, d)
                self._downloaded += 1

    @property
    def users(self):
        members = None
        if self.list_slug:
            owner = self.user or self.auth_user
            _members = self.api.GetListMembers(list_id=None,
                                               slug=self.list_slug,
                                               owner_screen_name=owner)
            members = [member.screen_name for member in _members]
        else:
            if self.user:
                members = [self.user]
            else:
                members = [self.auth_user]
        return members

    def verify_credentials(self):
        return self.api.VerifyCredentials()

    def print_urls(self):
        for user in self.photos:
            photos = self.photos[user]
            for photo in photos:
                line = '%s %s %s' % (user, photo[0], photo[1])
                print(line)

    def _get_progress(self, user, media_url):
        m = 'Downloading %(media_url)s from %(user)s: %(index)s/%(total)s'
        d = {
            'media_url': os.path.basename(media_url),
            'user': user,
            'index': self._downloaded + 1,
            'total': self._total,
        }
        msg = m % d
        return msg

    def _print_progress(self, user, media_url):
        sys.stdout.write('\r%s' % self._get_progress(user, media_url))
        sys.stdout.flush()


def new_line():
    sys.stdout.write('\n')


def main():
    args = parse_args()
    twphotos = TwitterPhotos(user=args.user,
                             list_slug=args.list_slug,
                             outdir=args.outdir,
                             num=args.num)
    twphotos.verify_credentials()
    twphotos.get()
    # Print only scree_name, tweet id and media_url
    if args.print:
        twphotos.print_urls()
    else:
        twphotos.download()


# Register cleanup functions
atexit.register(new_line)
