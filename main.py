import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from textblob import TextBlob
import re
from PIL import Image


API_KEY = "AIzaSyDohi1bI6QnqMBbN7LOggmpWvabYM04j8c"

def extract_video_id(url):
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        st.error("Invalid YouTube URL. Please make sure the URL is in the format: https://www.youtube.com/watch?v=VIDEO_ID")
        return None


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

def classify_comments(comments):
    comment_sentiments = []
    for comment in comments:
        analysis = TextBlob(comment)
        sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative"
        comment_sentiments.append(sentiment)
    return comment_sentiments
st.markdown(
    """
    <style>
    .reportview-container {
        background: url('https://static01.nyt.com/images/2019/07/23/arts/23youtube/merlin_155983551_a3c15fea-a1c7-4c46-8063-06a1fefe4673-superJumbo.jpg') no-repeat center center fixed;
        background-size: cover;
        min-height: 100vh;  /* Ensure the background covers the full viewport height */
    }
    .sidebar .sidebar-content {
        background-color: rgba(255, 255, 255, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("YouTube Video Comments Sentiment Analysis")







video_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=VIDEO_ID")

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
