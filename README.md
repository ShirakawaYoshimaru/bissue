bissue
====

Overview
Bitbucketでissue情報をインポートするときに必要となるzipを自動で作成します。

## Description
bissue = Bitbucket + issue

-  issueの情報をターミナルから登録することができます(title,id,content)
- テキストファイルからissue情報を取得し、zipにして出力できます
-  issueの情報をzipにして出力できます

つまり、issueの登録からzipの出力までをターミナル上で行うことができます。
あとは出力されたzipをBitbucketにインポートするだけ!

## Demo
![demo gif](https://github.com/ShirakawaYoshimaru/bissue/raw/master/material/demo.gif)

## Requirement
- pip
- click(pythonのコマンドアプリケーションを楽に作れるようにするライブラリ)
- python2系(3系でも動くと思うけど・・・)

## Usage
bissue は bie コマンドにて動作します。

```lang:Help
Usage: bie [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add       issue情報を追加
  convert   issue情報をまとめる
  count     一時領域に保存してあるissue情報の数を表示
  delete    登録したissueを削除
  init      プロジェクトをセットアップ
  list      issue情報を表示
  loadfile  テキストからissue情報を保存する
  path      一時ファイルpathを表示
```

####1.まずはじめに初期化しましょう
initコマンドを使用します。
`$ bie init`
--nameでプロジェクト名をつけることもできます。
プロジェクト名をつけると、後に出力されるzipファイルの名前の一部として使用されます。
`$ bie init --name hogeProject`
また --assignee プロパティを付けることでissueに登録するassigneeを指定することができます。
assigneeの指定はinit時にしかできないので注意しましょう。

####2.issueを登録しましょう
addコマンドを使用します。
最低限title情報があればaddすることができます。
`$ bie add "【メイン画面】UIを組む"`
titleの他にcontent(本文)やidを指定することもできます。
`$ bie add --content "HeaderUIとかを組む" --id 1001 "【メイン画面】UIを組む"`
といった感じです。
なお、contentとidは指定しなくても大丈夫です。
contentを指定しない場合、contentは空文字としてissueに登録されます。
idを指定しない場合、最後に登録したissueのid + 1された数が指定されます。

正常にaddされた際は、
`success! TITLE`
が表示されます。


####3.登録したissue情報を確認しましょう
listコマンドを使用します。
`$ bie list`

こんな感じでidとtitleを確認することができます。
```lang:リザルト
 [id] - [title]
    0 - 【メイン画面】敵AIを作成
    1 - 【メイン画面】UIの作成
```

####4.今何個issueを登録したか確認しましょう
countコマンドを使用します。
`$ bie count`

こんな感じでcountを確認することができます。
```lang:リザルト
2
```

####5.登録したissueを削除しましょう
deleteコマンドを使用します。
`$ bie delete 1`
delete + id を指定することで、そのidのissueを削除してくれます。

####6.登録したissue情報をzipにしましょう
convertコマンドを使用します
`$ bie convert`
これだけです。
これで今まで登録したissue情報からjsonを作成し、そのjsonをzipにしてくれます。

成功した場合、こんな感じになります。
```lang:リザルト
maked bissueProject.zip
```
「bissueProject.zip」の部分はinitコマンド使用時に--nameオプションでプロジェクト名を指定していた場合はそちらがzipのファイル名として使用されます。


####7.出力されたzipをBitbucketへインポートする
http://qiita.com/ShirakawaYoshimaru/items/b3665ea3b66eafc0bdc5
ここらへんを見てやってみてください。

####1~6が面倒な方へ(loadfileコマンド)
テキストファイルからissue登録を行った後、zipにconvertしてくれるコマンドもあります。
loadfileコマンドです。
`$ bie loadfile filePath`
で使用できます。
テキストファイルは1行に1つ登録したいissueのtitleを記述してください。
例えば、
```lang:hoge.txt
【メイン画面】敵AIを作成
【メイン画面】UIの作成
```
のようなテキストファイルをご用意ください。

####その他
pathコマンド:issue情報を一時的に保存しているtmpファイルのパスを表示

## Install
pipで配布しています。
```
sudo pip install bissue
```

## Contribution
1. Fork it ( https://github.com/ShirakawaYoshimaru/bissue )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request
気軽にPRください

## Licence

MIT

## Author

[Shirakawa Yoshimaru](https://github.com/ShirakawaYoshimaru)
