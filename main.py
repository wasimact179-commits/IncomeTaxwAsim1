from fastapi import FastAPI
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

genai.configure(api_key="YOUR_GEMINI_API_KEY")

app = FastAPI()

@app.get("/ask")
def ask(q: str):
    url = "http://bdlaws.minlaw.gov.bd/act-1429/section-51885.html"
    html = requests.get(url, timeout=15).text
    text = BeautifulSoup(html, "html.parser").get_text()

    prompt = f"""
    তুমি একজন বাংলাদেশি আয়কর আইন বিশেষজ্ঞ।

    CONTEXT:
    {text}

    QUESTION:
    {q}

    সঠিক ধারা, সহজ বাংলা ব্যাখ্যা,
    Accounting treatment ও প্রয়োজনে flowchart দাও।
    """

    model = genai.GenerativeModel("gemini-pro")
    ans = model.generate_content(prompt)

    return {"answer": ans.text}
