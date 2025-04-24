import os
import logging
import pandas as pd
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class SentimentAnalyzer:
    def __init__(self,
                 emotion_model="j-hartmann/emotion-english-distilroberta-base",
                 device=0):
        """
        Initializes the sentiment analyzer with a specified emotion model.
        """
        logging.info("Loading emotion detection model...")
        tokenizer = AutoTokenizer.from_pretrained(emotion_model)
        model = AutoModelForSequenceClassification.from_pretrained(
            emotion_model
        )
        self.emotion_classifier = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            padding=True,
            truncation=True,
            max_length=512,
            device=device if torch.cuda.is_available() else -1
        )
        logging.info("Emotion detection model loaded successfully.")

    def analyze_file(self, file_path, output_folder):
        """
        Analyze sentiments for a single file of reviews.

        Parameters:
            file_path (str): Path to the file containing reviews.
            output_folder (str): Path to the folder where results will be
                                  saved.
        """
        try:
            df = pd.read_csv(file_path)
            imdb_id = os.path.basename(file_path).split("_")[1].split(".")[0]
            logging.info(f"Processing file: {file_path} (IMDb ID: {imdb_id})")

            # Perform sentiment analysis
            results = []
            for review in df['Review']:
                try:
                    emotion = self.emotion_classifier(review)
                    predicted_emotion = emotion[0]['label']
                    score = emotion[0]['score']
                    results.append({
                        "Review": review,
                        "Emotion": predicted_emotion,
                        "Score": score
                    })
                except Exception as e:
                    logging.warning(
                        f"Error analyzing review: {review[:50]}... Error: {e}"
                    )

            # Save results
            output_file = f"emotions_{imdb_id}.csv"
            output_path = os.path.join(output_folder, output_file)
            os.makedirs(output_folder, exist_ok=True)
            pd.DataFrame(results).to_csv(output_path, index=False)
            logging.info(f"Sentiment analysis results saved to {output_path}")
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")

    def aggregate_results(self, input_folder):
        """
        Combine all emotion analysis files into a single DataFrame.

        Parameters:
            input_folder (str): Path to the folder containing emotion
                                analysis files.

        Returns:
            pd.DataFrame: Combined DataFrame of all movies.
        """
        aggregated_data = []
        for file_name in os.listdir(input_folder):
            if file_name.endswith(".csv"):
                file_path = os.path.join(input_folder, file_name)
                logging.info(f"Aggregating data from: {file_path}")
                movie_data = pd.read_csv(file_path)
                imdb_id = file_name.split("_")[1].split(".")[0]
                movie_data["imbd_id"] = imdb_id
                aggregated_data.append(movie_data)

        combined_df = pd.concat(aggregated_data, ignore_index=True)
        logging.info(f"Aggregated data contains {len(combined_df)} reviews.")
        return combined_df

    def rank_movies(self, combined_df, emotion_label="fear"):
        """
        Rank movies by the average score of a specific emotion.

        Parameters:
            combined_df (pd.DataFrame): DataFrame containing all reviews
                                         and emotions.
            emotion_label (str): The emotion label to use for ranking
                                  (e.g., "fear").

        Returns:
            pd.DataFrame: DataFrame with IMDb IDs and their average scores.
        """
        logging.info(f"Ranking movies by emotion: {emotion_label}")
        filtered_df = combined_df[combined_df["Emotion"] == emotion_label]
        scores = (
            filtered_df.groupby("imbd_id")["Score"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
            .rename(columns={"Score": "Average_Score"})
        )
        logging.info("Ranking complete.")
        return scores


# Main Execution
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/sentiment_analysis.log"),
        ],
    )

    movie_reviews_folder = "movie_reviews"
    output_folder = "movie_emotions"

    # Initialize sentiment analyzer
    analyzer = SentimentAnalyzer()

    # Process each movie review file
    for file_name in os.listdir(movie_reviews_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(movie_reviews_folder, file_name)
            analyzer.analyze_file(file_path, output_folder)

    # Aggregate all emotion analysis results
    combined_results = analyzer.aggregate_results(output_folder)

    # Rank movies by "fear" scores
    scary_scores = analyzer.rank_movies(combined_results, emotion_label="fear")

    # Save rankings
    scary_scores.to_csv("scary_movie_rankings.csv", index=False)
    logging.info("Scary movie rankings saved to 'scary_movie_rankings.csv'")
