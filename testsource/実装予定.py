#バージョンの読み込み
with open('AssetBundleInfo.txt','r') as f:
    version=f.readlines()
    print (version[1])
