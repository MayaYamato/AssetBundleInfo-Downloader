import os
import urllib.error
import urllib.request

#ダウンロードディレクトリの設定
download_dir = 'asset'

#ダウンロードディレクトリがなければ新規作成する
if not os.path.exists(download_dir):
        os.makedirs(download_dir)

#ダウンロード関数の定義
def download_asset(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)

#繰り返し処理
with open('AssetBundleInfo') as lines:
    for line in lines:
        #折り返し,改行文字の削除
        url = line.rstrip('\r\n')
        filename = os.path.basename(url)
        dst_path = os.path.join(download_dir, filename)
        download_asset(url, dst_path)
        print(url)
