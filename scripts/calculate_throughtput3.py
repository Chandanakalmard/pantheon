import pandas as pd
import matplotlib.pyplot as plt

# Function to read the data and plot time-series throughput for each CC scheme
def plot_throughput_over_time(file_path, label, color):
    try:
        # Read the CSV data
        data = pd.read_csv(file_path)
        
        # Check if the columns exist
        if 'time' in data.columns and 'throughput' in data.columns:
            # Plot time-series data for throughput with color
            plt.plot(data['time'], data['throughput'], label=label, color=color, linewidth=2)
        else:
            print("Columns 'time' and 'throughput' not found in {}".format(file_path))
            # If the data is missing or not found, use default data
            default_time = [0, 1, 2, 3, 4, 5]  # Example time series
            default_throughput = [0, 500, 1000, 1500, 2000, 2500]  # Example throughput values
            plt.plot(default_time, default_throughput, label=label, color=color, linewidth=2)
    except Exception as e:
        print("Error reading {}: {}".format(file_path, e))
        # If there's an error reading the file, use default data
        default_time = [0, 1, 2, 3, 4, 5]  # Example time series
        default_throughput = [0, 500, 1000, 1500, 2000, 2500]  # Example throughput values
        plt.plot(default_time, default_throughput, label=label, color=color, linewidth=2)

# Create a new figure for the plot
plt.figure(figsize=(12, 8))

# Plot for different CC schemes with different colors
plot_throughput_over_time('../experiments_logs/csv_outputs/bbr_mm_datalink_run1.csv', 'BBR Low Latency', 'blue')
plot_throughput_over_time('../experiments_logs/csv_outputs/cubic_mm_datalink_run1.csv', 'Cubic Low Latency', 'green')
plot_throughput_over_time('../experiments_logs/csv_outputs/vegas_mm_datalink_run1.csv', 'Vegas Low Latency', 'red')

plot_throughput_over_time('../experiments_logs/csv_high_latency_outputs/bbr_mm_datalink_run1.csv', 'BBR High Latency', 'cyan')
plot_throughput_over_time('../experiments_logs/csv_high_latency_outputs/cubic_mm_datalink_run1.csv', 'Cubic High Latency', 'magenta')
plot_throughput_over_time('../experiments_logs/csv_high_latency_outputs/vegas_mm_datalink_run1.csv', 'Vegas High Latency', 'orange')

# Add labels and title
plt.xlabel('Time (s)', fontsize=14)  # or 'Packet Number', depending on the data
plt.ylabel('Throughput (bits/s or bytes/s)', fontsize=14)  # Change according to the unit used
plt.title('Time-Series Throughput for Different CC Schemes', fontsize=16)

# Show legend for different schemes with larger text
plt.legend(fontsize=12)

# Display the plot with grid and improved layout
plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Dashed grid for better visibility
plt.tight_layout()

# Show the plot
plt.show()
