import os
import logging
import pandas as pd


class MovieExporter:
    """ A class to export movie data to a file. """

    def __init__(self, output_folder="movie_data"):
        self.output_folder = output_folder
        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

    def save_to_csv(self, dataframe, genre=None, start_year=None,
                    end_year=None):
        """
        Save a DataFrame to a CSV file with a dynamic filename
        based on filter parameters.
        """
        if dataframe.empty:
            logging.warning("The DataFrame is empty. No file will be saved.")
            return

        # Construct the filename based on filter parameters
        filename_parts = ["movies"]
        if genre:
            filename_parts.append(f"genre_{genre}")
        if start_year:
            filename_parts.append(f"start_{start_year}")
        if end_year:
            filename_parts.append(f"end_{end_year}")
        filename = "_".join(filename_parts) + ".csv"
        file_path = os.path.join(self.output_folder, filename)

        # Save the DataFrame to a CSV file
        try:
            dataframe.to_csv(file_path, index=False)
            logging.info(f"DataFrame saved to {file_path}")
        except Exception as e:
            logging.error(
                f"An error occurred while saving the DataFrame to CSV: {e}"
            )


# Example usage
if __name__ == "__main__":
    # Create a sample DataFrame
    data = {
        "title": ["Movie1", "Movie2", "Movie3"],
        "genre": ["Action", "Comedy", "Drama"],
        "year": [2001, 2002, 2003]
    }
    df = pd.DataFrame(data)

    # Create an instance of MovieExporter and save the DataFrame to a CSV file
    exporter = MovieExporter()
    exporter.save_to_csv(df, genre="Action", start_year=2000, end_year=2005)
