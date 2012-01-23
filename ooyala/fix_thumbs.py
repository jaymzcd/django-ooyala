import re
import tempfile
import urllib

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
    

from PIL import Image

from ooyala.models import OoyalaItem
from ooyala.library import OoyalaThumbnail



FIXED_THUMB_SYMBOL = '#'

def enlarge_thumbnail(oitem, desired_size='278x175'):
    desired_x = int(desired_size.split('x')[0])

    small_url = oitem.thumbnail
    if not small_url:
        print 'no thumb in place, TODO: get a random new one'
        return None
    img_data = urllib.urlopen(small_url).read()
    f = StringIO(img_data)
    size = Image.open(f).size
    if size[0] > desired_x:
        print 'already have a bigger image: %s > %s' % (size, desired_size)
        if '#' not in oitem.thumbnail:
            oitem.thumbnail += FIXED_THUMB_SYMBOL
            oitem.save()
        return None
    res = '%sx%s' % size

    small_thumbs = OoyalaThumbnail(embed_code=oitem.embed_code, resolution=res, indicies='0-25').process()
    if isinstance(small_thumbs, str):
        print 'OoyalaThumbnail error:', small_thumbs
        return None
    if oitem.thumbnail not in small_thumbs.toprettyxml():
        print 'existing thumb not found in xml'
        return None
    res = re.findall(r'index="(\d+)".*\n.*%s' % oitem.thumbnail, small_thumbs.toprettyxml())
    if res and res[0] and res[0].isdigit:
        idx = int(res[0])
    else:
        print 'regex not matched:', repr(res)
        if 'promo' in oitem.thumbnail:
            print 'promo image', oitem.thumbnail
        return None

    thumbs_data = small_thumbs.getElementsByTagName('thumbnail')


    big_thumbs = OoyalaThumbnail(embed_code=oitem.embed_code, resolution=desired_size, indicies='0-25').process()
    thumbs_data = big_thumbs.getElementsByTagName('thumbnail')
    big_url = thumbs_data[idx].firstChild.nodeValue
    # mark enlarged thumbs with a hash
    oitem.thumbnail = big_url + FIXED_THUMB_SYMBOL
    oitem.save()
    return big_url

if __name__ == '__main__':
    # only do thumbs not marked with a hash
    for oitem in OoyalaItem.live.exclude(thumbnail__contains=FIXED_THUMB_SYMBOL):
        small_url = oitem.thumbnail
        print small_url
        res = enlarge_thumbnail(oitem)
