from pathlib import Path
import re,json,base64,zipfile,shutil,datetime
p=Path(__file__).resolve().parents[2]
source=p/'第5回_教材構成案.md'
s=source.read_text()
b=p/'archive'/('lesson05_before_export_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S'));b.mkdir()
for f in [source,p/'static/5_R_Regression.ipynb',p/'static/5_R_Regression.Rmd',p/'static/5_R_Regression_PositCloud.zip']:
 shutil.copy2(f,b/f.name)
s=s.replace('皆産の演習用','皆さんの演習用').replace('そのままそのまま','そのまま').replace('`〜`(チルダ記号)','`~`(チルダ記号)')
s=s.replace('総入荷量が1トン多いと、熊本産の予測価格は約1.6円/kg','総入荷量が10トン多いと、熊本産の予測価格は約12.6円/kg')
s=s.replace('predict(lmオブジェクト, data=...)`：`data`','predict(lmオブジェクト, newdata=...)`：`newdata`')
s=s.replace('\n```\nanalysis_data |>','\n```r\nanalysis_data |>')
source.write_text(s)
# Source remains the authority. Convert admonitions to portable Markdown callouts.
def portable(t):
 def callout(m):
  title=m[2] or ('補足' if m[1]=='note' else '確認')
  return '> **'+title+'**\n>\n'+'\n'.join('> '+line for line in m[3].strip().splitlines())+'\n'
 return re.sub(r'```\{(admonition|note)\}[^\S\n]*([^\n]*)\n(.*?)\n```',callout,t,flags=re.S)
imgpat=r'!\[([^\]]*)\]\((images/[^)]+)\)'
def embed(t,attachment=False):
 attachments={}
 def sub(m):
  data=base64.b64encode((p/m[2]).read_bytes()).decode();name=Path(m[2]).name
  if attachment:
   attachments[name]={'image/png':data};return f'![{m[1]}](attachment:{name})'
  return f'![{m[1]}](data:image/png;base64,{data})'
 return re.sub(imgpat,sub,t),attachments
# Keep folded solutions as Markdown; only top-level R blocks become executable.
parts=[];buf=[];lines=portable(s).splitlines(keepends=True);i=0;details=False
while i<len(lines):
 line=lines[i]
 if '<details>' in line:details=True
 if not details and re.fullmatch(r'```[rR]\s*\n?',line):
  if ''.join(buf).strip():parts.append(('markdown',''.join(buf).strip()))
  buf=[];i+=1;code=[]
  while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
  parts.append(('code',''.join(code).rstrip()))
 else:
  buf.append(line)
  if '</details>' in line:details=False
 i+=1
if ''.join(buf).strip():parts.append(('markdown',''.join(buf).strip()))
old=json.loads((p/'static/5_R_Regression.ipynb').read_text());cells=[]
for typ,t in parts:
 meta={};c={'cell_type':typ,'metadata':meta,'source':t.splitlines(keepends=True)}
 if typ=='code':
  c.update(execution_count=None,outputs=[])
  ex=re.search(r'演習([AR]\d+)',t)
  if ex:meta.update(tags=['exercise'],lesson05_exercise=ex[1],lesson05_mode='main' if ex[1].startswith('A') else 'review')
 else:
  t,att=embed(t,True);c['source']=t.splitlines(keepends=True)
  if att:c['attachments']=att
 cells.append(c)
nb={'cells':cells,'metadata':old['metadata'],'nbformat':4,'nbformat_minor':5}
for i,c in enumerate(cells):c['id']=f'lesson05-{i:03}'
(p/'static/5_R_Regression.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
rmd='''---
title: "第5回　Rによる回帰分析：熊本産トマトの高値を、市場の入荷量と時期から読み解く"
output:
  html_document:
    toc: true
    toc_depth: 2
    self_contained: true
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = TRUE,
                      fig.width = 9, fig.height = 5.5, dev = "ragg_png")
```

'''
for j,(typ,t) in enumerate(parts):
 if typ=='code':rmd+=f'```{{r cell-{j:03}}}\n{t}\n```\n\n'
 else:
  t=re.sub(r'^# [^\n]+\n*','',t,count=1) if j==0 else t
  t=t.replace('「第5回」フォルダに`5_R_Regression.ipynb`と`tomato.xlsx`を保存し、VS Codeでこのフォルダを開きます。カーネルはR(DS)を選びます。','''ZIPを展開し、`5_R_Regression.Rmd`と`tomato.xlsx`を同じフォルダに置いて、RStudioでRmdを開きます。Posit CloudではFiles → UploadからZIPをアップロードすると展開されます。図はRmdに埋め込まれています。

初回のみConsoleで次を実行します。

```r
install.packages(c("readxl", "tidyverse", "systemfonts", "rmarkdown", "ragg"))
```

チャンク右上の実行ボタンで上から順に進めます。HTMLへの出力にはKnitを使います。''').replace('ExcelファイルをNotebookと同じ','ExcelファイルをRmdと同じ')
  rmd+=embed(t)[0]+'\n\n'
(p/'static/5_R_Regression.Rmd').write_text(rmd)
readme='''第5回 Rによる回帰分析（RStudio / Posit Cloud）

1. ZIPを展開し、Rmdとtomato.xlsxを同じフォルダに置きます。
   Posit CloudではFiles → UploadでZIPをアップロードすると展開されます。
2. 5_R_Regression.Rmdを開き、冒頭にあるパッケージをConsoleでインストールします（初回のみ）。
3. コードを上から実行します。A1〜A8は授業中、R1〜R5は復習です。
4. 解答例は折りたたみ内にあります。HTMLはKnitで作成できます。
図はRmdに埋め込まれており、別の画像フォルダは不要です。
'''
with zipfile.ZipFile(p/'static/5_R_Regression_PositCloud.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('5_R_Regression.Rmd',rmd);z.write(p/'dataset/tomato.xlsx','tomato.xlsx');z.writestr('README.txt',readme)
# MyST page: source admonitions preserved, solutions rendered as dropdowns.
web=s
web=re.sub(r'<details>\s*<summary>(.*?)</summary>\s*(.*?)\s*</details>',lambda m:'::::{dropdown} '+m[1]+'\n'+m[2]+'\n::::',web,flags=re.S)
header='''---
title: 第5回：Rによる回帰分析
---

'''
links='''
## 教材のダウンロード

- [VS Code用ノートブック](static/5_R_Regression.ipynb)
- [分析用Excelデータ](dataset/tomato.xlsx)
- [RStudio・Posit Cloud用ZIP（Rmdとデータ）](static/5_R_Regression_PositCloud.zip)

'''
web=header+web.replace('\n\n', '\n'+links,1)
(p/'5_R_Regression.md').write_text(web)
config=p/'myst.yml';v=config.read_text()
if 'file: 5_R_Regression.md' not in v:v=v.replace('site:\n','    - file: 5_R_Regression.md\n      title: 第5回：Rによる回帰分析\nsite:\n')
config.write_text(v)
idx=p/'index.md';v=idx.read_text()
if '(5_R_Regression.md)' not in v:v+='- [第5回：Rによる回帰分析](5_R_Regression.md)\n'
idx.write_text(v)
print('Created notebook cells:',len(cells),'exercises:',sum('exercise' in c['metadata'].get('tags',[]) for c in cells))
print('Backup:',b)
