#
# [重要]
# VSCodeを実行中の人は、このプログラムを実行する*前*に、確実に終了してください。
#
Sys.setenv(PATH = paste(file.path(Sys.getenv("USERPROFILE"), "miniforge3", "envs", "DS", "Scripts"), Sys.getenv("PATH"), sep = .Platform$path.sep))
install.packages("IRkernel", repos = "https://cloud.r-project.org")
IRkernel::installspec(name = "ds", displayname = "R(DS)",  user = TRUE)
install.packages(c("tidyverse", "psych", "plotly", "languageserver"),repos = "https://cloud.r-project.org")