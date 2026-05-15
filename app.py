import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="WhatsApp Analytics Dashboard",
    page_icon="💬",
    layout="wide"
)

# ---------------- WHATSAPP STYLE UI ---------------- #

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

.main {
    background: linear-gradient(to right, #f0f2f5, #d9fdd3);
}

h1 {
    color: #075E54;
    font-weight: 800;
}

h2, h3 {
    color: #128C7E;
}

section[data-testid="stSidebar"] {
    background-color: #075E54;
}

section[data-testid="stSidebar"] * {
    color: white;
}

.stButton>button {
    background-color: #25D366;
    color: white;
    border-radius: 15px;
    border: none;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #128C7E;
    color: white;
}

[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.7);
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
}

[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown("""
<h1 style='text-align:center;'>
💬 WhatsApp Chat Analytics Dashboard
</h1>

<p style='text-align:center; font-size:18px; color:#555;'>
Analyze conversations, activity trends, emojis, word usage & engagement insights
</p>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("📂 Upload Chat File")

st.sidebar.info(
    "Upload your exported WhatsApp .txt chat file to begin analysis."
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.sidebar.file_uploader(
    "Choose WhatsApp Chat File"
)

if uploaded_file is not None:

    st.success("✅ Chat file uploaded successfully!")

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # ---------------- LOADING ---------------- #

    with st.spinner("Analyzing chat data..."):

        df = preprocessor.preprocess(data)

    # ---------------- RAW DATA ---------------- #

    with st.expander("📄 Show Raw Chat Data"):
        st.dataframe(df)

    # ---------------- USER LIST ---------------- #

    user_list = df['user'].unique().tolist()

    if 'Group_notification' in user_list:
        user_list.remove('Group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "👤 Show Analysis W.R.T",
        user_list
    )

    # ---------------- ANALYSIS BUTTON ---------------- #

    if st.sidebar.button("🚀 Show Analysis"):

        # ---------------- FETCH STATS ---------------- #

        num_messages, words, num_media_msg, num_links = helper.fetch_stats(
            selected_user,
            df
        )

        # ---------------- TOP STATS ---------------- #

        st.title("📊 Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("💬 Total Messages", num_messages)

        with col2:
            st.metric("📝 Total Words", words)

        with col3:
            st.metric("🖼️ Media Shared", num_media_msg)

        with col4:
            st.metric("🔗 Links Shared", num_links)

        # ---------------- MOST ACTIVE USERS ---------------- #

        if selected_user == 'Overall':

            st.title("🔥 Most Active Users")

            x, new_df = helper.most_active_user(df)

            col1, col2 = st.columns(2)

            with col1:

                fig, ax = plt.subplots()

                ax.bar(
                    x.index,
                    x.values,
                    color='#25D366'
                )

                plt.xticks(rotation='vertical')

                st.pyplot(fig)

            with col2:

                st.dataframe(new_df)

        # ---------------- MONTHLY TIMELINE ---------------- #

        st.title("📅 Monthly Timeline")

        timeline = helper.monthly_timeline(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.plot(
            timeline['time'],
            timeline['message'],
            color='#128C7E',
            linewidth=3
        )

        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # ---------------- DAILY TIMELINE ---------------- #

        st.title("📆 Daily Timeline")

        daily_timeline = helper.daily_timeline(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.plot(
            daily_timeline['only_date'],
            daily_timeline['message'],
            color='#075E54',
            linewidth=3
        )

        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # ---------------- ACTIVITY MAP ---------------- #

        st.title("📌 Activity Insights")

        col1, col2 = st.columns(2)

        with col1:

            st.header("📅 Most Busy Day")

            busy_day = helper.week_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots()

            ax.bar(
                busy_day.index,
                busy_day.values,
                color='#34B7F1'
            )

            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        with col2:

            st.header("📆 Most Busy Month")

            busy_month = helper.month_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots()

            ax.bar(
                busy_month.index,
                busy_month.values,
                color='#25D366'
            )

            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        # ---------------- HEATMAP ---------------- #

        st.title("🔥 Weekly Activity Heatmap")

        user_heatmap = helper.activity_heatmap(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        sns.heatmap(
            user_heatmap,
            ax=ax,
            cmap="Greens"
        )

        st.pyplot(fig)

        # ---------------- WORDCLOUD ---------------- #

        st.title("☁️ WordCloud")

        df_wc = helper.create_wordcloud(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.imshow(df_wc)

        ax.axis("off")

        st.pyplot(fig)

        # ---------------- MOST COMMON WORDS ---------------- #

        st.title("📝 Most Common Words")

        most_common_df = helper.most_common_words(
            selected_user,
            df
        )

        fig, ax = plt.subplots()

        ax.barh(
            most_common_df[0],
            most_common_df[1],
            color='#128C7E'
        )

        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        # ---------------- EMOJI ANALYSIS ---------------- #

        emoji_df = helper.emoji_helper(
            selected_user,
            df
        )

        st.title("😀 Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.dataframe(emoji_df)

        with col2:

            fig, ax = plt.subplots()

            ax.pie(
                emoji_df[1].head(),
                labels=emoji_df[0].head(),
                autopct="%0.2f"
            )

            st.pyplot(fig)

# ---------------- FOOTER ---------------- #

st.markdown("---")

st.markdown(
    """
    <center>
    💚 Developed by Yash Nada
    </center>
    """,
    unsafe_allow_html=True
)