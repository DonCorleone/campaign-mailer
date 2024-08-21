import csv

# Read the template row from 37032635_template
with open('37032635_template.csv', 'r') as template_file:
    reader = csv.reader(template_file)
    # save the header row
    header = next(reader)
    template_row = next(reader)

# Read the values from mailing_lists/stamm_petruschka.csv
with open('mailing_lists/stamm_petruschka.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    next(reader)  # Skip the header row
    values = [[template_row[0], template_row[1], template_row[2], template_row[3], template_row[4]] + [row[0], row[1], row[2]] for row in reader]

# Write the values to mailing_lists/recipients_full.csv
with open('mailing_lists/37032635_full.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(header)  # Write the header row
    writer.writerow(template_row)  # Write the template row as the header
    writer.writerows(values)

print("Values populated and saved in mailing_lists/37032635_full.csv.")