# Flask App to Batch process the data

## Overview
This Flask application processes CSV files containing raw text data in batches, categorizes the text, and outputs categorized data into new files. It provides features like batch processing, checkpointing, error logging, and final data combining.

## Features
- **Batch Processing**: Processes large CSV files in batches of customizable size (e.g., 2000 records per batch).
- **Text Categorization**: from predefined categories, assign categories to batches of text data (e.g., 20 records per batch).
- **Error Handling**: Logs errors encountered during processing to facilitate debugging and troubleshooting.
- **Checkpointing**: Saves checkpoints to resume processing from the last successfully processed batch in case of failures.
- **File Combination**: Combines processed batch files into a single consolidated file for easy access and analysis.

## How It Works
1. **Upload CSV**: Upload a CSV file containing raw text data.
2. **Batch Processing**:
   - Divides the CSV file into batches (e.g., 2000 records).
   - Further divides each batch into smaller batches (e.g., 20 records).
   - Sends each smaller batch of raw text data to the LLM for categorization.
3. **Checkpointing**:
   - Automatically saves checkpoints after processing each batch.
   - Allows resuming processing from the last checkpoint in case of interruptions.
4. **Error Logging**:
   - Logs errors encountered during processing to `logs/error.log`.
   - Provides detailed information to diagnose issues and ensure smooth operation.
5. **File Combination**:
   - After processing all batches, combines the categorized data into a single CSV file (`output.csv`).
   - Ensures all processed data is consolidated for further analysis.

## Usage
To use the application:
- Clone the repository and install necessary dependencies.
- Run the Flask application (`app.py`).
- Access the application through a web browser.
- Upload your CSV file and specify batch size parameters.
- Monitor progress, view logs for errors, and download the final combined output file.

## Dependencies
- Python 3.x
- Flask
- Pandas
- scikit-learn (for ML operations)
- OpenAI GPT-3 (for LLM operations)

## Configuration
Ensure the following configurations are set correctly:
- `app.py`: Main Flask application file.
- `templates/`: Directory containing HTML templates for frontend.
- `static/`: Directory containing static files (e.g., CSS, JS).
- `logs/`: Directory to store application logs.

