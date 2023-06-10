import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


x_axis = "Distance"

# Load data and select relevant columns for the first CSV
df1 = pd.read_csv("Generated Files/DR_USA_Roundabout_EP/Predicted Results - P(Y) and Y.csv")
df1 = df1[[x_axis, 'p(y)']]

# Sort dataframe by distance in ascending order for the first CSV
df1 = df1.sort_values(x_axis)

# Find the range where the majority of values lie
majority_range = (df1[x_axis].quantile(0.25), df1[x_axis].quantile(0.75))

# Calculate the interval size for selecting 10 rows
num_rows = 10

# Calculate the gap for the Distance column
distance_gap = (majority_range[1] - majority_range[0]) / (num_rows - 1)

# Select rows based on the interval and gap for the first CSV
selected_rows = []
for i in range(num_rows):
    target_distance = majority_range[0] + i * distance_gap
    closest_row = df1.iloc[(df1[x_axis] - target_distance).abs().argsort()[:1]]  # Find the closest row
    selected_rows.append(closest_row)

# Convert selected rows to a DataFrame for the first CSV
selected_df1 = pd.concat(selected_rows)
selected_df1 = selected_df1.reset_index(drop=True)

# Create bar graph for the first CSV
plt.bar(selected_df1.index, selected_df1['p(y)'], width=0.25, align='center', label='After')

# Load data and select relevant columns for the second CSV
df2 = pd.read_csv("Generated Files/DR_USA_Roundabout_EP/Predicted Results - P(Y) and Y2.csv")
df2 = df2[[x_axis, 'p(y)']]

# Sort dataframe by distance in ascending order for the second CSV
df2 = df2.sort_values(x_axis)

# Select rows based on the interval and gap for the second CSV
selected_rows2 = []
for _, row in selected_df1.iterrows():
    selected_row = df2[df2[x_axis] == row[x_axis]]
    selected_rows2.append(selected_row)

# Convert selected rows to a DataFrame for the second CSV
selected_df2 = pd.concat(selected_rows2)
selected_df2 = selected_df2.reset_index(drop=True)

# Adjust x-coordinates for the bars of the second CSV
x_coordinates = selected_df1.index + 0.4

# Create bar graph for the second CSV
plt.bar(x_coordinates, selected_df2['p(y)'], width=0.25, align='center', label='Before', alpha=0.5, color="orange")

# Set x-axis ticks and labels
plt.xticks(selected_df1.index, [f"{round(majority_range[0] + i * distance_gap, 2)}" for i in range(num_rows)], fontsize=5)

plt.rcParams['font.size'] = 8
# Add labels and title
plt.ylim((0,1.8))
#plt.yticks([])
plt.xlabel(x_axis)
plt.ylabel("P (Y)")

plt.text(5, 1.6, 'My Plot Title', fontsize=8, ha='center')
for i, value in enumerate(selected_df1['p(y)']):
    plt.text(i, value + 0.1, str(round(value, 2)), ha='center', rotation='vertical', fontsize=8)
for i, value in enumerate(selected_df2['p(y)']):
    plt.text(i + 0.4, value + 0.1, str(round(value, 2)), ha='center', rotation='vertical', fontsize=8)
    
# Add legend
plt.legend()



# Show plot
plt.show()
