rootPath="/Users/maxsterman/Downloads/PA Term Project_submit"

setwd(paste(rootPath,"/Data",sep=""))
#VIX_Vader_neu=read.csv("/Users/maxsterman/Downloads/PA Term Project/Data/All_Data_Original_DBSCAN_plus_lags.csv")

VIX_Vader_neu=read.csv("All_Data_Original_DBSCAN_plus_lags.csv")

VIX_Vader_train_neu=VIX_Vader_neu[as.POSIXlt(VIX_Vader_neu[,"date"])<as.POSIXlt("2018-11-15"),]
VIX_Vader_test_neu=VIX_Vader_neu[as.POSIXlt(VIX_Vader_neu[,"date"])>=as.POSIXlt("2018-11-15"),]


range_data<-function(x){
  (x-apply(x,2,min))/(apply(x,2,max)-apply(x,2,min))
  }
range_data_vec<-function(x){
  (x-min(x))/(max(x)-min(x))
  }






VIX_lag_cols=grepl("lag",colnames(VIX_Vader_neu))*grepl("VIX",colnames(VIX_Vader_neu))
date_cols=(colnames(VIX_Vader_neu)=="date")

sentiment_names=c("Vader_neu","Vader_pos","Vader_comp","Vader_neg",
                  "TB_polarity","TB_subjectivity")
