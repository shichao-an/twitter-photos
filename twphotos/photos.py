from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
import os
import requests
import twitter
from .settings import (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
                       ACCESS_TOKEN_SECRET, COUNT_PER_GET, MEDIA_SIZES)


class TwitterPhotos(object):
    def __init__(self, user=None, list_slug=None, outdir=None):
        """
        :param user: The screen_name of the user whom to return results for
        :param list_slug: The slug identifying the list owned by the `user`
        :param outdir: The output directory
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

        self.photos = self.get_once(count=count, since_id=since_id)
        return self.photos

    def get_once(self, count=None, max_id=None, since_id=None, photos=[]):
        statuses = self.api.GetUserTimeline(screen_name=self.user,
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
        for photo in self.photos:
            r = requests.get(photo[1] + ':' + size, stream=True)
            bs = os.path.basename(photo[1])
            if self.outdir is not None:
                filename = os.path.join(self.outdir, bs)
            else:
                filename = bs
            with open(filename, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=1024):
                    fd.write(chunk)

    def verify_credentials(self):
        return self.api.VerifyCredentials()


def main():
    twphotos = TwitterPhotos()
    twphotos.verify_credentials()
    p = twphotos.get(count=20, since_id=None)
    twphotos.download()
