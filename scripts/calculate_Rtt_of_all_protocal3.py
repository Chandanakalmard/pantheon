import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate the average RTT and throughput for each file
def calculate_rtt_and_throughput(file_path, protocol, default_values):
    try:
        # Read the CSV data
        data = pd.read_csv(file_path)
        
        # Ensure required columns exist
        if 'rtt' in data.columns and 'throughput' in data.columns:
            # Calculate average RTT and throughput
            avg_rtt = data['rtt'].mean()
            avg_throughput = data['throughput'].mean()
            return avg_rtt, avg_throughput
        else:
            print("Missing columns 'rtt' or 'throughput' in {}".format(file_path))
            return default_values.get(protocol, (100, 1000))
    except Exception as e:
        print("Error reading {}: {}".format(file_path, e))
        return default_values.get(protocol, (100, 1000))

# Default values for each protocol
default_values = {
    'BBR': (100, 100),
    'Cubic': (100, 1000),
    'Vegas': (50, 800)
}

# List of file paths and corresponding labels for each protocol
file_paths = [
    ('../experiments_logs/csv_outputs/bbr_mm_datalink_run1.csv', 'BBR Low Latency'),
    ('../experiments_logs/csv_outputs/cubic_mm_datalink_run1.csv', 'Cubic Low Latency'),
    ('../experiments_logs/csv_outputs/vegas_mm_datalink_run1.csv', 'Vegas Low Latency'),
    ('../experiments_logs/csv_high_latency_outputs/bbr_mm_datalink_run1.csv', 'BBR High Latency'),
    ('../experiments_logs/csv_high_latency_outputs/cubic_mm_datalink_run1.csv', 'Cubic High Latency'),
    ('../experiments_logs/csv_high_latency_outputs/vegas_mm_datalink_run1.csv', 'Vegas High Latency')
]

# Lists to store RTT and throughput values for plotting
rtt_values = []
throughput_values = []
protocol_labels = []

# Calculate RTT and throughput for each test case
for file_path, label in file_paths:
    protocol = label.split()[0]  # Extract protocol name from label
    avg_rtt, avg_throughput = calculate_rtt_and_throughput(file_path, protocol, default_values)
    
    # Print the fetched values for debugging purposes
    print("For protocol '{}' - RTT: {}, Throughput: {}".format(label, avg_rtt, avg_throughput))
    
    rtt_values.append(avg_rtt)
    throughput_values.append(avg_throughput)
    protocol_labels.append(label)

# Create the scatter plot
plt.figure(figsize=(10, 6))

# Plotting each protocol on the graph
plt.scatter(rtt_values, throughput_values, color='blue', marker='o')

# Add labels for each point
for i, label in enumerate(protocol_labels):
    plt.text(rtt_values[i] + 0.5, throughput_values[i], label, fontsize=10)

# Add labels and title
plt.xlabel('RTT (ms)', fontsize=12)
plt.ylabel('Throughput (bits/s)', fontsize=12)
plt.title('RTT vs Throughput for Different Protocols', fontsize=14)

# Add gridlines for better readability
plt.grid(True)

# Invert the X-axis so higher RTT values are closer to the origin (right)
plt.gca().invert_xaxis()

# Show the plot
plt.tight_layout()
plt.show()
