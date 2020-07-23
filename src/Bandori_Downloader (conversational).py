import os
import re
import mylib
import codecs
import requests
import urllib.error
import urllib.request

### SET VARIABLE ###
local_version = 4.1
name_software = 'Bandori_Downloader (conversational)'
url_AWS = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'
url_BGM = 'https://res.bandori.ga/assets/sound/'
url_version = 'https://raw.githubusercontent.com/MayaYamato/Bandori_Downloader/master/version'
url_github = 'https://github.com/MayaYamato/Bandori_Downloader/releases/'
url_ABIversion = 'https://raw.githubusercontent.com/esterTion/bangdream_master_db_diff/master/!dataVersion.txt\n'
name_software = os.path.basename(os.path.abspath(__file__))

os.chdir(os.path.dirname(os.path.abspath(__file__)))
download_dir_asset = os.getcwd()+r'\asset'
download_dir_bgm = os.getcwd()+r'\bgm'
download_dir_exe = os.getcwd()+r'\update_exe'
dst_path_exe = os.path.join(download_dir_exe, os.path.basename(os.path.abspath(__file__)))

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
mylib.update_check(local_version,url_version,url_github)

### Asset or BGM ###
tmp = input('Which do you want Asset or BGM? \n (Asset ⇒ 0 Bgm ⇒ 1 )\n>>').rstrip()

### ABI/Asset Download ###
if int(tmp) == 0:

    ### ABI Version ###
    tmp = input('\nWhat version of ABI do you want?\n latest version ⇒ 0\n Direct Input ⇒ \n>>').rstrip()
    if len(tmp) < 2:
        with urllib.request.urlopen(url_ABIversion) as response:
            html = response.read().decode() #responseで得たbyte列を変換
            ver = html[:-1]
        print(ver)
    else:
        ver = tmp

    ### OS Version ###
    tmp = input("\nWhich do you want Android or iOS? \n(Android ⇒ 0 iOS ⇒ 1 )\n>> ").rstrip()
    if int(tmp) == 0:
        OS='Android'
    elif int(tmp) == 1:
        OS='iOS'
    else :
        print('ERROR')

    ### ABI Shaping ###
    print("Choose Shaping ABI method###Choose Latest if you want to format the latest ABI,")
    tmp = input("###Old is effective against ABI before 2020\n(Latest ⇒ 0 Old ⇒ 1)\n>> ").rstrip()
    
    if int(tmp) == 0:
        print("Please enter the URL change character string.")
        print("※This character string can be confirmed by packet capture etc.")
        print("If you do not understand the meaning, ask the author")
        tmp = input("forexample:p3HzsCWjkY\n>>").rstrip()
        filename = os.path.basename('AssetBundleInfo(raw) ver '+str(ver)+' .txt')
        dst_path = os.path.join(download_dir_asset, filename)
        ABI_Download(ver,tmp,OS,dst_path)
    
        ### latest ABI Shaping ###
        retxt = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'_'+str(tmp)+'/'+str(OS)+r'/\1\n'
        ABI_Shaping(ver)

    elif int(tmp)==1:
        filename = os.path.basename('AssetBundleInfo(raw) ver '+str(ver)+' .txt')
        dst_path = os.path.join(download_dir_asset, filename)
        ABI_Download(ver,tmp,OS,dst_path)

        ### OLD ABI Shaping ###
        retxt = 'https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'/'+str(OS)+r'/\1\n'
        ABI_Shaping(ver)

    else :
        print("ERROR")
    print("Complete\n")

    ### All Asset Download ###
    print("Do you want to download all asset or only assets that contain a specific string?")
    tmp = input("### But not recommended to download:Too many assets. all yes ⇒ 0 specific asset ⇒ 1 no ⇒ 2\n>>")
    if int(tmp) == 0 :
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
    elif int(tmp) == 1 :
        tmp1 = input("Enter the specific character string you want:\nex:live2d\n>>")
        tmp2 = input("Shall we set up another word?:\nEnter no if not required.\n>>")
        if str(tmp2) == "no":
            tmp2 = "22/7 音楽の時間 運営はクソ"

        print('Loading ABI')
        with open(r'asset/AssetBundleInfo ver '+str(ver)+' .txt') as lines:
            for line in lines:
                if "sound/voice/scenario/loginstory13" in line:
                    continue
                else:
                    if str(tmp1) in line or str(tmp2) in line:
                        url = line.rstrip('\r\n')
                        dst_path = os.path.join(download_dir_asset,url.replace("/",' ',10)[url.replace("/",' ',10).find(str(OS)):])
                        mylib.download_file(url, dst_path)
                    else:
                        continue
    else:
        exit()

### BGM Download ###
elif int(tmp) == 1:
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