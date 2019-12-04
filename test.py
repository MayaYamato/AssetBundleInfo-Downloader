import os
import re
import codecs

#カレントディレクトリ変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ABI='AssetBundleInfo'

print('18Aprir:2.0.0.300 欲しい場合は1')
print('19Aprir:3.0.0.500 欲しい場合は2')
tmp0 = input("バージョンを指定してください.\n(例1:1\n例2:2.0.0.300)\n>> ").rstrip()

if tmp0 == 1:
    ver = '2.0.0.300'
elif tmp0 == 2:
    ver = '3.0.0.500'
else:
    ver = tmp0

tmp1 = input("android版かiOS版を指定してください.(android=1 iOS=2)\n>> ").rstrip()
if int(tmp1)==1:
    OS='android'
elif int(tmp1)==2:
    OS='iOS'

AWSURL=r'https://d2ktlshvcuasnf.cloudfront.net/Release/'+str(ver)+'/'+str(OS)+'/'

print('AssetBundleInfoを確認します・・・')

with codecs.open(ABI,"r","cp932","ignore") as lines:
    print('正常に開くことに成功しました')
    for line in lines:
        txt0 = line
        txt1=re.sub(r'^(?!.*@).*$','',txt0)
        txt2=re.sub(r'^\n|\r','',txt1)
        txt3=re.sub(r'^[a-z]',' ',txt2)
        txt4=re.sub(r'@.*?\n','\n',txt3)
        txt5=re.sub(r'@.*?\Z','',txt4)
        new_txt=re.sub(r'^.',AWSURL,txt5)
        #print(new_txt)
        with open(ABI+'.txt','a') as f:
            f.write(new_txt)