for(first_layer in 7){
  #for(second_layer in 6:8){
    forecast_acc=data.frame(matrix(nrow=7,ncol=(length(sentiment_names)+1)))
    colnames(forecast_acc)<-c("VIX Change", sentiment_names)
    forecast_cor=data.frame(matrix(nrow=7,ncol=(length(sentiment_names)+1)))
    colnames(forecast_cor)<-c("VIX Change", sentiment_names)
    
    forecast_dir=data.frame(matrix(nrow=7,ncol=(length(sentiment_names)+1)))
    colnames(forecast_dir)<-c("VIX Change", sentiment_names)
    forecast_dir_first_diff=data.frame(matrix(nrow=7,ncol=(length(sentiment_names)+1)))
    colnames(forecast_dir_first_diff)<-c("VIX Change", sentiment_names)
    
    for(j in 1:7){
      
      print("j")
      
      
      cols_to_use_VIX=c("date")
      
      for(i in 1:j){ 
        cols_to_use_VIX=c(cols_to_use_VIX,paste("VIX.Change_lag_",toString(i),sep=""))
        
      }
      
      VIX_Matrix=VIX_Vader_neu[,cols_to_use_VIX]
      
      
      VIX_Change=VIX_Vader_neu[,c("date","VIX.Change")]
      
      complete_cases_to_use=complete.cases(VIX_Matrix)
      
      #only using complete cases
      VIX_Matrix=VIX_Matrix[complete_cases_to_use,]
      VIX_Change=VIX_Change[complete_cases_to_use,]
      
      
      
      
      
      
      train_dates=(as.POSIXlt(VIX_Matrix[,"date"])<as.POSIXlt("2018-11-15"))
      test_dates=(as.POSIXlt(VIX_Matrix[,"date"])>=as.POSIXlt("2018-11-15"))
      
      
      VIX_Matrix=VIX_Matrix[,-which(colnames(VIX_Matrix)=="date")]
      VIX_Change=VIX_Change[,-which(colnames(VIX_Change)=="date")]
      
      VIX_Change_min=min(VIX_Change)
      VIX_Change_max=max(VIX_Change)
      
      print("Min VIX Change")
      print(VIX_Change_min)
      print("Max VIX Change")
      print(VIX_Change_max)
      
      
      if(j==1){
        VIX_Matrix_norm=data.matrix(range_data_vec(VIX_Matrix))
        
      }else{  
        VIX_Matrix_norm=range_data(VIX_Matrix)
      }
      VIX_Change_norm=range_data_vec(VIX_Change)
      
      
      VIX_Matrix_norm_train=VIX_Matrix_norm[train_dates,]
      VIX_Change_norm_train=VIX_Change_norm[train_dates]
      
      VIXs<-as.matrix(VIX_Matrix_norm_train)
      y<-as.matrix(VIX_Change_norm_train)
      
      VIX_trains=as.matrix(t(VIXs))
      y_train<-as.matrix(t(y))
      
      
      x_train<-array(c(t(rbind(VIX_trains))),
                     dim=c(1,dim(VIXs)[1],dim(VIXs)[2]))
      
      require(rnn)
      set.seed(2018)
      model1<-trainr(Y=y_train,
                     X=x_train,
                     learningrate=0.05,
                     hidden_dim = c(first_layer),
                     numepochs = 500,
                     network_type = "rnn",
                     sigmoid="logistic")
      error_1<-t(model1$error)
      rownames(error_1)<-1:nrow(error_1)
      colnames(error_1)<-"error"
      plot(error_1)
      
      
      VIX_Matrix_norm_test=VIX_Matrix_norm[test_dates,]
      VIX_Change_norm_test=VIX_Change_norm[test_dates]
      
      VIXs_test<-as.matrix(VIX_Matrix_norm_test)
      y_test<-as.matrix(VIX_Change_norm_test)
      
      VIX_tests=as.matrix(t(VIXs_test))
      y_tests<-as.matrix(t(y_test))
      
      x_tests<-array(c(t(rbind(VIX_tests))),
                     dim=c(1,dim(VIXs_test)[1],dim(VIXs_test)[2]))
      
      pred1_test<-t(predictr(model1,x_tests))
      
      
      
      forecast_cor[j,1]<-cor(t(y_tests),pred1_test)
      
      unnormed_actual_y<-VIX_Change_min+(t(y_tests)*(VIX_Change_max-VIX_Change_min))
      unnormed_predicted_y<-VIX_Change_min+(pred1_test*(VIX_Change_max-VIX_Change_min))
      
      
      forecast_acc[j,1]<-accuracy(c(unnormed_actual_y),c(unnormed_predicted_y))[,"RMSE"]
      forecast_dir[j,1]<-round(sum((unnormed_predicted_y * unnormed_actual_y) > 0)/length(unnormed_predicted_y),3)*100
      forecast_dir_first_diff[j,1]<-round(sum((diff(unnormed_predicted_y) * diff(unnormed_actual_y)) > 0)/length(diff(unnormed_predicted_y)),3)*100
      #}
    }  
  
    for (sent_name in sentiment_names){ 
    
      #sent_name="Vader_pos"
      #Vader_lag_cols=grepl("lag",colnames(VIX_Vader_neu))*grepl(sent_name,colnames(VIX_Vader_neu))
      for(j in 1:7){
      
      
      
      
        # VIX_Matrix=VIX_Vader_neu[,c(which(date_cols),which(VIX_lag_cols==1))]
        # Vader_Matrix=VIX_Vader_neu[,c(which(date_cols),which(Vader_lag_cols==1))]
        # 
        # print(colnames(Vader_Matrix))
        # 
        # VIX_Matrix=VIX_Matrix[,1:5]
        # Vader_Matrix=Vader_Matrix[,1:5]
        
        cols_to_use_Vader=c("date")
        cols_to_use_VIX=c("date")
        
        for(i in 1:j){ 
          cols_to_use_Vader=c(cols_to_use_Vader,paste(sent_name,"_lag_",toString(i),sep=""))
          cols_to_use_VIX=c(cols_to_use_VIX,paste("VIX.Change_lag_",toString(i),sep=""))
          
          }
      
        VIX_Matrix=VIX_Vader_neu[,cols_to_use_VIX]
        Vader_Matrix=VIX_Vader_neu[,cols_to_use_Vader]
        
        
        VIX_Change=VIX_Vader_neu[,c("date","VIX.Change")]
        
        complete_cases_to_use=complete.cases(Vader_Matrix)
        
        #only using complete cases
        VIX_Matrix=VIX_Matrix[complete_cases_to_use,]
        Vader_Matrix=Vader_Matrix[complete_cases_to_use,]
        VIX_Change=VIX_Change[complete_cases_to_use,]
        
        
        
      
      
        
        train_dates=(as.POSIXlt(VIX_Matrix[,"date"])<as.POSIXlt("2018-11-15"))
        test_dates=(as.POSIXlt(VIX_Matrix[,"date"])>=as.POSIXlt("2018-11-15"))
        
       
        VIX_Matrix=VIX_Matrix[,-which(colnames(VIX_Matrix)=="date")]
        Vader_Matrix=Vader_Matrix[,-which(colnames(Vader_Matrix)=="date")]
        VIX_Change=VIX_Change[,-which(colnames(VIX_Change)=="date")]
        
        VIX_Change_min=min(VIX_Change)
        VIX_Change_max=max(VIX_Change)
        
        print("Min VIX Change")
        print(VIX_Change_min)
        print("Max VIX Change")
        print(VIX_Change_max)
        
        
        if(j==1){
          VIX_Matrix_norm=data.matrix(range_data_vec(VIX_Matrix))
          Vader_Matrix_norm=data.matrix(range_data_vec(Vader_Matrix)) 
          
        }else{  
          VIX_Matrix_norm=range_data(VIX_Matrix)
          Vader_Matrix_norm=range_data(Vader_Matrix)
        }
        VIX_Change_norm=range_data_vec(VIX_Change)
         
        
        VIX_Matrix_norm_train=VIX_Matrix_norm[train_dates,]
        Vader_Matrix_norm_train=Vader_Matrix_norm[train_dates,]  
        VIX_Change_norm_train=VIX_Change_norm[train_dates]
      
        Vaders<-as.matrix(Vader_Matrix_norm_train)
        VIXs<-as.matrix(VIX_Matrix_norm_train)
        y<-as.matrix(VIX_Change_norm_train)
      
        Vader_trains=as.matrix(t(Vaders))
        VIX_trains=as.matrix(t(VIXs))
        y_train<-as.matrix(t(y))
      
        c(t(rbind(VIX_trains,
                  Vader_trains)))
        
        x_train<-array(c(t(rbind(VIX_trains,
                                 Vader_trains))),
                       dim=c(1,dim(Vaders)[1],dim(Vaders)[2]*2))
        
        
        # for(j in 1:13){
        #   assign(paste("Vader","j",sep=""),as.matrix(Vader[,i]))
        # }
        
        
      
        # Vader1<-as.matrix(Vader_Matrix[,1])
        # Vader2<-as.matrix(Vader_Matrix[,2])
        # Vader3<-as.matrix(Vader_Matrix[,3])
        # Vader4<-as.matrix(Vader_Matrix[,4])
        # 
        # VIX1<-as.matrix(VIX_Matrix[,1])
        # VIX2<-as.matrix(VIX_Matrix[,2])
        # VIX3<-as.matrix(VIX_Matrix[,3])
        # VIX4<-as.matrix(VIX_Matrix[,4])
        # 
        # 
        # 
        # 
        # 
        # y_train<-as.matrix(t(y))
        # VIX1_train<-as.matrix(t(VIX1))
        # VIX2_train<-as.matrix(t(VIX2))
        # VIX3_train<-as.matrix(t(VIX3))
        # VIX4_train<-as.matrix(t(VIX4))
        # 
        # Vader1_train<-as.matrix(t(Vader1))
        # Vader2_train<-as.matrix(t(Vader2))
        # Vader3_train<-as.matrix(t(Vader3))
        # Vader4_train<-as.matrix(t(Vader4))
        # 
        # 
        # x_trains<-array(c(VIX1_train,
        #                  VIX2_train,
        #                  VIX3_train,
        #                  VIX4_train,
        #                  Vader1_train,
        #                  Vader2_train,
        #                  Vader3_train,
        #                  Vader4_train),
        #                dim=c(dim(VIX1_train),8))
        require(rnn)
        set.seed(2018)
        model1<-trainr(Y=y_train,
                       X=x_train,
                       learningrate=0.05,
                       hidden_dim = c(first_layer),
                       numepochs = 500,
                       network_type = "rnn",
                       sigmoid="logistic")
        error_1<-t(model1$error)
        rownames(error_1)<-1:nrow(error_1)
        colnames(error_1)<-"error"
        plot(error_1)
        
        
        # VIX_test_Matrix=VIX_Vader_test_neu[,which(VIX_lag_cols==1)]
        # Vader_test_Matrix=VIX_Vader_test_neu[,which(Vader_lag_cols==1)]
        # 
        # print(colnames(Vader_Matrix))
        # 
        # VIX_test_Matrix=VIX_test_Matrix[,1:4]
        # Vader_test_Matrix=Vader_test_Matrix[,1:4]
        # VIX_test_Change=VIX_Vader_test_neu[,"VIX.Change"]
        # 
        # 
        # VIX_test_Matrix=range_data(VIX_test_Matrix)
        # Vader_test_Matrix=range_data(Vader_test_Matrix)
        # VIX_test_Change=range_data_vec(VIX_test_Change)
        
        VIX_Matrix_norm_test=VIX_Matrix_norm[test_dates,]
        Vader_Matrix_norm_test=Vader_Matrix_norm[test_dates,]  
        VIX_Change_norm_test=VIX_Change_norm[test_dates]
        
        Vaders_test<-as.matrix(Vader_Matrix_norm_test)
        VIXs_test<-as.matrix(VIX_Matrix_norm_test)
        y_test<-as.matrix(VIX_Change_norm_test)
        
        Vader_tests=as.matrix(t(Vaders_test))
        VIX_tests=as.matrix(t(VIXs_test))
        y_tests<-as.matrix(t(y_test))
        
        x_tests<-array(c(t(rbind(VIX_tests,
                                Vader_tests))),
                       dim=c(1,dim(Vaders_test)[1],dim(Vaders_test)[2]*2))
        
        pred1_test<-t(predictr(model1,x_tests))
        
        
        
        
        forecast_cor[j,sent_name]<-cor(t(y_tests),pred1_test)
        
        unnormed_actual_y<-VIX_Change_min+(t(y_tests)*(VIX_Change_max-VIX_Change_min))
        unnormed_predicted_y<-VIX_Change_min+(pred1_test*(VIX_Change_max-VIX_Change_min))
        
        
        forecast_acc[j,sent_name]<-accuracy(c(unnormed_actual_y),c(unnormed_predicted_y))[,"RMSE"]
        
        forecast_dir[j,sent_name]<-round(sum((unnormed_predicted_y * unnormed_actual_y) > 0)/length(unnormed_predicted_y),3)*100
        forecast_dir_first_diff[j,sent_name]<-round(sum((diff(unnormed_predicted_y) * diff(unnormed_actual_y)) > 0)/length(diff(unnormed_predicted_y)),3)*100
      #}
    }
    
    forecast_acc_fname=paste(rootPath,"/Data/Results/",
                             "RNN_RMSES.csv",sep="")
    forecast_cor_fname=paste(rootPath,"/Data/RNN/",
                             "RNN_Forecast_cor.csv",sep="")
    
    forecast_dir_name=paste(rootPath,"/Data/RNN/",
                             "RNN_Forecast_dir.csv",sep="")
    forecast_dir_first_diff_name=paste(rootPath,"/Data/Results/",
                             "RNN_Forecast_dir_first_diff.csv",sep="")
    
    write.csv(forecast_acc, file=forecast_acc_fname)
    write.csv(forecast_cor, file=forecast_cor_fname)
    write.csv(forecast_dir, file=forecast_dir_name)
    write.csv(forecast_dir_first_diff, file=forecast_dir_first_diff_name)
    }
}

