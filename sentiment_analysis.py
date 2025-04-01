import pandas as pd # type: ignore
from transformers import pipeline

def analyze_sentiment(input_path="cleaned_comments.csv", output_path="comments_with_sentiment.csv"):
    # 加载预训练情绪分析模型（DistilBERT）
    classifier = pipeline("sentiment-analysis")

    # 加载评论数据
    df = pd.read_csv(input_path)

    # 对每条文本执行情绪预测
    print("Performing sentiment analysis on comments...")
    results = classifier(df["text"].tolist(), truncation=True)

    # 将标签结果加入原数据
    df["label"] = [r["label"] for r in results]
    df["score"] = [round(r["score"], 3) for r in results]

    # 保存结果
    df.to_csv(output_path, index=False)
    print(f"Sentiment analysis complete! Results saved to {output_path}")

if __name__ == "__main__":
    analyze_sentiment()
