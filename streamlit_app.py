import streamlit as st # type: ignore
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
from wordcloud import WordCloud # type: ignore

# 1. 加载数据
@st.cache_data
def load_data(path="comments_with_sentiment2.csv"):
    return pd.read_csv(path)

df = load_data()

# 2. 页面标题
st.title("Realtime Sentiment Analysis Dashboard")
st.markdown("Built with HuggingFace Transformers + Streamlit")

# 3. 情绪分布图（饼图 + 条形图）
st.subheader("Sentiment Distribution")
sentiment_counts = df["label"].value_counts().sort_index()

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(sentiment_counts)

with col2:
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=["#ff6b6b", "#feca57", "#1dd1a1"])
    ax.axis("equal")
    st.pyplot(fig)

# 4. 词云图
st.subheader("Top Keywords WordCloud")
text_all = " ".join(df["text"].tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_all)
fig_wc, ax_wc = plt.subplots()
ax_wc.imshow(wordcloud, interpolation="bilinear")
ax_wc.axis("off")
st.pyplot(fig_wc)

# 5. 评论浏览器
st.subheader("Comment Browser")
filter_option = st.selectbox("Filter by Sentiment", options=["All", "Positive", "Neutral", "Negative"])

if filter_option != "All":
    filtered_df = df[df["label"] == filter_option]
else:
    filtered_df = df

st.dataframe(filtered_df[["text", "label", "score"]].reset_index(drop=True))
