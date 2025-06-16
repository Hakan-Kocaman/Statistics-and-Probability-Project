import pandas as pd # for Data reading and calculations
import matplotlib.pyplot as plt # for Plots
import seaborn as sns # for Boxplots
from scipy import stats # for Advanced calculations
import numpy as np # for Advanced calculations

def descriptiveStatisticsofPrice():
    price=df["Fiyat"]
    # Printing descriptive statistics
    print("According to Prices:")
    print(f"Count:{price.count():.2f}")
    print(f"Mean: {price.mean():.2f}")
    print(f"Median: {price.median():.2f}")
    print(f"Variance: {price.var():.2f}")
    print(f"Standart deviation: {price.std():.2f}")
    print(f"Standart error: {price.std() / len(price) ** 0.5:.2f}")
def descriptiveStatisticsofConsumption():
    consumption = df["Tuketim"]
    # Printing descriptive statistics
    print("According to Consumptions:")
    print(f"Count:{consumption.count():.2f}")
    print(f"Mean: {consumption.mean():.2f}")
    print(f"Median: {consumption.median():.2f}")
    print(f"Variance: {consumption.var():.2f}")
    print(f"Standart deviation: {consumption.std():.2f}")
    print(f"Standart error: {consumption.std() / len(consumption) ** 0.5:.2f}")

def confidenceIntervals(Fiyat_Or_Tuketim):
    data = df[Fiyat_Or_Tuketim]
    # confidence level = 0.95
    # alpha = 0.05

    # Calculate the mean
    z = stats.norm.ppf(0.975)
    se = np.std(data) / np.sqrt(len(data))
    ort = (np.mean(data) - z * se, np.mean(data) + z * se)
    # Calculate the variance
    var_lower = stats.chi2.ppf(0.025, df=len(data)-1)
    var_upper = stats.chi2.ppf(0.975, df=len(data)-1)
    var = ((len(data) - 1) * np.var(data) / var_upper, (len(data) - 1) * np.var(data) / var_lower)

    print(Fiyat_Or_Tuketim," mean of confidence interval:",ort)
    print(Fiyat_Or_Tuketim," variance of confidence interval:",var)

def sampleSizeEstimation(Fiyat_Or_Tuketim):
    std = df[Fiyat_Or_Tuketim].std()
    z = stats.norm.ppf(0.55)# confidence level = 0.90  '1 - (1 - 0.90) / 2'
    n = (z * std / 0.1) ** 2# margin of error = 0.10 '(z * std / 0.10) ** 2'
    result=np.ceil(n)
    print(Fiyat_Or_Tuketim,"sample size estimation:",result)
def hypothesisTesting():
    dizel = df[df["Yakit"] == "Dizel"]["Tuketim"]
    benzin = df[df["Yakit"] == "Benzin"]["Tuketim"]

    print("Hypothesis: 'Diesel cars usually burns less than gasoline cars' ")

    # Hypothesis Test
    t_stat, p_value = stats.ttest_ind(dizel, benzin, equal_var=False)

    print(f"p value: {p_value:.9f}")

    # Comments
    if t_stat >0:
        print("Diesel Consumption > Gasoline Consumption")
    elif t_stat<0:
        print("Gasoline Consumption > Diesel Consumption")
    else:
        print("Consumptions are close to each other")

    if p_value < 0.05:
        print("Hypothesis denied.")
    else:
        print("Difference is not enough, Hypothesis can not be denied.")

    compareTwoParameters("Yakit","Tuketim")

def compareTwoParameters(Yil_Or_Yakit_Or_Vites,Fiyat_Or_Tuketim):
    # Used for compare two features of car
    # This function allows multicombinations

    # Creating plot
    ort = df.groupby(Yil_Or_Yakit_Or_Vites)[Fiyat_Or_Tuketim].mean()

    # Translate
    if Yil_Or_Yakit_Or_Vites=="Yil":
        Yil_Or_Yakit_Or_Vites="Year"
    elif Yil_Or_Yakit_Or_Vites=="Yakit":
        Yil_Or_Yakit_Or_Vites="Fuel"
    else:
        Yil_Or_Yakit_Or_Vites="Shift"
    if Fiyat_Or_Tuketim=="Fiyat":
        Fiyat_Or_Tuketim="Price"
    else:
        Fiyat_Or_Tuketim="Consumption"

    # Configrations
    ort.plot(kind="bar", title=Fiyat_Or_Tuketim+" by "+Yil_Or_Yakit_Or_Vites, ylabel=Fiyat_Or_Tuketim, xlabel=Yil_Or_Yakit_Or_Vites)
    plt.tight_layout()
    plt.grid(True)

    # Plot is being Shown
    plt.show()

def compareYearandTwoParameters(Yakit_Or_Vites,Fiyat_Or_Tuketim):
    # Used for compare two features of car and The year
    # So we can detect improvements of features
    # This function also allows multicombinations

    # Creating plot
    pivot = df.pivot_table(index="Yil", columns=Yakit_Or_Vites,values=Fiyat_Or_Tuketim, aggfunc="mean").sort_index()

    # Translate
    if Yakit_Or_Vites == "Yakit":
        Yakit_Or_Vites = "Fuel"
    else:
        Yakit_Or_Vites = "Shift"

    if Fiyat_Or_Tuketim == "Fiyat":
        Fiyat_Or_Tuketim = "Price"
    else:
        Fiyat_Or_Tuketim = "Consumption"

    # Configurations
    pivot.plot(marker="o", figsize=(8, 5))
    plt.title(Yakit_Or_Vites+" and "+Fiyat_Or_Tuketim+" compared by Years")
    plt.xlabel("Year")
    plt.ylabel(Fiyat_Or_Tuketim)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.grid(True)

    # Plot is being Shown
    plt.show()

