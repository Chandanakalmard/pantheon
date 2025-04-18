import os
import re
import csv

# Regular expressions to match the different formats in the log files
log_pattern_hash = r"(\d+)\s+#\s+(\d+)"  # Timestamp # Metric value
log_pattern_dash = r"(\d+)\s+-\s+(\d+)\s+(\d+)"  # Timestamp - Metric value

# Function to convert log file to CSV
def convert_log_to_csv(input_file, output_file):
    # Prepare lists to hold data
    timestamps = []
    metric_values = []

    # Open the log file
    with open(input_file, 'r') as f:
        log_data = f.readlines()

    # Parse the log data
    for line in log_data:
        match_hash = re.search(log_pattern_hash, line)
        match_dash = re.search(log_pattern_dash, line)
        
        if match_hash:
            timestamps.append(int(match_hash.group(1)))  # Timestamp
            metric_values.append(int(match_hash.group(2)))  # Metric value after #
        elif match_dash:
            timestamps.append(int(match_dash.group(1)))  # Timestamp
            metric_values.append(int(match_dash.group(2)))  # First value after -

    # Write data to CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Metric Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for timestamp, value in zip(timestamps, metric_values):
            writer.writerow({'Timestamp': timestamp, 'Metric Value': value})

    print(f"Data saved to {output_file}")

# Define the directory where your log files are stored
log_directory = "/home/chandana/pantheon/experiments_logs/high_latency"  # Adjust to your directory
output_directory = "/home/chandana/pantheon/experiments_logs/csv_high_latency_outputs"  # Adjust to your desired output folder

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# List all log files in your log directory (you can also specify file names if you prefer)
log_files = [f for f in os.listdir(log_directory) if f.endswith('.log')]

# Process each log file and convert it to CSV
for log_file in log_files:
    input_file_path = os.path.join(log_directory, log_file)
    output_file_path = os.path.join(output_directory, log_file.replace(".log", ".csv"))
    
    convert_log_to_csv(input_file_path, output_file_path)
