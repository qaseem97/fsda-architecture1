using HTTP
using JSON

function fsda_call(func_name::String, args...; base_url="http://127.0.0.1:8000")
    body = JSON.json(Dict("args" => collect(args)))
    
    response = HTTP.post(
        "$base_url/call/$func_name",
        ["Content-Type" => "application/json"],
        body
    )
    
    parsed = JSON.parse(String(response.body))
    
    if response.status != 200
        error(parsed["detail"])
    end
    
    return parsed["result"]
end