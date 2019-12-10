import os
import re
import codecs
import requests
import urllib.error
import urllib.request

os.chdir(os.path.dirname(os.path.abspath(__file__)))
download_dir_asset = os.getcwd()+r'\asset'
download_dir_bgm = os.getcwd()+r'\bgm'

if not os.path.exists(download_dir_asset):
        os.makedirs(download_dir_asset)
if not os.path.exists(download_dir_bgm):
        os.makedirs(download_dir_bgm)

def download_asset(url, dst_path):
    try:
        data = urllib.request.urlopen(url).read()
        with open(dst_path, mode="wb") as f0:
            f0.write(data)
    except urllib.error.URLError as e:
        pass

def download_bgm(url,dst_path):
    try:
        download = requests.get(url)
        with open(dst_path,'wb') as f1:
            f1.write(download.content)
    except urllib.error.URLError as e:
        pass

tmp0 = input('Which do you want Asset or BGM? \n (Asset ⇒ 1 Bgm ⇒ 2 )\n>>').rstrip()
if int(tmp0) == 1:

    tmp1 =input('What version of ABI do you want?\n ex:latest version ⇒ 0\n ex:2.0.0.300(18 Aprir) ⇒ 1\n ex:3.0.0.500(19 Aprir) ⇒ 2\n ex:Direct Input\n>>').rstrip()
    if int(tmp1) == 0:
        with urllib.request.urlopen('https://github.com/esterTion/bangdream_master_db_diff/blob/master/!dataVersion.txt') as response:
            html = response.read().decode() #responseで得たbyte列を変換
            m = re.search(r'master: (.+)</a>', html)
        ver = m.group()[8:17]
        print(ver)
    elif int(tmp1) == 1:
        ver = '2.0.0.300'
    elif int(tmp1) == 2:
        ver = '3.0.0.500'
    else :
        ver = tmp1

    tmp2 = input("Which do you want android or iOS? \n(android ⇒ 1 iOS ⇒ 2 )\n>> ").rstrip()
    if int(tmp2)==1:
        OS='Android'
    elif int(tmp2)==2:
        OS='iOS'
    else :
        print('ERROR')
    
    #ABI ダウンロード
    print('ABI Downloading:')
    filename = os.path.basename('AssetBundleInfo')
    url = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'/'+str(OS)+r'/AssetBundleInfo'
    dst_path = os.path.join(download_dir_asset, filename)
    download_asset(url, dst_path)

    #ABI 整形
    print('ABI Download complete\nShaping ABI started')
    if os.path.exists(os.getcwd()+r'\asset\AssetBundleInfo.txt'):
        os.remove(os.getcwd()+r'\asset\AssetBundleInfo.txt')
    with codecs.open(r'asset/AssetBundleInfo',"r","cp932","ignore") as lines:
        for line in lines:
            seiki = r'^(?!.*'+str(ver)+r').*$'
            txt0=re.sub(seiki,'',line)
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
                url = line.rstrip('\r\n')
                filename = os.path.basename(url)
                dst_path = os.path.join(download_dir_asset, filename)
                if os.path.exists(dst_path):
                    for n in range (1, 1000):
                        new_filename = str(filename)  + '(' + str(n) + ')'
                        dst_path = os.path.join(download_dir_asset, new_filename)
                        if not os.path.exists(dst_path):
                            download_asset(url, dst_path)
                            break
                        else:
                            continue
                else:
                    download_asset(url, dst_path)
    elif tmp3 == 'no' :
        exit()
    print('Download complete')

if int(tmp0) == 2:
    print('Downloading BGM')
    filename = os.path.basename('bgm.json')
    dst_path = os.path.join(download_dir_bgm, filename)
    print(dst_path)
    print(filename)
    download_bgm('https://res.bandori.ga/assets/sound/', dst_path)

    with open(dst_path) as lines:
        for line in lines:
            m = re.search(r'bgm(.+)_rip', line)
            if m == None:
                continue
            else:
                url = 'http://res.bandori.ga/assets/sound/'+str(m.group()[:-4])+'_rip/'+str(m.group()[:-4])+'.mp3'
                filename = os.path.basename(url)
                dst_path = os.path.join(download_dir_bgm, filename)
                print(url)
                if os.path.exists(dst_path):
                    continue
                else :
                    download_bgm(url, dst_path)
    os.remove(os.getcwd()+r'\bgm\bgm.json')