import logging
import boto3
import pandas as pd
import os
import csv
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime, timedelta  # Import datetime and timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraping5.log"),
        logging.StreamHandler()
    ]
)

# Initialize UserAgent for rotation
ua = UserAgent()

def get_reviews_count(imdb_id):
    """Get the number of reviews for a specific IMDb ID."""
    url = f"https://www.imdb.com/title/{imdb_id}/reviews"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument(f"--user-agent={ua.random}")  # Rotate user-agent

    # Set the Chrome binary location (specific to AWS EC2)
    chrome_binary_path = "/usr/bin/google-chrome"
    if os.path.exists(chrome_binary_path):
        chrome_options.binary_location = chrome_binary_path
    else:
        logging.error("Google Chrome binary not found. Ensure Chrome is installed.")
        return 0

    # Explicitly set the ChromeDriver path
    chromedriver_path = ChromeDriverManager().install()

    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)

        # Wait for reviews to load
        driver.implicitly_wait(10)

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        # Extract reviews count
        total_reviews_element = soup.find("div", {"data-testid": "tturv-total-reviews"})
        if total_reviews_element:
            total_reviews_text = total_reviews_element.get_text(strip=True)
            total_reviews = int(total_reviews_text.split()[0].replace(',', ''))  # Extract numeric part
            return total_reviews
        else:
            logging.warning(f"Total reviews element not found for IMDb ID {imdb_id}.")
            return 0
    except Exception as e:
        logging.error(f"Error fetching reviews for IMDb ID {imdb_id}: {e}")
        return 0

def save_to_s3(file_name, bucket_name, object_name=None):
    """Save a file to an S3 bucket."""
    s3_client = boto3.client('s3')
    try:
        if object_name is None:
            object_name = file_name
        s3_client.upload_file(file_name, bucket_name, object_name)
        logging.info(f"File {file_name} uploaded to S3 bucket {bucket_name} as {object_name}.")
    except Exception as e:
        logging.error(f"An error occurred while uploading file to S3: {e}")

def download_from_s3(bucket_name, object_name, local_file):
    """Download a file from an S3 bucket."""
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket_name, object_name, local_file)
        logging.info(f"File {object_name} downloaded from S3 bucket {bucket_name} to {local_file}.")
    except Exception as e:
        logging.error(f"An error occurred while downloading file from S3: {e}")

def scrape_review(imdb_id, output_file):
    """Scrape reviews for a single IMDb ID and save the result."""
    reviews_count = get_reviews_count(imdb_id)
    logging.info(f"IMDb ID: {imdb_id}, Reviews Count: {reviews_count}")
    with open(output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([imdb_id, reviews_count])
    return imdb_id

def scrape_reviews(input_file, output_file, bucket_name=None, max_workers=5, save_interval=100, save_time_minutes=10):
    """Scrape reviews for movies in the input file and save the results to the output file."""
    logging.info("Starting the scraping process...")
    last_scraped_id = None
    start_time = datetime.now()
    processed_count = 0

    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write header if the file does not exist
        if not os.path.exists(output_file):
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['IMDb ID', 'Number of Reviews'])  # Write header

        # Download the input file from S3
        local_input_file = "local_input_file.tsv"
        download_from_s3(bucket_name, input_file, local_input_file)

        # Read the input file
        df = pd.read_csv(local_input_file, sep='\t')
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for index, row in df.iterrows():
                imdb_id = row['tconst']
                logging.info(f"Processing IMDb ID: {imdb_id}")
                # Submit a task to the executor for each IMDb ID
                futures.append(executor.submit(scrape_review, imdb_id, output_file))
                time.sleep(random.uniform(1, 3))  # Introduce a random delay between requests
                processed_count += 1

                # Save to S3 after processing a certain number of IDs or after a certain amount of time
                if processed_count % save_interval == 0 or (datetime.now() - start_time) > timedelta(minutes=save_time_minutes):
                    save_to_s3(output_file, bucket_name, object_name=f"output/{output_file}")
                    start_time = datetime.now()  # Reset the timer

            # Wait for all futures to complete
            for future in as_completed(futures):
                last_scraped_id = future.result()  # Get the last scraped IMDb ID
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if last_scraped_id:
            logging.info(f"Saving last scraped IMDb ID: {last_scraped_id}")
            with open("last_scraped_id.txt", 'w') as f:
                f.write(last_scraped_id)
            logging.info(f"Last scraped IMDb ID saved to last_scraped_id.txt")

        # Final save to S3 after all processing is complete
        if bucket_name:
            save_to_s3(output_file, bucket_name, object_name=f"output/{output_file}")

    logging.info("Scraping process completed.")

if __name__ == "__main__":
    # Example usage
    input_file = "input/filtered_ids_part_5.tsv"  # Replace with your input file path in S3
    output_file = "output/title_with_reviews5.csv"  # Replace with desired output file
    bucket_name = "reviewsimbd"  # Replace with your S3 bucket name

    scrape_reviews(input_file=input_file, output_file=output_file, bucket_name=bucket_name, max_workers=3)
    print(f"Results saved to {output_file}")