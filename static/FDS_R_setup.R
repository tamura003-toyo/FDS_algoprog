#
# [重要]
# VSCodeを実行中の人は、このプログラムを実行する*前*に、確実に終了してください。
#
# Miniforgeのインストール先に応じて、DS環境のJupyterを探します。
miniforge_dirs <- c(
  file.path(Sys.getenv("USERPROFILE"), "miniforge3"),
  "C:/miniforge3",
  "C:/miniforge"
)
jupyter_dirs <- file.path(miniforge_dirs, "envs", "DS", "Scripts")
# condaがユーザー別の環境フォルダにDS環境を作成した場合にも対応します。
jupyter_dirs <- c(jupyter_dirs,
                  file.path(Sys.getenv("USERPROFILE"), ".conda", "envs", "DS", "Scripts"))
jupyter_dirs <- jupyter_dirs[file.exists(file.path(jupyter_dirs, "jupyter.exe"))]
if (length(jupyter_dirs) == 0L) {
  stop("DS環境のjupyter.exeが見つかりません。先に教材のPython環境の作成を完了してください。Miniforgeを別の場所にインストールした場合は、miniforge_dirsにそのパスを追加してください。")
}
Sys.setenv(PATH = paste(jupyter_dirs[1], Sys.getenv("PATH"), sep = .Platform$path.sep))
install.packages("IRkernel", repos = "https://cloud.r-project.org")
IRkernel::installspec(name = "ds", displayname = "R(DS)",  user = TRUE)
install.packages(c("tidyverse", "psych", "plotly", "languageserver"),repos = "https://cloud.r-project.org")