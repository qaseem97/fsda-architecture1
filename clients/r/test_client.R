source("fsda_client.R")

# Test 1: zscoreFS
data <- list(c(1,2,3), c(4,5,6), c(7,8,9))
result <- FSDA_call("zscoreFS", data)
print(result)

# Test 2: getYahoo
result2 <- FSDA_call("getYahoo", "AAPL", "plots", FALSE, "LastPeriod", "1mo")
print(result2$Ticker)
print(result2$Success)