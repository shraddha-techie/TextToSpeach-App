import streamlit as st
import requests
import json

st.title("🌟 Cloud + AI: Text to Speech App")
st.write("Enter text below and convert it into speech using AWS Polly!")

user_text = st.text_area("Enter your text:")

if st.button("Convert to Speech"):
    if user_text.strip() != "":
        url = "https://1q10knetjg.execute-api.ap-south-1.amazonaws.com/dev/speak"

        try:
            response = requests.post(url, json={"text": user_text})
            
            if response.status_code == 200:
                st.success("✅ Speech generated successfully!")

                # 🔹 Step 1: Safe response parsing
                try:
                    resp_json = response.json()
                except Exception:
                    st.error("Response is not valid JSON.")
                    st.write(response.text)
                    resp_json = {}

                # 🔹 Step 2: Check if 'body' exists
                if "body" in resp_json:
                    # body is JSON string → convert to dict
                    body_json = json.loads(resp_json["body"])
                else:
                    # normal dict
                    body_json = resp_json

                # 🔹 Step 3: Get audio_url
                audio_url = body_json.get("audio_url")
                if audio_url:
                    st.audio(audio_url)
                    st.write(f"🔗 [Download Audio File]({audio_url})")
                else:
                    st.warning("⚠️ Audio URL not found in response.")

            else:
                st.error(f"❌ API error: {response.status_code}")

        except Exception as e:
            st.error(f"Error parsing response: {e}")

    else:
        st.warning("⚠️ Please enter some text!")
