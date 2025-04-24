import pandas as pd

def filter_ids(unique_review_counts_file, title_ids_file, output_file):
    """Filter IDs from title_ids_file that are not in unique_review_counts_file and write to output_file."""
    try:
        # Read the unique review counts file
        unique_review_df = pd.read_csv(unique_review_counts_file)
        
        # Read the title IDs file
        title_ids_df = pd.read_csv(title_ids_file, sep='\t')
        
        # Extract the IDs from both dataframes
        unique_review_ids = set(unique_review_df['IMDb ID'])
        title_ids = set(title_ids_df['tconst'])
        
        # Find IDs that are in title_ids but not in unique_review_counts
        filtered_ids = title_ids - unique_review_ids
        
        # Create a DataFrame with the filtered IDs
        filtered_ids_df = pd.DataFrame(list(filtered_ids), columns=['tconst'])
        
        # Write the filtered IDs to the output file
        filtered_ids_df.to_csv(output_file, index=False, sep='\t')
        print(f"Filtered IDs saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    unique_review_counts_file = "data/unique_review_counts3.csv"  # Path to the unique review counts file
    title_ids_file = "data/title_types/movie.tsv"  # Path to the title IDs file
    output_file = "data/filtered_movie_ids2.tsv"  # Path to the output file

    filter_ids(unique_review_counts_file, title_ids_file, output_file)