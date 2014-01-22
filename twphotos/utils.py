import os
import requests


def download(media_url, size, outdir):
    r = requests.get(media_url + ':' + size, stream=True)
    bs = os.path.basename(media_url)
    filename = os.path.join(outdir or '', bs)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)
    return filename


def create_directory(d):
    if not os.path.exists(d):
        os.makedirs(d)
