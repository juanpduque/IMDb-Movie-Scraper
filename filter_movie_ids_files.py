import pandas as pd

def filter_movie_ids(movie_ids_file, filtered_ids_file, output_file):
    """
    Filter the movie IDs in movie_ids_file to include only the IDs present in filtered_ids_file.

    Parameters:
        movie_ids_file (str): Path to the movie_ids.tsv file.
        filtered_ids_file (str): Path to the filtered_ids.tsv file.
        output_file (str): Path to the output TSV file to save the filtered movie IDs.
    """
    try:
        # Read the movie IDs file
        movie_ids_df = pd.read_csv(movie_ids_file, sep='\t', dtype=str)

        # Read the filtered IDs file
        filtered_ids_df = pd.read_csv(filtered_ids_file, sep='\t', dtype=str)

        # Filter the movie IDs that are in the filtered IDs file
        filtered_movie_ids_df = movie_ids_df[movie_ids_df['tconst'].isin(filtered_ids_df['tconst'])]

        # Save the filtered movie IDs to the output file
        filtered_movie_ids_df.to_csv(output_file, sep='\t', index=False)
        print(f"Filtered movie IDs saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    movie_ids_file = "data/movie_ids.tsv"  # Path to the movie_ids.tsv file
    filtered_ids_file = "data/filtered_ids.tsv"  # Path to the filtered_ids.tsv file
    output_file = "data/filtered_movie_ids.tsv"  # Path to the output TSV file

    filter_movie_ids(movie_ids_file, filtered_ids_file, output_file)