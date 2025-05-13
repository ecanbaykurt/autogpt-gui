import streamlit as st
import openai

# Setup OpenAI API Key (safe with Streamlit secrets if deployed)
openai.api_key = st.secrets.get("OPENAI_API_KEY", "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")  # Replace with your key or use secrets

# Title and description
st.title("🧠 AutoGPT-Style Research Agent")
st.write("This app simulates an AutoGPT-style agent that searches academic papers and writes Python code.")

# User task input
task = st.text_area("Enter your task:", 
    value="""Find 3 recent academic papers (after 2021) related to the use of machine learning for early cancer detection. Summarize the main contributions of each. Then, write Python code that simulates a basic logistic regression classifier using a sample dataset (e.g., breast cancer dataset from scikit-learn) to demonstrate the concept.""")

# Execution button
if st.button("Run Agent"):
    st.info("Agent is working on your task. Please wait...")

    # Compose conversation
    conversation = [
        {"role": "system", "content": "You are an autonomous research agent working step by step."},
        {"role": "user", "content": task}
    ]

    # Call GPT-4o or GPT-3.5-turbo fallback
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=conversation,
            max_tokens=3500,
            temperature=0.2
        )
    except Exception as e:
        st.error(f"Error: {e}")
    else:
        st.success("Agent completed the task!")
        st.write(response.choices[0].message.content)
