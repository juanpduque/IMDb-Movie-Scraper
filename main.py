import logging
import os
import sys
import argparse
import pandas as pd
from src import IMDbDataset
from src import MovieExporter
from src import MovieScraperPipeline
from src import WebDriverManager
from src.progress_manager import ProgressManager
from src.sentiment_analyzer import SentimentAnalyzer


def get_filter_parameters(args):
    """Prompt the user for filter parameters or use command-line arguments."""
    if args.genre:
        genre = args.genre
    else:
        genre = input("Enter genre to filter (or leave blank for no filter): ")

    if args.title_type:
        title_type = args.title_type
    else:
        title_type = input(
            "Enter title type (e.g., movie, short) "
            "(or leave blank for 'movie'): "
        ) or "movie"

    if args.start_year:
        start_year = args.start_year
    else:
        start_year = input("Enter start year (or leave blank for no filter): ")

    if args.end_year:
        end_year = args.end_year
    else:
        end_year = input("Enter end year (or leave blank for no filter): ")

    if args.is_adult is not None:
        is_adult = args.is_adult
    else:
        is_adult = input(
            "Include adult titles? (yes/no or leave blank for 'no'): "
        ).lower()

    # Convert inputs to appropriate types
    is_adult = (
        True if is_adult == 'yes'
        else False if is_adult == 'no'
        else None
    )
    start_year = int(start_year) if start_year else None
    end_year = int(end_year) if end_year else None

    return genre, title_type, start_year, end_year, is_adult


