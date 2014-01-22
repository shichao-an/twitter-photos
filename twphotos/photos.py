# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals, absolute_import
import os
import twitter
from .settings import (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
                       ACCESS_TOKEN_SECRET, COUNT_PER_GET, MEDIA_SIZES)
from .utils import download, create_directory


class TwitterPhotos(object):
    def __init__(self, user=None, list_slug=None, outdir=None):
        """
        :param user: The screen_name of the user whom to return results for
        :param list_slug: The slug identifying the list owned by the `user`
        :param outdir: The output directory (absolute path)
        """
        self.user = user
        self.list_slug = list_slug
        self.outdir = outdir
        self.api = twitter.Api(consumer_key=CONSUMER_KEY,
                               consumer_secret=CONSUMER_SECRET,
                               access_token_key=ACCESS_TOKEN,
                               access_token_secret=ACCESS_TOKEN_SECRET)

    def get(self, count=None, since_id=None):
        """
        Get all photos from the user or members of the list
        :param count: Number of tweets to try and retrieve. If None, return
            all photos since `since_id`
        :param since_id: An integer specifying the oldest id
        """
        self.auth_user = self.verify_credentials().screen_name
        self.photos = {}
        for user in self.users:
            self.photos[user] = self.get_once(user=user,
                                              count=count,
                                              since_id=since_id)
        return self.photos

    def get_once(self, user=None, count=None, max_id=None,
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
            return self.get_once(count=None,
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
            d = create_directory(os.path.join(self.outdir, user))
            for photo in self.photos[user]:
                photos = self.photos[user]
                media_url = photo[1]
                download(media_url, size, d)

    @property
    def users(self):
        members = None
        if self.list_slug:
            owner = self.user or self.auth_user
            print (owner)
            print (self.list_slug)
            _members = self.api.GetListMembers(list_id=None,
                                               slug=self.list_slug,
                                               owner_screen_name=owner)
            members = [member.screen_name for member in _members]
        else:
            members = [self.auth_user]
        return members

    def verify_credentials(self):
        return self.api.VerifyCredentials()


def main():
    twphotos = TwitterPhotos(list_slug='h')
    p = twphotos.get(count=20, since_id=None)
    print (p)
