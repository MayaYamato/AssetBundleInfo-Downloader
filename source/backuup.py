import os
import requests
import os

#ダウンロードディレクトリの設定
download_dir_asset = 'asset'
download_dir_bgm = 'bgm'

#カレントディレクトリ確認用
#print(os.getcwd())

#ダウンロードディレクトリがなければ新規作成する
if not os.path.exists(download_dir_bgm):
        os.makedirs(download_dir_bgm)
if not os.path.exists(download_dir_asset):
        os.makedirs(download_dir_asset)

#tmp = input("Which do you want, music or asset?").rstrip()

def download_bgm(url,dst_path):
    f5 = open(dst_path,'wb')
    mp3down = requests.get(url)
    f5.write(mp3down.content)
    f5.close()

print('AssetBundleInfoを読み込みます')
with open('a') as lines:
    for line in lines:
        #折り返し,改行文字の削除
        url = line.rstrip('\r\n')
        #ファイルの保存名の設定
        filename = os.path.basename(url)
        #pathの結合 asset/+filename
        dst_path = os.path.join(download_dir_bgm, filename)
        print(url)
        #既存ファイルの存在判定
        if os.path.exists(dst_path):
            #10000回までfor同一ファイル保存を回避できる
            for n in range (1, 10000):
                #保存名をfilename+(n)に変更
                new_filename = str(filename)  + '(' + str(n) + ')'
                #dst_pathの再設定(ファイルネームの変更)
                dst_path = os.path.join(download_dir_bgm, new_filename)

                if not os.path.exists(dst_path):
                    download_bgm(url, dst_path)
                    break

                else:
                    #既に重複ファイル回避がされていた場合さらにforを回す必要がある
                    continue
        else:
            download_bgm(url, dst_path)
