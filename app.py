import streamlit as st
import joblib
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import os
from datetime import datetime Enhancement

# Load models and preprocessing tools
logistic_model = joblib.load('logistic_model.pkl')
naive_bayes_model = joblib.load('naive_bayes_model.pkl')
lstm_model = tf.keras.models.load_model('lstm_model.h5')
tfidf = joblib.load('tfidf_vectorizer.pkl')
tokenizer = joblib.load('tokenizer.pkl')

# Preprocessing function
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def preprocess_text(text):
    text = remove_html_tags(text)
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    text = re.sub(r'\b[a-zA-Z]\b', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to log review and predictions
def log_review(review, log_pred, nb_pred, lstm_pred):
    log_dir = '/logs'
    log_file = os.path.join(log_dir, 'history.log')
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Format the log entry
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = (f"{timestamp} | Review: {review[:100]}... | "
                 f"Logistic: {'Positive' if log_pred == 1 else 'Negative'} | "
                 f"Naive Bayes: {'Positive' if nb_pred == 1 else 'Negative'} | "
                 f"LSTM: {'Positive' if lstm_pred == 1 else 'Negative'}\n")
    
    # Append to log file
    with open(log_file, 'a') as f:
        f.write(log_entry)

# Streamlit app
st.set_page_config(page_title="Movie Sentiment Analyzer", page_icon="🎬")
st.title("🎬 Movie Review Sentiment Analyzer")
st.markdown("Enter a movie review to see predictions from multiple models. Check the history to view past submissions!")

# Sidebar with info
st.sidebar.header("About This App")
st.sidebar.markdown("""
This app uses three models to predict movie review sentiment:
- **Logistic Regression**: Linear model with TF-IDF features.
- **Naive Bayes**: Probabilistic model based on word frequencies.
- **LSTM**: Neural network with GloVe embeddings.
**Note**: Models may struggle with sarcasm.
""")

# User input
review = st.text_area("Enter Your Movie Review", "Type your review here...", height=150)

# Analyze button
if st.button("Analyze", key="analyze_button"):
    with st.spinner("Analyzing your review..."):
        # Preprocess the input
        cleaned_review = preprocess_text(review)

        # For Logistic Regression and Naive Bayes (TF-IDF)
        tfidf_input = tfidf.transform([cleaned_review])

        # For LSTM (tokenization and padding)
        seq_input = tokenizer.texts_to_sequences([cleaned_review])
        padded_input = pad_sequences(seq_input, maxlen=100, padding='post')

        # Get predictions
        log_pred = logistic_model.predict(tfidf_input)[0]
        log_prob = logistic_model.predict_proba(tfidf_input)[0][log_pred] * 100
        nb_pred = naive_bayes_model.predict(tfidf_input)[0]
        nb_prob = naive_bayes_model.predict_proba(tfidf_input)[0][nb_pred] * 100
        lstm_prob = lstm_model.predict(padded_input, verbose=0)[0][0]
        lstm_pred = 1 if lstm_prob > 0.5 else 0
        lstm_prob = lstm_prob * 100 if lstm_pred == 1 else (1 - lstm_prob) * 100

        # Convert predictions to labels
        log_label = "Positive" if log_pred == 1 else "Negative"
        nb_label = "Positive" if nb_pred == 1 else "Negative"
        lstm_label = "Positive" if lstm_pred == 1 else "Negative"

        # Log the review and predictions
        log_review(review, log_pred, nb_pred, lstm_pred)

        # Display results
        st.subheader("Predictions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Logistic Regression", log_label, f"{log_prob:.1f}% confident")
        with col2:
            st.metric("Naive Bayes", nb_label, f"{nb_prob:.1f}% confident")
        with col3:
            st.metric("LSTM", lstm_label, f"{lstm_prob:.1f}% confident")

        # Show processed review
        with st.expander("See Your Processed Review"):
            st.write(f"**Original**: {review}")
            st.write(f"**Cleaned**: {cleaned_review}")

# History display
with st.expander("View History"):
    log_file = '/logs/history.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            history = f.read()
        st.text_area("Submission History", history, height=200, disabled=True)
    else:
        st.write("No history yet. Submit a review to start logging!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by [Atul 🤠] | Powered by Streamlit, Scikit-Learn, TensorFlow")