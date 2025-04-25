import pandas as pd
from pathlib import Path

# Definir rutas de prueba
TEST_ROOT = Path(__file__).parent
TEST_DATA_DIR = TEST_ROOT / "data"
TEST_RAW_DATA_DIR = TEST_DATA_DIR / "raw"
TEST_PROCESSED_DATA_DIR = TEST_DATA_DIR / "processed"
TEST_RESULTS_DIR = TEST_DATA_DIR / "results"
TEST_MOVIE_DATA_DIR = TEST_RAW_DATA_DIR / "movie_data"
TEST_REVIEWS_DIR = TEST_RAW_DATA_DIR / "reviews"

def test_data_loading():
    """Test loading of test data files."""
    try:
        # Test loading movies data
        movies_df = pd.read_csv(TEST_MOVIE_DATA_DIR / "test_movies.tsv", sep='\t')
        print("✓ Movies data loaded successfully")
        print(f"  Shape: {movies_df.shape}")
        print(f"  Columns: {movies_df.columns.tolist()}")
        
        # Test loading reviews data
        reviews_df = pd.read_csv(TEST_PROCESSED_DATA_DIR / "test_reviews.csv")
        print("✓ Reviews data loaded successfully")
        print(f"  Shape: {reviews_df.shape}")
        print(f"  Columns: {reviews_df.columns.tolist()}")
        
        # Test loading analysis data
        analysis_df = pd.read_csv(TEST_PROCESSED_DATA_DIR / "test_analysis.csv")
        print("✓ Analysis data loaded successfully")
        print(f"  Shape: {analysis_df.shape}")
        print(f"  Columns: {analysis_df.columns.tolist()}")
        
        return True
    except Exception as e:
        print(f"✗ Error loading test data: {e}")
        return False

def test_directory_structure():
    """Test if all required directories exist."""
    required_dirs = [
        TEST_MOVIE_DATA_DIR,
        TEST_REVIEWS_DIR,
        TEST_PROCESSED_DATA_DIR,
        TEST_RESULTS_DIR
    ]
    
    all_dirs_exist = True
    for directory in required_dirs:
        if not directory.exists():
            print(f"✗ Directory not found: {directory}")
            all_dirs_exist = False
        else:
            print(f"✓ Directory exists: {directory}")
    
    return all_dirs_exist

if __name__ == "__main__":
    print("Testing directory structure...")
    dir_test = test_directory_structure()
    
    print("\nTesting data loading...")
    data_test = test_data_loading()
    
    if dir_test and data_test:
        print("\n✓ All tests passed successfully!")
    else:
        print("\n✗ Some tests failed. Please check the output above.") 