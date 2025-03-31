from kafka import KafkaConsumer
from transformers import pipeline
import json

# 1. 加载情绪分析模型
print("正在加载情绪分析模型(distilbert-base-uncased-finetuned-sst-2-english)...")
classifier = pipeline("sentiment-analysis")

# 2. Kafka Consumer 配置
consumer = KafkaConsumer(
    'reddit-comments',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='sentiment-consumer-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("正在监听 Kafka 评论流...")

# 3. 实时读取 Kafka 消息并情绪分析
for message in consumer:
    comment = message.value
    text = comment.get("body", "")
    
    if len(text.strip()) == 0:
        continue

    # 分析情绪
    result = classifier(text[:512])[0]  # 限制512字符内
    label = result['label']
    score = result['score']

    print(f"\n评论内容: {text[:100]}...")
    print(f"情绪判断: {label} ({score:.2f})")

    



