import os
import re
import mylib
import codecs
import requests
import urllib.error
import urllib.request

### SET VARIABLE ###
local_version = 3.0
url_AWS = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'
url_BGM = 'https://res.bandori.ga/assets/sound/'
url_version = 'https://raw.githubusercontent.com/MayaYamato/Bandori_Downloader/master/version'
url_github = 'https://github.com/MayaYamato/Bandori_Downloader/releases/latest'
url_ABIversion = 'https://raw.githubusercontent.com/esterTion/bangdream_master_db_diff/master/!dataVersion.txt'

os.chdir(os.path.dirname(os.path.abspath(__file__)))
download_dir_asset = os.getcwd()+r'\asset'
download_dir_bgm = os.getcwd()+r'\bgm'

def ABI_Download(ver,tmp,OS,dst_path):
    print('\nABI Downloading:')
    if len(tmp) > 2:
        url = AWSURL +str(ver)+'_'+str(tmp)+'/'+str(OS)+r'/AssetBundleInfo'
    else:
        url = AWSURL +str(ver)+'/'+str(OS)+r'/AssetBundleInfo'
    download_asset(url, dst_path)
    print('ABI Download complete\nShaping ABI started')

####################### main source #######################
introduce(local_version)

### Version Check ##
update_check(local_version,url_version,url_github,path)

### Asset or BGM ###
tmp = input('Which do you want Asset or BGM? \n (Asset ⇒ 0 Bgm ⇒ 1 )\n>>').rstrip()

### ABI/Asset Download ###
if int(tmp) == 0:

    if not os.path.exists(download_dir_asset):
        os.makedirs(download_dir_asset)

    ### ABI Version ###
    tmp =input('\nWhat version of ABI do you want?\n latest version ⇒ 0\n Direct Input ⇒ \n>>').rstrip()
    if int(tmp) == 0:
        with urllib.request.urlopen(VERSIONURL) as response:
            html = response.read().decode() #responseで得たbyte列を変換
            ver = html[:-1]
        print(ver)
    else:
        ver = tmp

    ### OS Version ###
    tmp = input("\nWhich do you want Android or iOS? \n(Android ⇒ 0 iOS ⇒ 1 )\n>> ").rstrip()
    if int(tmp)==0:
        OS='Android'
    elif int(tmp)==1:
        OS='iOS'
    else :
        print('ERROR')

    ### ABI Shaping ###
    tmp = input("\nChoose Shaping ABI method\n###Choose Latest if you want to format the latest ABI,\n###Old is effective against ABI before 2020\n(Latest ⇒ 0 Old ⇒ 1)\n>> ").rstrip()
    
    if int(tmp)==0:
        tmp = input("Please enter the URL change character string. \n(This character string can be confirmed by packet capture etc. If you do not understand the meaning, ask the author)\nforexample:p3HzsCWjkY\n>>").rstrip()
        filename = os.path.basename('AssetBundleInfo(raw) ver '+str(ver)+' .txt')
        dst_path = os.path.join(download_dir_asset, filename)
        ABI_Download(ver,tmp,OS,dst_path)
    
        ### latest ABI Shaping ###
        if os.path.exists(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt'):
            os.remove(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt')
        with codecs.open(r'asset/AssetBundleInfo(raw) ver '+str(ver)+' .txt',"r","cp932","ignore") as lines:
            for line in lines:
                seiki = r'^(?!.*'+str(ver)+r').*$'
                txt0=re.sub(seiki,'',line)
                txt0=re.sub(r'^\n|\r','',txt0)
                txt0=re.sub(r'@.*?\n','\n',txt0)
                txt0=re.sub(r'@.*?\Z','\n',txt0)
                new_txt=re.sub(r'^[^a-z]?(.+)\x12.*?\n','https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'_'+str(tmp)+'/'+str(OS)+r'/\1\n',txt0)
                with open(r'asset\AssetBundleInfo ver '+str(ver)+' .txt',"a") as f:
                    f.write(new_txt)

    elif int(tmp)==1:
        filename = os.path.basename('AssetBundleInfo(raw) ver '+str(ver)+' .txt')
        dst_path = os.path.join(download_dir_asset, filename)
        ABI_Download(ver,tmp,OS,dst_path)

        ### OLD ABI Shaping ###
        if os.path.exists(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt'):
            os.remove(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt')
        with codecs.open(r'asset/AssetBundleInfo(raw) ver '+str(ver)+' .txt',"r","cp932","ignore") as lines:
            for line in lines:
                seiki = r'^(?!.*'+str(ver)+r').*$'
                txt0=re.sub(seiki,'',line)
                txt0=re.sub(r'^\n|\r','',txt0)
                txt0=re.sub(r'@.*?\n','\n',txt0)
                txt0=re.sub(r'@.*?\Z','\n',txt0)
                new_txt=re.sub(r'^[^a-z]?(.+)\x12.*?\n','https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'/'+str(OS)+r'/\1\n',txt0)
                with open(r'asset\AssetBundleInfo ver '+str(ver)+' .txt',"a") as f:
                    f.write(new_txt)
    else :
        print("ERROR")
    print("Complete\n")

    ### All Asset Download ###
    tmp = input("Do you want to download all asset or only assets that contain a specific string?\n### But not recommended to download:Too many assets. all yes ⇒ 0 only asset ⇒ 1 no ⇒ 2\n>>")
    if int(tmp) == 0 :
        print('Loading ABI')
        with open(r'asset/AssetBundleInfo ver '+str(ver)+' .txt') as lines:
            for line in lines:
                if "sound/voice/scenario/loginstory13" in line:
                    continue
                else:
                    url = line.rstrip('\r\n')
                    filename = url.replace("/",' ',10)[url.replace("/",' ',10).find(str(OS)):]
                    dst_path = os.path.join(download_dir_asset, filename)
                    download_asset(url, dst_path)
        print("Download complete")
    elif int(tmp) == 1 :
        tmp = input("Enter the specific character string you want:\nex:live2d\n>>")
        print('Loading ABI')
        with open(r'asset/AssetBundleInfo ver '+str(ver)+' .txt') as lines:
            for line in lines:
                if "sound/voice/scenario/loginstory13" in line:
                    continue
                else:
                    if str(tmp) in line:
                        url = line.rstrip('\r\n')
                        filename = url.replace("/",' ',10)[url.replace("/",' ',10).find(str(OS)):]
                        dst_path = os.path.join(download_dir_asset, filename)
                        download_asset(url, dst_path)
                    else:
                        continue
    else:
        exit()

### BGM Download ###
elif int(tmp) == 1:

    if not os.path.exists(download_dir_bgm):
        os.makedirs(download_dir_bgm)

    print('Downloading BGM')
    filename = os.path.basename('bgm.json')
    dst_path = os.path.join(download_dir_bgm, filename)
    download_bgm(BGMURL, dst_path)

    with open(dst_path) as lines:
        for line in lines:
            m = re.search(r'bgm(.+)_rip', line)
            if m == None:
                continue
            else:
                url = BGMURL+str(m.group()[:-4])+'_rip/'+str(m.group()[:-4])+'.mp3'
                filename = os.path.basename(url)
                dst_path = os.path.join(download_dir_bgm, filename)
                print(url)
                if os.path.exists(dst_path):
                    continue
                else :
                    download_bgm(url, dst_path)
    os.remove(os.getcwd()+r'\bgm\bgm.json')

else:
    print('ERROR')