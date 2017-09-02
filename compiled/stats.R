setwd("~/Documents/Hackz/Simulation/compiled/high")


iters <- 408
high <- c()
for (n in 0:iters) {
  temp <- read.table(paste("statsEnd",n,".txt", sep=""), 
                   header = FALSE,
                   sep=",",
                   colClasses = "numeric")
  mean <- mean(temp[is.na(temp) == FALSE])
  high[n] <- mean
}

setwd("~/Documents/Hackz/Simulation/compiled/low")

low <- c()
for (n in 0:iters) {
  temp <- read.table(paste("statsEnd",n,".txt", sep=""), 
                     header = FALSE,
                     sep=",",
                     colClasses = "numeric")
  mean <- mean(temp[is.na(temp) == FALSE])
  low[n] <- mean
}

hist(high, col=rgb(1,0,0,0.5),breaks=50, xlim = c(40,90), ylim = c(0,100)) # colour is red
hist(low, col=rgb(0,0,1,0.5), breaks=25, add=T) # colour is blue
box()

density.high <- density(high)
density.low <- density(low)
plot(density.high, col=rgb(1,0,0,0.5), xlab="", ylab="", main="", xlim = c(50,90), ylim = c(0,0.240)) # colour is red
title(xlab="Mutation Rate (length of lifespan)", ylab="Density", main="Density Plot of High Predation (red) vs Low Predation (blue)")
lines(density.low, col=rgb(0,0,1,0.5), xlab="", ylab="", main="") # colour is blue

high.normal = shapiro.test(high)
low.normal = shapiro.test(low)
ks.distribution <- ks.test(high, low)
test.student <- t.test(high,low)

high.normal
low.normal
ks.distribution
test.student