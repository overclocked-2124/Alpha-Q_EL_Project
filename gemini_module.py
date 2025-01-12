import google.generativeai as genai


def analyze_data(prompt):
    # Configure the API key
    genai.configure(api_key="AIzaSyAy2h11mWJ-ew43uVR2SZ3cMyqt8cTgfbs")  # Replace with your actual API key

    # Initialize the GenerativeModel
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Define the 2-shot prompt with examples
    examples = """
    Example 1:
    - X-axis: Temperature Front (°C)
    - Y-axis: Power TEG (W)
    - Analysis: The data shows a strong positive correlation between Temperature Front and Power TEG. As the temperature increases, the power output from the TEG also increases. This suggests that the TEG is more efficient at higher temperatures.

    Example 2:
    - X-axis: Voltage Solar (V)
    - Y-axis: Current Solar (A)
    - Analysis: The data exhibits a linear relationship between Voltage Solar and Current Solar. As the voltage increases, the current also increases proportionally. This indicates that the solar panel is operating within its expected range.
    """

    # Combine the examples with the user's prompt
    full_prompt = f"{examples}\n\nAnalyze the following data and provide insights:\n{prompt}"

    # Generate a response using the correct method
    response = model.generate_content(full_prompt)

    # Clean up the response and structure it into sections
    cleaned_response = clean_and_structure_response(response.text)

    # Return the cleaned and structured response
    return cleaned_response


def clean_and_structure_response(response_text):
    # Remove redundant phrases like "Insights:" if they appear multiple times
    response_text = response_text.replace("Insights:", "").strip()

    # Split the response into paragraphs
    paragraphs = response_text.split("\n\n")

    # Remove empty paragraphs
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    # Structure the response into HTML
    structured_response = "<ul>"
    for paragraph in paragraphs:
        structured_response += f"<li>{paragraph}</li>"
    structured_response += "</ul>"

    return structured_response