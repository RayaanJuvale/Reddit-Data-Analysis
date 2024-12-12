import streamlit as st
import pg8000
import pandas as pd
import plotly.express as px

# PostgreSQL credentials
DB_HOST = "db"
DB_PORT = 5432
DB_NAME = "reddit_data"
DB_USER = "postgres"
DB_PASSWORD = "Rayu45678&"

def fetch_trending_data(subreddit):
    """Fetch trending topics analysis data from PostgreSQL."""
    conn, cursor = None, None
    try:
        conn = pg8000.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Fetch data from trending_topics table
        cursor.execute("""
            SELECT subreddit, common_keywords, top_post_title, top_post_score, top_post_url
            FROM trending_topics WHERE subreddit = %s;
        """, (subreddit,))
        data = cursor.fetchall()

        if data:
            # Process results into a DataFrame
            return pd.DataFrame(data, columns=['subreddit', 'common_keywords', 'top_post_title', 'top_post_score', 'top_post_url'])
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data
    except Exception as e:
        st.error(f"Error fetching trending data: {e}")
        return pd.DataFrame()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def fetch_posts_data(subreddit):
    """Fetch post data for the selected subreddit."""
    conn, cursor = None, None
    try:
        conn = pg8000.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Fetch data from reddit_posts table
        cursor.execute("""
            SELECT title, created_at, score, comments FROM reddit_posts WHERE subreddit = %s;
        """, (subreddit,))
        posts_data = cursor.fetchall()

        if posts_data:
            # Convert to a DataFrame
            df_posts = pd.DataFrame(posts_data, columns=['title', 'created_at', 'score', 'comments'])
            df_posts['created_at'] = pd.to_datetime(df_posts['created_at'])
            return df_posts
        else:
            return pd.DataFrame()  # Return empty DataFrame if no data
    except Exception as e:
        st.error(f"Error fetching posts data: {e}")
        return pd.DataFrame()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def plot_score_vs_time(df_posts):
    """Plot the score of posts over time."""
    if not df_posts.empty:
        fig = px.scatter(df_posts, x='created_at', y='score', title="Post Score vs. Time")
        fig.update_layout(xaxis_title="Date", yaxis_title="Score")
        return fig
    return None

def plot_comments_vs_time(df_posts):
    """Plot the number of comments over time."""
    if not df_posts.empty:
        fig = px.line(df_posts, x='created_at', y='comments', title="Comments vs. Time")
        fig.update_layout(xaxis_title="Date", yaxis_title="Comments")
        return fig
    return None

# Streamlit UI
st.title("Reddit Analysis Dashboard")
st.sidebar.header("Select Subreddit")

# Dropdown to select subreddit
subreddit_list = [
    "AskReddit", "news", "funny", "gaming", "pics", "science", "todayilearned", "worldnews",
    "movies", "aww", "Music", "videos", "technology", "books", "sports", "food",
    "history", "Art", "memes", "space"
]
selected_subreddit = st.sidebar.selectbox("Choose a Subreddit", subreddit_list)

# Fetch and display trending data
st.header(f"Trending Topics in {selected_subreddit}")
trending_data = fetch_trending_data(selected_subreddit)
if not trending_data.empty:
    st.write(trending_data)

    # Display common keywords as a list
    common_keywords = trending_data['common_keywords'].iloc[0]
    st.subheader("Common Keywords in Titles")
    st.write(common_keywords)

    # Display the top post details
    st.subheader("Top Post Details")
    st.write(f"**Title:** {trending_data['top_post_title'].iloc[0]}")
    st.write(f"**Score:** {trending_data['top_post_score'].iloc[0]}")
    st.write(f"[**Link to Post**]({trending_data['top_post_url'].iloc[0]})")
else:
    st.info("No trending data available for this subreddit.")

# Fetch posts data for the selected subreddit
st.header(f"Posts Analysis for {selected_subreddit}")
df_posts = fetch_posts_data(selected_subreddit)
if not df_posts.empty:
    st.write(df_posts)

    # Plot Score vs Time
    score_vs_time_fig = plot_score_vs_time(df_posts)
    if score_vs_time_fig:
        st.plotly_chart(score_vs_time_fig)

    # Plot Comments vs Time
    comments_vs_time_fig = plot_comments_vs_time(df_posts)
    if comments_vs_time_fig:
        st.plotly_chart(comments_vs_time_fig)
else:
    st.info("No posts data available for this subreddit.")
