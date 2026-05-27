import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def load_and_preprocess_data(dataset_path, max_sequence_length=100):
    df = pd.read_csv(dataset_path)
    df.columns = [col.strip() for col in df.columns]  # Strip extra spaces in headers

    # Ensure required columns are present
    required_columns = {'code', 'severity', 'fixes'}
    if not required_columns.issubset(df.columns):
        raise ValueError("Dataset must have 'code', 'severity', and 'fixes' columns")

    severity_map = {"Critical": 3, "High": 2, "Medium": 1, "Low": 0}
    df['severity'] = df['severity'].map(severity_map)

    # BUG FIX #8: drop rows where severity didn't match any known label (would become NaN and crash training)
    invalid_count = df['severity'].isna().sum()
    if invalid_count > 0:
        print(f"Warning: {invalid_count} rows had unrecognized severity labels and were dropped.")
        df = df.dropna(subset=['severity'])

    df['severity'] = df['severity'].astype(int)

    # Tokenize the code
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(df['code'])

    # Convert 'code' to padded sequences
    padded_sequences = tokenizer.texts_to_sequences(df['code'])
    padded_sequences = pad_sequences(padded_sequences, maxlen=max_sequence_length, padding='post', truncating='post')

    labels = df['severity'].values
    fixes = df['fixes'].values
    return padded_sequences, labels, fixes, tokenizer, max_sequence_length
