import pandas as pd


def analyze_scariest_movies_with_review_balance(
    score_file, average_score_file, metadata_file, output_file, k_factor=None
):
    """
    Merge score data with metadata and balance analysis with review counts.

    Parameters:
        score_file (str): Path to the file containing imdb_id and Review_Count.
        average_score_file (str): Path to the file containing imdb_id and
        Average_Score.
        metadata_file (str): Path to the file containing imdb_id and metadata.
        output_file (str): Path to save the results.
        k_factor (float): Optional smoothing factor for weighting
        review counts.

    Returns:
        pd.DataFrame: A DataFrame of the top scariest movies.
    """
    try:
        # Load scores data (review counts)
        scores_df = pd.read_csv(score_file)  # Columns: imdb_id, Review_Count
        print(f"Loaded scores data:\n{scores_df.head()}")  # Debugging line

        # Load average scores data
        average_scores_df = pd.read_csv(
            average_score_file)  # Columns: imdb_id, Average_Score
        print("Loaded average scores data:")
        print(average_scores_df.head())  # Debugging line

        # Load metadata
        metadata_df = pd.read_csv(
            metadata_file)  # Columns: imdb_id, primaryTitle, genres, etc.
        print(f"Loaded metadata:\n{metadata_df.head()}")  # Debugging line

        # Merge scores data with average scores
        merged_df = pd.merge(
            scores_df, average_scores_df, on="imdb_id", how="inner"
        )
        print(
            f"Merged scores and average scores:\n{merged_df.head()}"
        )  # Debugging line

        # Merge with metadata
        merged_df = pd.merge(merged_df, metadata_df, on="imdb_id", how="inner")
        print(f"Merged with metadata:\n{merged_df.head()}")  # Debugging line

        # Set a default k_factor if not provided
        # (use the mean of the Review_Count)
        if k_factor is None:
            k_factor = scores_df["Review_Count"].mean()
            print(f"Default k_factor set to: {k_factor}")  # Debugging line

        # Calculate Weighted Score
        merged_df["Weighted_Score"] = (
            merged_df["Average_Score_x"] * merged_df["Review_Count"] / (
                merged_df["Review_Count"] + k_factor
            )
        )

        # Sort by Weighted Score in descending order
        merged_df = merged_df.sort_values(by="Weighted_Score", ascending=False)

        # Save the merged DataFrame to a CSV file
        merged_df.to_csv(output_file, index=False)
        print(f"Analysis results saved to {output_file}.")

        # Return the top scariest movies for inspection
        return merged_df.head(10)

    except Exception as e:
        print(f"Error during analysis: {e}")
    return pd.DataFrame()  # Return an empty DataFrame on error


# Example usage
score_file = "review_counts.csv"  # imdb_id, Review_Count
average_score_file = "scary_movie_rankings.csv"  # imdb_id, Average_Score
metadata_file = "scary_movies_analysis.csv"  # imdb_id, primaryTitle, genres
output_file = "balanced_scary_movies_analysis.csv"

# Analyze scariest movies with balanced scoring
scariest_movies = analyze_scariest_movies_with_review_balance(
    score_file, average_score_file, metadata_file, output_file
)

# Display the top scariest movies
print("Top Scariest Movies with Balanced Scores:")
print(scariest_movies)
