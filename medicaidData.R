library(httr)

response <- GET("https://data.cms.gov/data-api/v1/dataset/be64fce3-e835-4589-b46b-024198e524a6/data")
data <- content(response,as="parsed")

print(data[1])

