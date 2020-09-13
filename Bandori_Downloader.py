import os
import re
import mylib
import codecs
import requests
import configparser
import urllib.error
import urllib.request

### SET VARIABLE ###
local_version = 5.0
name_software = 'Bandori_Downloader'
url_AWS = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'
url_BGM = 'https://res.bandori.ga/assets/sound/'
url_version = 'https://raw.githubusercontent.com/kuragevs/Bandori_Downloader/master/version'
url_github = 'https://github.com/kuragevs/Bandori_Downloader/releases//download'
url_ABIversion = 'https://raw.githubusercontent.com/esterTion/bangdream_master_db_diff/master/!dataVersion.txt\n'

os.chdir(os.path.dirname(os.path.abspath(__file__)))
download_dir_asset = os.getcwd()+r'\asset'
download_dir_bgm = os.getcwd()+r'\bgm'
download_dir_exe = os.getcwd()+r'\update_exe'
dst_path_exe = os.path.join(download_dir_exe, os.path.basename(os.path.abspath(__file__)))

### Loading Settings ###
config_ini = configparser.ConfigParser()
config_ini.read('settings.ini', encoding='utf-8')
read_default = config_ini['DEFAULT']
tmps = []

for i in range(0,9):
    tmp = read_default['line'+str(i)]
    tmps.append(tmp)

if int(tmps[8]) == 1:
    import conv
    exit()

### MAKE DIRECTORY ###
if not os.path.exists(download_dir_asset):
    os.makedirs(download_dir_asset)
if not os.path.exists(download_dir_bgm):
    os.makedirs(download_dir_bgm)
if not os.path.exists(download_dir_exe):
    os.makedirs(download_dir_exe)

### SET FUNCTION ###
def ABI_Download(ver,tmp,OS,dst_path):
    print('ABI Downloading:')
    if len(tmp) > 3:
        url = url_AWS +str(ver)+'_'+str(tmp)+'/'+str(OS)+r'/AssetBundleInfo'
    else:
        url = url_AWS +str(ver)+'/'+str(OS)+r'/AssetBundleInfo'
    mylib.download_file(url, dst_path)
    print('ABI Download complete\nShaping ABI started')

def ABI_Shaping(ver):
    if os.path.exists(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt'):
        os.remove(os.getcwd()+r'\asset\AssetBundleInfo ver '+str(ver)+' .txt')
    with codecs.open(r'asset/AssetBundleInfo(raw) ver '+str(ver)+' .txt',"r","cp932","ignore") as lines:
        for line in lines:
            seiki = r'^(?!.*'+str(ver)+r').*$'
            txt0=re.sub(seiki,'',line)
            txt0=re.sub(r'^\n|\r','',txt0)
            txt0=re.sub(r'@.*?\n','\n',txt0)
            txt0=re.sub(r'@.*?\Z','\n',txt0)
            new_txt=re.sub(r'^[^a-z]?(.+)\x12.*?\n',retxt,txt0)
            with open(r'asset\AssetBundleInfo ver '+str(ver)+' .txt',"a") as f:
                f.write(new_txt)

####### MAIN SOURCE #######
mylib.introduce(name_software,local_version)

### Version Check ###
mylib.update_check(name_software,local_version,url_version,url_github)

### ABI/Asset Download ###
if int(tmps[0]) == 0:
    ### ABI Version ###
    if len(tmps[1]) < 3:
        with urllib.request.urlopen(url_ABIversion) as response:
            html = response.read().decode() 
            ver = html[:-1]
        print("version:"+ver)
    else:
        ver = tmps[1]

    ### OS Version ###
    if int(tmps[2]) == 0:
        OS = 'Android'
    elif int(tmps[2]) == 1:
        OS = 'iOS'
    else :
        print('ERROR')

    ### ABI Shaping ###    
    if int(tmps[3]) == 0:
        dst_path = os.path.join(download_dir_asset, os.path.basename('AssetBundleInfo(raw) ver '+str(ver)+' .txt'))
        ABI_Download(ver,str(tmps[4]),OS,dst_path)
        ### latest ABI Shaping ###
        retxt = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'_'+str(tmps[4])+'/'+str(OS)+r'/\1\n'
        ABI_Shaping(ver)

    elif int(tmps[3]) == 1:
        dst_path = os.path.join(download_dir_asset, os.path.basename('AssetBundleInfo(raw) ver '+str(ver)+' .txt'))
        ABI_Download(ver,str(tmps[3]),OS,dst_path)
        ### OLD ABI Shaping ###
        retxt = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'/'+str(OS)+r'/\1\n'
        ABI_Shaping(ver)

    else :
        print("ERROR")
    print("Complete\n")

    ### All Asset Download ###
    if int(tmps[5]) == 0 :
        print('Loading ABI')
        with open(r'asset/AssetBundleInfo ver '+str(ver)+' .txt') as lines:
            for line in lines:
                if "sound/voice/scenario/loginstory13" in line:
                    continue
                else:
                    url = line.rstrip('\r\n')
                    dst_path = os.path.join(download_dir_asset, url.replace("/",' ',10)[url.replace("/",' ',10).find(str(OS)):])
                    mylib.download_file(url, dst_path)
        print("Download complete")

    elif int(tmps[5]) == 1 :
        if str(tmps[7]) == "no":
            tmp7 = "22/7 音楽の時間 運営はクソ"

        print('Loading ABI')
        with open(r'asset/AssetBundleInfo ver '+str(ver)+' .txt') as lines:
            for line in lines:
                if "sound/voice/scenario/loginstory13" in line:
                    continue
                else:
                    if str(tmps[6]) in line or str(tmp7) in line:
                        url = line.rstrip('\r\n')
                        dst_path = os.path.join(download_dir_asset,url.replace("/",' ',10)[url.replace("/",' ',10).find(str(OS)):])
                        mylib.download_file(url, dst_path)
                    else:
                        continue

    else:
        exit()

### BGM Download ###
elif int(tmps[0]) == 1:
    print('Downloading BGM')
    dst_path = os.path.join(download_dir_bgm, os.path.basename('bgm.json'))
    mylib.download_content(url_BGM, dst_path)

    with open(dst_path) as lines:
        for line in lines:
            m = re.search(r'bgm(.+)_rip', line)
            if m == None:
                continue
            else:
                url = url_BGM+str(m.group()[:-4])+'_rip/'+str(m.group()[:-4])+'.mp3'
                dst_path = os.path.join(download_dir_bgm, os.path.basename(url))
                print(url)
                if os.path.exists(dst_path):
                    continue
                else :
                    mylib.download_content(url, dst_path)
    os.remove(os.getcwd()+r'\bgm\bgm.json')

else:
    print('ERROR')