import yaml
import re

# Function to parse port variables from the text file
def parse_port_variables(file_path):
    port_variables = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            # Parse ipvar and portvar
            match = re.match(r'(ipvar|portvar) (\$\w+)\s+(.+)', line.strip())
            if match:
                var_type, var_name, var_value = match.groups()
                # Remove extra spaces or parentheses for special cases
                var_value = var_value.replace('(', '').replace(')', '')
                # Store the variable
                port_variables[var_name] = {
                    'type': var_type,
                    'value': var_value
                }
    return port_variables

# Function to update only port variables in Suricata YAML configuration
def update_suricata_config(yaml_file_path, port_variables):
    with open(yaml_file_path, 'r') as yaml_file:
        config = yaml.safe_load(yaml_file)

    # Iterate through port variables to add or update them in the YAML structure
    for var_name, details in port_variables.items():
        var_value = details['value']
        var_type = details['type']

        # Only update address-groups for ipvars and port-groups for portvars
        if var_type == 'ipvar':
            if 'vars' in config and 'address-groups' in config['vars']:
                config['vars']['address-groups'][var_name] = var_value
        elif var_type == 'portvar':
            if 'vars' in config and 'port-groups' in config['vars']:
                config['vars']['port-groups'][var_name] = var_value

    # Write the updated config back to the YAML file
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(config, yaml_file, default_flow_style=False)

if __name__ == "__main__":
    port_variables_file = r'C:\Users\Admin\OneDrive - Subex Limited\Documents\Kali_shared\sectriolabupdates\Rules\Variables.txt'  # Path to port variables file
    suricata_config_file = r'C:\Users\Admin\OneDrive - Subex Limited\Documents\Kali_shared\suricata_logs\suricata_sectrio_dpi.yaml'  # Path to Suricata config file

    # Parse the port variables from the text file
    port_variables = parse_port_variables(port_variables_file)

    # Update only the port variables section in the Suricata configuration file
    update_suricata_config(suricata_config_file, port_variables)

    print("Port variables updated in Suricata configuration file successfully.")
