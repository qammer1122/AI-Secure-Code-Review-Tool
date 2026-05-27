from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


def run_ml_analysis(code, tokenizer, model, max_sequence_length, dataset, low_threshold=0.5):
    # Preprocess the code line and get the model's prediction
    try:
        encoded_code = tokenizer.texts_to_sequences([code.strip()])
        padded_code = pad_sequences(encoded_code, maxlen=max_sequence_length, padding='post')
        prediction_scores = model.predict(padded_code)[0]  # Assuming model outputs probabilities for each severity

        # Check for an exact match in the dataset first
        severity, suggested_fix = get_severity_and_fix(code, prediction_scores, dataset, low_threshold)

        # If severity is None (below Low threshold), exclude from the report
        if severity is None:
            return None, None, None  # BUG FIX #1: was returning bare None, causing TypeError on unpack in app.py

        # Log final results for debugging
        print(f"Code Line: '{code}'")
        print(f"Severity: {severity}")
        print(f"Suggested Fix: {suggested_fix}")

        return prediction_scores, severity, suggested_fix

    except Exception as e:
        print(f"Error in ML analysis: {e}")
        return None, None, None  # Consistent 3-tuple return on error


def get_severity_and_fix(code_line, prediction_scores, dataset, low_threshold):
    stripped_code_line = code_line.strip()  # Normalize the code line
    exact_matches = dataset['code'].str.strip() == stripped_code_line

    # Check for an exact match
    if exact_matches.any():
        row = dataset.loc[exact_matches].iloc[0]  # Retrieve the row with the exact match
        fix = row['fixes']
        severity = row['severity']
        print(f"Exact match found in dataset. Overriding severity to: {severity}, Fix: {fix}")
        return severity, fix  # Use dataset's severity and fix directly if exact match is found

    # If no exact match, apply prediction-based severity mapping
    mapped_severity = map_severity(prediction_scores, low_threshold)
    if mapped_severity is None:  # If severity is below the threshold, exclude it
        print("Severity below threshold. Excluding code line.")
        return None, None

    suggested_fix = "No suggested fix available"
    print(f"No exact match found. Using model-mapped Severity: {mapped_severity}")
    return mapped_severity, suggested_fix


def map_severity(prediction_scores, low_threshold=0.5):
    severity_mapping = {0: "Low", 1: "Medium", 2: "High", 3: "Critical"}

    # Log prediction scores for debugging
    print(f"Prediction scores: {prediction_scores}")

    # Determine the index with the highest probability score
    max_index = np.argmax(prediction_scores)
    max_score = prediction_scores[max_index]

    # Stricter thresholds for adaptive severity classification
    if max_score < low_threshold:  # Exclude anything below the Low threshold
        return None  # Return None to indicate exclusion
    elif max_index == 3 and max_score >= 0.7:  # Threshold for "Critical"
        severity = "Critical"
    elif max_index == 2 and max_score >= 0.6:  # Threshold for "High"
        severity = "High"
    elif max_index == 1 and max_score >= 0.5:  # Threshold for "Medium"
        severity = "Medium"
    else:
        severity = "Low"  # Default to "Low"

    print(f"Mapped severity: {severity} based on score {max_score} at index {max_index}")
    return severity
