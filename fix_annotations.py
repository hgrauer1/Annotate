import csv

# Open the input CSV file and create a new output file for corrected entries
with open('annotations_simulate.csv', 'r') as csv_file, open('output_file.csv', 'w', newline='') as output_file:
    csv_reader = csv.reader(csv_file)
    csv_writer = csv.writer(output_file)

    # Write the header row to the output file
    header = next(csv_reader)
    csv_writer.writerow(header)

    # Loop through each row in the input file
    for row in csv_reader:
        # Check if the row has enough columns
        if len(row) >= 6:
            # Get the bounding box coordinates from the row
            xmin, ymin, xmax, ymax = int(row[2]), int(row[3]), int(row[4]), int(row[5])

            # Check if the bounding box is invalid
            if xmin > xmax:
                # Swap the x coordinates
                xmin, xmax = xmax, xmin
            if ymin > ymax:
                # Swap the y coordinates
                ymin, ymax = ymax, ymin

            # Write the corrected row to the output file
            csv_writer.writerow([row[0], row[1], xmin, ymin, xmax, ymax])
        else:
            # Write the row as-is if it doesn't have enough columns
            csv_writer.writerow(row)