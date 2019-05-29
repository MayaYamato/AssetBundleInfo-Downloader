import os
import re

print('AssetBundleInfoを確認します')
AWStext="https://d2ktlshvcuasnf.cloudfront.net/Release/$2/Android/$1"
f = open('AssetBundleInfo.txt','w')
#cp932でエンコードされるのを回避する
with codec.open('AssetBundleInfo',"r","utf-8","ignore") as lines:
  print('開いた')
  for line in lines:
    #rをつけるとバックスラッシュ関係の⇓のエラーが消える
    #SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 12-13: truncated \xXX escape
    new_line1=re.sub(r'^[^a-z]?(.+)\x{0012}@[0-9a-f]+\x{001A}\x{0009}([\d.]+).+$',r"AWStext",line)
    new_line2=re.sub('^(?!(https)).*$',"",new_line1)
    new_line3=re.sub('^[\r\n]',"",new_line2)
    print (str(new_line3))
    f.write('str(new_line3)\n')
