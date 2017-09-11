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
    mean <- median(temp[is.na(temp) == FALSE])
    #datas[match(n, file.names)] <- mean
    datas[n] <- mean
  }
  return(datas)
}

density1 <- density.data("~/Documents/Hackz/Simulation/1/data", "statsEnd", 1001)
density0.4 <- density.data("~/Documents/Hackz/Simulation/0.4/data", "statsEnd", 1001)
density0.1 <- density.data("~/Documents/Hackz/Simulation/0.1/data", "statsEnd", 1001)
density0.01 <- density.data("~/Documents/Hackz/Simulation/0.01/data", "statsEnd", 1001)

densities <- data.frame(density1, density0.4, density0.1, density0.01)
colnames(densities) <- c("1", "0.4", "0.1", "0.01")
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
  geom_histogram(binwidth = 0.4, alpha=0.5) + 
  xlim(min(densities$value), 100)
p$labels$x <- "Mutation Index (Lifespan)"
p$labels$y <- "Density"
p$labels$fill <- "P(kill)"
p$labels$colour <- "P(kill)"
p + theme_minimal()

medians = c(median(density0.01),median(density0.1),median(density0.4),median(density1))
prs = c(0.01,0.1,0.4,1)
plotting = data.frame(medians, prs)
linear.model <- lm(prs ~ medians, plotting)

p <- ggplot(plotting, aes(medians,prs)) + geom_point()
p +  geom_smooth(method="lm", formula = y ~ exp(-x))


high.normal = shapiro.test(high)
low.normal = shapiro.test(low)
ks.distribution <- ks.test(high, low)
test.student <- t.test(high,low)
