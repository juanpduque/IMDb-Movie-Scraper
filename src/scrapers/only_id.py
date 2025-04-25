import pandas as pd

def extract_id_column(input_file, output_file):
    """Extract the ID column from the input TSV file and write it to the output file."""
    try:
        # Read the input TSV file
        df = pd.read_csv(input_file, sep='\t', usecols=['tconst'])
        
        # Write the ID column to the output file
        df.to_csv(output_file, index=False, sep='\t')
        print(f"Extracted ID column saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "data/title.basics.tsv"  # Path to the input TSV file
    output_file = "data/title_ids.tsv"    # Path to the output TSV file

    extract_id_column(input_file, output_file)