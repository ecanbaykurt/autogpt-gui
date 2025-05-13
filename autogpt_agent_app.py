import streamlit as st
import openai

# Title and description
st.title("🧠 AutoGPT-Style Research Agent (Streamlit)")
st.write("This app simulates an AutoGPT-style agent that searches academic papers and writes Python code using OpenAI GPT-4o or GPT-3.5.")

# API Key input (safe, no hardcoding)
api_key = st.text_input("Enter your OpenAI API Key (starts with sk-...):", type="password")

# User task input
task = st.text_area("Enter your task:", 
    value="""Find 3 recent academic papers (after 2021) related to the use of machine learning for early cancer detection. Summarize the main contributions of each. Then, write Python code that simulates a basic logistic regression classifier using a sample dataset (e.g., breast cancer dataset from scikit-learn) to demonstrate the concept.""")

# Execution button
if st.button("Run Agent"):
    if not api_key.startswith("sk-"):
        st.error("Please enter a valid OpenAI API key starting with 'sk-'.")
    else:
        openai.api_key = api_key
        st.info("Agent is working on your task. Please wait...")

        conversation = [
            {"role": "system", "content": "You are an autonomous research agent working step by step."},
            {"role": "user", "content": task}
        ]

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=conversation,
                max_tokens=3500,
                temperature=0.2
            )
            st.success("Agent completed the task!")
            st.write(response.choices[0].message.content)
        except openai.OpenAIError as e:
            st.error(f"OpenAI API Error: {e}")
        except Exception as e:
            st.error(f"General Error: {e}")
