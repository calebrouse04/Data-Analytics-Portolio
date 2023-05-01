rm(list=ls(all=TRUE));gc()
setwd("/Users/calebrouse/Documents/ECON4620")
packages <- c("tidyverse",'openxlsx','caret',"rvest","AER","spdep","readxl","relaimpo","psych","pdfetch","tseries",'broom')
packages[!unlist(lapply(packages, require, character.only = TRUE))]
]

dpv<-"Unemployment"
ivv<-c("AdultLiteracy","EducationInequality","DigitalSkillsAmongPopulation","EducationLevelOfAdultPopulation")
bb<-WDI(country="all",indicator=c(dpv,ivv),start=2016,end=2016)
dim(bb)

data("wrld_simpl")
plot(wrld_simpl)

w<-merge(bb,wrld_simpl@data,by.x="iso2c",by.y="ISO2",all.y=TRUE)
rownames(w)<-w$ISO3
pii<-rownames(wrld_simpl@data) # here we make sure the rows are the same in w and wrld_simpl@data
w<-w[pii,]

fxx<-formula(paste(dpv,paste(ivv,collapse="+"),sep="~")) # create formula
summary(xR<-lm(fxx,data=w))  # run regression

fii<-rownames(xR$model)  # identify observations without missing values
w<-w[fii,] # keep only those observations in our data

wdd<-as.matrix(w[,c("LON","LAT")]) # longitude is the x coordinate, latitude is the y coordinate
wdd<-distm(wdd)/1000  # create a matrix that will have the distance in km between each country
dimnames(wdd)<-list(rownames(w),rownames(w)) # assign country names to rownames and colnames
table(rowSums(y<-(wdd<=apply(wdd,1,quantile,.075))*1)) # A zero matrix y with ones for the closest 14 countries to each country

diag(y)<-0
quantile(round(apply(y*wdd,1,max))) # can see how far the furthest are
wdd<-y*wdd^(-2) # convert distance to proximity and set all but the 13 closest to zero
diag(wdd)<-0
wdd<-wdd/rowSums(wdd) # row normalize (so that rows sum to one)
range(wdd)

table(rowSums(wdd>0))

wdd[1:6,1:6]

x <- mat2listw(wdd) # convert the matrix to a listw object
wmatdd<- nb2listw(x$neighbours, style="W") # this second step simply helps avoid a warning message

summary(xR<-lm(fxx,data=w))  # run regression
lm.LMtests(xR, wmatdd, test=c("LMlag")) #H0: no spatial lag needed


w$alat<-abs(w$LAT) # higher values mean greater distance from equator
w$rn<-rnorm(nrow(w)) # randomly generated variable
for(i in c(dpv,ivv,"rn","alat")){ 
  print(paste("==========",i,"=================="))
  print(moran.mc(w[,i], wmatdd, 500)) # H0: no spatial autocorrelation
}

w$Wy<-wdd%*%as.matrix(w$SP.DYN.TFRT.IN) # multiply the spatial weight matrix by the dependent variable to get the spatial lag term
# --unfortunately, the spatial lag term is endogenous, so we have to make an IV for the spatial lag
zz<-wdd%*%as.matrix(w[,ivv]) # multiply the spatial weight matrix by the exogenous independent variables to get spatially lagged independent variables. these have been shown to make good instruments.
colnames(zz)<-paste("z",1:ncol(zz),sep="")
identical(rownames(zz),rownames(w)) # verify that the rownames are identical for zz and w
## [1] TRUE
wr<-data.frame(w,zz) # if they are the same, this is an easy way to merge the two data sets

# -- do two stage least squares --
summary(ivD<-ivreg(SP.DYN.TFRT.IN ~ Wy +alat+ SL.FAM.WORK.MA.ZS + SL.EMP.TOTL.SP.FE.ZS|alat+z1+z2+SL.FAM.WORK.MA.ZS+SL.EMP.TOTL.SP.FE.ZS,data=wr),diagnostics=TRUE)
vif(ivD)
reset(ivD)
CDcoef<-function(data,i){
  d<-coef(ivreg(SP.DYN.TFRT.IN ~ Wy +alat+ SL.FAM.WORK.MA.ZS + SL.EMP.TOTL.SP.FE.ZS | alat+z1+z2+SL.FAM.WORK.MA.ZS+SL.EMP.TOTL.SP.FE.ZS,data=data[i,]))
}
system.time(bs<-boot(wr,CDcoef,1000))
coeftest(ivD,vcov=cov(bs$t))
rr<-ivD$model
mnv<-apply(rr,2,mean)
sdv<-apply(rr,2,sd)
cf<-coef(ivD)[-1]
mhh<-setdiff(names(cf),dpv)
elast<-cf[mhh]*mnv[mhh]/mnv[dpv]
stdcf<-cf[mhh]*sdv[mhh]/sdv[dpv]

r2p<-calc.relimp(cov(rr[,1:5]))$lmg # since ivD is an ivreg object, not an lm object, we use a different method to find relative importance
data.frame(elast,stdcf,r2p)



