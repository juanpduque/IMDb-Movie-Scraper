"""
This module defines the MovieScraperPipeline class for scraping IMDb reviews
and managing progress for multiple movies in a dataset.
"""


import os
import time
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from src.progress_manager import ProgressManager


class MovieScraperPipeline:
    """A class to manage the scraping of reviews for a list of IMDb IDs."""

    def __init__(self, driver, max_retries: int = 3):
        self.driver = driver
        self.max_retries = max_retries

    def scrape_reviews(self, imdb_id: str) -> list[str]:
        """Scrape reviews for a given IMDb ID."""
        url = f"https://www.imdb.com/title/{imdb_id}/reviews"
        retries = 0

        while retries < self.max_retries:
            try:
                logging.info(
                    "Attempting to scrape reviews for IMDb ID %s "
                    "(Attempt %d/%d)",
                    imdb_id,
                    retries + 1,
                    self.max_retries
                )
                self.driver.get(url)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@data-testid='tturv-total-reviews']")
                    )
                )

                total_reviews_element = self.driver.find_element(
                    By.XPATH,
                    "//div[@data-testid='tturv-total-reviews']"
                )
                # e.g., "14 reviews"
                total_reviews_text = total_reviews_element.text.strip()
                # Extract numeric part
                total_reviews = int(
                    total_reviews_text.split()[0].replace(',', '')
                )

                if total_reviews == 0:
                    logging.info(
                        "Movie %s has 0 reviews. Skipping...", imdb_id
                    )
                    return []

                if total_reviews >= 25:
                    self._click_all_button(imdb_id)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "ipc-html-content-inner-div")
                    )
                )
                time.sleep(2)  # Allow time for the reviews to load completely
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                review_elements = soup.find_all(
                    "div", class_="ipc-html-content-inner-div"
                )
                reviews = [review.text.strip() for review in review_elements]

                logging.info(
                    "Successfully scraped %d reviews for IMDb ID %s.",
                    len(reviews),
                    imdb_id
                )
                return reviews

            except TimeoutException as e:
                logging.warning(
                    "Timeout while scraping IMDb ID %s: %s. Retrying...",
                    imdb_id, e
                )
            except WebDriverException:
                logging.warning(
                    "WebDriver error while scraping IMDb ID %s. Retrying...",
                    imdb_id,
                    exc_info=True
                )

            retries += 1
            time.sleep(2)

        logging.error(
            "Failed to scrape reviews for IMDb ID %s after %d retries.",
            imdb_id,
            self.max_retries
        )
        return []

    def _click_all_button(self, imdb_id: str) -> None:
        """Click the 'All' button to load all reviews."""
        try:
            all_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[.//span[text()='All']]")
                )
            )
            all_button.click()
            logging.info("Clicked 'All' button for movie %s.", imdb_id)
        except (TimeoutException, WebDriverException) as e:
            logging.warning(
                "Error while trying to click 'All' button for movie %s: %s",
                imdb_id,
                e
            )

    def run_pipeline(
        self,
        movie_list: pd.DataFrame,
        output_folder: str = "reviews",
        dataset_name: str = None,
        start_from_id: str = None,
    ) -> None:
        """
        Run the pipeline to scrape and save reviews for movies in the list.
        """
        if not dataset_name:
            raise ValueError(
                "Dataset name is required to save reviews in a specific "
                "folder."
            )

        output_folder = os.path.join(output_folder, dataset_name)
        os.makedirs(output_folder, exist_ok=True)
        logging.info("Output folder: %s", output_folder)

        movie_list = self._resume_from_id(movie_list, start_from_id)
        progress_manager = ProgressManager()

        for _, movie in movie_list.iterrows():
            imdb_id = movie['imdb_id']
            title = movie['primaryTitle']
            logging.info("Processing movie: %s (%s)", title, imdb_id)

            reviews = self.scrape_reviews(imdb_id)

            # Save progress whether reviews are found or not
            progress_manager.save_progress(imdb_id, dataset_name)

            if reviews:
                output_file = os.path.join(
                    output_folder, f"reviews_{imdb_id}.csv"
                )
                pd.DataFrame(reviews, columns=["Review"]).to_csv(
                    output_file, index=False
                )
                logging.info(
                    "Saved reviews for '%s' to %s.", title, output_file
                )
            else:
                logging.warning(
                    "No reviews found for movie: %s (%s). Skipping.",
                    title, imdb_id
                )

    def _resume_from_id(
        self, movie_list: pd.DataFrame, start_from_id: str
    ) -> pd.DataFrame:
        """Resume scraping from a specific IMDb ID."""
        if start_from_id:
            if start_from_id in movie_list['imdb_id'].values:
                start_index = movie_list[
                    movie_list['imdb_id'] == start_from_id
                ].index[0]
                logging.info("Resuming from movie ID: %s.", start_from_id)
                return movie_list.iloc[start_index:]
            logging.warning(
                "Starting ID '%s' not found in the movie list.", start_from_id
            )
        return movie_list
