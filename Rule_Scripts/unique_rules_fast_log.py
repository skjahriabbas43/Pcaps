import re
import csv

def extract_unique_rules(logfile):
    unique_rules = {}
    pattern = re.compile(r'\[\*\*\] \[(\d+:\d+:\d+)\] (.*?) \[\*\*\] \[Classification: (.*?)\] \[Priority: (\d+)\]')

    with open(logfile, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                rule_id = match.group(1)
                if rule_id in unique_rules:
                    unique_rules[rule_id]["count"] += 1
                else:
                    rule_details = {
                        "message": match.group(2),
                        "classification": match.group(3),
                        "priority": match.group(4),
                        "line": line.strip(),
                        "count": 1
                    }
                    unique_rules[rule_id] = rule_details

    return unique_rules

def save_to_csv(unique_rules, csvfile):
    fieldnames = ["rule_id", "count", "message", "classification", "priority", "log_entry"]
    with open(csvfile, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for rule_id, details in unique_rules.items():
            writer.writerow({
                "rule_id": rule_id,
                "count": details['count'],
                "message": details['message'],
                "classification": details['classification'],
                "priority": details['priority'],
                "log_entry": details['line']
            })

def main():
    logfile = r"C:\Users\Admin\OneDrive - Subex Limited\Documents\Kali_shared\suricata_logs\fast.log"
    csvfile = 'unique_rules_schneider.csv'
    unique_rules = extract_unique_rules(logfile)
    save_to_csv(unique_rules, csvfile)
    print(f"Unique rules have been saved to {csvfile}")

if __name__ == "__main__":
    main()
