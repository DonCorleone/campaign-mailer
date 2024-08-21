import csv

# Read the template row from mailing_lists/recipients.csv
with open('32402726_template.csv', 'r') as template_file:
    reader = csv.reader(template_file)
    # save the header row
    header = next(reader)
    template_row = next(reader)

# Read the values from mailing_lists/recipients_export.csv
with open('mailing_lists/stamm_schlosswochen.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    next(reader)  # Skip the header row
    values = [[template_row[0], template_row[1], template_row[2]] + [row[4], row[5], row[6]] + [template_row[6], template_row[7]] for row in reader]

# Write the values to mailing_lists/recipients_full.csv
with open('mailing_lists/32402726_full.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header)  # Write the header row
    writer.writerow(template_row)  # Write the template row as the header
    writer.writerows(values)

print("Values populated and saved in mailing_lists/32402726_full.csv.")