def compareByBrand(Fiyat_Or_Tuketim,brand_name):

    # Creating plot According to Brand name
    brand_df = df[df['Marka'] == brand_name]
    plt.figure(figsize=(14, 6))
    sns.boxplot(data=brand_df, x='Yil', y=Fiyat_Or_Tuketim)

    # Translate
    if Fiyat_Or_Tuketim=="Fiyat":
        Fiyat_Or_Tuketim="Price"
    else:
        Fiyat_Or_Tuketim="Consumption"

    # Configrations
    plt.title(brand_name+" cars compared by "+Fiyat_Or_Tuketim)
    plt.xlabel("Year")
    plt.ylabel(Fiyat_Or_Tuketim)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)

    # Plot is being Shown
    plt.show()

def createHistogram(feature):
    # Bins are like frequence of columns
    bin=100
    if feature=="Vites" or feature=="Yakit":
        bin=5

    plt.figure(figsize=(36, 6))

    # Creating the histogram
    plt.hist(df[feature], bins=bin, color='orange', edgecolor='black')

    # Configrations
    plt.title("Histogram of "+feature)
    plt.xlabel(feature)
    plt.ylabel("Amount")
    plt.grid(True)

    # Plot is being shown
    plt.show()


# Data reading
df = pd.read_csv("datas.csv")

# Main loop
while True:
    print("1-Descriptive Statistics (Price)")
    print("2-Descriptive Statistics (Consumption)")
    print("3-Create 2 Dimension Plot")
    print("4-Create 3 Dimension Plot")
    print("5-Create Boxplot")
    print("6-Create Histogram")
    print("7-Confidence Intervals Values")
    print("8-Sample Size Estimation")
    print("9-Hypothesis Test")
    print("0-Quit")
    i=int(input("Enter Index: "))
    print("----------------------------------------")
    if i == 1:
        descriptiveStatisticsofPrice()
        print("----------------------------------------")
    elif i == 2:
        descriptiveStatisticsofConsumption()
        print("----------------------------------------")
    elif i == 3:
        print("Select A Parameter: ")
        print("1-Year")
        print("2-Fuel")
        print("3-Shift")
        j=int(input("Enter Index: "))
        Yil_Or_Yakit_Or_Vites=None
        if j==1:
            Yil_Or_Yakit_Or_Vites="Yil"
        elif j==2:
            Yil_Or_Yakit_Or_Vites="Yakit"
        elif j==3:
            Yil_Or_Yakit_Or_Vites="Vites"
        else:
            continue
        print("----------------------------------------")
        print("Select A Parameter: ")
        print("1-Price")
        print("2-Consumption")
        j = int(input("Enter Index: "))
        Fiyat_Or_Tuketim = None
        if j == 1:
            Fiyat_Or_Tuketim = "Fiyat"
        elif j == 2:
            Fiyat_Or_Tuketim = "Tuketim"
        else:
            continue
        print("----------------------------------------")
        compareTwoParameters(Yil_Or_Yakit_Or_Vites,Fiyat_Or_Tuketim)
    elif i == 4:
        print("Select A Parameter: ")
        print("1-Fuel")
        print("2-Shift")
        j = int(input("Enter Index: "))
        Yakit_Or_Vites = None
        if j == 1:
            Yakit_Or_Vites = "Yakit"
        elif j == 2:
            Yakit_Or_Vites = "Vites"
        else:
            continue
        print("----------------------------------------")
        print("Select A Parameter: ")
        print("1-Price")
        print("2-Consumption")
        j = int(input("Enter Index: "))
        Fiyat_Or_Tuketim = None
        if j == 1:
            Fiyat_Or_Tuketim = "Fiyat"
        elif j == 2:
            Fiyat_Or_Tuketim = "Tuketim"
        else:
            continue
        print("----------------------------------------")
        compareYearandTwoParameters(Yakit_Or_Vites, Fiyat_Or_Tuketim)
    elif i == 5:
        print("Select A Parameter: ")
        print("1-Price")
        print("2-Consumption")
        j = int(input("Enter Index: "))
        Fiyat_Or_Tuketim = None
        if j == 1:
            Fiyat_Or_Tuketim = "Fiyat"
        elif j == 2:
            Fiyat_Or_Tuketim = "Tuketim"
        else:
            continue
        print("----------------------------------------")
        brandstr = str(input("Enter A Brand: "))
        compareByBrand(Fiyat_Or_Tuketim,brandstr)
    elif i == 6:
        print("Select A Parameter:")
        print("1-Brand")
        print("2-Year")
        print("3-Km")
        print("4-Transmission")
        print("5-Fuel")
        print("6-Price")
        print("7-Consumption")
        j = int(input("Enter Index: "))
        parameter = None
        if j == 1:
            parameter = "Marka"
        elif j == 2:
            parameter = "Yil"
        elif j == 3:
            parameter = "Km"
        elif j == 4:
            parameter = "Vites"
        elif j == 5:
            parameter = "Yakit"
        elif j == 6:
            parameter = "Fiyat"
        elif j == 7:
            parameter = "Tuketim"
        else:
            continue
        print("----------------------------------------")
        createHistogram(parameter)
    elif i==7:
        confidenceIntervals("Fiyat")
        print("----------------------------------------")
        confidenceIntervals("Tuketim")
        print("----------------------------------------")
    elif i==8:
        sampleSizeEstimation("Fiyat")
        print("----------------------------------------")
        sampleSizeEstimation("Tuketim")
        print("----------------------------------------")
    elif i==9:
        hypothesisTesting()
        print("----------------------------------------")
    elif i==0:
        break
    else:
        continue




