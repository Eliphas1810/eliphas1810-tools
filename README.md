# eliphas1810-tools

## Overview

Tools of Eliphas1810 by Chrome Extensions, Python, .apk of Android Appli, Java, and JavaScript in HTML.

*Public Domain.*

*Japanese Only.*

ChangePngColor.py changes RGBA in PNG image file. it requires tkinter and Pillow of Python.

ColorCode.py displays color by a RGB hexadecimal notation or a color name for example "black". it requires tkinter of Python.

ListColorCode.py lists RGBs in PNG image file by hexadecimal notation. it requires tkinter and Pillow of Python.

OpenJTalk.py reads text in textarea using OpenJTalk. it requires tkinter of Python and OpenJTalk.

OpenJTalkMP3.py reads text in textarea and save .mp3 file using OpenJTalk. it requires tkinter and pydub of Python and OpenJTalk.

TtcToTtf.py converts a .ttc file to .ttf files. it requires tkinter of Python.

VolumeUp.py turns the volume up of .mp3 file. it requires tkinter and pydub of Python.

OdtRecompressor.py zips a directory of a unzipped .odt file as a mimetype file will be the first file in the zip file.

JaTextToOdt.py converts .txt files to a .odt file, converting rubys of Japanese novel web sites to xml snippets of rubys of content.xml in the .odt file.

BitFlipper.py flips all bit of a file.

<br />

EvenLineExtractor.html extracts even lines( and odd lines).

HalfWidthCounter.html counts almost half-width characters( and full-width characters).

KatakanaGenerator.html generates Katakana text at random.

RubyReplacer.html converts ruby notation of the Japanese novel site, "Narou" to the another Japanese novel site, "Kakuyomu".

JaTextToOdt.html converts .txt files to a .odt file, converting rubys of Japanese novel web sites to xml snippets of rubys of content.xml in the .odt file.

Crc32.html calculates CRC32.

StoredZip.html zips files by "STORED" of zip.

UuidVersion4.html generates UUID Version 4.

BitFlipper.html flips all bit of a file.

BitFlippedImageViewer.html shows images of bit flipped image files.

BitFlippedMoviePlayer.html plays a movie of bit flipped .mp4 files.

BitFlippedLoopMoviePlayer.html plays a movie of bit flipped .mp4 files by a single movie loop mode.

BitFlippedTextViewer.html shows texts of a bit flipped .txt file.

KatakanaExtractor.html extracts Katakana words.

LevenshteinDistanceCalculator.html calculates a Levenshtein distance between 2 words. A normalized Levenshtein distance is zero or more, and 1 or less. A normalized Levenshtein distance or a Levenshtein distance is smaller, 2 words are more similar.

KatakanaLevenshteinDistanceCalculator.html calculates Levenshtein distances of Katakana pairs and lists Katakana Pairs, by the order of the normalized Levenshtein distance, from the most similar Katakana pair to the least.

<br />

Self-made Chrome Extensions "SelectNewTab" adds new context menu item. the context menu item opens URL link by a new tab and select the new tab.

<br />

BitFlipper.apk flips all bit of a file on android.

BitFlippedImageViewer.apk shows images of bit flipped image files on android.

BitFlippedTextViewer.apk shows texts of a bit flipped .txt file on android.

TextViewer.apk shows texts of a .txt file on android.

<br />

/ePubXhtmlValidator/Main.java validates XHTML files in a .epub file, as XHTML1. Not Support (X)HTML5 tags except nav tag.

---

## 概要

　Chromeの拡張機能と、Pythonと、アンドロイドのスマホのアプリの.apkファイルと、Javaと、JavaScript(とHTML)による、エリファス1810のツールです。

　*パブリック ドメインです。*

　*日本語表記です。*

　ChangePngColor.pyでPNG画像の色を変更できますし、PNG画像の色を透明化できます。PythonのtkinterとPillowが必要です。

　ColorCode.pyで色を表示できます。Pythonのtkinterが必要です。

　ListColorCode.pyでPNG画像の全カラーコードを取得できます。PythonのtkinterとPillowが必要です。

　OpenJTalk.pyでテキストエリアのテキストをOpenJTalkで読み上げできます。OpenJTalkとPythonのtkinterが必要です。

　OpenJTalkMP3.pyでテキストエリアのテキストをOpenJTalkで読み上げできますし、MP3ファイルで保存できます。OpenJTalkとPythonのtkinterとpydubが必要です。

　TtcToTtf.pyで.ttcファイルを1つ以上の.ttfファイルへ変換できます。Pythonのtkinterが必要です。

　VolumeUp.pyでMP3ファイルの音量をアップできます。Pythonのtkinterとpydubが必要です。

　OdtRecompressor.pyでLibreOfficeのWriterの.odtファイルを展開したディレクトリを再zip圧縮できます。mimetypeファイルがzipファイル内の最初のファイルと成るように再zip圧縮します。

