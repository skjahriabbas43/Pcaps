from scapy.all import rdpcap
import os
import pandas as pd

# Directory containing the PCAP files
pcap_directory = r"C:\Users\Admin\OneDrive - Subex Limited\Desktop\SITE_Pcaps"

# Define Suricata supported protocols (this list can be extended)
suricata_supported_protocols = [
    'Ethernet', 'IP', 'TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'FTP', 'TFTP', 'DNS', 'DHCP', 
    'SMTP', 'IMAP', 'POP3', 'SNMP', 'SSH', 'MQTT', 'COAP', 'RDP', 'Telnet', 'SMB', 'NFS', 
    'LDAP', 'SIP', 'RTSP', 'RTP', 'ICMP', 'Modbus', 'DNP3', 'ENIP', 'NTP', 'QUIC'
]

# Function to check if a protocol is supported by Suricata
def is_supported_by_suricata(protocol):
    return 'yes' if protocol.lower() in [p.lower() for p in suricata_supported_protocols] else 'no'

# List to hold the results
protocols_data = []

# Function to extract the protocol hierarchy from each packet
def extract_protocol_hierarchy(packet):
    hierarchy = []
    current_layer = packet
    while current_layer:
        hierarchy.append(current_layer.name)  # Add the name of the current layer
        current_layer = current_layer.payload  # Move to the next layer
        if not isinstance(current_layer, packet.__class__):  # Break if it's not a valid layer
            break
    return hierarchy

# Process each pcap file in the directory
for pcap_file in os.listdir(pcap_directory):
    if pcap_file.endswith('.pcap'):
        file_path = os.path.join(pcap_directory, pcap_file)
        try:
            # Read the pcap file
            packets = rdpcap(file_path)
            
            # Extract protocol hierarchy from each packet
            for packet in packets:
                protocol_hierarchy = extract_protocol_hierarchy(packet)
                hierarchy_str = ' -> '.join(protocol_hierarchy)  # Join the hierarchy for this packet
                suricata_support = [is_supported_by_suricata(proto) for proto in protocol_hierarchy]
                
                # Add a row for this packet's hierarchy and Suricata support status
                protocols_data.append([pcap_file, hierarchy_str, ', '.join(suricata_support)])

        except Exception as e:
            print(f"Error reading pcap file {pcap_file}: {e}")

# Create a DataFrame from the extracted protocol data
protocols_df = pd.DataFrame(protocols_data, columns=['PCAP File', 'Protocol Hierarchy', 'Suricata Support'])

# Save the results to an Excel file
output_file = 'protocol_hierarchies_suricata_support.csv'
protocols_df.to_excel(output_file, index=False)

print(f"Excel file created: {output_file}")
