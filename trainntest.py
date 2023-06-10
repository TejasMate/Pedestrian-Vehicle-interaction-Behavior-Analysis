from sklearn.model_selection import train_test_split

def trainntest(df):  
    
    train_df, test_df = train_test_split(df, test_size=0.3, random_state=1, stratify=None)
    
    # Ensure no rows are common in train and test
    train_df = train_df[~train_df.index.isin(test_df.index)] 
    test_df = test_df[~test_df.index.isin(train_df.index)]
    
    # Define feature and target columns
    features = ['Current_Pedestrian_Velocity', 'Current_Pedestrian_Average', 'Pedestrian_Maximum_Speed',  
                'Pedestrian_Variance_in_Speed', 'Current_Vehicle_Velocity','Current_Vehicle_Average', 'Vehicle_Maximum_Speed', 'Distance', 
                'Lanewidth']
    
    target = 'Decision' 
    
    # Separate train features and target
    X_train = train_df[features]  
    y_train = train_df[target]
    
    # Initialize model  
    model = LogisticRegression()
    
    # Fit model excluding intercept 
    model.fit(X_train[features], y_train)     
    
    # Separate test features       
    X_test = test_df[features]
    
    # Make predictions 
    y_pred = model.predict(X_test)
    
    # Get actual decisions   
    try: 
        y_test = test_df['Decision']  
    except KeyError:
        pass 
   
    # Print predictions    
    for p, t in zip(y_pred, y_test):
        print(f"Predicted: {p}, Actual: {t}")  
    
    # Total, Correct, Incorrect and its Percentage predictions
    total = len(y_pred)
    correct = sum(p == t for p, t in zip(y_pred, y_test))
    incorrect = total - correct
    correct_percent = correct / total * 100
    incorrect_percent = incorrect / total * 100
    
    # Print results
    print(f"{correct} predictions were correct ({correct_percent}%)")  
    print(f"{incorrect} predictions were incorrect ({incorrect_percent}%)")
