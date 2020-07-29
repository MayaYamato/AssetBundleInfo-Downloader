import os
import requests
import urllib.error
import urllib.request

### my library ###

def introduce(name_software,local_version):
    print(name_software+' ver '+str(local_version))
    print('Created By : VERSUS.log')
    print('Twitter : @227_VS')
    print('Blog : https://raspberrypi422.mydns.jp')
    print('Github : https://github.com/kuragevs')

def download_file(url,dst_path):
    try:
        file = urllib.request.urlopen(url).read()
        with open(dst_path,'wb') as f0:
            f0.write(file)
    except urllib.error.URLError as __e:
        pass

def download_content(url,dst_path):
    try:
        file = requests.get(url)
        with open(dst_path,'wb') as f0:
            f0.write(file.content)
    except urllib.error.URLError as __e:
        pass

def update_check(name_software,local_version,url_version,url_github):
    print('Version Checking ... ')
    with urllib.request.urlopen(url_version) as response:
        html = response.read().decode() 
        remote_version = html
    if float(remote_version) - float(local_version) > 0:
        print('New Version Released:'+str(remote_version)+'\n')
        download_dir_exe = os.getcwd()+r'\update_exe'
        if not os.path.exists(download_dir_exe):
            os.makedirs(download_dir_exe)
        dst_path_exe = os.path.join(download_dir_exe, name_software+'.zip')
        url_download_exe = url_github+r'/'+str(remote_version)+r'/'+name_software+'.zip'
        print(url_download_exe)
        download_content(url_download_exe,dst_path_exe)
        print('Download Complete')
    else:
        print(float(remote_version))
        print('Latest Version\n')