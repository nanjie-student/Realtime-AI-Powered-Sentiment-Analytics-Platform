from kafka import KafkaProducer # type: ignore
import json
import time

# Kafka 配置（注意：这是连接 Docker 启动的 Kafka）
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # 如果你把 producer 放进 Docker，记得用 kafka:9092
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'reddit-comments'
input_file = 'reddit_comments_cleaned.json'  # 你之前保存的 JSON 文件

# 逐行读取并发送评论数据
with open(input_file, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        try:
            data = json.loads(line.strip())  # 加 strip 避免换行
            producer.send(topic_name, value=data)
            print(f"[{i+1}] Sent: {data['body'][:80]}...")
            time.sleep(0.5)  # 模拟实时发送
        except json.JSONDecodeError as e:
            print(f"跳过无效 JSON 行: {e}")
        except Exception as e:
            print(f"发送失败: {e}")

producer.flush()
print("所有评论已发送完毕！")
