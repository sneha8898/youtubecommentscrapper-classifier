import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import re
from util import classify, set_background
import time

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

# Set background image and styles
background_css = set_background('https://static01.nyt.com/images/2019/07/23/arts/23youtube/merlin_155983551_a3c15fea-a1c7-4c46-8063-06a1fefe4673-superJumbo.jpg')
st.markdown(background_css, unsafe_allow_html=True)

st.title("YouTube Video Comments Sentiment Analysis")

# Display loading spinner while fetching data
video_url = st.text_input("Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=VIDEO_ID")

if st.button("Fetch Video Details and Comments"):
    with st.spinner("Fetching video details and comments..."):
        video_id = extract_video_id(video_url)
        if video_id:
            try:
                video_title, comments = fetch_youtube_video_details(video_id, API_KEY)
                comment_sentiments = classify(comments)
                comments_df = pd.DataFrame({
                    "Comment": comments,
                    "Sentiment": comment_sentiments
                })

                # Add sentiment filter
                sentiment_filter = st.selectbox(
                    "Filter comments by sentiment",
                    ["All", "Positive", "Negative"]
                )
                if sentiment_filter != "All":
                    comments_df = comments_df[comments_df["Sentiment"] == sentiment_filter]

                st.write(f"**Video Title:** {video_title}")
                st.write(comments_df)
            except Exception as e:
                st.error(f"An error occurred: {e}")
