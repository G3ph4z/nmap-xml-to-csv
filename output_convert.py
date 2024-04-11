import xml.etree.ElementTree as ET
import csv
import argparse

def convert_nmap_xml_to_csv(xml_file, csv_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open the CSV file for writing
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')

        # Write the header row
        writer.writerow(['subdomain', 'ip', 'ports'])

        # Iterate over each host in the XML file
        for host in root.findall('host'):
            # Get the subdomain, IP address, and ports
            subdomain = host.find('hostnames/hostname').get('name')
            ip = host.find('address').get('addr')
            ports = host.findall('ports/port')

            # Format the ports as 'port(service),...'
            ports_str = ','.join([f"{port.get('portid')}({port.find('service').get('name') if port.find('service') is not None else 'unknown'})" for port in ports])

            # Write the row to the CSV file
            writer.writerow([subdomain, ip, ports_str])

# Argument Parser
parser = argparse.ArgumentParser(description='Convert nmap XML output to CSV.')
parser.add_argument('xml_file', help='The nmap XML output file.')
parser.add_argument('csv_file', help='The CSV output file.')

# Parse the arguments
args = parser.parse_args()

# Call the function that does the job
convert_nmap_xml_to_csv(args.xml_file, args.csv_file)

# Print a happy message
print(f"{args.xml_file} was successfully converted to CSV and saved as {args.csv_file}")
