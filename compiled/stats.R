library(gtools)

setwd("~/Documents/Hackz/Simulation/compiled/high")

files = dir(pattern="statsEnd")

temporary <- lapply(files,read.table,sep=",")
data <- rbindlist( temporary )

stats.End <- data.frame()

for (n in 99) {
  n <- read.table(paste("high/statsEnd",n,".txt", sep=""), 
                   header = FALSE,
                   sep=",")
}
