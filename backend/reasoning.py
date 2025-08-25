import google.generativeai as genai

def generate_reasoning(stock_info: str, headlines: list, api_key: str) -> str:
    """Use Gemini API to generate reasoning from news headlines."""
    if not api_key:
        return "Gemini API key not found."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        headlines_text = "\n".join([f"- {h['title']}" for h in headlines]) if headlines else "No major news available."
        prompt = f"""
        Stock Analysis:
        {stock_info}

        Relevant News Headlines:
        {headlines_text}

        Based on the above, summarize why this stock may have moved.
        """

        response = model.generate_content(prompt)
        return response.text if response and response.text else "No explanation generated."
    except Exception as e:
        return f"Error generating reasoning: {str(e)}"
