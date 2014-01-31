import os
import Queue
import threading
import sys
import urllib3
from .settings import PROGRESS_FORMATTER, NUM_THREADS


pool_manager = urllib3.PoolManager()
photo_queue = Queue.Queue()
lock = threading.Lock()
downloaded = 0


def parallel_download(photos, user, size, outdir):
    threads = []
    # Put photos into `photo_queue`
    for photo in photos:
        photo_queue.put(photo)

    thread_pool = [
        threading.Thread(
            target=worker,
            args=(photo_queue, user, size, outdir, len(photos))
        ) for i in range(NUM_THREADS)
    ]

    for t in thread_pool:
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def worker(queue, user, size, outdir, total):
    while True:
        try:
            photo = queue.get(False)
        except Queue.Empty:
            break
        media_url = photo[1]
        urllib3_download(media_url, size, outdir)
        with lock:
            global downloaded
            downloaded += 1
            d = {
                'media_url': os.path.basename(media_url),
                'user': user,
                'index': downloaded + 1 if downloaded < total else total,
                'total': total,
            }
            progress = PROGRESS_FORMATTER % d
            sys.stdout.write('\r%s' % progress)
            sys.stdout.flush()


def urllib3_download(media_url, size, outdir):
    r = pool_manager.request('GET', media_url + ':' + size)
    bs = os.path.basename(media_url)
    filename = os.path.join(outdir or '', bs)
    with open(filename, 'wb') as fd:
        fd.write(r.data)
    return filename
