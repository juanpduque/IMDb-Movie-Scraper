import os
import logging


class ProgressManager:
    """
    Class to manage saving and loading progress of IMDb IDs and
    sentiment analysis.
    """

    def __init__(
        self,
        id_filename: str = "last_scraped_id.txt",
        dataset_filename: str = "last_dataset_name.txt",
        sentiment_id_filename: str = "last_sentiment_id.txt"
    ):
        """
        Initialize ProgressManager with file paths for IMDb IDs,
        datasets, and sentiment analysis.

        Args:
            id_filename (str): File to store the last scraped IMDb ID.
                               Defaults to "last_scraped_id.txt".
            dataset_filename (str): File to store the last dataset name.
                                    Defaults to "last_dataset_name.txt".
            sentiment_id_filename (str): File to store the last
                                         sentiment-analyzed IMDb ID.
                                         Defaults to "last_sentiment_id.txt".
        """
        self.id_filename = id_filename
        self.dataset_filename = dataset_filename
        self.sentiment_id_filename = sentiment_id_filename

    def save_progress(
        self, last_id: str, dataset_name: str, sentiment_id: str = None
    ) -> None:
        """
        Save progress of the last scraped IMDb ID, dataset name, and
        optionally the last sentiment-analyzed IMDb ID.

        Args:
            last_id (str): The last scraped IMDb ID.
            dataset_name (str): The last processed dataset name.
            sentiment_id (str): The last sentiment-analyzed IMDb ID.
                                Defaults to None.
        """
        logging.info(
            f"Attempting to save progress with last_id={last_id}, "
            f"dataset_name={dataset_name}, sentiment_id={sentiment_id}"
        )

        # Save the last scraped ID
        with open(self.id_filename, 'w', encoding='utf-8') as id_file:
            id_file.write(last_id)
            id_file.flush()
            logging.info(f"Saved last scraped ID: {last_id}")

        # Save the dataset name
        with open(
            self.dataset_filename, 'w', encoding='utf-8'
        ) as dataset_file:
            dataset_file.write(dataset_name)
            dataset_file.flush()
            logging.info(f"Saved dataset name: {dataset_name}")

        # Save the last sentiment-analyzed ID (if provided)
        if sentiment_id:
            with open(
                self.sentiment_id_filename, 'w', encoding='utf-8'
            ) as sentiment_file:
                sentiment_file.write(sentiment_id)
                sentiment_file.flush()
                logging.info(
                    f"Saved last sentiment-analyzed ID: {sentiment_id}"
                )

    def load_progress(self) -> tuple[str, str, str]:
        """
        Load the last successfully scraped IMDb ID, dataset name,
        and sentiment-analyzed IMDb ID.

        Returns:
            tuple[str, str, str]: A tuple containing:
                - The last scraped IMDb ID.
                - The last dataset name.
                - The last sentiment-analyzed IMDb ID.
                Returns (None, None, None) if no progress is saved.
        """
        last_id = self._read_file(self.id_filename)
        dataset_name = self._read_file(self.dataset_filename)
        sentiment_id = self._read_file(self.sentiment_id_filename)

        logging.info(
            f"Loaded progress: last_id={last_id}, "
            f"dataset_name={dataset_name}, "
            f"sentiment_id={sentiment_id}"
        )
        return last_id, dataset_name, sentiment_id

    @staticmethod
    def _read_file(filepath: str) -> str:
        """
        Helper to read the content of a file if it exists.

        Args:
            filepath (str): The path of the file to read.

        Returns:
            str: The file's content stripped of whitespace,
            or None if not found.
        """
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read().strip()
        return None
