include("fsda_client.jl")

# Test 1: zscoreFS
data = [[1,2,3], [4,5,6], [7,8,9]]
result = fsda_call("zscoreFS", data)
println(result)

# Test 2: getYahoo
result2 = fsda_call("getYahoo", "AAPL", "plots", false, "LastPeriod", "1mo")
println(result2["Ticker"])
println(result2["Success"])