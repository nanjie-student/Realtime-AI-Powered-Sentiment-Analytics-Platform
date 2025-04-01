import pandas as pd # type: ignore
import json
import re

def clean_text(text):
    # 去除链接、多余空格、换行、标点统一
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def load_and_clean_ndjson(input_path="reddit_comments_cleaned.json", output_path="cleaned_comments.csv", max_rows=100):
    data = []
    with open(input_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= max_rows:  # 限制最多加载 max_rows 条评论
                break
            try:
                item = json.loads(line)
                body = item.get("body", "").strip().lower()
                if body and body not in ["[deleted]", "[removed]"]:
                    data.append({
                        "id": item.get("id"),
                        "text": clean_text(body),
                        "subreddit": item.get("subreddit"),
                        "timestamp": item.get("created_utc"),
                        "author": item.get("author")
                    })
            except json.JSONDecodeError:
                continue

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Cleaned {len(df)} entries saved to {output_path}")

if __name__ == "__main__":
    load_and_clean_ndjson()
