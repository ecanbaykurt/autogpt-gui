import streamlit as st
import openai

# Title and description
st.title("🧠 Ultimate Quota-Aware AutoGPT Agent (Stable)")
st.write("This agent checks your key, tries to see quotas, smartly falls back from GPT-4o to GPT-3.5, and estimates token usage before running.")

# API Key input
api_key = st.text_input("Enter your OpenAI API Key (starts with sk-...):", type="password")

# User task input
task = st.text_area("Enter your task:", 
    value="""Find 3 recent academic papers (after 2021) related to the use of machine learning for early cancer detection. Summarize the main contributions of each. Then, write Python code that simulates a basic logistic regression classifier using a sample dataset (e.g., breast cancer dataset from scikit-learn) to demonstrate the concept.""")

def estimate_tokens(prompt_text):
    # Rough estimate: 1 token ~= 4 characters in English (safe estimate)
    return int(len(prompt_text) / 4)

# Execution button
if st.button("Run Agent"):
    if not api_key.startswith("sk-"):
        st.error("❌ Invalid API Key. Must start with 'sk-'.")
    else:
        openai.api_key = api_key

        # Estimate token usage
        est_tokens = estimate_tokens(task)
        st.info(f"Estimated token usage for your input: ~{est_tokens} tokens (prompt only)")

        # Try to check quota or usage if allowed
        try:
            usage = openai.billing.usage()
            st.info(f"✅ API Key valid. Usage checked (you have access).")
        except Exception as e:
            st.warning(f"⚠ Could not check your usage or quota directly: {e}\nProceeding anyway...")

        # Smart fallback task runner
        conversation = [
            {"role": "system", "content": "You are an autonomous research agent working step by step."},
            {"role": "user", "content": task}
        ]

        try:
            st.info("🔄 Trying GPT-4o...")
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=conversation,
                max_tokens=3500,
                temperature=0.2
            )
            st.success("✅ Task completed with GPT-4o")
            st.write(response.choices[0].message.content)

        except openai.OpenAIError as e:
            st.warning(f"⚠ GPT-4o failed or quota exceeded: {e}\n🔄 Trying GPT-3.5 Turbo...")
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=conversation,
                    max_tokens=3500,
                    temperature=0.2
                )
                st.success("✅ Task completed with GPT-3.5 Turbo")
                st.write(response.choices[0].message.content)
            except openai.OpenAIError as e:
                st.error(f"❌ OpenAI API Error even with GPT-3.5 Turbo: {e}")
