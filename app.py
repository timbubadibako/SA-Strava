"""
Interactive Data Analyst Dashboard - Strava Review Sentiment & Aspect Analytics
Standar: Riset Publikasi Ilmiah (Ponytail / Zero-Bloat)
Dijalankan via: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Strava Sentiment & Aspect Intelligence",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan analitik modern & bersih
st.markdown("""
<style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-label {
        font-size: 13px;
        color: #64748b;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("strava_reviews_processed.csv")
    df["at"] = pd.to_datetime(df["at"], errors="coerce")
    return df


df = load_data()

# 2. Sidebar Filters
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/cb/Strava_Logo.svg", width=160)
st.sidebar.title("Filter Parameter")

# Filter Sentimen
sentiment_options = ["Semua"] + list(df["sentiment_label"].unique())
selected_sentiment = st.sidebar.selectbox("Pilih Sentimen", sentiment_options)

# Filter Aspek
aspect_options = ["Semua"] + list(df["aspect_category"].unique())
selected_aspect = st.sidebar.selectbox("Pilih Aspek", aspect_options)

# Filter Rating Bintang
selected_scores = st.sidebar.multiselect(
    "Rating Bintang (Score)",
    options=[1, 2, 3, 4, 5],
    default=[1, 2, 3, 4, 5]
)

# Apply Filter
filtered_df = df.copy()
if selected_sentiment != "Semua":
    filtered_df = filtered_df[filtered_df["sentiment_label"] == selected_sentiment]
if selected_aspect != "Semua":
    filtered_df = filtered_df[filtered_df["aspect_category"] == selected_aspect]
filtered_df = filtered_df[filtered_df["score"].isin(selected_scores)]

# 3. Header & KPI Metrics
st.title("🏃 Strava Review Sentiment & Aspect-Based Analytics")
st.caption("Eksplorasi Data & Komparasi Kinerja Algoritma | Peneliti: Syifa Pajril Yaum")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
total_rev = len(filtered_df)
pos_count = (filtered_df["sentiment_label"] == "POSITIVE").sum()
neu_count = (filtered_df["sentiment_label"] == "NEUTRAL").sum()
neg_count = (filtered_df["sentiment_label"] == "NEGATIVE").sum()
avg_score = filtered_df["score"].mean() if total_rev > 0 else 0

with kpi1:
    st.markdown(f"<div class='metric-card'><div class='metric-value'>{total_rev:,}</div><div class='metric-label'>Total Ulasan Terpilih</div></div>", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"<div class='metric-card'><div class='metric-value'>{avg_score:.2f} ⭐</div><div class='metric-label'>Rata-rata Rating</div></div>", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#10b981;'>{pos_count:,}</div><div class='metric-label'>Sentimen Positif ({pos_count/max(total_rev,1)*100:.1f}%)</div></div>", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#64748b;'>{neu_count:,}</div><div class='metric-label'>Sentimen Netral ({neu_count/max(total_rev,1)*100:.1f}%)</div></div>", unsafe_allow_html=True)
with kpi5:
    st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:#ef4444;'>{neg_count:,}</div><div class='metric-label'>Sentimen Negatif ({neg_count/max(total_rev,1)*100:.1f}%)</div></div>", unsafe_allow_html=True)

st.write("")

# 4. Tab Navigasi Visualisasi
tab_overview, tab_aspect, tab_models, tab_raw = st.tabs([
    "📊 Distribusi Sentimen & Rating",
    "🎯 Analisis 5 Aspek Kunci",
    "🤖 Benchmark Model ML",
    "📑 Eksplorasi Data Mentah"
])

with tab_overview:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Donut Chart Sentimen
        sentiment_counts = filtered_df["sentiment_label"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentimen", "Jumlah"]
        fig_donut = px.pie(
            sentiment_counts,
            values="Jumlah",
            names="Sentimen",
            hole=0.45,
            color="Sentimen",
            color_discrete_map={"POSITIVE": "#10b981", "NEUTRAL": "#94a3b8", "NEGATIVE": "#ef4444"},
            title="Proporsi Polaritas Sentimen"
        )
        fig_donut.update_layout(margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig_donut, use_container_width=True)

    with col2:
        # Bar Chart Rating Bintang
        score_counts = filtered_df["score"].value_counts().sort_index().reset_index()
        score_counts.columns = ["Rating", "Jumlah"]
        fig_bar = px.bar(
            score_counts,
            x="Rating",
            y="Jumlah",
            text="Jumlah",
            color="Rating",
            color_continuous_scale="Viridis",
            title="Distribusi Rating Bintang (1 - 5)"
        )
        fig_bar.update_layout(margin=dict(t=40, b=20, l=20, r=20), xaxis=dict(tickmode="linear", tick0=1, dtick=1))
        st.plotly_chart(fig_bar, use_container_width=True)

with tab_aspect:
    st.subheader("Distribusi Sentimen per Kategori Aspek Aplikasi")
    
    # Cross-tab aspect vs sentiment
    aspect_sentiment = pd.crosstab(
        df[df["aspect_category"] != "GENERAL"]["aspect_category"],
        df["sentiment_label"],
        normalize="index"
    ) * 100

    aspect_sentiment = aspect_sentiment.reindex(["SUBSCRIPTION", "STABILITY", "GPS_TRACKING", "UI_UX", "GAMIFICATION"])
    
    fig_aspect = go.Figure()
    fig_aspect.add_trace(go.Bar(
        y=aspect_sentiment.index,
        x=aspect_sentiment.get("NEGATIVE", 0),
        name="Negatif",
        orientation="h",
        marker=dict(color="#ef4444")
    ))
    fig_aspect.add_trace(go.Bar(
        y=aspect_sentiment.index,
        x=aspect_sentiment.get("NEUTRAL", 0),
        name="Netral",
        orientation="h",
        marker=dict(color="#94a3b8")
    ))
    fig_aspect.add_trace(go.Bar(
        y=aspect_sentiment.index,
        x=aspect_sentiment.get("POSITIVE", 0),
        name="Positif",
        orientation="h",
        marker=dict(color="#10b981")
    ))

    fig_aspect.update_layout(
        barmode="stack",
        xaxis_title="Persentase (%)",
        yaxis_title="Kategori Aspek",
        legend_title="Sentimen",
        margin=dict(t=30, b=40, l=120, r=20),
        height=380
    )
    st.plotly_chart(fig_aspect, use_container_width=True)

    # Key Takeaways
    st.markdown("""
    **💡 Key Findings untuk Pembahasan Jurnal:**
    - **Subscription (Langganan/Paywall)** memiliki sentimen negatif tertinggi (**73.3%**), didominasi keluhan fitur segmen yang dikunci dan harga mahal.
    - **Stability & Baterai** menempati posisi kedua masalah pengguna (**55.8% Negatif**), akibat crash aplikasi dan sinkronisasi jam smartwatch yang terputus.
    - **UI/UX & Gamifikasi** menuai kepuasan tinggi (**>59% Positif**), membuktikan komunitas pelari sangat menyukai fitur kompetisi sosial (KOM/QOM, Kudos).
    """)

with tab_models:
    st.subheader("Hasil Komparasi Kinerja Algoritma (RQ-2)")
    
    benchmark_data = pd.DataFrame([
        {"Model": "IndoBERT (Fine-Tuned)", "Fitur": "Subword Embeddings", "Accuracy": 86.90, "Precision": 67.44, "Recall": 64.77, "Macro F1": 65.55, "Hardware / Time": "RTX 3050 (~15m)"},
        {"Model": "Linear SVM", "Fitur": "TF-IDF (1,2-gram)", "Accuracy": 83.70, "Precision": 63.98, "Recall": 65.39, "Macro F1": 64.62, "Hardware / Time": "CPU (0.11s)"},
        {"Model": "Multinomial Naive Bayes", "Fitur": "TF-IDF (1,2-gram)", "Accuracy": 86.54, "Precision": 88.27, "Recall": 60.88, "Macro F1": 58.90, "Hardware / Time": "CPU (0.02s)"},
        {"Model": "Random Forest", "Fitur": "TF-IDF (1,2-gram)", "Accuracy": 84.76, "Precision": 62.57, "Recall": 60.24, "Macro F1": 58.76, "Hardware / Time": "CPU (0.47s)"}
    ])

    st.dataframe(benchmark_data, use_container_width=True)

    # Chart Komparasi F1-Score & Akurasi
    fig_models = px.bar(
        benchmark_data,
        x="Model",
        y=["Macro F1", "Accuracy"],
        barmode="group",
        color_discrete_sequence=["#f97316", "#3b82f6"],
        title="Komparasi Macro F1-Score vs Accuracy Antar Model"
    )
    fig_models.update_layout(yaxis_title="Skor (%)", margin=dict(t=40, b=20, l=20, r=20))
    st.plotly_chart(fig_models, use_container_width=True)

with tab_raw:
    st.subheader("Data Ulasan Bersih & Hasil Klasifikasi")
    search_keyword = st.text_input("🔍 Cari kata kunci dalam teks ulasan:", "")
    
    display_df = filtered_df[["content", "clean_text", "score", "sentiment_label", "aspect_category"]]
    if search_keyword:
        display_df = display_df[display_df["clean_text"].str.contains(search_keyword.lower(), na=False)]
    
    st.dataframe(display_df.head(100), use_container_width=True)
    st.caption(f"Menampilkan 100 ulasan teratas dari total {len(display_df):,} baris.")
