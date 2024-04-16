import matplotlib.pyplot as plt

def read_data(file_path):
    """
    Reads data from the given file path, ignoring non-data lines.
    Extracts FOV and Error Percentage for plotting.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Skip lines that do not contain data entries
            if line.strip().startswith('---'):
                continue
            try:
                parts = line.strip().split(', ')
                camera = parts[0].split(': ')[1]
                fov = int(parts[1].split(': ')[1])
                error_percentage = float(parts[-1].split(': ')[1][:-1])  # Remove '%' and convert to float
                data.append((camera, fov, error_percentage))
            except (IndexError, ValueError) as e:
                print(f"Error processing line: '{line.strip()}': {e}")
    return data

def plot_fov_vs_error(data, title):
    """
    Plots FOV vs Error Percentage for the given data.
    """
    # Extract FOV and Error Percentage
    fovs = [item[1] for item in data]
    errors = [item[2] for item in data]

    plt.figure(figsize=(10, 6))
    plt.scatter(fovs, errors, alpha=0.7, marker='o', c='b', label='Error Percentage')
    plt.title(title)
    plt.xlabel('FOV (Degrees)')
    plt.ylabel('Error Percentage (%)')
    plt.grid(True)
    plt.legend()
    plt.show()

# Paths to your data files, adjusted to your provided path
upper_file_path = r'C:\Users\mike1\Documents\nao\controllers\nao\controllers\Nao_test2\fov_test_results_upper.txt'
lower_file_path = r'C:\Users\mike1\Documents\nao\controllers\nao\controllers\Nao_test2\fov_test_results_lower.txt'

# Process and plot data for each camera
data_upper = read_data(upper_file_path)
plot_fov_vs_error(data_upper, 'Upper Camera: FOV vs Error Percentage')

data_lower = read_data(lower_file_path)
plot_fov_vs_error(data_lower, 'Lower Camera: FOV vs Error Percentage')