#!/bin/bash

# Define the Python script to execute
python_script="/home/zikachuuu/.local/bin/aletheia.py"

# Specify the directory containing the files to process
input_directory="/media/sf_VirtualBoxSharedFolder/URECA/greyScale/random_lsbm"

# Specify the directory where you want to save the output
output_directory="/media/sf_VirtualBoxSharedFolder/URECA/greyScale/random_lsbm"
output_csv="$output_directory/output.csv"

# Ensure the output directory exists, create it if not
mkdir -p "$output_directory"

# Create the CSV file with headers
echo "InputFile,Output" > "$output_csv"

# Iterate through the input files
for input_file in "$input_directory"/*.png; do

    # Execute the Python script on the input file
    output_result="$("$python_script" spa "$input_file")"

    # Append the input file and corresponding output to the CSV file
    echo "\"$input_file\",\"$output_result\"" >> "$output_csv"
    
    echo "Processed $input_file"

done

echo "Processing complete. Combined CSV output saved to $output_csv"
