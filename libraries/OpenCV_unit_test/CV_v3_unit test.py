import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Read the data from the files
bgr_data = pd.read_csv('C:\Users\mike1\Documents\nao\controllers\nao\controllers\Nao_test3\BGR_results.txt', usecols=[0], skipfooter=4, engine='python')
bgr_hough_data = pd.read_csv('C:\Users\mike1\Documents\nao\controllers\nao\controllers\Nao_test3\BGR_Hough_results.txt', usecols=[0], skipfooter=4, engine='python')

# Extract the time values
bgr_times = bgr_data['Time:'].str.extract(r'(\d+\.\d+)').astype(float)
bgr_hough_times = bgr_hough_data['Time:'].str.extract(r'(\d+\.\d+)').astype(float)

# Create a scatter plot
plt.figure(figsize=(10, 6))

# Plot each method's times
plt.scatter(np.arange(len(bgr_times)), bgr_times, label='BGR', alpha=0.6)
plt.scatter(np.arange(len(bgr_hough_times)), bgr_hough_times, label='BGR+Hough Circle', alpha=0.6)

# Plot lines to connect the dots
plt.plot(bgr_times, label='BGR - Line', linestyle='--', color='blue', alpha=0.5)
plt.plot(bgr_hough_times, label='BGR+Hough Circle - Line', linestyle='--', color='orange', alpha=0.5)

plt.title('Comparison of Detection Times (BGR vs BGR+Hough Circle)')
plt.xlabel('Sample Number')
plt.ylabel('Time (seconds)')
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig('/mnt/data/comparison_plot.png')

plt.show()