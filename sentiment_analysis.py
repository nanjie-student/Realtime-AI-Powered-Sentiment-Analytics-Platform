import pandas as pd # type: ignore
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def analyze_sentiment(input_path="cleaned_comments.csv", output_path="comments_with_sentiment2.csv"):
    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    # 读取清洗后的评论
    df = pd.read_csv(input_path)

    # 对所有文本执行推理
    print("Running 3-class sentiment analysis...")
    results = classifier(df["text"].tolist(), truncation=True)

    # 解码标签
    label_map = {
        "LABEL_0": "Negative",
        "LABEL_1": "Neutral",
        "LABEL_2": "Positive"
    }

    df["label"] = [label_map[r["label"]] for r in results]
    df["score"] = [round(r["score"], 3) for r in results]

    df.to_csv(output_path, index=False)
    print(f"Done. Results saved to {output_path}")

if __name__ == "__main__":
    analyze_sentiment()
