-- Drop tables if they exist
DROP TABLE IF EXISTS reddit_posts CASCADE;
DROP TABLE IF EXISTS trending_topics CASCADE;

-- Create reddit_posts table
CREATE TABLE IF NOT EXISTS reddit_posts (
    post_id VARCHAR PRIMARY KEY,
    subreddit VARCHAR NOT NULL,
    title TEXT NOT NULL,
    author VARCHAR,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    score INT DEFAULT 0,
    comments INT DEFAULT 0,
    url TEXT
);

-- Create trending_topics table
CREATE TABLE IF NOT EXISTS trending_topics (
    subreddit VARCHAR NOT NULL,
    common_keywords TEXT,
    top_post_title TEXT,
    top_post_score INT DEFAULT 0,
    top_post_url TEXT
);
