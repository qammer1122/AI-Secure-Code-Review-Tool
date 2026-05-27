from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from data_processing import load_and_preprocess_data
import pandas as pd

def train_ml_model():
    dataset_path = 'security_dataset.csv'
    padded_sequences, labels, fixes, tokenizer, max_sequence_length = load_and_preprocess_data(dataset_path)
    dataset = pd.read_csv(dataset_path)

    X_train, X_val, y_train, y_val = train_test_split(padded_sequences, labels, test_size=0.2, random_state=42)
    
    model = Sequential([
        Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_sequence_length),
        LSTM(64),
        Dense(64, activation='relu'),
        Dense(4, activation='softmax')
    ])
    
    model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    class_weights = {0: 1, 1: 1.5, 2: 2, 3: 3}  # Example: increase weights for higher severities
    model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val), class_weight=class_weights)

    return model, tokenizer, max_sequence_length, dataset
