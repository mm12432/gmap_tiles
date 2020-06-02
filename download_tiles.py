#!/usr/bin/python

import urllib.request as urllib2
import os, sys
from gmap_utils import *

import time
import random


def download_tiles(zoom,
                   lat_start,
                   lat_stop,
                   lon_start,
                   lon_stop,
                   satellite=True):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    headers = {'User-Agent': user_agent}
    for z in zoom:
        start_x, start_y = latlon2xy(z, lat_start, lon_start)
        stop_x, stop_y = latlon2xy(z, lat_stop, lon_stop)
        print("x range", start_x, stop_x)
        print("y range", start_y, stop_y)
        for x in range(start_x, stop_x):
            for y in range(start_y, stop_y):

                url = None
                filename = None

                if satellite:
                    url = "http://khm1.google.com/kh?v=87&hl=en&x=%d&y=%d&z=%d" % (
                        x, y, z)
                    filename = "%d_%d_%d_s.jpg" % (z, x, y)
                else:
                    url = "http://mt1.google.cn/vt/lyrs=s&hl=zh-CN&x=%d&y=%d&z=%d&s=Gali" % (
                        x, y, z)
                    filename = "%d_%d_%d_r.png" % (z, x, y)

                if not os.path.exists(filename):

                    bytes = None

                    try:
                        req = urllib2.Request(url, data=None, headers=headers)
                        response = urllib2.urlopen(req)
                        bytes = response.read()


                    except Exception as e:
                        print("error", filename, "->", e)
                        continue
                        # sys.exit(1)
                    #if bytes.startswith("<html>"):
                    #     print("-- forbidden", filename)
                    #     sys.exit(1)
                    print("-- saving", filename)
                    f = open(filename, 'wb')
                    f.write(bytes)
                    f.close()

                    # time.sleep(1 + random.random())


if __name__ == "__main__":

    zoom = range(8, 11)

    lat_start, lon_start = 85.05112877980659, -180
    lat_stop, lon_stop = -85.05112877980659, 180

    download_tiles(zoom,
                   lat_start,
                   lat_stop,
                   lon_start,
                   lon_stop,
                   satellite=False)
