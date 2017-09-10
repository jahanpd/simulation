library(ggplot2)
library(reshape2)

density.data <- function(path, filename.pattern, iterations) {
  datas <- c()
  setwd(path)
  file.names <- dir(path, pattern = filename.pattern)
  for (n in 1:iterations) {
    temp <- read.table(file.names[n], 
                       header = FALSE,
                       sep=",",
                       colClasses = "numeric")
    mean <- mean(temp[is.na(temp) == FALSE])
    #datas[match(n, file.names)] <- mean
    datas[n] <- mean
  }
  return(datas)
}

density1 <- density.data("~/Documents/Hackz/Simulation/1/data", "statsEnd", 860)
density0.4 <- density.data("~/Documents/Hackz/Simulation/0.4/data", "statsEnd", 860)
density0.1 <- density.data("~/Documents/Hackz/Simulation/0.1/data", "statsEnd", 860)
density0.01 <- density.data("~/Documents/Hackz/Simulation/0.01/data", "statsEnd", 860)

densities <- data.frame(density0.1, density0.4, density1, density0.01)
colnames(densities) <- c("0.1", "0.4", "1", "0.01")
densities <- melt(densities)

p <- ggplot(densities, aes(value, fill = variable)) + 
  geom_density(alpha = 0.5, adjust=1) + 
   xlim(min(densities$value), 100)
p$labels$x <- "Mutation Index (Lifespan)"
p$labels$y <- "Density"
p$labels$fill <- "P(kill)"
p$labels$colour <- "P(kill)"
p + theme_minimal()

p <- ggplot(densities, aes(value, fill = variable)) + 
  geom_histogram(binwidth = 0.1, alpha=0.5) + 
  xlim(min(densities$value), 100)
p$labels$x <- "Mutation Index (Lifespan)"
p$labels$y <- "Density"
p$labels$fill <- "P(kill)"
p$labels$colour <- "P(kill)"
p + theme_minimal()



high.normal = shapiro.test(high)
low.normal = shapiro.test(low)
ks.distribution <- ks.test(high, low)
test.student <- t.test(high,low)
