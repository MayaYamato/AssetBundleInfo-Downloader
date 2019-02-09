import os
import requests
import os

#ダウンロードディレクトリの設定
download_dir_bgm = 'bgm'

#カレントディレクトリ確認用
#print(os.getcwd())

#ダウンロードディレクトリがなければ新規作成する
if not os.path.exists(download_dir_bgm):
        os.makedirs(download_dir_bgm)

#新しいダウンロード関数
def download_bgm(url,dst_path):
    f5 = open(dst_path,'wb')
    download = requests.get(url)
    f5.write(download.content)
    f5.close()

print('Loading BgmLists')
with open('BgmLists') as lines:
    for line in lines:
        #折り返し,改行文字の削除
        url = line.rstrip('\r\n')
        #ファイルの保存名の設定
        filename = os.path.basename(url)
        #pathの結合 asset/+filename
        dst_path = os.path.join(download_dir_bgm, filename)
        print(url)
        download_bgm(url, dst_path)
