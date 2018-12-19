import os
import urllib.error
import urllib.request
download_dir = 'asset'
if not os.path.exists(download_dir):
        os.makedirs(download_dir)
def download_asset(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)
with open('b.txt') as lines:
    for line in lines:
        url = line.rstrip('\r\n')
        filename = os.path.basename(url)
        dst_path = os.path.join(download_dir, filename)
        if os.path.exists(dst_path):
            for n in range (1, 10):
                new_filename = str(filename) + '(' + str(n) + ')'
                dst_path = os.path.join(download_dir, new_filename)
                if not os.path.exists(dst_path):
                    download_asset(url, dst_path)
                    break
                else:
                    continue
        else:
            download_asset(url, dst_path)
