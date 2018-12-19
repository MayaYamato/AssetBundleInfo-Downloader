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

#一行ずつ繰り返し処理
print('AssetBundleInfoを読み込みます')
with open('AssetBundleInfo') as lines:
    for line in lines:
        #折り返し,改行文字の削除
        url = line.rstrip('\r\n')
        #ファイルの保存名の設定
        filename = os.path.basename(url)
        #pathの結合 asset/+filename
        dst_path = os.path.join(download_dir, filename)
        print(url)
        #既存ファイルの存在判定
        if os.path.exists(dst_path):
            #10000回までfor同一ファイル保存を回避できる
            for n in range (1, 10000):
                #保存名をfilename+(n)に変更
                new_filename = str(filename)  + '(' + str(n) + ')'
                #dst_pathの再設定(ファイルネームの変更)
                dst_path = os.path.join(download_dir, new_filename)

                if not os.path.exists(dst_path):
                    download_asset(url, dst_path)
                    break

                else:
                    #既に重複ファイル回避がされていた場合さらにforを回す必要がある
                    continue
        else:
            download_asset(url, dst_path)
