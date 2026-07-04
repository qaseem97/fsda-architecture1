library(httr)
library(jsonlite)

FSDA_call <- function(func_name, ..., base_url = "http://127.0.0.1:8000") {
  args_list <- list(...)
  
  response <- POST(
    url = paste0(base_url, "/call/", func_name),
    body = toJSON(list(args = args_list), auto_unbox = TRUE),
    content_type_json()
  )
  
  parsed <- content(response, as = "parsed", type = "application/json")
  
  if (status_code(response) != 200) {
    stop(paste("Error:", parsed$detail))
  }
  
  return(parsed$result)
}