　JaTextToOdt.pyで1つ以上の.txtファイルを.odtファイルに変換できます。「小説家になろう」と「カクヨム」の大体のルビを.odtファイル内のcontent.xmlのルビのXMLに変換します。「小説家になろう」と「カクヨム」の半角縦線(|)のルビには対応していません。

　BitFlipper.pyで1つのファイルの全てのビットを反転できます。

<br />

　EvenLineExtractor.htmlでテキストエリアのテキストの偶数行(と奇数行)を抽出できます。

　HalfWidthCounter.htmlで(半角記号と半角英数字を含む)ASCII文字、半角カタカナ、ラテン1補助、ラテン文字拡張A、ラテン文字拡張Bを半角文字として文字数を数える事できますし、全角記号、全角英数字、ひらがな、全角カタカナを全角文字として文字数を数える事ができます。ラテン1補助、ラテン文字拡張A、ラテン文字拡張B、以外のラテン文字のうち多くは半角文字ですが、一部、全角文字が混在しているため、非対応です。全角文字として文字数を数えてしまいます。

　KatakanaGenerator.htmlで2文字以上10文字以下のカタカナをランダムに生成できます。ファンタジー小説の人物や街の名前を考えるのに役立つと思います。

　RubyReplacer.htmlで「小説家になろう」の半角括弧()のルビ記法を「カクヨム」の二重山括弧《》のルビ記法に置換できます。

　JaTextToOdt.htmlで1つ以上の.txtファイルを.odtファイルに変換できます。「小説家になろう」と「カクヨム」の大体のルビを.odtファイル内のcontent.xmlのルビのXMLに変換します。「小説家になろう」と「カクヨム」の半角縦線(|)のルビには対応していません。

　Crc32.htmlでzip圧縮などに必要なCRC32を計算できます。

　StoredZip.htmlで無圧縮(STORED)でzip圧縮できます。

　UuidVersion4.htmlでUUID Version 4を生成できます。

　BitFlipper.htmlで1つのファイルの全てのビットを反転できます。

　BitFlippedImageViewer.htmlで全てのビットが反転されている画像ファイルをビットを反転し直して表示できます。

　BitFlippedMoviePlayer.htmlで全てのビットが反転されている.mp4動画ファイルをビットを反転し直して表示、再生できます。

　BitFlippedLoopMoviePlayer.htmlで全てのビットが反転されている.mp4動画ファイルをビットを反転し直して表示、それぞれの動画1つだけのループ再生ができます。

　BitFlippedTextViewer.htmlで全てのビットが反転されているテキスト ファイルをビットを反転し直して表示できます。

　KatakanaExtractor.htmlでテキストエリアのテキストの連続しているカタカナを、同じ複数の物を1つだけにして、アイウエオ順に抽出できます。カタカナの誤字脱字を見つけやすくします。

　LevenshteinDistanceCalculator.htmlでレーベンシュタイン距離を計算できます。正規化されたレーベンシュタイン距離はゼロ以上1以下の実数です。正規化されたレーベンシュタイン距離やレーベンシュタイン距離が小さいほど、2つの文字は似ています。

　KatakanaLevenshteinDistanceCalculator.htmlでカタカナの2つ1組のレーベンシュタイン距離を計算して、正規化されたレーベンシュタイン距離の順に、最も似ているカタカナの2つ1組から、カタカナの2つ1組を一覧表示します。正規化されたレーベンシュタイン距離はゼロ以上1以下の実数です。正規化されたレーベンシュタイン距離が小さいほど、2つの文字は似ています。カタカナの誤字脱字と日本語での表記のゆれを見つけやすくします。ただし、レーベンシュタイン距離の計算は重いので、表示する最大の正規化されたレーベンシュタイン距離を0.2程度にしてください。

<br />

　自作のChromeの拡張機能　SelectNewTab　リンクを新しいタブで開いて選択状態にするメニュー項目をマウスの右クリック メニューに追加します。

<br />

　BitFlipper.apkは1つのファイルの全てのビットを反転できるアンドロイドのスマホのアプリです。

　BitFlippedImageViewer.apkは全てのビットが反転されている画像ファイルをビットを反転し直して表示できるアンドロイドのスマホのアプリです。

　BitFlippedTextViewer.apkは全てのビットが反転されているテキスト ファイルをビットを反転し直して表示できるアンドロイドのスマホのアプリです。

　TextViewer.apkはテキスト ファイルを表示できるアンドロイドのスマホのアプリです。

<br />

　/ePubXhtmlValidator/Main.javaは.epubファイル内のXHTMLファイルをXHTML1として妥当性検査します。navタグを除いてHTML5のタグは非対応です。全角空白の字下げの誤り、HTMLのタグではないタグの利用の誤り、タグの閉じ忘れなどを完全ではありませんが、ある程度、発見できます。.epubファイル内のnav.xhtml内のnavタグのepub:type属性の.xsdファイルのURIが不明のためnavタグのepub:type属性は妥当性検査できません。
