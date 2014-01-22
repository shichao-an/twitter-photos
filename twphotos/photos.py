import twitter
from .settings import (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
                       ACCESS_TOKEN_SECRET, COUNT_PER_GET)


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
            all photos
        :param since_id: Number of tweets to try and retrieve. If None, return
            all photos
        """

        return self.get_once(count=count, since_id=since_id)

    def get_once(self, count=None, max_id=None, since_id=None):
        statuses = self.api.GetUserTimeline(screen_name=self.user,
                                            count=count or COUNT_PER_GET,
                                            max_id=max_id,
                                            since_id=since_id,
                                            exclude_replies=True)
        if statuses:
            min_id = statuses[-1].id
        photos = [
            s.media[0]['id'] for s in statuses if s.media
        ]

        if statuses and count is None:
            return photos + self.get_once(count=None,
                                          max_id=min_id - 1,
                                          since_id=since_id)
        else:
            return photos

    def download(self, size=None):
        pass

    def verify_credentials(self):
        return self.api.VerifyCredentials()


def main():
    twphotos = TwitterPhotos()
    twphotos.verify_credentials()
    p = twphotos.get(since_id=None)
    print p
    print len(p)
