import streamlit as st
import requests

st.set_page_config(page_title="Cold Email Generator", page_icon="📧")
st.title("📧 Cold Email Generator")

st.subheader("✏️ Describe your campaign")
product = st.text_area("🧾 Product/Service Description")
audience = st.text_input("🎯 Target audience")
tone = st.selectbox("🗣️ Tone", ["Formal", "Friendly", "Casual", "Persuasive"])
cta = st.text_input("📣 Call to Action (e.g., Book a call)")

if st.button("Generate Email"):
    if not all([product, audience, tone, cta]):
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Generating..."):
            try:
                response = requests.post(
                    "https://cold-email-backend-358a.onrender.com/generate",
                    json={
                        "product": product,
                        "audience": audience,
                        "tone": tone,
                        "cta": cta
                    },
                    timeout=20
                )
                data = response.json()
                if "email" in data:
                    st.text_area("📨 Generated Email", value=data["email"], height=300)
                else:
                    st.error(f"Error: {data.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Request failed: {e}")
