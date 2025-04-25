import pandas as pd
import os

def split_ids(input_file, output_folder, num_splits=8):
    """Split the IDs in the input file into multiple files."""
    try:
        # Read the input file
        df = pd.read_csv(input_file, sep='\t')
        
        # Calculate the number of rows per split
        num_rows = len(df)
        rows_per_split = num_rows // num_splits
        
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Split the DataFrame and save each part to a new file
        for i in range(num_splits):
            start_idx = i * rows_per_split
            if i == num_splits - 1:  # Last split takes the remainder
                end_idx = num_rows
            else:
                end_idx = (i + 1) * rows_per_split
            
            split_df = df.iloc[start_idx:end_idx]
            output_file = os.path.join(output_folder, f"filtered_ids_part_{i+1}.tsv")
            split_df.to_csv(output_file, index=False, sep='\t')
            print(f"Saved {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_file = "data/filtered_movie_ids.tsv"  # Path to the input TSV file
    output_folder = "data/split_ids_movies"  # Path to the folder to save the split files

    split_ids(input_file, output_folder)