def list_filtered_files(directory="movie_data"):
    """List all CSV files in the specified directory and prompt the user
    to select one."""
    try:
        files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        if not files:
            logging.error("No filtered movie files found.")
            return None

        logging.info("Available filtered movie files:")
        for index, file in enumerate(files):
            print(f"{index + 1}: {file}")

        choice = input(f"Select a file by number (1-{len(files)}): ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            selected_file = files[int(choice) - 1]  # Get the selected file
            logging.info(f"User selected file: {selected_file}")
            return os.path.join(directory, selected_file)
        else:
            logging.error(
                "Invalid choice. Please enter a number corresponding to a "
                "file."
            )
            return None
    except OSError as e:
        logging.error(f"Error accessing directory {directory}: {e}")
        return None


def list_review_folders(review_base_folder="reviews"):
    """List all directories in the specified review folder."""
    try:
        folders = [
            f for f in os.listdir(review_base_folder)
            if os.path.isdir(os.path.join(review_base_folder, f))
        ]
        if not folders:
            logging.error("No review folders found.")
            return None

        logging.info("Available review folders:")
        for index, folder in enumerate(folders):
            print(f"{index + 1}: {folder}")

        choice = input(f"Select a folder by number (1-{len(folders)}): ")
        if choice.isdigit() and 1 <= int(choice) <= len(folders):
            # Get the selected folder
            selected_folder = folders[int(choice) - 1]
            logging.info(f"User selected folder: {selected_folder}")
            return os.path.join(review_base_folder, selected_folder)
        else:
            logging.error(
                "Invalid choice. Please enter a number corresponding to a "
                "folder."
            )
            return None
    except OSError as e:
        logging.error(f"Error accessing directory {review_base_folder}: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IMDb Movie Scraper")
    parser.add_argument("--genre", type=str, help="Genre to filter")
    parser.add_argument(
        "--title_type", type=str, default="movie",
        help="Title type (e.g., movie, short)"
    )
    parser.add_argument("--start_year", type=int, help="Start year")
    parser.add_argument("--end_year", type=int, help="End year")
    parser.add_argument(
        "--is_adult",
        type=str,
        choices=["yes", "no"],
        help="Include adult titles (yes/no)"
    )

    args = parser.parse_args()

    progress_manager = ProgressManager()
    last_id, last_dataset_name, last_sentiment_id = \
        progress_manager.load_progress()

    while True:
        choice = input(
            "Do you want to:\n"
            "(1) Load an existing filtered file to start the scraping\n"
            "(2) Filter a new dataset and start the scraping\n"
            "(3) Start from the last IMDb ID to finish the scraping\n"
            "(4) Start sentiment analysis (if you already have reviews)\n"
            "Enter 1, 2, 3, or 4: "
        )

        if choice == '1':
            selected_file = list_filtered_files()
            if selected_file:
                try:
                    # Load the filtered movies directly from CSV
                    filtered_movies = pd.read_csv(
                        selected_file
                    )
                    logging.info(
                        f"Loaded {len(filtered_movies)} filtered movies from "
                        f"{selected_file}."
                    )
                    # Get filename without extension
                    dataset_name = os.path.splitext(
                        os.path.basename(selected_file)
                    )[0]

                    # Ask the user if they want to start from a specific
                    # IMDb ID
                    start_from_id = input(
                        "Do you want to start from a specific IMDb ID? "
                        "(yes/no): "
                    ).lower()

                    if start_from_id == 'yes':
                        imdb_id = input("Enter the IMDb ID to start from: ")
                        # Check if the IMDb ID exists in the dataset
                        if imdb_id in filtered_movies['imdb_id'].values:
                            # Find the row that corresponds to the IMDb ID
                            imdb_id_to_start = imdb_id
                            logging.info(
                                f"Starting from IMDb ID: {imdb_id_to_start}."
                            )
                        else:
                            logging.warning(
                                f"IMDb ID {imdb_id} not found in the dataset. "
                                "Starting from the beginning."
                            )
                            imdb_id_to_start = None
                    else:
                        imdb_id_to_start = None
                        # Start from the beginning of the file

                    # Exit the loop since we successfully loaded the file
                    # and determined the start point
                    break

                except FileNotFoundError:
                    logging.error(
                        f"Filtered movies file {selected_file} not found. "
                        "Please check the path."
                    )
                    continue

        elif choice == '2':
            imdb_dataset = IMDbDataset(
                args.tsv_file)  # Ensure this path is correct
            imdb_dataset.load_data()

            genre, title_type, start_year, end_year, is_adult = \
                get_filter_parameters(args)

            filtered_movies = imdb_dataset.filter_movies(
                genre=genre,
                title_type=title_type,
                start_year=start_year,
                end_year=end_year,
                is_adult=is_adult
            )

            if len(filtered_movies) == 0:
                logging.error("Filtered results: 0 movies. Exiting program.")
                sys.exit(1)  # Exit the program

            exporter = MovieExporter()
            exporter.save_to_csv(
                filtered_movies,
                genre=genre,
                start_year=start_year,
                end_year=end_year
            )
            # Save current dataset name for future reference
            dataset_name = (
                f"{genre}_{start_year}_{end_year}" if genre else "all_movies"
            )
            progress_manager.save_progress(
                '', dataset_name)  # Save progress here
            imdb_id_to_start = None  # Start from the beginning of the file
            break

        elif choice == '3':
            if last_id and last_dataset_name:
                logging.info(f"Starting from last IMDb ID: {last_id}.")
                try:
                    filtered_movies = pd.read_csv(
                        f"movie_data/{last_dataset_name}.csv"
                    )  # Adjust path as necessary
                    logging.info(
                        f"Loaded previous filtered movies for IMDb ID: "
                        f"{last_id}."
                    )
                    # Use the last dataset name
                    dataset_name = last_dataset_name
                    imdb_id_to_start = last_id
                except FileNotFoundError:
                    logging.error(
                        f"Previous filtered movies file "
                        f"'{last_dataset_name}.csv' not found."
                    )
                    continue
                break
            else:
                logging.warning(
                    "No last dataset or IMDb ID found. "
                    "Please load a file or create a new filter."
                )
                continue

        elif choice == '4':
            # List and select the review folder
            review_folder = list_review_folders()
            if review_folder:
                # Initialize SentimentAnalyzer and process reviews
                analyzer = SentimentAnalyzer()
                # Define where the results will be saved
                output_folder = "movie_emotions"

                # Process each review file in the selected folder
                for file_name in os.listdir(review_folder):
                    if file_name.endswith(".csv"):
                        file_path = os.path.join(review_folder, file_name)
                        # Process individual file
                        analyzer.analyze_file(file_path, output_folder)

                # Optionally, aggregate the results and rank movies by emotion
                combined_results = analyzer.aggregate_results(output_folder)
                scary_scores = analyzer.rank_movies(
                    combined_results, emotion_label="fear"
                )

                # Save rankings
                scary_scores.to_csv("scary_movie_rankings.csv", index=False)
                logging.info(
                    "Scary movie rankings saved to 'scary_movie_rankings.csv'"
                )

                # Save the last sentiment ID after sentiment analysis is
                # complete
                if scary_scores.shape[0] > 0:
                    # Get the first IMDb ID from the rankings
                    last_sentiment_id = scary_scores.iloc[0]["imdb_id"]
                    logging.info(
                        f"Saving last sentiment ID: {last_sentiment_id}"
                    )
                    progress_manager.save_progress(
                        last_id='',
                        dataset_name=last_dataset_name,
                        sentiment_id=last_sentiment_id
                    )

                # Terminate the program after ranking is complete
                logging.info("Ranking complete. Exiting program.")
                sys.exit(0)  # Exit the program

            else:
                logging.error("Invalid or missing review folder. Exiting.")
                continue

        else:
            logging.error("Invalid choice. Please enter 1, 2, 3, or 4.")

    # Initialize and start the scraping pipeline
    web_driver_manager = WebDriverManager()
    try:
        driver = web_driver_manager.setup_driver(headless=False)
        scraper_pipeline = MovieScraperPipeline(driver)
        scraper_pipeline.run_pipeline(
            filtered_movies,
            dataset_name=dataset_name,
            start_from_id=imdb_id_to_start
        )
    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
    finally:
        web_driver_manager.quit_driver()
