# 第5回教材の変換・公開

編集元：第5回_教材構成案.md。プロジェクト直下で実行します。

```sh
python3 analysis/lesson05_publish/build_materials.py
BASE_URL=/FDS_algoprog npm run build
```

配布版はstatic、MySTページは5_R_Regression.mdに生成します。変換前ファイルはarchiveへ保存します。解答例は説明内、演習はexerciseタグ付き実行セルにします。図は配布版に埋め込みます。

既存の.github/workflows/deploy.ymlがmainへのpushで公開します。GitHubのSettings → PagesではGitHub Actionsを指定します。今回はpush・公開を行っていません。

公開にはmyst.yml、index.md、5_R_Regression.md、staticの第5回ipynbとZIP、dataset/tomato.xlsx、images/lesson05の本文参照PNG4点を含めてください。編集元md、Rmd、変換スクリプトも保管してください。_buildは生成物です。別作業の変更を含めず、対象ファイルを選択してコミットしてください。

検証：ZIP展開後のRmdのHTML出力、全解答の実行、130行と推定係数の一致、図4点の埋め込み、MySTのHTMLビルド、ダウンロード3点のコピーとリンク。

[MyST公式の公開手順](https://mystmd.org/guide/deployment-github-pages)
