import streamlit as st

# Define your questions and weights
questions_and_weights = {
    "Do you have a vision statement?": 5,
    "How many pages is your strategy document?": 3,
    # Add more questions and their weights here
}

# Initialize the total score
total_score = 0

# Create the questionnaire
for question, weight in questions_and_weights.items():
    # Use a numeric input for answers
    answer = st.number_input(question, min_value=0.0)
    # Update total score based on the answer and the weight
    total_score += answer * weight

# Set a threshold for a "good" client
good_client_threshold = 50  # This is an example threshold

# Display the result
if total_score >= good_client_threshold:
    st.success("This client is good: YES")
else:
    st.error("This client is good: NO")

st.write(f"Total Score: {total_score}")
