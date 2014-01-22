import os
import requests


def download(media_url, size, outdir):
    r = requests.get(media_url + ':' + size, stream=True)
    bs = os.path.basename(media_url)
    if outdir is not None:
        filename = os.path.join(outdir, bs)
    else:
        filename = bs
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)


def create_directory(d):
    if not os.path.exists(d):
        os.makedirs(d)
