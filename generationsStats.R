library(ggplot2)
library(reshape2)

genData <- function(path, cycles) {
  setwd(path)
  folder.names <- dir(path, pattern ="gen")
  genMatrix <- matrix(NA, cycles, length(folder.names))
  for (n in folder.names) {
    all.temp <- c()
    setwd(path)
    file.names <- dir(n, pattern =".txt")
    setwd(n)
    for (i in 1:length(file.names)) {
      temp <- read.table(file.names[i], 
                         header = FALSE,
                         sep=",",
                         colClasses = "numeric")
      mean <- mean(temp[is.na(temp) == FALSE])
      all.temp[i] <- mean
    }
  genMatrix[1:length(file.names),match(n, folder.names)] <- all.temp
  }
  genMatrix <- data.frame(genMatrix)
  colnames(genMatrix) <- folder.names
  return(genMatrix)
}

high.data <- genData("~/Documents/Hackz/Simulation/gen/high",100)
low.data <- genData("~/Documents/Hackz/Simulation/gen/low",100)

  test.student <- t.test(high.temp,low.temp)
  ks.distribution <- ks.test(high.temp, low.temp)
  high.normal = shapiro.test(high.temp)
  low.normal = shapiro.test(low.temp)
  
  if (n == 0) {
    high.1 <- high.temp
    low.1 <- low.temp
  }
  if (stop.depart == 0) {
    if (test.student$p.value < 0.05) {
      high.depart <- high.temp
      low.depart <- low.temp
      print(paste("generation:",n))
      print(paste("t-test p-value:", test.student$p.value))
      print(paste("KS test p-value:", ks.distribution$p.value))
      print(paste("shapiro normality p-value high",high.normal$p.value))
      print(paste("shapiro normality p-value low", low.normal$p.value))
      stop.depart <- 1
    }
  }
  if (n == 49) {
    high.final <- high.temp
    low.final <- low.temp
  }
}

density.high.1 <- density(high.1)
density.low.1 <- density(low.1)
density.high.depart <- density(high.depart)
density.low.depart <- density(low.depart)
density.high.final <- density(high.final)
density.low.final <- density(low.final)
plot(density.high.1, col=rgb(1,0,0,0.5), xlab="", ylab="", main="", xlim = c(50,90), ylim = c(0,0.300)) # colour is red
title(xlab="Mutation Rate (length of lifespan)", ylab="Density", main="Density Plot of High Predation (red) vs Low Predation (blue)")
lines(density.low.1, col=rgb(0,0,1,0.5), xlab="", ylab="", main="") # colour is blue
lines(density.high.depart, col=rgb(1,0,0,0.5), xlab="", ylab="", main="") # colour is red
lines(density.low.depart, col=rgb(0,0,1,0.5), xlab="", ylab="", main="") # colour is blue
lines(density.high.final, col=rgb(1,0,0,0.5), xlab="", ylab="", main="") # colour is red
lines(density.low.final, col=rgb(0,0,1,0.5), xlab="", ylab="", main="") # colour is blue
text(locator(), labels = c("0", "2*", "49*"))

