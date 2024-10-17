# Install and load necessary libraries for the database interaction, random forest and model evaluation

#install.packages("DBI")
#install.packages("ranger")
#install.packages("randomForest")
#install.packages("caret")
#install.packages("ggplot2")

#install.packages("lubridate")
library(DBI)
library(ranger)
library(randomForest)
library(caret)
library(rpart)
library(ggplot2)
library(lubridate)

# Connect to SQLite database
con <- dbConnect(RSQLite::SQLite(), "Path to DataBase.db")

# List available tables
tables <- dbListTables(con)
print(tables)

# Read the data from the selected table
data <- dbReadTable(con, "updated_table")
head(data) # Display the first row in the dataset

# Disconnect from the database
dbDisconnect(con)

# Show the summary of the dataset and check for missing values
summary(data)
missing_values <- colSums(is.na(data))
print(missing_values)


# Plot all variables 

# Ensure the "date" column is properly formatted as Date
data$date <- as.Date(data$date)

# Extract year and month from the "date" column
data$year <- year(data$date)
data$month <- month(data$date)

# Get the names of all columns
variable_names <- colnames(data)

# Columns to exclude
exclude_columns <- c("date", "year", "month", "day", "time")

# Plot with exact dates using geom_col()
for (variable in setdiff(variable_names, exclude_columns)) {
  
  # Create a plot using exact dates
  p <- ggplot(data, aes(x = date, y = .data[[variable]])) +
    geom_col() +  # Column plot
    labs(title = paste("Date vs", variable),
         x = "Date", y = variable) +
    theme_minimal() +
    scale_x_date(date_labels = "%Y-%m", date_breaks = "6 months") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  print(p)
}


# Shuffle the data for randomness  
set.seed(42)
shuffled_data <- data[sample(nrow(data)), ]

# Split the data into training 80% and validation 20%
train_index <- createDataPartition(shuffled_data$price_kw.ore, p = .8, list = FALSE, times = 1)
train_data <- shuffled_data[train_index,]
val_data <- shuffled_data[-train_index,]

# Remove unwanted columns from the training and validation set
train_data <- subset(train_data, select = -c(date, year, day, time))
val_data <- subset(val_data, select = -c(date, year, day, time))


# Function to calculate RMSE
calculate_rmse <- function(model, data, actual_value){
  pred <- predict(model, newdata = data)
  rmse <- RMSE(pred, actual_value)
  return(list(pred = pred, rmse = rmse))
}

# Function to calculate r-squared
calculate_r2 <- function(pred, actual_values){
  return(R2(pred, actual_values))
}

 # Function to calculate adjusted r-squared
adjusted_r2 <- function(r2, n, p){
  return(1 - ((1 - r2) * (n - 1)) / (n - p - 1))
}


# Function to evaluate models and print performance metrics
evaluate_model <- function(model, train_data, test_data, respons_var) {
  
  # Get the model name for printing
  model_name <- deparse(substitute(model))
  cat("Model used:", model_name, "\n\n")
  
  # Evaluate the model on training data
  train_results <- calculate_rmse(model, train_data, train_data[[respons_var]])
  train_r2 <- calculate_r2(train_results$pred, train_data[[respons_var]])
  n_train <- nrow(train_data)
  p_train <- length(model$finalModel$xNames)
  train_adj_r2 <- adjusted_r2(train_r2, n_train, p_train)
  
  # Evaluate the model on validation data 
  val_results <- calculate_rmse(model, val_data, val_data[[respons_var]])
  val_r2 <- calculate_r2(val_results$pred, val_data[[respons_var]])
  n_val <- nrow(val_data)
  p_val <- length(model$finalModel$xNames)
  val_adj_r2 <- adjusted_r2(val_r2, n_val, p_val)
  
  # Print the evaluation metrics
  cat("Train RMSE:", train_results$rmse, "\n")
  cat("Train Adjusted R-squared:", train_adj_r2, "\n")
  cat("Val RMSE:", val_results$rmse, "\n")
  cat("Val Adjusted R-squared", val_adj_r2, "\n\n")
  
  # Get and print the variable importance
  importance_values <- varImp(model)
  print(importance_values)
}


# Linear Regression
lm_1 <- lm(price_kw.ore ~., data = train_data)

# Show the model summary
summary(lm_1) 

# Evaluate the linear model
evaluate_model(lm_1, train_data, val_data, "price_kw.ore")


# CART Model 
set.seed(42)
cart_model <- rpart(price_kw.ore ~., data = train_data, method = "anova")

# Evaluate the CART model
evaluate_model(cart_model, train_data, val_data, "price_kw.ore")

# Plot the decision tree
plot(cart_model)

# Add text to the decision tree
text(cart_model, use.n = TRUE, all = TRUE, cex = 0.8)


# Define Control for cross validation
control <- trainControl(method = "cv", number = 5)

# Random Forest model
set.seed(42)
rf_model <- train(price_kw.ore ~., data = train_data,
                    method="rf",
                    trainControl=control,
                    tuneGrid=expand.grid(.mtry = c(2, 3, 4)))

# Evaluate the Random Forest model
evaluate_model(rf_model, train_data, val_data, "price_kw.ore")


# Ranger model 
set.seed(42)
ranger_model <- train(price_kw.ore ~., data = train_data,
                  method="ranger",
                  trControl=control,
                  tuneGrid=expand.grid(.mtry = c(2, 3, 4),
                                       .splitrule = c("variance"),
                                       .min.node.size = c(1, 5, 10)),
                  num.trees = 500,
                  importance= "impurity")

# Evaluate the Ranger model
evaluate_model(ranger_model, train_data, val_data, "price_kw.ore")



# Test on new observations

# Data September 19 and October 12
new_obs <- data.frame(
  inflation = c(1.6, 1.4),
  month = c(9, 10),
  temperature_2m_max...C. = c(20.1, 11.6),
  temperature_2m_min...C. = c(8.3, 5.9),
  temperature_2m_mean...C. = c(14, 8.5),
  precipitation_sum..mm. = c(0, 0),
  rain_sum..mm. = c(0, 0),
  snowfall_sum..cm. = c(0, 0),
  wind_speed_10m_max..km.h. = c(7.4, 20.4),
  wind_gusts_10m_max..km.h. = c(616.9, 44.6),
  sunshine_duration..min. = c(124.23, 371.9)
)

# Print the new observations 
print(new_obs)

# Predict prices for the new observations
predict_price <- predict(ranger_model, newdata = new_obs)

# Print the predicted prices
print(predict_price)
