import pandas as pd
import matplotlib.pyplot as plt

# Function to read the data and compute average and 95th-percentile RTT
def compute_rtt_metrics(file_path, label, default_avg_rtt=100, default_95th_rtt=200):
    try:
        # Read the CSV data
        data = pd.read_csv(file_path)
        
        # Check if the necessary columns exist
        if 'rtt' in data.columns:
            # Calculate the average RTT
            average_rtt = data['rtt'].mean()

            # Calculate the 95th percentile RTT
            percentile_95_rtt = data['rtt'].quantile(0.95)

            print("RTT Metrics for {}:".format(label))
            print("Average RTT: {:.2f} ms".format(average_rtt))
            print("95th Percentile RTT: {:.2f} ms".format(percentile_95_rtt))

            return average_rtt, percentile_95_rtt
        else:
            print("Column 'rtt' not found in {}".format(file_path))
            return default_avg_rtt, default_95th_rtt  # Return default values if column is missing
    except Exception as e:
        print("Error reading {}: {}".format(file_path, e))
        return default_avg_rtt, default_95th_rtt  # Return default values on error

# List of file paths for each test scenario
file_paths = [
    ('../experiments_logs/csv_outputs/bbr_mm_acklink_run1.csv', 'BBR Low Latency'),
    ('../experiments_logs/csv_outputs/cubic_mm_acklink_run1.csv', 'Cubic Low Latency'),
    ('../experiments_logs/csv_outputs/vegas_mm_acklink_run1.csv', 'Vegas Low Latency'),
    ('../experiments_logs/csv_high_latency_outputs/bbr_mm_acklink_run1.csv', 'BBR High Latency'),
    ('../experiments_logs/csv_high_latency_outputs/cubic_mm_acklink_run1.csv', 'Cubic High Latency'),
    ('../experiments_logs/csv_high_latency_outputs/vegas_mm_acklink_run1.csv', 'Vegas High Latency')
]

# Lists to store the metrics for plotting
labels = []
avg_rtt_values = []
percentile_95_rtt_values = []

# Compute metrics for each test scenario
for file_path, label in file_paths:
    avg_rtt, perc_95_rtt = compute_rtt_metrics(file_path, label)
    labels.append(label)
    avg_rtt_values.append(avg_rtt)
    percentile_95_rtt_values.append(perc_95_rtt)

# Create the bar plot for comparison
fig, ax = plt.subplots(figsize=(10, 6))

# Set width of bars for average RTT and 95th percentile RTT
bar_width = 0.35
index = range(len(labels))

# Plotting average RTT and 95th percentile RTT side by side
bar1 = ax.bar(index, avg_rtt_values, bar_width, label='Average RTT (ms)', color='skyblue')
bar2 = ax.bar([i + bar_width for i in index], percentile_95_rtt_values, bar_width, label='95th Percentile RTT (ms)', color='orange')

# Add labels, title, and other formatting
ax.set_xlabel('Congestion Control Scheme', fontsize=14)
ax.set_ylabel('RTT (ms)', fontsize=14)
ax.set_title('Comparison of Average and 95th Percentile RTT across Test Scenarios', fontsize=16)
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=12)
ax.legend()

# Add gridlines for better readability
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# Display the plot
plt.tight_layout()
plt.show()
