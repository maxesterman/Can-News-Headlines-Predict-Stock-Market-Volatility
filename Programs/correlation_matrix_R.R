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

goodCols=(colnames(Sent_DataFrame) != "VIX_open") * (colnames(Sent_DataFrame) != "VIX_close")
goodCols=goodCols*1:length(goodCols)
Data_For_Col=Sent_DataFrame[,goodCols]
Data_For_Col=Data_For_Col[-nrow(Data_For_Col),-7]
Correlation_Matrix=cor(Data_For_Col)
Correlation_Matrix=round(Correlation_Matrix,2)

Data_For_Col_lag_1=Data_For_Col[1:(nrow(Data_For_Col)-1),1:6]
Data_For_Col_lag_1=cbind(Data_For_Col_lag_1,(Data_For_Col[2:(nrow(Data_For_Col)),7]))
colnames(Data_For_Col_lag_1)[7]<-"VIX_Change_(t+1)"
corr_lag_1=cor(Data_For_Col_lag_1)
corr_lag_1=round(corr_lag_1,2)
rownames(corr_lag_1)[7]<-"VIX_Change"
Correlation_Matrix=cbind(Correlation_Matrix,data.frame("VIX_Change_t_plus_1"=(corr_lag_1)[,7]))

Data_For_Col_lag_2=Data_For_Col[1:(nrow(Data_For_Col)-2),1:6]
Data_For_Col_lag_2=cbind(Data_For_Col_lag_2,Data_For_Col[3:(nrow(Data_For_Col)),7])
colnames(Data_For_Col_lag_2)[7]<-"VIX_Change_(t+2)"
corr_lag_2=cor(Data_For_Col_lag_2)
corr_lag_2=round(corr_lag_2,2)
rownames(corr_lag_2)[7]<-"VIX_Change"
Correlation_Matrix=cbind(Correlation_Matrix,data.frame("VIX_Change_t_plus_2"=(corr_lag_2)[,7]))
#write.csv(corr_lag_3,"lag_2_correlation_matrix.csv")

Data_For_Col_lag_3=Data_For_Col[1:(nrow(Data_For_Col)-3),1:6]
Data_For_Col_lag_3=cbind(Data_For_Col_lag_3,Data_For_Col[4:(nrow(Data_For_Col)),7])
colnames(Data_For_Col_lag_3)[7]<-"VIX_Change_(t+3)"
corr_lag_3=cor(Data_For_Col_lag_3)
corr_lag_3=round(corr_lag_3,2)
rownames(corr_lag_3)[7]<-"VIX_Change"
Correlation_Matrix=cbind(Correlation_Matrix,data.frame("VIX_Change_t_plus_3"=(corr_lag_3)[,7]))
#write.csv(corr_lag_3,"lag_3_correlation_matrix.csv")

Data_For_Col_lag_4=Data_For_Col[1:(nrow(Data_For_Col)-4),1:6]
Data_For_Col_lag_4=cbind(Data_For_Col_lag_4,Data_For_Col[5:(nrow(Data_For_Col)),7])
colnames(Data_For_Col_lag_4)[7]<-"VIX_Change_(t+4)"
corr_lag_4=cor(Data_For_Col_lag_4)
corr_lag_4=round(corr_lag_4,2)
rownames(corr_lag_4)[7]<-"VIX_Change"
Correlation_Matrix=cbind(Correlation_Matrix,data.frame("VIX_Change_t_plus_4"=(corr_lag_4)[,7]))

Data_For_Col_lag_5=Data_For_Col[1:(nrow(Data_For_Col)-5),1:6]
Data_For_Col_lag_5=cbind(Data_For_Col_lag_5,Data_For_Col[6:(nrow(Data_For_Col)),7])
colnames(Data_For_Col_lag_5)[7]<-"VIX_Change_(t+5)"
corr_lag_5=cor(Data_For_Col_lag_5)
corr_lag_5=round(corr_lag_5,2)
rownames(corr_lag_5)[7]<-"VIX_Change"
Correlation_Matrix=cbind(Correlation_Matrix,data.frame("VIX_Change_t_plus_5"=(corr_lag_5)[,7]))

Data_For_Col_lag_6=Data_For_Col[1:(nrow(Data_For_Col)-6),1:6]
Data_For_Col_lag_6=cbind(Data_For_Col_lag_6,Data_For_Col[7:(nrow(Data_For_Col)),7])
colnames(Data_For_Col_lag_6)[7]<-"VIX_Change_(t+6)"
corr_lag_6=cor(Data_For_Col_lag_6)
corr_lag_6=round(corr_lag_6,2)
rownames(corr_lag_6)[7]<-"VIX_Change"
Correlation_Matrix=cbind(Correlation_Matrix,data.frame("VIX_Change_t_plus_6"=(corr_lag_6)[,7]))

Data_For_Col_lag_7=Data_For_Col[1:(nrow(Data_For_Col)-7),1:6]
Data_For_Col_lag_7=cbind(Data_For_Col_lag_7,Data_For_Col[8:(nrow(Data_For_Col)),7])
colnames(Data_For_Col_lag_7)[7]<-"VIX_Change_(t+7)"
corr_lag_7=cor(Data_For_Col_lag_7)
corr_lag_7=round(corr_lag_7,2)
rownames(corr_lag_7)[7]<-"VIX_Change"
Correlation_Matrix=cbind(Correlation_Matrix,data.frame("VIX_Change_t_plus_7"=(corr_lag_7)[,7]))


write.csv(Correlation_Matrix, "Results/Correlation_Matrix_All.csv")
#write.csv(corr_lag_4,"lag_4_correlation_matrix.csv")
