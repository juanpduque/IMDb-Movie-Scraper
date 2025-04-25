import os
import pandas as pd


def count_reviews_in_folder(folder_path):
    """
    Count the number of reviews for each movie in the specified folder.

    Parameters:
        folder_path (str): Path to the folder containing review files.

    Returns:
        pd.DataFrame: A DataFrame with IMDb_ID and Review_Count.
    """
    try:
        # List all review files in the folder
        files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

        review_counts = []
        for file in files:
            try:
                # Extract IMDb ID from the filename
                # Assumes format: reviews_ttXXXX.csv
                imdb_id = os.path.splitext(file)[0].split("_")[1]
                file_path = os.path.join(folder_path, file)
                # Count the number of rows (reviews) in the file
                review_count = pd.read_csv(file_path).shape[0]
                review_counts.append({
                    "IMDb_ID": imdb_id,
                    "Review_Count": review_count
                })
            except Exception as e:
                print(f"Error processing file {file}: {e}")

        # Create a DataFrame
        review_counts_df = pd.DataFrame(review_counts)
        return review_counts_df

    except Exception as e:
        print(f"Error processing folder {folder_path}: {e}")
        return pd.DataFrame()


# Example usage
reviews_folder = "reviews/horror_movies"  # Path to the folder with review
# files
review_counts_df = count_reviews_in_folder(reviews_folder)

# Save the review counts to a CSV file
review_counts_file = "review_counts.csv"
review_counts_df.to_csv(review_counts_file, index=False)
print(f"Review counts saved to {review_counts_file}.")
