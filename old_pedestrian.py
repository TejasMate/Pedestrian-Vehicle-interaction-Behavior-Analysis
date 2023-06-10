from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def current_velocity(pedestrian_df, vehicle_df, interact_onepair):
   
    #ped = interact_df.iloc[0]['Pedestrian TrackID']
    timestamps = interact_onepair['Timestamp'].values.flatten()
    pedestrian_speeds = interact_onepair['Pedestrian Speed'].values
    vehicle_speeds = interact_onepair['Vehicle Speed'].values
    
    # plot the data
    plt.plot(timestamps, pedestrian_speeds, 'o', markersize=1, label='Pedestrian Speed')
    plt.plot(timestamps, vehicle_speeds, 'o', markersize=1, label='Vehicle Speed')
    
    # calculate linear regression for pedestrian speed
    x_ped = np.array(timestamps)
    y_ped = np.array(pedestrian_speeds)
    slope_ped, intercept_ped = np.polyfit(x_ped, y_ped, 1)
    plt.plot(x_ped, slope_ped*x_ped + intercept_ped, '-')
    
    # calculate linear regression for vehicle speed
    valid_indices = np.where(~np.isnan(vehicle_speeds))[0]
    x_veh = np.array(timestamps)[valid_indices]
    y_veh = np.array(vehicle_speeds)[valid_indices]
    slope_veh, intercept_veh = np.polyfit(x_veh, y_veh, 1)
    plt.plot(x_veh, slope_veh*x_veh + intercept_veh, '-')
    
    # add labels and legend
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.legend()
    
    # show the plot
    plt.show()

    
    
    """
    # Extract the timestamp and speed values into separate arrays
    X = interact_onepair['Timestamp'].values.reshape(-1, 1)
    ped_y = interact_onepair['Pedestrian Speed'].values
    veh_y = interact_onepair['Vehicle Speed'].values
    
    #curr_ped_df = pedestrian_df[pedestrian_df['track_id'] == ped]

    
    # Create a linear regression model
    model = LinearRegression()
    
    # Fit the model to the data
    model.fit(X, ped_y)
        
    # Plot the data points and the linear regression line
    plt.scatter(X, ped_y, s=1, alpha=0.8)
    plt.plot(X, model.predict(X), color='red')
           
    # Create a linear regression model
    model = LinearRegression()
    
    # Fit the model to the data
    model.fit(X, veh_y)
        
    # Plot the data points and the linear regression line
    plt.scatter(X, veh_y, s=10, alpha=0.8)
    plt.plot(X, model.predict(X), color='red')
    
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.title('Current Speed of Pedestrian')
    plt.show()
    
    print(type(X))
    
    #df = pd.DataFrame({'Timestamp': X, 'Current Speed at that timestamp': y})
    #df.to_csv("Generated Files/Current Speed of Pedestrian.csv")    
    """

def average_velocity(pedestrian_df, vehicle_df, interact_onepair):
    
    timestamps = interact_onepair['Timestamp'].values.flatten()
    pedestrian_speeds = interact_onepair['Pedestrian Speed'].values
    vehicle_speeds = interact_onepair['Vehicle Speed'].values
    
    ped_avg = [sum(pedestrian_speeds[:i+1])/(i+1) for i in range(len(pedestrian_speeds))]
    ped_avg = np.array(ped_avg)
    
    veh_avg = [sum(vehicle_speeds[:i+1])/(i+1) for i in range(len(vehicle_speeds))]
    veh_avg = np.array(veh_avg)
    
    print(veh_avg)
    
    # plot the data
    plt.plot(timestamps, ped_avg, 'o', markersize=1, label='Pedestrian Speed')
    plt.plot(timestamps, veh_avg, 'o', markersize=1, label='Vehicle Speed')
    
    # calculate linear regression for pedestrian speed
    x_ped = np.array(timestamps)
    y_ped = np.array(ped_avg)
    slope_ped, intercept_ped = np.polyfit(x_ped, y_ped, 1)
    plt.plot(x_ped, slope_ped*x_ped + intercept_ped, '-')
    
    # calculate linear regression for vehicle speed
    x_veh = np.array(timestamps)
    y_veh = np.array(veh_avg)
    slope_veh, intercept_veh = np.polyfit(x_veh, y_veh, 1)
    plt.plot(x_veh, slope_veh*x_veh + intercept_veh, '-')
    
    # add labels and legend
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.legend()
    
    # show the plot
    plt.show()
    
    """
    
    ped = interact_df.iloc[0]['Pedestrian TrackID']
    curr_ped_df = pedestrian_df[pedestrian_df['track_id'] == ped]
    
    # Extract the timestamp and speed values into separate arrays
    X = curr_ped_df['timestamp_ms'].values.reshape(-1, 1)
    y = curr_ped_df['speed'].values
    
    avg = [sum(y[:i+1])/(i+1) for i in range(len(y))]
    
    # Create a linear regression model
    model = LinearRegression()
    # Fit the model to the data
    model.fit(X, avg)
    
    # Plot the data points and the linear regression line
    plt.scatter(X, avg, s=10, alpha=0.8)
    plt.plot(X, model.predict(X), color='red')
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.title('Average Speed of Pedestrian')
    plt.show()
    
    #df = pd.DataFrame({'Timestamp': X, 'Average Speed at that timestamp': avg})
    #df.to_csv("Generated Files/Average Speed of Pedestrian.csv")  
    """
    
