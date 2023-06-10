import pandas as pd
import statsmodels.formula.api as smf 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from sklearn.linear_model import LogisticRegression 

import trainntest


def confusion_mtx(df):
    actual = df['Decision'].values 
    predicted = df['y'].values >= 0.5

    cm = confusion_matrix(actual, predicted)

    # Create a heatmap using seaborn
    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, square=True,
                xticklabels=['Predicted Positive', 'Predicted Negative'],
                yticklabels=['Actual Positive', 'Actual Negative'])

    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    
    plt.savefig("Generated Files\DR_USA_Roundabout_EP\Confusion Matrix.png")
    #plt.savefig("Generated Files\DR_USA_Intersection_EP0\Confusion Matrix.png")

    # Show plot
    plt.show() 
    plt.clf()
    


def plot(df, lowest_p_value_col):

    # Sort the data by Distance
    df_sorted = df.sort_values('Distance')
    
    # Define feature and target columns
    features = ['Distance']
    target = ['y']
    
    # Separate features and target
    X = df_sorted[features]
    y = df_sorted[target]
    
    # Initialize and fit the logistic regression model
    model = LogisticRegression()
    model.fit(X, y)
    
    # Create a range of x values for the curve
    x_curve = np.linspace(X.min(), X.max(), 100)
    
    # Predict the yield probability for the x values
    y_curve = model.predict_proba(x_curve)[:, 1]
    
    # Plot the curve
    plt.figure(figsize=(8, 6))
    plt.plot(x_curve, y_curve, color='red', label='Yield Probability Curve')
    
    # Add legend and labels
    plt.legend()
    plt.xlabel('Distance')
    plt.ylabel('Yield Probability')
    plt.title('Yield Probability Curve for Logistic Regression Model')
    
    # Add grid lines
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Customize the appearance
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xlim(X.min(), X.max())
    plt.ylim(0, 1)
    
    # Show plot
    plt.tight_layout()
    plt.show()

    plt.savefig(f"Generated Files\DR_USA_Roundabout_EP\{lowest_p_value_col} vs Yielding.png")
    #plt.savefig(f"Generated Files\DR_USA_Intersection_EP0\{lowest_p_value_col} vs Yielding.png")
    

# Load data
df = pd.read_csv("Generated Files\DR_USA_Roundabout_EP\DR_USA_Roundabout_EP.csv")
#df = pd.read_csv("Generated Files\DR_USA_Intersection_EP0\DR_USA_Intersection_EP0.csv")

df = df[["Decision", "Current_Pedestrian_Velocity", "Current_Pedestrian_Average", "Pedestrian_Maximum_Speed", "Pedestrian_Variance_in_Speed", "Current_Vehicle_Velocity", "Current_Vehicle_Average", "Vehicle_Maximum_Speed", "Distance", "Lanewidth"]]
df = df.dropna()

# Define and fit model 
log_reg = smf.logit("Decision ~ Current_Pedestrian_Velocity + Current_Pedestrian_Average + Pedestrian_Maximum_Speed + Pedestrian_Variance_in_Speed + Current_Vehicle_Velocity + Current_Vehicle_Average + Vehicle_Maximum_Speed + Distance + Lanewidth", data=df).fit()
print(log_reg.summary())

# Get coefficients 
b0 = log_reg.params['Intercept']  
b1 = log_reg.params['Current_Pedestrian_Velocity']   
b2 = log_reg.params['Current_Pedestrian_Average']    
b3 = log_reg.params['Pedestrian_Maximum_Speed']    
b4 = log_reg.params['Pedestrian_Variance_in_Speed']    
b5 = log_reg.params['Current_Vehicle_Velocity']    
b6 = log_reg.params['Current_Vehicle_Average']    
b7 = log_reg.params['Vehicle_Maximum_Speed']    
b8 = log_reg.params['Distance']    
b9 = log_reg.params['Lanewidth']   

logits = [] 
ps = []
ys = [] 

for row in df.iterrows(): 
    x1 = row[1]['Current_Pedestrian_Velocity']  
    x2 = row[1]['Current_Pedestrian_Average']  
    x3 = row[1]['Pedestrian_Maximum_Speed']   
    x4 = row[1]['Pedestrian_Variance_in_Speed']   
    x5 = row[1]['Current_Vehicle_Velocity']   
    x6 = row[1]['Current_Vehicle_Average']   
    x7 = row[1]['Vehicle_Maximum_Speed']   
    x8 = row[1]['Distance']   
    x9 = row[1]['Lanewidth']   
    
    logit = b0 + b1*x1 + b2*x2 + b3*x3 + b4*x4 + b5*x5 + b6*x6 + b7*x7 + b8*x8 + b9*x9
    p = 1 / (1 + np.e**-logit)
    y = 1 if p >= 0.5 else 0
    
    logits.append(logit)
    ps.append(p)
    ys.append(y)

df['logit'] = logits
df['p(y)'] = ps
df['y'] = ys
df.to_csv("Generated Files\DR_USA_Roundabout_EP\Predicted Results - P(Y) and Y.csv") 
#df.to_csv("Generated Files\DR_USA_Intersection_EP0\Predicted Results - P(Y) and Y.csv") 

lowest_p_value_col = log_reg.pvalues.idxmin()


confusion_mtx(df)
plot(df, lowest_p_value_col)
trainntest.trainntest(df)