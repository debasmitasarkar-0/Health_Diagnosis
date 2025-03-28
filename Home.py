import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Health Management App", layout="wide")

# App Title
st.title("🏥 Health Management App")
st.subheader("Your AI-powered health assistant")


# Fetch Health News from Free API
def fetch_health_news():
    try:
        api_key = os.getenv("NEWS_API_KEY")
        url = f"https://newsapi.org/v2/top-headlines?category=health&country=us&apiKey={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            news_data = response.json()
            if news_data["articles"]:
                top_article = news_data["articles"][0]
                return f"📢 **{top_article['title']}**\n\n📰 {top_article['description']} [Read More]({top_article['url']})"
            else:
                return "⚠️ No health news available at the moment."
        else:
            return "⚠️ Unable to fetch health news at the moment."
    except:
        return "⚠️ Unable to fetch health news at the moment."


st.markdown("### 📰 Latest Health News")
st.info(fetch_health_news())





# Home Page Content
st.markdown("## 🌟 Choose an Option Below")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🥗 Food Calories Calculator"):
        st.switch_page("pages/Food Calories Calculator.py")

with col2:
    if st.button("📑 Clinical Lab Report Analyzer"):
        st.switch_page("pages/Clinical Lab Report Analyzer.py")

with col3:
    if st.button("🩺 Health Diagnosis AI"):
        st.switch_page("pages/Health Diagnosis.py")

st.markdown("👆 Click on any option above to proceed!")