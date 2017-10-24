# qrwifi
Wi-Fi のキーや設定をQRコードで出力するJavascript 他です。  

## FILES

* htdocs/index.html
Webページ

* htdocs/keys.js
JSONを読み取ってQRコードを表示するJavascript

## FILES おまけ

* mkwifikey
SSIDおよびKEYをランダムに生成してJSON出力するスクリプトおよびそのラッパー
  - mkwifikey.py

* set_to_ddwrt.py
生成したSSID,KEYをDD-WRTに反映するスクリプトとライブラリ
  - settoddwrt23.py
  - settoddwrt24.py

## INSTALLATION

* htdocs/index.html, htdocs/keys.js を公開する場所に設置する
```mkdir -p public_html/qrwifi && cp htdocs/index.html htdocs/keys.js public_html/qrwifi/```

* jquery.js, jquery-qrcode.js を公開する場所に設置する
```
curl -o public_html/jquery.min.js http://code.jquery.com/jquery-X.X.X.min.js
curl -o public_html/jquery.qrcode.min.js https://raw.githubusercontent.com/jeromeetienne/jquery-qrcode/master/jquery.qrcode.min.js
```

* keys.json(SSID,KEYの定義)を公開する場所に設置する (以下は例)
```
{
"LABEL": [ "SSID", "KEY", "AUTH" ],
}
```

* スクリプト中のDATA_DIR などの置き場所を現状に合わせて変更する

* おわり
