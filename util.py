from textblob import TextBlob

def classify(comments):
    """
    Classifies the sentiment of comments as Positive or Negative.
    
    Args:
    comments (list): List of comment strings.
    
    Returns:
    list: List of sentiment classifications ("Positive" or "Negative").
    """
    comment_sentiments = []
    for comment in comments:
        analysis = TextBlob(comment)
        sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative"
        comment_sentiments.append(sentiment)
    return comment_sentiments

def set_background('bg.jpg'):
    """
    Generates CSS for setting a background image.
    
    Args:
    image_url (str): URL of the background image.
    
    Returns:
    str: CSS style string to set the background image.
    """
    css = f"""
    <style>
    .reportview-container {{
        background: url('{image_url}') no-repeat center center fixed;
        background-size: cover;
        min-height: 100vh;
        color: #ffffff;
    }}
    .sidebar .sidebar-content {{
        background-color: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 5px;
    }}
    .stButton > button {{
        background-color: #007bff;
        color: white;
        border-radius: 5px;
    }}
    .stButton > button:hover {{
        background-color: #0056b3;
    }}
    .header {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }}
    .footer {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        text-align: center;
        font-size: 12px;
    }}
    </style>
    """
    return css
