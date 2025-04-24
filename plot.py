import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_scary_movies(analysis_file):
    """
    Generate plots for the scariest movies analysis.

    Parameters:
        analysis_file (str): Path to the CSV file containing the analysis
        results.
    """
    try:
        # Load the analysis data
        df = pd.read_csv(analysis_file)

        # Bar Plot: Top 10 scariest movies by Weighted Score
        top_movies = df.head(10)
        plt.figure(figsize=(12, 6))
        sns.barplot(
            data=top_movies,
            x="Weighted_Score",
            y="primaryTitle",
            palette="viridis"
        )
        plt.title("Top 10 Scariest Movies by Weighted Score", fontsize=16)
        plt.xlabel("Weighted Score", fontsize=14)
        plt.ylabel("Movie Title", fontsize=14)
        plt.tight_layout()
        plt.savefig("top_10_scary_movies.png")  # Save the plot as an image
        plt.show()

        # Distribution Plot: Weighted Scores distribution
        plt.figure(figsize=(12, 6))
        sns.histplot(df["Weighted_Score"], kde=True, color="purple", bins=20)
        plt.title("Distribution of Weighted Scary Scores", fontsize=16)
        plt.xlabel("Weighted Score", fontsize=14)
        plt.ylabel("Frequency", fontsize=14)
        plt.tight_layout()
        plt.savefig("weighted_score_distribution.png")
        plt.show()

        # Genres vs. Weighted Scores
        plt.figure(figsize=(12, 6))
        # Explode genres into multiple rows for movies with multiple genres
        genres_df = df.dropna(subset=["genres"])
        genres_df = genres_df.assign(
            genre=genres_df["genres"].str.split(",")
        ).explode("genre")
        sns.boxplot(
            data=genres_df,
            x="genre",
            y="Weighted_Score",
            palette="coolwarm"
        )
        plt.title("Genres vs. Weighted Scary Scores", fontsize=16)
        plt.xlabel("Genre", fontsize=14)
        plt.ylabel("Weighted Score", fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("genres_vs_weighted_scores.png")
        plt.show()

    except Exception as e:
        print(f"Error generating plots: {e}")


# Example usage
analysis_file = (
    "balanced_scary_movies_analysis.csv"  # Results from the analysis
)
plot_scary_movies(analysis_file)
