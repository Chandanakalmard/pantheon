import pandas as pd

# Calculate Throughput
def calculate_throughput(file_name):
    try:
        data = pd.read_csv(file_name)
        data['bytes'] = data['bytes'].diff().dropna()  # Calculate throughput (difference in bytes)
        return data['bytes']
    except Exception as e:
        print("Error calculating throughput for {}: {}".format(file_name, e))
        return None

# Calculate RTT
def calculate_rtt(file_name):
    try:
        data = pd.read_csv(file_name)
        return data['rtt'].mean()  # Return the average RTT
    except Exception as e:
        print("Error calculating RTT for {}: {}".format(file_name, e))
        return None

# Calculate Loss Rate
def calculate_loss_rate(datalink_file, acklink_file):
    try:
        datalink_data = pd.read_csv(datalink_file)
        acklink_data = pd.read_csv(acklink_file)
        
        total_packets = len(datalink_data)
        lost_packets = len(datalink_data[datalink_data['ack_received'] == 0])
        
        return lost_packets / total_packets if total_packets > 0 else 0
    except Exception as e:
        print("Error calculating loss rate: {}".format(e))
        return None

def main():
    # List of protocols to analyze
    protocols = ['bbr', 'cubic', 'vegas']
    
    # Low and High latency directories
    latencies = ['low_latency', 'high_latency']
    
    for protocol in protocols:
        for latency in latencies:
            # File names based on the protocol and latency
            datalink_file = '../experiments_logs/csv_' + latency + '_outputs/' + protocol + '_mm_datalink_run1.csv'
            acklink_file = '../experiments_logs/csv_' + latency + '_outputs/' + protocol + '_mm_acklink_run1.csv'
            
            # Calculate throughput
            throughput = calculate_throughput(datalink_file)
            if throughput is not None:
                print('{} Throughput in {}: {}'.format(protocol, latency, throughput.head()))
            
            # Calculate RTT
            rtt = calculate_rtt(acklink_file)
            if rtt is not None:
                print('{} Average RTT in {}: {} ms'.format(protocol, latency, rtt))
            
            # Calculate loss rate
            loss_rate = calculate_loss_rate(datalink_file, acklink_file)
            if loss_rate is not None:
                print('{} Loss Rate in {}: {}%\n'.format(protocol, latency, loss_rate * 100))

if __name__ == "__main__":
    main()

