### Cleaning our data 

## Importing modules and datassets 

# Importing Pandas 
import pandas as pd 

# Importing the datasets needed 
path = "C:/Users/fredr/OneDrive/Documents/Master/Semester_1/Visual_analytics/Project/"
df_all_data = pd.read_csv(path + "gvc_trade_WITS-update.csv")
df_sectors = pd.read_csv(path + "sector-tiva.csv", sep=";") # The seperator for this dataset is ";"
df_countries = pd.read_csv(path + "gvc-countries.csv")

## Getting a understanding of our dataset 
# Getting a look at the data 
df_all_data.head()

# Counting values in the dataset 
df_all_data.count()

# Getting the infromation about the attributes 
df_all_data.info()

# Checking for null values 
df_all_data.isnull().sum()

## Filtering and merging the datasets 
# Create a list of the columns to be dropped
uneccesary_col = ["gtrade_fin", "gtrade_int", "traditional_trade_int", "traditional_trade_fin", "gvcbp", "gvcfp", "gvcmix"]

# Drop the specified columns
df_data = df_all_data.drop(uneccesary_col, axis=1)
# Filtering data for a range of years 

# Creating a index of year that we want dropped 
before95_index = df_data[df_data["t"] < 1995].index 

# Dropping the index 
df_data.drop(before95_index, inplace = True)

# Specify the names of the columns to use for the merge
left_on = ["sect", "source"]
right_on = ["sect", "source"]
# Perform the merge
df_filtered = pd.merge(df_data, df_sectors, left_on=left_on, right_on=right_on, how = "left")

# Drop uncessesary columns
df_filtered.drop(["sect"], axis=1, inplace=True)

# Change country abbreviation to ful name (eg. GER --> Germany)

# Use a dictionary comprehension to create a dictionary from the dataframe
dic_country_name = {row["country"]: row["country_name"] for _, row in df_countries.iterrows()}

# change country abbreviation to full name in exp and imp column
for col in ["exp", "imp"]:
    df_filtered[col] = df_filtered[col].map(dic_country_name)

## Cleaning the data 
# Getting a look at the filtered data 
df_filtered.sample(15)

# Cheking for null values 
df_filtered.isnull().sum()

# Cheking if the source is correct 
df_filtered.groupby("source").count()

# Chaning the null values to "Rest of the World"
df_filtered["exp"].fillna("Rest of the World", inplace = True)
df_filtered["imp"].fillna("Rest of the World", inplace = True)

# Defining the values we want to be droppped 
Dropp_sectors = ["adb", "eora", "wiodlr", "wiodn", "wiodo"]

# Dropping the rows that contain these values
df_clean = df_filtered[df_filtered.source.isin(Dropp_sectors) == False]

# Chainging "Viet Nam" to Vietnam
df_clean["exp"] = df_clean["exp"].replace(["Viet Nam"], "Vietnam")
df_clean["imp"] = df_clean["imp"].replace(["Viet Nam"], "Vietnam")

# Chainging the column names 
df_clean.rename(columns = {"exp":"Export", "imp":"Import", "t":"Year", "source":"Source", "gtrade":"Gross Trade", "traditional_trade":"Traditional Trade", "gvc":"GVC", "category":"Category"}, inplace = True)

# Removing where export and import is the same country 
df_clean = df_clean[df_clean["Export"] != df_clean["Import"]]

# Looking at the clean dataframe
df_clean.sample(15)

# Counting the clean dataset 
df_clean.count()

# Checking for null values 
df_clean.isnull().sum()

## Saving the data 
# Save the clean dataset as a csv file
# df_clean.to_csv("C:/Users/fredr/OneDrive/Documents/Master/Semester_1/Visual_analytics/Project/cleaned_data.csv")