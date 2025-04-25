import os
import pandas as pd

def find_difference_ids(split_ids_file, reviews_count_file, output_file):
    """
    Find the IDs in split_ids_file that are not present in reviews_count_file.
    
    Parameters:
        split_ids_file (str): Path to the file containing split IDs.
        reviews_count_file (str): Path to the file containing review counts.
        output_file (str): Path to the output file to save the results.
    """
    try:
        # Read the split IDs file
        split_ids_df = pd.read_csv(split_ids_file, sep='\t', dtype=str)
        split_ids_df['tconst'] = split_ids_df['tconst'].str.strip()
        split_ids = set(split_ids_df['tconst'].tolist())

        # Read the reviews count file
        reviews_count_df = pd.read_csv(reviews_count_file, dtype=str)
        reviews_count_df.iloc[:, 0] = reviews_count_df.iloc[:, 0].str.strip()
        reviews_ids = set(reviews_count_df.iloc[:, 0].tolist())

        # Check for duplicates in split IDs and review IDs
        duplicate_split_ids = split_ids_df[split_ids_df.duplicated('tconst')]
        print(f"Duplicate split IDs: {len(duplicate_split_ids)}")

        duplicate_review_ids = reviews_count_df[reviews_count_df.duplicated(reviews_count_df.columns[0])]
        print(f"Duplicate review IDs: {len(duplicate_review_ids)}")

        # Calculate the difference between reviews_ids and split_ids
        remaining_reviews_ids = reviews_ids - split_ids

        # Debugging: Print sizes and sample IDs
        print(f"Total reviews_count_file IDs: {len(reviews_ids)}")
        print(f"Total split_ids_file IDs: {len(split_ids)}")
        print(f"Total remaining review IDs (reviews_ids - split_ids): {len(remaining_reviews_ids)}")
        
        # Now, calculate the difference between the total review count and the remaining IDs
        expected_difference = len(reviews_ids) - len(remaining_reviews_ids)
        print(f"Expected difference (should be 682,447): {expected_difference}")

        # Save the remaining review IDs to the output file
        with open(output_file, 'w') as f:
            for imdb_id in remaining_reviews_ids:
                f.write(f"{imdb_id}\n")

        print(f"Remaining review IDs saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    split_ids_file = "data/split_ids_movies/filtered_ids_part_8.tsv"  # Path to the file containing split IDs
    reviews_count_file = "data/reviews_count/title_with_reviews8.csv"  # Path to the file containing review counts
    output_file = "data/remaining_reviews_ids8.txt"  # Path to the output file

    find_difference_ids(split_ids_file, reviews_count_file, output_file)
