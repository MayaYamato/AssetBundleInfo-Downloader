import os
import re
import codecs
import requests
import urllib.error
import urllib.request

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#ダウンロードディレクトリの設定
download_dir_asset = os.getcwd()+r'\asset'
download_dir_bgm = os.getcwd()+r'\bgm'

#DBのURL
DBURL = 'http://res.bandori.ga/assets/sound/bgm'

#ダウンロードディレクトリがなければ新規作成する
if not os.path.exists(download_dir_asset):
        os.makedirs(download_dir_asset)
if not os.path.exists(download_dir_bgm):
        os.makedirs(download_dir_bgm)

#Assetのダウンロード関数
def download_asset(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)

#BGMのダウンロード関数
def download_bgm(url,dst_path):
    f5 = open(dst_path,'wb')
    download = requests.get(url)
    f5.write(download.content)
    f5.close()

tmp0 = input('Which do you want Asset or BGM? \n (Asset ⇒ 1 Bgm ⇒ 2 )\n>>').rstrip()
if int(tmp0) == 1:
    tmp1 =input('What version of ABI do you want?\n ex:2.0.0.300(18 Aprir) ⇒ 1\n ex:3.0.0.500(19 Aprir) ⇒ 2\n ex:Direct Input\n>>').rstrip()
    if int(tmp1) == 1:
        ver = '2.0.0.300'
    elif int(tmp1) == 2:
        ver = '3.0.0.500'
    else :
        ver = tmp1

    tmp2 = input("Which do you want android or iOS? \n(android ⇒ 1 iOS ⇒ 2 )\n>> ").rstrip()
    if int(tmp1)==1:
        OS='android'
    elif int(tmp1)==2:
        OS='iOS'
    
    #ABI ダウンロード
    print('ABI Downloading:')
    filename = os.path.basename('AssetBundleInfo')
    url = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'/'+str(OS)+r'/AssetBundleInfo'
    dst_path = os.path.join(download_dir_asset, filename)
    download_asset(url, dst_path)

    #ABI 整形
    print('ABI Download complete\nShaping ABI started')
    with codecs.open(r'asset/AssetBundleInfo',"r","cp932","ignore") as lines:
        for line in lines:
            txt0=re.sub(r'^(?!.*@).*$','',line)
            txt1=re.sub(r'^\n|\r','',txt0)
            txt2=re.sub(r'@.*?\n','\n',txt1)
            txt3=re.sub(r'@.*?\Z','\n',txt2)
            new_txt=re.sub(r'^[^a-z]?(.+)\x12.*?\n','https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'/'+str(OS)+r'/\1\n',txt3)
            with open(r'asset/AssetBundleInfo.txt',"a") as f:
                f.write(new_txt)
    print('Complete\n')

    tmp3=input('Do you want to download asset? yes or no\n>>')

    if tmp3 == 'yes' :
        #Assetのダウンロード
        print('Loading ABI')
        with open(r'asset/AssetBundleInfo.txt') as lines:
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
    elif tmp3 == 'no' :
        exit()

if int(tmp1) == 2:
    tmp2 = input('BGM id "How" many will you get?\nex:200 ⇒ BGM001~BGM200 Download').rstrip()
    l=int(tmp2)
    print('Downloading BGM')
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