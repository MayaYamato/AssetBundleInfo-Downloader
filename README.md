# AssetDownloader
バンドリ！ガールズバンドパーティーで使用されているファイル
「AssetBundleInfo」に記されているファイルリストを一括でダウンロードするツールです。

使い方<br>
AssetBundleInfo(Masterブランチで提供している整形版)を<br>
AssetDownloader.exeと同じ階層において,exeを起動するだけです。<br>
(読み込ませたいAssetBundleInfoの名前はちゃんとAssetBundleInfoにしてね)<br>

Assetというフォルダを同階層に作成し,そこにAssetBundleInfoに記されている<br>
バンドリのデータファイルをダウンロードし,保存します。<br>


今後の機能追加予定<br>
・生のAssetBundleInfoに対しても実行できる<br>
・端末から取得したAssetBundleInfoとAWS上のAssetBundleInfoと差分ダウンロードできる<br>
・進行状況とかわかるようにしたい(なぜかprintされないんだけど・・・)<br>
機能も付加予定。(当方プログラム下手なので別ツールに分けるかもしれないとかはある)<br>

version 1.01<br>
一旦不要なファイルを吐き捨てて提供用として整形したのでリリース
Githubの勉強も続けます。

version 1.00<br>
私が作成,配布している整形版AssetBundleInfoに対してダウンロード処理が可能なツールとして作成<br>
現在64bit版のみ。(Pyinstallerと私のPCの都合上)<br>
もっと勉強して32bit版も作ります。お待ちください。<br>
