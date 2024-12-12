import pg8000
from datetime import datetime
import praw
from collections import Counter
import re

# Reddit API credentials
CLIENT_ID = "rx3BEHmQCd6UYMr7HAxfuQ"
CLIENT_SECRET = "wittjuA1Fimt4b1WnQ7U1xgJ-UrAPA"
USER_AGENT = "Rayaan Juvale"

# PostgreSQL credentials
DB_HOST = "db"
DB_PORT = 5432
DB_NAME = "reddit_data"
DB_USER = "postgres"
DB_PASSWORD = "Rayu45678&"

# Top 20 popular US-based subreddits
SUBREDDITS = [
    "AskReddit", "news", "funny", "gaming", "pics",
    "science", "todayilearned", "worldnews", "movies", "aww",
    "Music", "videos", "technology", "books", "sports",
    "food", "history", "Art", "memes", "space"
]

def fetch_reddit_data(subreddit_name, limit=100):
    """Fetch Reddit posts from a subreddit."""
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)
    
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for post in subreddit.hot(limit=limit):
        posts.append({
            "post_id": post.id,
            "subreddit": post.subreddit.display_name,
            "title": post.title,
            "author": str(post.author),
            "created_at": datetime.utcfromtimestamp(post.created_utc),
            "score": post.score,
            "comments": post.num_comments,
            "url": post.url
        })
    return posts

def create_tables():
    """Create or replace the required tables."""
    try:
        conn = pg8000.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Drop and recreate the reddit_posts table
        cursor.execute("DROP TABLE IF EXISTS reddit_posts;")
        cursor.execute("""
            CREATE TABLE reddit_posts (
                post_id VARCHAR PRIMARY KEY,
                subreddit VARCHAR,
                title TEXT,
                author VARCHAR,
                created_at TIMESTAMP,
                score INT,
                comments INT,
                url TEXT
            );
        """)

        # Drop and recreate the trending_topics table
        cursor.execute("DROP TABLE IF EXISTS trending_topics;")
        cursor.execute("""
            CREATE TABLE trending_topics (
                subreddit VARCHAR,
                common_keywords TEXT,
                top_post_title TEXT,
                top_post_score INT,
                top_post_url TEXT
            );
        """)
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def load_to_postgresql(posts):
    """Load data into the reddit_posts table."""
    try:
        conn = pg8000.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Batch insert data for better performance
        values = [
            (post["post_id"], post["subreddit"], post["title"], post["author"],
             post["created_at"], post["score"], post["comments"], post["url"])
            for post in posts
        ]
        cursor.executemany("""
            INSERT INTO reddit_posts (post_id, subreddit, title, author, created_at, score, comments, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (post_id) DO NOTHING;
        """, values)

        conn.commit()
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def analyze_trending_topics():
    """Analyze trending topics and store the results in the trending_topics table."""
    try:
        conn = pg8000.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Fetch data for analysis
        cursor.execute("SELECT subreddit, title, score, url FROM reddit_posts;")
        rows = cursor.fetchall()

        # Group data by subreddit
        subreddit_data = {}
        for row in rows:
            subreddit, title, score, url = row
            if subreddit not in subreddit_data:
                subreddit_data[subreddit] = []
            subreddit_data[subreddit].append((title, score, url))

        # Analyze and populate trending_topics
        cursor.execute("DELETE FROM trending_topics;")  # Clear previous data
        for subreddit, posts in subreddit_data.items():
            # Top post by score
            top_post = max(posts, key=lambda x: x[1])
            top_post_title, top_post_score, top_post_url = top_post

            # Common keywords
            all_titles = " ".join([post[0] for post in posts])
            words = re.findall(r'\b\w+\b', all_titles.lower())
            common_keywords = ", ".join([word for word, _ in Counter(words).most_common(5)])

            # Insert into trending_topics table
            cursor.execute("""
                INSERT INTO trending_topics (subreddit, common_keywords, top_post_title, top_post_score, top_post_url)
                VALUES (%s, %s, %s, %s, %s);
            """, (subreddit, common_keywords, top_post_title, top_post_score, top_post_url))

        conn.commit()
        print("Trending topics analysis complete.")
    except Exception as e:
        print(f"Error analyzing trending topics: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_tables()
    for subreddit in SUBREDDITS:
        print(f"Fetching data for subreddit: {subreddit}")
        posts = fetch_reddit_data(subreddit, limit=100)
        load_to_postgresql(posts)
        print(f"Data for {subreddit} loaded successfully.")
    analyze_trending_topics()
