import streamlit as st
import requests

st.set_page_config(page_title="Cold Email Generator", page_icon="📧")
st.title("📧 Cold Email Generator")

# Footer credit
st.markdown("<p style='text-align:right; font-size:14px;'>Made by <b>Siddarth Choudhary</b></p>", unsafe_allow_html=True)

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

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
                res = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3-70b-8192",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 400
                    }
                )
                data = res.json()
                if "choices" in data:
                    default_email = data["choices"][0]["message"]["content"]
                    st.subheader("📨 Generated Email (Editable)")
                    final_email = st.text_area("Edit the email if you'd like", value=default_email, height=300, key="editable_email")

                    # Download button
                    st.download_button(
                        label="💾 Download Email",
                        data=final_email,
                        file_name="cold_email.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"❌ Unexpected API response:\n\n{data}")
            except Exception as e:
                st.error(f"🚨 Request failed: {e}")
