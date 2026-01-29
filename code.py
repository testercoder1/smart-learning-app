import praw
from collections import Counter
import re

# -------------------------
# REDDIT API CONFIG
# -------------------------

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    user_agent="StudySummaryBot v1.0 by YOUR_USERNAME"
)

# -------------------------
# SETTINGS
# -------------------------

SUBREDDITS = ["learnprogramming", "AskReddit", "explainlikeimfive", "science"]
POST_LIMIT = 5
COMMENT_LIMIT = 20
MIN_UPVOTES = 5


# -------------------------
# TEXT CLEANER
# -------------------------

def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# -------------------------
# FETCH DISCUSSIONS
# -------------------------

def fetch_reddit_answers(topic):
    collected_answers = []

    for sub in SUBREDDITS:
        subreddit = reddit.subreddit(sub)
        results = subreddit.search(topic, limit=POST_LIMIT)

        for post in results:
            post.comments.replace_more(limit=0)

            for comment in post.comments.list():
                if comment.score >= MIN_UPVOTES:
                    collected_answers.append({
                        "text": clean_text(comment.body),
                        "score": comment.score,
                        "author": str(comment.author),
                        "subreddit": sub
                    })

    return collected_answers


# -------------------------
# RANK HIGH QUALITY ANSWERS
# -------------------------

def rank_answers(answers):
    sorted_answers = sorted(
        answers,
        key=lambda x: x["score"],
        reverse=True
    )

    return sorted_answers[:10]


# -------------------------
# SIMPLE SUMMARY GENERATOR
# -------------------------

def generate_summary(top_answers):
    notes = []

    for idx, ans in enumerate(top_answers, start=1):
        short_text = ans["text"][:300] + "..."
        notes.append(
            f"{idx}. ({ans['score']} upvotes | r/{ans['subreddit']})\n{short_text}\n"
        )

    return "\n".join(notes)


# -------------------------
# MAIN BOT FUNCTION
# -------------------------

def run_bot():
    print("\n--- REDDIT STUDY BOT ---")
    topic = input("Enter topic or question: ")

    print("\nFetching Reddit discussions...")
    answers = fetch_reddit_answers(topic)

    if not answers:
        print("No useful answers found.")
        return

    print("Ranking high-
