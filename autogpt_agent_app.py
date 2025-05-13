import streamlit as st
import openai

# Title and description
st.title("🧠 Smart Quota-Aware AutoGPT Agent")
st.write("This agent checks your API key, usage, available models, and smartly falls back to GPT-3.5 Turbo if needed.")

# API Key input (masked)
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

        # Test quota and model access first
        try:
            models = openai.models.list()
            model_ids = [m.id for m in models.data]
            st.info(f"✅ Models you have access to: {', '.join(model_ids)}")

        except Exception as e:
            st.error(f"Failed to check your models or key: {e}")
            st.stop()

        # Compose conversation
        conversation = [
            {"role": "system", "content": "You are an autonomous research agent working step by step."},
            {"role": "user", "content": task}
        ]

        # Try GPT-4o first
        try:
            st.info("Trying GPT-4o...")
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=conversation,
                max_tokens=3500,
                temperature=0.2
            )
            st.success("✅ Agent completed the task using GPT-4o!")
            st.write(response.choices[0].message.content)

        except openai.OpenAIError as e:
            st.warning(f"⚠ GPT-4o failed or quota exceeded: {e}\nTrying GPT-3.5 Turbo as fallback...")
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=conversation,
                    max_tokens=3500,
                    temperature=0.2
                )
                st.success("✅ Agent completed the task using GPT-3.5 Turbo!")
                st.write(response.choices[0].message.content)
            except openai.OpenAIError as e:
                st.error(f"❌ OpenAI API Error even with GPT-3.5 Turbo: {e}")
