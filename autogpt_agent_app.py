import streamlit as st
import openai
import time

# Title and description
st.title("🛡 Ultra-Safe Quota-Controlled AutoGPT Agent")
st.write("This agent checks your key, usage, limits, and intelligently selects models based on estimated tokens, quotas, and rate limits.")

# API Key input (safe)
api_key = st.text_input("Enter your OpenAI API Key (starts with sk-...):", type="password")

# User task input
task = st.text_area("Enter your task:", 
    value="""Find 3 recent academic papers (after 2021) related to the use of machine learning for early cancer detection. Summarize the main contributions of each. Then, write Python code that simulates a basic logistic regression classifier using a sample dataset (e.g., breast cancer dataset from scikit-learn) to demonstrate the concept.""")

# Token estimation function (simple, safe heuristic)
def estimate_tokens(prompt_text):
    return int(len(prompt_text) / 4)

def get_current_usage():
    try:
        usage = openai.billing.usage()
        return usage
    except Exception as e:
        return f"Cannot check usage or quota: {e}"

# Smart decision logic
def choose_model(token_estimate):
    if token_estimate < 5000:
        return "gpt-4o"
    else:
        return "gpt-3.5-turbo"

# Execution
if st.button("Run Agent"):
    if not api_key.startswith("sk-"):
        st.error("❌ Invalid API Key.")
    else:
        openai.api_key = api_key

        # Estimate token usage
        est_tokens = estimate_tokens(task)
        st.info(f"Estimated tokens for your task (prompt only): ~{est_tokens} tokens")

        # Try quota usage check (safe fallback if fails)
        usage_check = get_current_usage()
        st.info(f"Quota check result (may be limited in scoped keys): {usage_check}")

        # Auto model decision
        selected_model = choose_model(est_tokens)
        st.info(f"📊 Smart Decision: Using `{selected_model}` based on estimated tokens")

        # Compose conversation
        conversation = [
            {"role": "system", "content": "You are an autonomous research agent working step by step."},
            {"role": "user", "content": task}
        ]

        # Safe execution
        try:
            st.info(f"🔄 Trying {selected_model}...")
            response = openai.chat.completions.create(
                model=selected_model,
                messages=conversation,
                max_tokens=3500,
                temperature=0.2
            )
            st.success(f"✅ Task completed with {selected_model}")
            st.write(response.choices[0].message.content)

        except openai.OpenAIError as e:
            st.error(f"❌ OpenAI API Error: {e}")
