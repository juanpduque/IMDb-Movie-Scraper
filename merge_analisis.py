import os
import pandas as pd
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def analyze_scariest_movies(score_file, metadata_file, output_file):
    """
    Merge score data with metadata to analyze the scariest movies.

    Parameters:
        score_file (str): Path to the file containing IMDb_ID and
        Average_Score.
        metadata_file (str): Path to the file containing IMDb_ID and metadata.
        output_file (str): Path to save the results.

    Returns:
        pd.DataFrame: A DataFrame of the top scariest movies.
    """
    try:
        # Load scores data
        scores_df = pd.read_csv(score_file)
        metadata_df = pd.read_csv(metadata_file)

        # Merge the dataframes on IMDb_ID
        merged_df = pd.merge(scores_df, metadata_df, on="imdb_id", how="inner")

        # Sort by Average_Score in descending order
        merged_df = merged_df.sort_values(by="Average_Score", ascending=False)

        # Save the merged dataframe to a CSV file
        merged_df.to_csv(output_file, index=False)
        logging.info(f"Analysis results saved to {output_file}.")

        return merged_df.head(10)  # Top 10 scariest movies

    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


# Example usage
score_file = "scary_movie_rankings.csv"  # IMDb_ID, Average_Score
metadata_file = "movie_data/filtered_horror_movies.csv"  # IMDb_ID,
# primaryTitle, genres, etc.
output_file = "scary_movies_analysis.csv"

# Check if input files exist
if not os.path.exists(score_file):
    logging.error(f"Score file not found: {score_file}")
elif not os.path.exists(metadata_file):
    logging.error(f"Metadata file not found: {metadata_file}")
else:
    # Analyze scariest movies
    scariest_movies = analyze_scariest_movies(
        score_file, metadata_file, output_file
    )

    # Display the top scariest movies
    if not scariest_movies.empty:
        logging.info("Top Scariest Movies:")
        logging.info(scariest_movies)
    else:
        logging.info("No scariest movies found.")
