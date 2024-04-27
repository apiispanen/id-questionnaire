
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os, base64
import json

load_dotenv()

st.title("Prospect Evaluation Questionnaire")
# Define your questions and weights
st.write("Please answer the following questions to evaluate a potential client's performance:")
st.divider()
questions_and_weights = {
    "Do you have a vision statement?": 8,
    "Which of these four stakeholder groups are able to communicate your organisation’s vision?": 8,
    "Do you have a strategy document?": 5,
    "How many pages is your strategy document?": 6,
    "When was your strategy document last updated?": 8,
    "Does your strategy have clearly defined objectives?": 9,
    "Is your organisation achieving its strategic objectives?": 4,
    "Which of these four stakeholder groups are able to communicate your organisation’s strategy?": 5,
    "Is there a clear linkage between your strategy and allocation of company resources?": 4,
    "How did you create your strategy?": 8,
    "To what extent were digital technologies a key factor in creating your strategy?": 8,
    "Does your organisation have a digital strategy?": 9,
    "How does your organisation define digital strategy?": 8,
    "Did you use external support (for example, a consulting company) to craft your digital strategy?": 9,
    "Does your organisation actively engage in 'M&A'?": 7,
    "How successful have your acquisitions been?": 8,
    "Do you have meetings to discuss and understand changes in the global business climate?": 6,
    "In response, do you consider making changes to any of your strategy, business model, organisational structure or planned investments?": 8,
    "When do you make changes to any of your strategy, business model, organisational structure or planned investments?": 7,
    "How well does your organisation differentiate itself from competitors?": 4,
    "How do you address defensibility and differentiation?": 1,
    "How often do you address defensibility and differentiation?": 10,
    "Do you believe your organisation is optimally designed to deliver your strategy?": 3,
    "Please elaborate on your answer.": 3,
    "Do you use analytics to measure the performance and delivery of KPIs?": 5
}

# Add more questions and their weights as needed

stream = None
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

st.session_state["openai_model"] = "gpt-3.5-turbo"

answer_list = []

# Initialize the total score
total_score = 0

# Create the questionnaire
for question, weight in questions_and_weights.items():
    # Use a checkbox input for answers
    answer = st.checkbox(question)
    # Convert boolean answer to integer (True = 1, False = 0)
    answer = int(answer)
    # Update total score based on the answer and the weight
    total_score += answer * weight
    # Save the answer to a list
    answer_list.append({"question":question, "answer": answer, "weight": weight})

# Set a threshold for a "good" client
good_client_threshold = 50  # This is an example threshold
great_client_threshold = 100  # This is an example threshold
# Display the result
if total_score >= good_client_threshold:
    st.success("This client is good: YES")
elif total_score >= great_client_threshold:
    st.success("This client is great: YES")
else:
    st.error("This client is good: NO")
st.divider()
st.write(f"Total Score: {total_score}")
st.write(f"Good Client Threshold: {good_client_threshold}")
st.write("Total possible score:", str(sum(questions_and_weights.values())))
st.divider()
st.write("Got questions on your score?")
# st.write("Answers:", answer_list)
with st.container():
    # st.write("Thank you for your feedback! User submitted question:", user_input)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])


    if prompt := st.chat_input("Ask AI a question about the prospect evaluation questionnaire."):
        
        user_prompt = {"role": "user", "content": prompt}

        st.session_state.messages.append(user_prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        system_prompt = {
            "role": "system",
            "content": f"You are an AI assistant. You can ask me questions about the binary prospect evaluation questionnaire. The user who is taking the questionnaire can also ask questions. Their total score currently is: {total_score} out of {sum(questions_and_weights.values())} possible points. To be a good client you need a score of {good_client_threshold} or higher. To be a great client, you need a score of {great_client_threshold} or higher. Their current answers to each question (1 being True, 0 being False) and their weights are:\n\n {questions_and_weights}.\n\n When prompted, don't reveal the weights, but reveal what questions could be the best to improve the score."
        }

        st.session_state.messages.append(system_prompt)


        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            # response = response.choices[0].message.content
            # print(response)
            # st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


    with st.sidebar:
        st.write("""#### **Note**: This Chat is not meant to produce real production-grade results, but to demonstrate the use of prospect questionnaires for practical applications. The actual implementation of these tools is not guaranteed.""")

