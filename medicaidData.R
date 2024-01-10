library(httr)


response <- GET("https://data.cms.gov/data-api/v1/dataset/be64fce3-e835-4589-b46b-024198e524a6/data")
rawData <- content(response,as="parsed")

# get sample for preallocation 
sampleData <- data.frame(rawData[1])
frame_colnames <- colnames(sampleData)
data <- data.frame(matrix(ncol=length(frame_colnames),nrow=length(rawData)))
colnames(data) <- frame_colnames

# iterate and fill data frame 
for (i in 1:length(rawData)) {
  data[i,] <- data.frame(rawData[i])
}

# view data
head(data)
