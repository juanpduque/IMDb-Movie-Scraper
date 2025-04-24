import pandas as pd
import os

def create_files_by_title_type(file_path):
    """
    Read the title.basics.tsv file and create a separate file for each title type.

    Parameters:
        file_path (str): Path to the title.basics.tsv file.
    """
    try:
        # Read the TSV file
        df = pd.read_csv(file_path, sep='\t', dtype=str)

        # Group the data by title type
        grouped = df.groupby('titleType')

        # Create a directory to save the files
        output_dir = os.path.join(os.path.dirname(file_path), 'title_types')
        os.makedirs(output_dir, exist_ok=True)

        # Save each group to a separate file
        for title_type, group in grouped:
            output_file = os.path.join(output_dir, f'{title_type}.tsv')
            group.to_csv(output_file, sep='\t', index=False)
            print(f"File saved: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    file_path = 'data/title.basics.tsv'  # Replace with your actual file path
    create_files_by_title_type(file_path)