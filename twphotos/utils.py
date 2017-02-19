import os
import requests


def download(media_url, size, outdir, download_name, file_naming):
    file_type = media_url[-3:]
    if file_type == "mp4":
        download_url = media_url
    else:
        download_url = media_url + ':' + size
    r = requests.get(download_url, stream=True)
    if file_naming:
        bs = download_name + "." + file_type
    else:
        bs = os.path.basename(media_url)
    filename = os.path.join(outdir or '', bs)
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)
    return filename


def create_directory(d):
    if not os.path.exists(d):
        os.makedirs(d)
