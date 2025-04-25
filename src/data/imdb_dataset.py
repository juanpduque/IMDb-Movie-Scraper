import logging
import pandas as pd


class IMDbDataset:
    """ A class to handle loading and filtering IMDb datasets. """

    def __init__(self, input_file):
        self.input_file = input_file
        self.data = None

    def load_data(self):
        """
        Load IMDb dataset from a TSV file and rename columns for better
        readability.

        Returns:
            pd.DataFrame: The loaded dataset or None if loading fails.
        """
        try:
            logging.info(f"Loading data from {self.input_file}...")
            self.data = pd.read_csv(self.input_file, sep='\t')
            logging.info("Data loaded successfully.")
            return self.data
        except Exception as e:
            logging.error(f"An error occurred while loading data: {e}")
            self.data = None
            return None

    def filter_data(self, column_name, filter_value):
        """
        Filter the dataset based on a column and a filter value.
        """
        if self.data is not None:
            filtered_data = self.data[self.data[column_name] == filter_value]
            logging.info(
                f"Filtered data based on {column_name} = {filter_value}."
            )
            return filtered_data
        else:
            logging.warning("Data is not loaded. Please load the data first.")
            return None


# Example usage
if __name__ == "__main__":
    dataset = IMDbDataset("path/to/your/imdb_dataset.tsv")
    dataset.load_data()
    filtered_data = dataset.filter_data("column_name", "filter_value")
    print(filtered_data)
