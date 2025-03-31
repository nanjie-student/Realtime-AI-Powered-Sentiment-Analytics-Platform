import praw
import json
import time
from langdetect import detect, LangDetectException # type: ignore

#Reddit API 配置
reddit = praw.Reddit(
    client_id="SYEbiHWSQrgX-XTP3KTL0g",
    client_secret="6YAZsds05TkLiZ0KjGbdUhKoX9vxhQ",
    user_agent="script:sentiment:v1.0 (by u/testPractice)"
)
# subReddit设置
subreddit = reddit.subreddit("technology")

#输出文件& 限制
output_file = "reddit_comments_cleaned.json"
max_comments = 50
comment_count = 0

#过滤数据       
def is_valid_comment(body):
    """简单过滤规则"""
    if not body or body.lower() in ['[deleted]', '[removed]']:
        return False
    if len(body.strip()) < 10:
        return False
    try:
        if detect(body) != "en":  # 只保留英文
            return False
    except LangDetectException:
        return False
    return True

# 开始抓取评论
with open(output_file, "a", encoding="utf-8") as f:
    #print("开始监听 Reddit 评论流（Ctrl+C 可中止）...")
    for comment in subreddit.stream.comments(skip_existing=True):
        body = comment.body

        if is_valid_comment(body):
            data = {
                "id": comment.id,
                "type": "comment",
                "subreddit": comment.subreddit.display_name,
                "body": body,
                "score": comment.score,
                "created_utc": comment.created_utc,
                "link_id": comment.link_id,
                "parent_id": comment.parent_id,
                "author": str(comment.author)
            }

            json.dump(data, f)
            f.write("\n")
            print(f"Saved comment {comment.id}: {body[:80]}...")
        
        time.sleep(0.3)  # 避免触发 Reddit API 限流
