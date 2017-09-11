library(ggplot2)
library(reshape2)

iter.data <- function(path, filename.pattern, iterations) {
  setwd(path)
  iters.avg <- c()
  iters.std <- c()
  file.names <- dir(path, pattern = filename.pattern)
  number.files <- length(file.names)
  matrix.iters <- matrix(NA, number.files, (iterations+1))
  for (i in 1:number.files) {
    temp <- read.table(file.names[i], 
                       header = FALSE,
                       sep=",",
                       colClasses = "numeric")
    temp <- as.matrix(temp)
    matrix.iters[i,1:length(temp)] = temp
  }
  for (n in 1:iterations) {
    data <- matrix.iters[1:number.files,n]
    data <- data[is.na(data) == FALSE]
    if (is.numeric(mean(data))) {
      iters.avg[n] <- median(data)
      iters.std[n] <- sd(data)
    }
  }
  return(list(avg = iters.avg, std = iters.std, x = c(0:(iterations-1))))
}

path.1 = "~/Documents/Hackz/Simulation/1/data"
path.0.4 = "~/Documents/Hackz/Simulation/0.4/data"
path.0.1 = "~/Documents/Hackz/Simulation/0.1/data"
path.0.01 = "~/Documents/Hackz/Simulation/0.01/data"
pattern = "statsRateAvg"

iters.1 = data.frame(iter.data(path.1, pattern, 1001))
iters.0.4 = data.frame(iter.data(path.0.4, pattern, 1001))
iters.0.1 = data.frame(iter.data(path.0.1, pattern, 1001))
iters.0.01 = data.frame(iter.data(path.0.01, pattern, 1001))

plotData <- data.frame(cbind(iters.1$avg, iters.0.4$avg, iters.0.1$avg, iters.0.01$avg, iters.0.01$x))
colnames(plotData) <- c("1","0.4", "0.1", "0.01", "x")
plotData <- melt(plotData, id="x")

p <- ggplot(plotData, aes(x, value, colour=variable)) + geom_line()
p$labels$colour <- "P(kill)"
p$labels$x <- "Iterations"
p$labels$y <- "Mutation Index (Lifespan)"
p + theme_minimal()

