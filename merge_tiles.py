from PIL import Image
import sys, os
from gmap_utils import *


def merge_tiles(zoom,
                lat_start,
                lat_stop,
                lon_start,
                lon_stop,
                satellite=True):

    TYPE, ext = 'r', 'png'
    if satellite:
        TYPE, ext = 's', 'jpg'

    for z in zoom:
        x_start, y_start = latlon2xy(z, lat_start, lon_start)
        x_stop, y_stop = latlon2xy(z, lat_stop, lon_stop)

        print("x range", x_start, x_stop)
        print("y range", y_start, y_stop)

        w = (x_stop - x_start) * 256
        h = (y_stop - y_start) * 256

        print("width:", w)
        print("height:", h)

        result = Image.new("RGBA", (w, h))
        for x in range(x_start, x_stop):
            for y in range(y_start, y_stop):

                filename = "%d_%d_%d_%s.%s" % (z, x, y, TYPE, ext)

                if not os.path.exists(filename):
                    print("-- missing", filename)
                    continue
                x_paste = (x - x_start) * 256
                y_paste = h - (y_stop - y) * 256

                try:
                    i = Image.open(filename)
                except Exception as e:
                    print("-- %s, removing %s" % (e, filename))
                    trash_dst = os.path.expanduser("~/.Trash/%s" % filename)
                    os.rename(filename, trash_dst)
                    continue

                result.paste(i, (x_paste, y_paste))

                del i

        result.save("map_%s_%s.%s" % (z, TYPE, ext))


if __name__ == "__main__":

    if len(sys.argv == 6):
        try:
            zoom = range(float(sys.argv[0]), float(sys.argv[1]))
            lat_start, lon_start = float(sys.argv[2]), float(sys.argv[3])
            lat_stop, lon_stop = float(sys.argv[4]), float(sys.argv[5])
            # Google算法最大经纬度 纬度从北纬85.05112877980659°到南纬85.05112877980659°;经度从西经180°到东经180°;北纬,东经为+ 南纬,西经为-
            '''
            lat_start, lon_start = 85.05112877980659, -180
            lat_stop, lon_stop = -85.05112877980659, 180
            '''
            merge_tiles(zoom,
                        lat_start,
                        lat_stop,
                        lon_start,
                        lon_stop,
                        satellite=False)
        except Exception as identifier:
            print("error", "->", identifier)

    else:
        print("args length is wrong")
