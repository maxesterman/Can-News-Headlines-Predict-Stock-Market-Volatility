rootPath="/Users/maxsterman/Downloads/PA Term Project_submit"

setwd(paste(rootPath,"/Data",sep=""))
VIX_Sentiment_Data=read.csv("VIX_And_Sentiment.csv")
Sent_DataToUse=data.frame(VIX_open=VIX_Sentiment_Data$X1..open,
                         VIX_close=VIX_Sentiment_Data$X4..close,
                         TB_Polarity=VIX_Sentiment_Data$TB_polarity,
                         TB_Subjectivity=VIX_Sentiment_Data$TB_subjectivity,
                         Vader_neg=VIX_Sentiment_Data$Vader_neg,
                         Vader_pos=VIX_Sentiment_Data$Vader_pos,
                         Vader_neu=VIX_Sentiment_Data$Vader_neu,
                         Vader_comp=VIX_Sentiment_Data$Vader_comp,
                         date=VIX_Sentiment_Data$date)
Sent_DataToUse$date=as.POSIXct(Sent_DataToUse$date)
VIX_Len=length(Sent_DataToUse$date)
Sent_DataToUse=Sent_DataToUse[2:VIX_Len,]
VIX_Len=length(Sent_DataToUse$date)
period_difference=12
#for(i in 12:12){
#print(i)


VIX_Change=log(Sent_DataToUse$VIX_close[(1+period_difference):VIX_Len]/
                 Sent_DataToUse$VIX_open[1:(VIX_Len-(period_difference))])

Sent_DataFrame=Sent_DataToUse[(1+period_difference):VIX_Len,]

Sent_DataFrame$VIX_Change=VIX_Change

#VIX_DataToUse$First_Dif=c(NA,VIX_DataToUse$Change[2:VIX_Len]-VIX_DataToUse$Change[1:VIX_Len-1])
#VIX_DataToUse$Second_Dif=c(NA,VIX_DataToUse$Change[2:VIX_Len]-VIX_DataToUse$First_Dif[1:VIX_Len-1])
library("forecast")
library("tseries")
library("ggplot2")
library("lmtest")
#adf.test(deseas)
# VIX_ts=ts(VIX_DataToUse$Change, frequency=13*365)
# VIX_Clean=tsclean(VIX_ts)
# adf.test(VIX_Clean)
# ggplot(data=Sent_DataFrame, aes(x=date, y=Vader_neu, group=1)) +
#   geom_line()
# 
# temp_ts = ts(Sent_DataFrame$Vader_neu, start=c(2018,09,20), end=c(2018,11,14), frequency = 365*13)
# temp_ts_clean=tsclean(temp_ts)
# 
# #getting the seasonal component of the data and removing it from the 
# #time series.
# decomp = stl(temp_ts_clean, s.window = "periodic")
# plot(decomp)

setwd("Results")
sink("Granger_Causality_test.txt")
for(sent_name in c("Vader_neg","Vader_neu","Vader_pos","Vader_comp",
                   "TB_Polarity","TB_Subjectivity")){
  print(sent_name)
  print("")
  print("")
  print("")
  for(lag in 1:7){
    print(lag)
    print("")
    print(grangertest(Sent_DataFrame$VIX_Change~Sent_DataFrame[,sent_name],
                  order=lag))
    print("")
  }
}
sink()

# sink("DBScan_ARIMAX.txt")
# for(sent_name in c("Vader_neg","Vader_neu","Vader_pos","Vader_comp",
#                    "TB_Polarity","TB_Subjectivity")){
#   print(sent_name)
#   print("")
#   print("")
#   print("")
#   print(auto.arima(Sent_DataFrame$VIX_Change, x_reg=Sent_DataFrame[,sent_name], seasonal=FALSE))
#   print("")
# 
# }
# sink()

# print(auto.arima(VIX_Clean, seasonal = FALSE))
# arima_fit=auto.arima(VIX_Clean, seasonal = FALSE)
# tsdisplay(residuals(arima_fit))
# print(summary(residuals(arima_fit)))
  
#}