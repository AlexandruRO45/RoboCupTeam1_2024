import matplotlib.pyplot as plt

def read_data(file_path):
    """
    Reads data from the given file path, ignoring non-data lines.
    Extracts FOV and scaled Error Percentage for further processing.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith('---'):  # Skip separator lines
                continue
            try:
                parts = line.strip().split(', ')
                fov = int(parts[1].split(': ')[1])
                # Scale the error percentage down by dividing by 100
                error_percentage = float(parts[-1].split(': ')[1][:-1]) / 100
                data.append((fov, error_percentage))
            except (IndexError, ValueError) as e:
                print(f"Error processing line: '{line.strip()}': {e}")
    return data

def calculate_average_error(data):
    """
    Calculates the average error per FOV.
    """
    error_sum = {}
    count = {}
    for fov, error in data:
        if fov not in error_sum:
            error_sum[fov] = 0
            count[fov] = 0
        error_sum[fov] += error
        count[fov] += 1
    # Calculate average
    average_errors = {fov: error_sum[fov] / count[fov] for fov in error_sum}
    return average_errors

def plot_average_error(average_errors, title):
    """
    Plots the average error per FOV.
    """
    fovs = sorted(average_errors.keys())
    errors = [average_errors[fov] for fov in fovs]

    plt.figure(figsize=(10, 6))
    plt.plot(fovs, errors, marker='o', linestyle='-', color='red',)
    # Set the font size
    plt.rcParams['font.size'] = 12  # You can adjust the size as needed

    plt.title(title, fontsize=14)  # Adjust title font size
    plt.xlabel('FOV (Degrees)', fontsize=12)  # Adjust x-axis label font size
    plt.ylabel('Average Error Percentage (%)', fontsize=12)  # Adjust y-axis label font size

    plt.xticks(fontsize=14)  # Adjust font size of the x-axis ticks
    plt.yticks(fontsize=14)  # Adjust font size of the y-axis ticks

    plt.xlim(0, 300)  # Set the limits of the x-axis to [0, 300]
    plt.grid(True)
    plt.show()

# File paths
upper_file_path = r'C:\Users\mike1\Documents\nao\controllers\nao\controllers\Nao_test2\fov_test_results_upper.txt'
lower_file_path = r'C:\Users\mike1\Documents\nao\controllers\nao\controllers\Nao_test2\fov_test_results_lower.txt'

# Process data for each camera
data_upper = read_data(upper_file_path)
average_errors_upper = calculate_average_error(data_upper)
plot_average_error(average_errors_upper, 'Upper Camera: Average Error per FOV')

data_lower = read_data(lower_file_path)
average_errors_lower = calculate_average_error(data_lower)
plot_average_error(average_errors_lower, 'Lower Camera: Average Error per FOV')