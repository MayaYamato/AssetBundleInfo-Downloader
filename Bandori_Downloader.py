import os
import requests
import urllib.error
import urllib.request

#ダウンロードディレクトリの設定
download_dir_asset = 'asset'
download_dir_bgm = 'bgm'
#DBのURL
DBURL = 'http://res.bandori.ga/assets/sound/bgm'

#ダウンロードディレクトリがなければ新規作成する
#正直これ関数一つだけでいいけど今後のことも考えて二つ用意
if not os.path.exists(download_dir_asset):
        os.makedirs(download_dir_asset)
if not os.path.exists(download_dir_bgm):
        os.makedirs(download_dir_bgm)


def download_asset(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)

def download_bgm(url,dst_path):
    f5 = open(dst_path,'wb')
    download = requests.get(url)
    f5.write(download.content)
    f5.close()

tmp1 = input("どっちを取得します？ Asset ⇒ 1を入力 Bgm ⇒ 2を入力 ").rstrip()

if int(tmp1) == 1:

    print('Loading file')
    with open('AssetBundleInfo') as lines:
        for line in lines:
            #折り返し,改行文字の削除
            url = line.rstrip('\r\n')
            #ファイルの保存名の設定
            filename = os.path.basename(url)
            #pathの結合 asset/+filename
            dst_path = os.path.join(download_dir_asset, filename)
            print(url)
            #既存ファイルの存在判定
            if os.path.exists(dst_path):
                #1000回までfor同一ファイル保存を回避できる
                for n in range (1, 1000):
                    #保存名をfilename+(n)に変更
                    new_filename = str(filename)  + '(' + str(n) + ')'
                    #dst_pathの再設定(ファイルネームの変更)
                    dst_path = os.path.join(download_dir_asset, new_filename)

                    if not os.path.exists(dst_path):
                        download_asset(url, dst_path)
                        break
                    else:
                        #既に重複ファイル回避がされていた場合さらにforを回す必要がある
                        continue
            else:
                download_asset(url, dst_path)

if int(tmp1) == 2:

    tmp2 = input("BGMのid 何番まで取得します？(多めの方がいいかも)").rstrip()
    l=int(tmp2)
    print('Loading file')
    for i in range (1, l):
        #music番号の桁数で場合分け
        if i<10 :
            url = (DBURL)+'00'+str(i)+'_rip/bgm'+'00'+str(i)+'.mp3'
        elif i<=99 :
            url = (DBURL)+'0'+str(i)+'_rip/bgm'+'0'+str(i)+'.mp3'
        else:
            url = (DBURL)+str(i)+'_rip/bgm'+str(i)+'.mp3'
        #ファイルの保存名の設定
        filename = os.path.basename(url)
        #pathの結合 asset/+filename
        dst_path = os.path.join(download_dir_bgm, filename)
        print(url)
        #既存bgmファイルがあったらダウンロードをしない
        if os.path.exists(dst_path):
            continue
        else :
            download_bgm(url, dst_path)