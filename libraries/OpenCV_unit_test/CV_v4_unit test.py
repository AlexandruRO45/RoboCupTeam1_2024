import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read the data from the files
bgr_data = pd.read_csv('C:\\Users\\mike1\\Documents\\nao\\controllers\\nao\\controllers\\Nao_test3\\BGR_results.txt', header=None, names=['Time', 'Detected', 'Target'], skipfooter=5, engine='python')
bgr_hough_data = pd.read_csv('C:\\Users\\mike1\\Documents\\nao\\controllers\\nao\\controllers\\Nao_test3\\BGR_Hough_results.txt',header=None, names=['Time', 'Detected', 'Target'], skipfooter=5, engine='python')

# Extract the time values
bgr_times = bgr_data['Time'].str.extract(r'(\d+\.\d+)').astype(float)
bgr_hough_times = bgr_hough_data['Time'].str.extract(r'(\d+\.\d+)').astype(float)

# Set the font size for all plot text
plt.rcParams.update({'font.size': 14})

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Plot each method's times without connecting lines
plt.scatter(np.arange(len(bgr_times)), bgr_times, label='BGR', alpha=0.6)
plt.scatter(np.arange(len(bgr_hough_times)), bgr_hough_times, label='BGR+Hough Circle', alpha=0.6)

# Titles and labels
plt.title('Comparison of Detection Times (BGR vs BGR+Hough Circle)')
plt.xlabel('Sample Number')
plt.ylabel('Time (seconds)')

# Move legend to the bottom right
plt.legend(loc='lower right')

# Set the x-axis limits
plt.xlim(left=0, right=len(bgr_times)-1)  # Adjusted to the length of data

plt.grid(True)

# Save the plot
plt.savefig('comparison_plot_updated.png')

plt.show()