def maximum_velocity(pedestrian_df, interact_df):
    ped = interact_df.iloc[0]['Pedestrian TrackID']
    curr_ped_df = pedestrian_df[pedestrian_df['track_id'] == ped]
    
    # Extract the timestamp and speed values into separate arrays
    X = curr_ped_df['timestamp_ms'].values.reshape(-1, 1)
    y = curr_ped_df['speed'].values
    
    max_vals = [max(y[:i+1]) for i in range(len(y))]

    # Create a linear regression model
    model = LinearRegression()
    # Fit the model to the data
    model.fit(X, max_vals)
    
    plt.scatter(X, max_vals, s=10, alpha=0.8)
    plt.plot(X, model.predict(X), color='red')
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.title('Maximum Speed of Pedestrian')
    plt.show()
    
    X = curr_ped_df['timestamp_ms'].values
    df = pd.DataFrame({'Timestamp': X, 'Maximum Speed at that timestamp': max_vals})
    df.to_csv("Generated Files/Maximum Speed of Pedestrian.csv")  
    
def variance_velocity(pedestrian_df, interact_df):
    ped = interact_df.iloc[0]['Pedestrian TrackID']
    curr_ped_df = pedestrian_df[pedestrian_df['track_id'] == ped]
    
    X = curr_ped_df['timestamp_ms'].values.reshape(-1, 1)
    y = curr_ped_df['speed'].values
    
    diff = [0] + [y[i] - y[i-1] for i in range(1, len(y))]         

    model = LinearRegression()
    model.fit(X, diff)
    
    plt.scatter(X, diff, s=10, alpha=0.8)
    plt.plot(X, model.predict(X), color='red')
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.title('Variance Speed of Pedestrian')
    plt.show()
    
    #df = pd.DataFrame({'Timestamp': X, 'Variance Speed at that timestamp': diff})
    #df.to_csv("Generated Files/Variance Speed of Pedestrian.csv") 
    
def ratio_velocity(pedestrian_df, interact_df):
    
    ped = interact_df.iloc[0]['Pedestrian TrackID']
    curr_ped_df = pedestrian_df[pedestrian_df['track_id'] == ped]
    
    X = curr_ped_df['timestamp_ms'].values.reshape(-1, 1)
    distance = curr_ped_df['distance'].values
    
    # Replace NaN values with 0
    distance[np.isnan(distance)] = 0
    
    ratio1 = [sum(distance[:i+1]) for i in range(len(distance))]
    ratio2 = [0] + [distance[i] - distance[i-1] for i in range(1, len(distance))]     
    
    ratio1 = np.array(ratio1)
    ratio2 = np.array(ratio2)

    y=ratio1/ratio2
    y[np.isnan(y)] = 0
    y[np.isinf(y)] = 0
    
    model = LinearRegression()
    model.fit(X, y)
    
    plt.scatter(X, y, s=10, alpha=0.8)
    plt.plot(X, model.predict(X), color='red')
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.title('Ratio Distance of Pedestrian')
    plt.show()
    
    #df = pd.DataFrame({'Timestamp': X, 'Ratio Speed at that timestamp': y})
    #df.to_csv("Generated Files/Ratio Speed of Pedestrian.csv") 
    