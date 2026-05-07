import os
import json
from groq import Groq
from flask import Flask, request, jsonify
print(">>> EL SCRIPT ESTA FUNCIONANDO <<<")


app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_APP_KEY"))


SYSTEM_PROMPT = """
You are a Senior Financial Analyst specializing in Global Markets.
Your task is to analyze financial news and provide a structured investment recommendation.

STRICT RULES:
1. Return ONLY a valid JSON object.
2. Do not include any conversational text or explanations outside the JSON.
3. If the news is not related to finance or markets, return an empty object {}.
4. Use the following JSON schema:
{
  "asset_name": "Full name of the company or commodity",
  "ticker": "Stock symbol (e.g., AAPL, TSLA, BTC)",
  "action": "BUY | SELL | HOLD",
  "risk_score": "Integer from 1 to 10",
  "sentiment": "BULLISH | BEARISH | NEUTRAL",
  "analysis_summary": "Concise justification under 150 characters",
  "potential_impact": "How this news affects the market sector"
}
"""

def get_investment_recommendation(news_text):
    try:
        user_prompt = f"Analyze the following news and generate a recommendation: {news_text}"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content 

    except Exception as e:
        print(f"Error en el servicio de IA: {e}")
        return None


@app.route('/test-ai', methods=['POST'])
def handle_test_ai():
    
    data = request.json
    news_text = data.get("news_text") if data else None
    
    if not news_text:
        return jsonify({"error": "El texto de la noticia está vacío"}), 400    
    
   
    result = get_investment_recommendation(news_text)
    
    if result is None:
        return jsonify({"error": "Hubo un problema al procesar la noticia"}), 500
        
   
    return jsonify(json.loads(result))


if __name__ == "__main__":
    app.run(debug=True, port=5000)