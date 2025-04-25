import os
import pandas as pd

def merge_review_counts(input_folder, output_file):
    """Merge all review count files in the input folder and write a unique ID file with review counts."""
    all_data = []

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            # Read the CSV file
            df = pd.read_csv(file_path)
            all_data.append(df)

    # Concatenate all dataframes
    merged_df = pd.concat(all_data, ignore_index=True)

    # Drop duplicate IDs, keeping the first occurrence
    unique_df = merged_df.drop_duplicates(subset=['IMDb ID'])

    # Ensure only the necessary columns are written to the output file
    unique_df = unique_df[['IMDb ID', 'Number of Reviews']]

    # Fill NaN values with 0 and convert the 'Number of Reviews' column to integers
    unique_df['Number of Reviews'] = unique_df['Number of Reviews'].fillna(0).astype(int)

    # Write the unique IDs and review counts to the output file
    unique_df.to_csv(output_file, index=False)
    print(f"Unique ID and review counts saved to {output_file}")

if __name__ == "__main__":
    input_folder = "data/reviews_count"  # Path to the folder containing review count files
    output_file = "data/unique_review_counts4.csv"  # Path to the output CSV file

    merge_review_counts(input_folder, output_file)