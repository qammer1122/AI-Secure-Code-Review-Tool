import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split


def load_and_preprocess_data(dataset_path, max_sequence_length=100):
    """Load and preprocess the security dataset for model training."""
    df = pd.read_csv(dataset_path)
    df.columns = [col.strip() for col in df.columns]

    severity_map = {"Critical": 3, "High": 2, "Medium": 1, "Low": 0}
    df['severity'] = df['severity'].map(severity_map)

    # Drop rows with unrecognized severity labels
    invalid_count = df['severity'].isna().sum()
    if invalid_count > 0:
        print(f"Warning: {invalid_count} rows had unrecognized severity labels and were dropped.")
        df = df.dropna(subset=['severity'])

    df['severity'] = df['severity'].astype(int)

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(df['code'])

    padded_sequences = tokenizer.texts_to_sequences(df['code'])
    padded_sequences = pad_sequences(
        padded_sequences, maxlen=max_sequence_length,
        padding='post', truncating='post'
    )

    labels = df['severity'].values
    return padded_sequences, labels, tokenizer, max_sequence_length


def train_severity_model(vocab_size, max_sequence_length, padded_sequences, labels):
    """Build and train the severity classification model."""
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=32, input_length=max_sequence_length),
        LSTM(32),
        Dense(4, activation='softmax')
    ])
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    X_train, X_val, y_train, y_val = train_test_split(
        padded_sequences, labels, test_size=0.2, random_state=42
    )
    model.fit(
        X_train, y_train, epochs=10,
        validation_data=(X_val, y_val),
        class_weight={0: 1, 1: 1, 2: 1, 3: 5}
    )
    return model


def calculate_severity_thresholds(model, tokenizer, max_sequence_length, data, labels):
    """Calculate adaptive severity thresholds from model predictions."""
    sequences = tokenizer.texts_to_sequences(data)
    padded_sequences = pad_sequences(
        sequences, maxlen=max_sequence_length,
        padding='post', truncating='post'
    )

    predictions = model.predict(padded_sequences)

    severity_scores = {"Critical": [], "High": [], "Medium": [], "Low": []}
    severity_labels = ["Low", "Medium", "High", "Critical"]

    for i, pred in enumerate(predictions):
        true_label = severity_labels[labels[i]]
        max_score = np.max(pred)
        severity_scores[true_label].append(max_score)

    thresholds = {}
    for severity, scores in severity_scores.items():
        if scores:
            mean_score = np.mean(scores)
            std_dev = np.std(scores)
            if severity == "Critical":
                thresholds[severity] = mean_score + std_dev
            elif severity == "High":
                thresholds[severity] = mean_score
            elif severity == "Medium":
                thresholds[severity] = mean_score - std_dev
            elif severity == "Low":
                thresholds[severity] = mean_score - 2 * std_dev
        else:
            thresholds[severity] = 0

    return thresholds


def analyze_severity_distribution(dataset_path):
    """Analyze and print severity distribution in the dataset."""
    df = pd.read_csv(dataset_path)
    df.columns = [col.strip() for col in df.columns]

    severity_counts = df['severity'].value_counts()
    severity_percentage = (severity_counts / len(df)) * 100

    print("Severity Distribution:")
    print(severity_counts)
    print("\nSeverity Distribution (Percentage):")
    print(severity_percentage)
    return severity_counts


if __name__ == "__main__":
    dataset_path = 'security_dataset.csv'
    max_sequence_length = 100

    # Load and preprocess
    padded_sequences, labels, tokenizer, max_sequence_length = load_and_preprocess_data(
        dataset_path, max_sequence_length
    )

    # Train model
    vocab_size = len(tokenizer.word_index) + 1
    model = train_severity_model(vocab_size, max_sequence_length, padded_sequences, labels)

    # Calculate thresholds
    data_samples = pd.read_csv(dataset_path)['code'].values
    thresholds = calculate_severity_thresholds(
        model, tokenizer, max_sequence_length, data_samples, labels
    )
    print("\nCalculated severity thresholds:", thresholds)

    # Analyze distribution
    analyze_severity_distribution(dataset_path)
