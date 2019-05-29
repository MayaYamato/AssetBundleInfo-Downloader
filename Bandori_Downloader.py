import os
import requests
import urllib.error
import urllib.request

#�_�E�����[�h�f�B���N�g���̐ݒ�
download_dir_asset = 'asset'
download_dir_bgm = 'bgm'
#DB��URL
DBURL = 'http://res.bandori.ga/assets/sound/bgm'

#�_�E�����[�h�f�B���N�g�����Ȃ���ΐV�K�쐬����
#��������֐�������ł������Ǎ���̂��Ƃ��l���ē�p��
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

tmp1 = input("�ǂ������擾���܂��H Asset �� 1����� Bgm �� 2����� ").rstrip()

if int(tmp1) == 1:

    print('Loading file')
    with open('AssetBundleInfo') as lines:
        for line in lines:
            #�܂�Ԃ�,���s�����̍폜
            url = line.rstrip('\r\n')
            #�t�@�C���̕ۑ����̐ݒ�
            filename = os.path.basename(url)
            #path�̌��� asset/+filename
            dst_path = os.path.join(download_dir_asset, filename)
            print(url)
            #�����t�@�C���̑��ݔ���
            if os.path.exists(dst_path):
                #1000��܂�for����t�@�C���ۑ�������ł���
                for n in range (1, 1000):
                    #�ۑ�����filename+(n)�ɕύX
                    new_filename = str(filename)  + '(' + str(n) + ')'
                    #dst_path�̍Đݒ�(�t�@�C���l�[���̕ύX)
                    dst_path = os.path.join(download_dir_asset, new_filename)

                    if not os.path.exists(dst_path):
                        download_asset(url, dst_path)
                        break
                    else:
                        #���ɏd���t�@�C�����������Ă����ꍇ�����for���񂷕K�v������
                        continue
            else:
                download_asset(url, dst_path)

if int(tmp1) == 2:

    tmp2 = input("BGM��id ���Ԃ܂Ŏ擾���܂��H(���߂̕�����������)").rstrip()
    l=int(tmp2)
    print('Loading file')
    for i in range (1, l):
        #music�ԍ��̌����ŏꍇ����
        if i<10 :
            url = (DBURL)+'00'+str(i)+'_rip/bgm'+'00'+str(i)+'.mp3'
        elif i<=99 :
            url = (DBURL)+'0'+str(i)+'_rip/bgm'+'0'+str(i)+'.mp3'
        else:
            url = (DBURL)+str(i)+'_rip/bgm'+str(i)+'.mp3'
        #�t�@�C���̕ۑ����̐ݒ�
        filename = os.path.basename(url)
        #path�̌��� asset/+filename
        dst_path = os.path.join(download_dir_bgm, filename)
        print(url)
        #����bgm�t�@�C������������_�E�����[�h�����Ȃ�
        if os.path.exists(dst_path):
            continue
        else :
            download_bgm(url, dst_path)