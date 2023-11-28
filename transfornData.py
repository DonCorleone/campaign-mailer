import csv

# Read the template row from mailing_lists/recipients.csv
with open('mailing_lists/recipients.csv', 'r') as template_file:
    reader = csv.reader(template_file)
    next(reader)  # Skip the header row
    template_row = next(reader)

# Read the values from mailing_lists/recipients_export.csv
with open('mailing_lists/recipients_export.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    next(reader)  # Skip the header row
    values = [[template_row[0], template_row[1], template_row[2], template_row[3]] + [row[4], row[5], row[6]] for row in reader]

# Write the values to mailing_lists/recipients_full.csv
with open('mailing_lists/recipients_full.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(template_row)  # Write the template row as the header
    writer.writerows(values)

print("Values populated and saved in mailing_lists/recipients_full.csv.")