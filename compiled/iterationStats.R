library(ggplot2)
path.high = "~/Documents/Hackz/Simulation/compiled/high"
path.low = "~/Documents/Hackz/Simulation/compiled/low"

# HIGH data
setwd(path.high)
iters.avg.high <- c()
iters.std.high <- c()
file.names <- dir(path.high, pattern ="statsRateAvg")
number.files <- length(file.names)
matrix.iters <- matrix(NA,number.files,1001)
for (i in 1:number.files) {
  temp <- read.table(file.names[i], 
                     header = FALSE,
                     sep=",",
                     colClasses = "numeric")
  temp <- as.matrix(temp)
  matrix.iters[i,1:length(temp)] = temp
}

for (n in 1:1000) {
  data <- matrix.iters[1:number.files,n]
  data <- data[is.na(data) == FALSE]
  iters.avg.high[n] <- mean(data)
  iters.std.high[n] <- sd(data)
}

#LOW data
setwd(path.low)
iters.avg.low <- c()
iters.std.low <- c()
file.names <- dir(path.low, pattern ="statsRateAvg")
number.files <- length(file.names)
matrix.iters <- matrix(NA,number.files,1001)
for (i in 1:number.files) {
  temp <- read.table(file.names[i], 
                     header = FALSE,
                     sep=",",
                     colClasses = "numeric")
  temp <- as.matrix(temp)
  matrix.iters[i,1:length(temp)] = temp
}

for (n in 1:1000) {
  data <- matrix.iters[1:number.files,n]
  data <- data[is.na(data) == FALSE]
  if (is.numeric(mean(data)))
    iters.avg.low[n] <- mean(data)
    iters.std.low[n] <- sd(data)
}

iters.avg.low <- iters.avg.low[is.nan(iters.avg.low) == FALSE]
df.iters.avg.low <- data.frame(iters.avg.low)
