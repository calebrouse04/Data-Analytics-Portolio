setwd("/Users/calebrouse/Documents/ECON4620")
getwd()
# Load the car library
library(car)
library(AER)
library(psych)
library(readxl)
library(relaimpo)
library(stargazer)
library(foreign)

#--Monte Carlo: Endogeneity--
#---We make up our data, 1500 times---
#---Since we make the data, we KNOW our coefficients--
#---We estimate the coefficients and compare the estimates with true values--

estcoef<-corvals<-NULL
nobs<-50
truecoef<-6
for (i in 1:1500){
  err<-33*rnorm(nobs) # error term    
  x<-33*scale(rnorm(nobs)) #exogenous independent variable
  q<-33*scale((err+x)) #endogenous independent variable
  y1<-x*truecoef+err
  y2<-q*truecoef+err  
  qe<-cbind(q,err)
  xe<-cbind(x,err)
  corvals<-rbind(corvals,cbind(cor(xe)[1,2],cor(qe)[1,2]))
  z1<-summary(lm(y1~x))
  cf1<-z1$coefficients[2,1]
  se1<-z1$coefficients[2,2]
  z2<-summary(lm(y2~q))
  cf2<-z2$coefficients[2,1]
  se2<-z2$coefficients[2,2]
  estcoef<-rbind(estcoef,cbind(cf1,se1,cf2,se2))
}
estcoef<-data.frame(estcoef)
names(estcoef)<-c("ExogBeta","ExogSE","EndogBeta","EndogSE")

head(estcoef)

#--correlation of variable with error term--
apply(corvals,2,range)

#--plot histograms of results: cor(et,et-1)--
layout(matrix(1:2,1,2))
hist(corvals[,1],breaks=50,xlim=c(-1,1),main="Exogenous")
abline(v=0,col="red",lty=2,lwd=2)
hist(corvals[,2],breaks=50,xlim=c(-1,1),main="Endogenous")
abline(v=0,col="red",lty=2,lwd=2)

#-True value of coefficient is 6; compare that to the mean of the estimated coefficients--
round(apply(estcoef[,c("ExogBeta","EndogBeta")],2,mean),6)

apply(estcoef[,c(c("ExogSE","EndogSE"))],2,mean) 

apply(estcoef[,c(c("ExogBeta","EndogBeta"))],2,sd) 

#--plot histograms of results: estimated coefficients and standard errors--
layout(matrix(1:4,2,2,byrow=TRUE))
xlm<-range(estcoef[,c("ExogBeta","EndogBeta")])
hist(estcoef$ExogBeta,breaks=50,main="Exogenous",xlim=xlm,
     xlab="Coefficients; true: red; mean: blue")
abline(v=truecoef,col="red",lty=2,lwd=2)
abline(v=mean(estcoef$ExogBeta),col="blue",lty=3,lwd=2)
hist(estcoef$EndogBeta,breaks=50,main="Endogenous",xlim=xlm,
     xlab="Coefficients; true: red; mean: blue")
abline(v=truecoef,col="red",lty=2,lwd=2)
abline(v=mean(estcoef$EndogBeta),col="blue",lty=3,lwd=2)
xlm<-range(estcoef[,c("ExogSE","EndogSE")])
hist(estcoef$ExogSE,breaks=30,main="Exogenous",xlim=xlm,
     xlab="Standard Errors; true: red; mean: blue")
abline(v=sd(estcoef$ExogBeta),col="red",lty=2,lwd=2)
abline(v=mean(estcoef$ExogSE),col="blue",lty=3,lwd=2)
hist(estcoef$EndogSE,breaks=30,main="Endogenous",xlim=xlm,
     xlab="Standard Errors; true: red; mean: blue")
abline(v=sd(estcoef$EndogBeta),col="red",lty=2,lwd=2)
abline(v=mean(estcoef$EndogSE),col="blue",lty=3,lwd=2)



download.file("http://capone.mtsu.edu/eaeff/6060/cop.dbf","zcop.dbf")
uu<-read.dbf("zcop.dbf")

summary(zD<-lm(QC~PC+Y+PA,data=uu)) # copper demand function
vif(zD)
ncvTest(zD) # H0: no heteroskedasticity
bgtest(zD,2) # H0: no 2nd order temporal autocorrelation
summary(zS<-lm(QC~PC+X+YEAR,data=uu)) # copper supply function
#--Regression on PC using only Exogenous regressors--
summary(zP<-lm(PC~PA+X+Y+YEAR,data=uu)) # first-stage regression
PCfit<-zP$fitted.values # fitted value for price of copper from first-stage regression
PCres<-zP$residuals    # residual from first-stage regression
summary(zDh<-lm(QC~PC+Y+PA+PCres,data=uu))
summary(zDiv<-lm(QC~PCfit+Y+PA,data=uu))
vif(zDiv)
#--bootstrapped standard errors--
CDcoef<-function(data,i){
  vzz<-data[i,]
  PCfit<-lm(PC~PA+X+Y+YEAR,data=vzz)$fitted.values
  coef(lm(QC~PCfit+Y+PA,data=vzz))
}
bs<-boot(uu,CDcoef,1000)
coeftest(zDiv,vcov=cov(bs$t))
summary(ivD<-ivreg(QC~PC+Y+PA|Y+PA+X+YEAR,data=uu),diagnostics=TRUE)

#--Use the bootstrap standard errors--
CDcoef<-function(data,i){
  coef(ivreg(QC~PC+Y+PA|Y+PA+X+YEAR,data=data[i,]))
}
bs<-boot(uu,CDcoef,1000)
summary(ivD,vcov=cov(bs$t),diagnostics=TRUE)

