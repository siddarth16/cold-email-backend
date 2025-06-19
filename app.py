import streamlit as st
import requests

st.set_page_config(page_title="Cold Email Generator", page_icon="📧")
st.title("📧 Free Cold Email Generator (Groq + Mixtral)")

# Load API key securely from Streamlit secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Input fields
product = st.text_area("🧾 Product/Service Description")
audience = st.text_input("🎯 Target audience")
tone = st.selectbox("🗣️ Tone", ["Formal", "Friendly", "Casual", "Persuasive"])
cta = st.text_input("📣 Call to Action (e.g., Book a call)")

if st.button("Generate Email"):
    if not all([product, audience, tone, cta]):
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Generating..."):
            prompt = f"""Write a cold email for:
Product: {product}
Target Audience: {audience}
Tone: {tone}
CTA: {cta}
Keep it short and engaging."""

            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "mixtral-8x7b-instruct",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 400
                    }
                )
                data = response.json()

                # Check if response contains choices
                if "choices" in data:
                    email = data["choices"][0]["message"]["content"]
                    st.text_area("📨 Generated Email", value=email, height=300)
                else:
                    st.error(f"❌ Unexpected API response:\n\n{data}")

            except Exception as e:
                st.error(f"🚨 Request failed: {e}")
