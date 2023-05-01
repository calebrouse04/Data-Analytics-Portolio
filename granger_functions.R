rm(list=ls(all=TRUE));gc()
setwd("C:/Users/eaeff/Documents/ECON4620")
packages <- c("tidyverse","rvest","AER","spdep","readxl","relaimpo","psych","pdfetch","tseries")
packages[!unlist(lapply(packages, require, character.only = TRUE))]

# AHETPI
# AAA

cz<-"UNRATE"
yz<-"CORESTICKM159SFRBATL"
dim(ww<-pdfetch_FRED(c(cz,yz)))
dim(ww<-ww[which(!is.na(rowSums(ww))),])
class(ww) 
tail(ww,20) # most recent data is strange
# look at plot
plot(ww) # the red is PINCOME; the black is PCEC

ww<-window(ww,end="2020-01-01") # restricting data to period before COVID-19

# head(embed(ww,20))
#--------------------------------------
#--Make stationary---------------------
#--------------------------------------
C<-ww[,cz]
Y<-ww[,yz]

#--augmented Dickey-Fuller test--
#--H0:series has unit root (series NON-stationary)--
adf.test(C) #accept
adf.test(Y) #accept

#--take first difference if variable is NON-stationary --
C<-diff(ww[,cz],1)
Y<-diff(ww[,yz],1)

#--H0:series has unit root (series NON-stationary)--
adf.test(C[which(!is.na(C))]) #reject
adf.test(Y[which(!is.na(Y))]) #reject

# -- look at plot--
a<-merge(C,Y) # it is understood that the merge is by date
plot(a) # the red is Y; the black is C

#--------------------------------------
#--find optimal lag length, using AIC--
#--------------------------------------
# C<-diff(ww[,cz],1)
# Y<-diff(ww[,yz],1)
# C<-ww[,cz]
# Y<-ww[,yz]

wx<-merge(C,Y) # make sure that you are using the stationary versions of C and Y
ss<-20
vx<-c("C","Y")

optlag<-function(wx,ss,vx){
  taic<-NULL
  for (k in 1:NCOL(wx)){
    v<-as.matrix(wx[,k])
    nobs<-NROW(wx)
    cb<-matrix(NA,nobs,ss)
    for (i in 1:ss){
      cb[(i+1):nobs,i]<-v[1:(nobs-i)]
      is.na(cb[1:i,i])<-TRUE
    }
    aic<-matrix(0,ss,2)
    z<-which(!is.na(cb[,ss]))
    for (i in 1:ss){
      aic[i,2]<-AIC(lm(v[z]~cb[z,(1:i)]),k=2)
    }
    aic[,1]<-(1:ss)
    aic<-data.frame(aic[order(aic[,2]),])
    names(aic)<-c("lags","aic")
    aic$varb<-as.character(vx[k])
    taic<-rbind(taic,aic[1,])
  }
  return(taic)
}

taic<-optlag(wx,ss,vx)
#--------------------------------------
#--Granger causality-------------------
#--------------------------------------

granger<-function(ww,taic){
  nbs<-NROW(ww)
  sc<-taic$lags[1]
  v<-as.matrix(ww[,1])
  cb<-matrix(0,nbs,sc)
  for (i in 1:sc){
    cb[(i+1):nbs,i]<-v[1:(nbs-i)]
    is.na(cb[1:i,i])<-TRUE
  }
  sy<-taic$lags[2]
  v<-as.matrix(ww[,2])
  yb<-matrix(0,nbs,sy)
  for (i in 1:sy){
    yb[(i+1):nbs,i]<-v[1:(nbs-i)]
    is.na(yb[1:i,i])<-TRUE
  }
  
  z<-which(!is.na(rowSums(yb)) & !is.na(rowSums(cb))) 
  o<-lm(C[z]~yb[z,]+cb[z,])
  kii<-names(coef(o))
  dropt<-kii[grep("yb",kii)]
  Ftest<-linearHypothesis(o,dropt)
  pval<-Ftest$`Pr(>F)`[2]
  r1<-data.frame(H0="H0: Y does not Granger cause C",pval)
  
  
  o<-lm(Y[z]~yb[z,]+cb[z,])
  kii<-names(coef(o))
  dropt<-kii[grep("cb",kii)]
  Ftest<-linearHypothesis(o,dropt)
  pval<-Ftest$`Pr(>F)`[2]
  r2<-data.frame(H0="H0: C does not Granger cause Y",pval)
  return(rbind(r1,r2))
}

granger(wx,taic)

