import os
import pandas as pd


def get_imdb_ids_from_emotions_folder(folder_path):
    """
    Extract IMDb IDs from filenames in the `movie_emotions` folder and return a
    DataFrame.

    Parameters:
        folder_path (str): Path to the folder containing emotion
        analysis files.

    Returns:
        pd.DataFrame: A DataFrame with IMDb IDs.
    """
    try:
        # List all CSV files in the folder
        files = [
            f for f in os.listdir(folder_path)
            if f.startswith("emotions_tt") and f.endswith(".csv")
        ]

        # Extract IMDb IDs from filenames
        # (e.g., 'emotions_tt0003419.csv' -> 'tt0003419')
        imdb_ids = [os.path.splitext(file)[0].split("_")[1] for file in files]

        # Create a DataFrame
        df = pd.DataFrame(imdb_ids, columns=["IMDb_ID"])

        # Optionally, sort the DataFrame by IMDb_ID
        df.sort_values(by="IMDb_ID", inplace=True, ignore_index=True)

        return df
    except Exception as e:
        print(f"Error processing folder {folder_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


# Example usage
emotions_folder_path = "movie_emotions"
imdb_ids_df = get_imdb_ids_from_emotions_folder(emotions_folder_path)

# Save the DataFrame to a CSV for inspection, if needed
output_csv = "movie_emotions_ids.csv"
imdb_ids_df.to_csv(output_csv, index=False)
print(f"IMDb IDs saved to {output_csv}.")
