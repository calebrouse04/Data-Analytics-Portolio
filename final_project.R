rm(list=ls(all=TRUE));gc()
setwd("/Users/calebrouse/Documents/ECON4620")
packages <- c("tidyverse",'openxlsx','caret',"rvest","AER","spdep","readxl","relaimpo","psych","pdfetch","tseries",'broom','readxl','boot')
packages[!unlist(lapply(packages, require, character.only = TRUE))]

ag<- read_xlsx("/Users/calebrouse/Documents/ECON4620/wiso/finXam.xlsx")
data <- read_xlsx("/Users/calebrouse/Documents/ECON4620/legatum.xlsx")
data<-merge(data,ag,by='iso3')
world <- read_xlsx("/Users/calebrouse/Documents/ECON4620/wiso/worldData.xlsx")
data <- merge(data,world, by= 'iso3')
head(data)

# Remove missing values from your data
data <- na.omit(data)

# Fit your regression model with the log-transformed variable
#---- unrestricted -----
urmodel<- lm(data$Unemployment ~  data$DigitalSkillsAmongPopulation + data$AdultLiteracy + data$EducationInequality + 
             data$Smoking + data$SafetyWalkingAloneAtNight + data$Obesity+
             data$OpportunityToMakeFriends+ data$FemaleLabourForceParticipation + data$EducationLevelOfAdultPopulation  , data = data)
summary(urmodel)

#correlation 
rownames(data)<-data$iso3
k<-data[,sapply(data,is.numeric)]
sort((cor(k$Unemployment,k)[1,]))

summary(model)
#---restricted-----
model<- lm(Unemployment ~  data$DigitalSkillsAmongPopulation + data$YouthUnemployment+ data$SkillsetOfUniversityGraduates
  + data$FreedomFromForcedLabour + 
             data$Obesity , data = data)

summary(model)
reset(model)
#.01
vif(model)
#--heteroskedacity issue
#highest is 3.279
ncvTest(model)

# Print the result
print(num_observations)

#------- Monte Carlo simulation--------#

# Define the number of simulations to run
n_sims <- 10000

# Define a vector to store the p-values
p_values <- rep(0, n_sims)

# Define the variables to use in the model
vars <- c("DigitalSkillsAmongPopulation" , "YouthUnemployment" , "SkillsetOfUniversityGraduates", "FreedomFromForcedLabour" , "Obesity")

# Start the simulation loop
for (i in 1:n_sims) {
  
  # Generate a random sample of data with the same structure as your data
  sim_data <- data.frame(lapply(data[vars], function(x) rnorm(nrow(data), mean(x), sd(x))))
  
  # Add the unemployment column to the simulated data
  sim_data$Unemployment <- rnorm(nrow(data), mean(data$Unemployment), sd(data$Unemployment))
  
  # Fit the regression model to the simulated data
  sim_model <- lm(Unemployment ~  data$DigitalSkillsAmongPopulation  + data$pctEmpAgr + data$FemaleLabourForceParticipation +
                    data$OpportunityToMakeFriends + data$LabourForceParticipation, data = sim_data)
  
  # Extract the p-value from the summary of the model
  p_values[i] <- summary(sim_model)$coefficients[5,4]
}

# Calculate the proportion of p-values that are less than 0.05
prop_significant <- sum(p_values < 0.05) / n_sims

# Print the proportion of significant p-values
cat("Proportion of significant p-values:", prop_significant)

# Calculate the mean of each variable
means <- colMeans(data[vars])

# Get the coefficients from the model
coefficients <- coef(model)[-1]

# Calculate the elasticities
elasticities <- means * coefficients / mean(data$Unemployment)

# Print the results
cat("Elasticities:")
print(elasticities)

# Create a new workbook
wb <- createWorkbook()

# Add a new worksheet to the workbook
addWorksheet(wb, "Summary")

# Tidy the model summary into a data frame using broom
model_summary <- tidy(urmodel)
# Write the summary output to the worksheet
writeDataTable(wb, "Summary", model_summary)

# Save the workbook
saveWorkbook(wb, "urrestrict.xlsx", overwrite = TRUE)
