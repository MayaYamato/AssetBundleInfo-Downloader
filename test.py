import os
import re
import codecs

tmp1 = input("android版とiOS版どっちが欲しい？(android=1 iOS=2)\n>> ").rstrip()
if int(tmp1)==1:
    OS='android'
elif int(tmp1)==2:
    OS='iOS'

#文字列内に/が入る(path指定とか)場合rをつけると良い
ABI='AssetBundleInfo'
AWSURL=r'https://d2ktlshvcuasnf.cloudfront.net/Release/$2/'+str(OS)+'/$1'
f1=r'^[^a-z]?(.+)\x{0012}@[0-9a-f]+\x{001A}\x{0009}([\d.]+).+$'
f2=r'^(?!(https)).*$'
f3='[\n\r]'

print('AssetBundleInfoを確認します・・・')

with codecs.open(ABI,"r","utf-8","ignore") as f:
      print('正常に開くことに成功しました')
      txt0=f.read()
      txt1=re.sub(f1,AWSURL,txt0)
      txt2=re.sub(f2,"",txt1)
      newtxt=re.sub(f3,"",txt2)

with open(ABI+'.txt',"w") as f:
    f.write(new_txt)
