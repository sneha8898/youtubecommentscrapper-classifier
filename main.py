import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from textblob import TextBlob
import re

# Predefined API key
API_KEY = "AIzaSyDohi1bI6QnqMBbN7LOggmpWvabYM04j8c"

# Function to extract video ID from URL
def extract_video_id(url):
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        st.error("Invalid YouTube URL. Please make sure the URL is in the format: https://www.youtube.com/watch?v=VIDEO_ID")
        return None

# Function to fetch YouTube video title and all comments
def fetch_youtube_video_details(video_id, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)

    # Fetch video details
    video_response = youtube.videos().list(
        part="snippet",
        id=video_id
    ).execute()

    video_title = video_response['items'][0]['snippet']['title']

    # Fetch comments with pagination
    comments = []
    next_page_token = None

    while True:
        comments_response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        ).execute()

        for item in comments_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        next_page_token = comments_response.get('nextPageToken')
        if not next_page_token:
            break

    return video_title, comments

# Function to classify comments
def classify_comments(comments):
    comment_sentiments = []
    for comment in comments:
        analysis = TextBlob(comment)
        sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative"
        comment_sentiments.append(sentiment)
    return comment_sentiments

# Streamlit App
st.title("YouTube Video Comments Sentiment Analysis")

# Ask for the YouTube video URL
video_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=VIDEO_ID")

# Fetch video details and comments when button is clicked
if st.button("Fetch Video Details and Comments"):
    video_id = extract_video_id(video_url)
    if video_id:
        video_title, comments = fetch_youtube_video_details(video_id, API_KEY)
        comment_sentiments = classify_comments(comments)
        
        comments_df = pd.DataFrame({
            "Comment": comments,
            "Sentiment": comment_sentiments
        })

        st.write(f"**Video Title:** {video_title}")
        st.write(comments_df)
