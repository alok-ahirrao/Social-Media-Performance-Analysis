import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import json
from wordcloud import WordCloud
from textblob import TextBlob
from datetime import datetime
from collections import Counter
from typing import Optional

# Base configuration for LangFlow API
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "837ccfac-bdbc-4d51-9f80-f7ddfb692eeb"
FLOW_ID = "688f35da-8346-4f55-95bc-1f44f55ca564"
APPLICATION_TOKEN = "AstraCS:XGRpeSZzlZQmkpTqMktwQOzK:03eec152f50859e5f9539c017acb505bb74642553f4ef99ff6ac79cc59b255a0"

# Function to run LangFlow flow
def run_flow(message: str, endpoint: str = FLOW_ID, output_type: str = "chat", input_type: str = "chat", tweaks: Optional[dict] = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    
    if tweaks:
        payload["tweaks"] = tweaks

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
        return {"error": str(e)}

# Function to display chat history
def display_chat_history():
    """Display the chat history."""
    for sender, msg in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(msg)

# Function to handle user input for the chatbot
def handle_user_input():
    """Handle user input and call LangFlow API."""
    user_input = st.chat_input("Ask your question here...")

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Call LangFlow API and display response
        with st.chat_message("ai"):
            placeholder = st.empty()
            response = run_flow(message=user_input)
            bot_message = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("data", {}).get("text", "Sorry, no response.")
            placeholder.markdown(bot_message)

            st.session_state.chat_history.append(("ai", bot_message))

# Load Instagram Insights Data
with open("refined_dataset.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Sidebar navigation for chatbot and analysis
st.set_page_config(page_title="Instagram Insights and Chatbot", layout="wide")
st.title("Social Media Performance Analysis and Chatbot")

# Function to render the sidebar with clickable buttons
def render_sidebar():
    # Initialize selected_option with a default value ("Chatbot")
    selected_option = "Chatbot"

    # Create clickable buttons with active button styles
    if st.sidebar.button("Chatbot", key="chatbot"):
        selected_option = "Chatbot"
    
    if st.sidebar.button("Instagram Insights", key="insights"):
        selected_option = "Instagram Insights"

    return selected_option

# Get selected option from the sidebar (default is "Chatbot")
selected_option = render_sidebar()

# Display the selected option in the main area
st.write(f"You selected: {selected_option}")


# Display content based on the selected option
if selected_option == "Chatbot":
    st.sidebar.header("Chatbot")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [("ai", "Hi! I'm your AI assistant. How can I help you today?")]
    
    display_chat_history()
    handle_user_input()

elif selected_option == "Instagram Insights":
    st.sidebar.header("Instagram Insights")
    tab1, tab2, tab3, tab5, tab6, tab8, tab9, tab10 = st.tabs([ 
        "Engagement Trends", "Top Posts", "Content Type Performance", "Engagement Rate Distribution", 
        "Hashtag Analysis", "Posting Time Analysis", "User Engagement Ratios", "Trend-Based Insights"
    ])
    # Function to extract hashtags
    def extract_hashtags(caption):
        if not caption:
            return []
        return [word for word in caption.split() if word.startswith("#")]

    # Extract hashtags column
    df['hashtags'] = df['caption'].apply(extract_hashtags)
    # Engagement Trends Tab
    with tab1:
        st.header("Engagement Trends Over Time")

        # Use the full data without filtering by date
        engagement_data = df[['timestamp', 'likesCount', 'commentsCount', 'engagement_rate']]

        # Convert 'timestamp' to period-based grouping (weekly)
        engagement_data['period'] = engagement_data['timestamp'].dt.to_period('W').dt.start_time

        # Group the data by period and calculate sum of engagement metrics
        engagement_data = engagement_data.groupby('period')[['likesCount', 'commentsCount', 'engagement_rate']].sum()

        # Add 7-day moving averages for likes and comments
        engagement_data['likes_moving_avg_7'] = engagement_data['likesCount'].rolling(window=7, min_periods=1).mean()
        engagement_data['comments_moving_avg_7'] = engagement_data['commentsCount'].rolling(window=7, min_periods=1).mean()

        # Plot the engagement trends
        fig = px.line(
            engagement_data, 
            x=engagement_data.index, 
            y=['likesCount', 'commentsCount', 'likes_moving_avg_7'],
            labels={"value": "Engagement Count", "variable": "Metrics", "period": "Date", "index": "Date"},
            title="Engagement Trends Over Time (Weekly)"
        )
        
        # Update the plot layout for better presentation
        fig.update_layout(
            plot_bgcolor='black', 
            paper_bgcolor='black', 
            font=dict(color='white'), 
            xaxis=dict(showgrid=False, color='white'), 
            yaxis=dict(showgrid=False, color='white'),
            legend=dict(
                title="Metrics", 
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="right", 
                x=1, 
                font=dict(color="white")
            ),
            title_font=dict(size=18, color='white'),
            xaxis_title="Date", 
            yaxis_title="Engagement Count",
            margin=dict(l=20, r=20, t=50, b=20)
        )

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)


    # Top Performing Posts Tab
    with tab2:
        st.header("Top Performing Posts")
        top_posts = df.sort_values(by="engagement_rate", ascending=False).head(10)
        st.table(top_posts[["caption", "likesCount", "commentsCount", "engagement_rate"]])

    # Content Type Performance Tab
    with tab3:
        df['likesCount'] = pd.to_numeric(df['likesCount'], errors='coerce')
        df['commentsCount'] = pd.to_numeric(df['commentsCount'], errors='coerce')
        df['engagement_rate'] = pd.to_numeric(df['engagement_rate'], errors='coerce')
        content_type_data = df.groupby("type")[["likesCount", "commentsCount", "engagement_rate"]].mean()
        st.subheader("Content Type Summary")
        st.dataframe(content_type_data.style.format("{:.2f}"))
        fig = px.bar(
            content_type_data.reset_index(), x="type", y=["likesCount", "commentsCount", "engagement_rate"], 
            barmode="group", labels={"value": "Average Count", "variable": "Metrics", "type": "Content Type"},
            title="Content Type Performance Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        st.header("Engagement Rate Distribution")

        # Filter engagement_rate to ensure it's numeric
        df['engagement_rate'] = pd.to_numeric(df['engagement_rate'], errors='coerce')
        df_filtered = df.dropna(subset=['engagement_rate'])

        # Calculate summary statistics
        mean_rate = df_filtered['engagement_rate'].mean()
        median_rate = df_filtered['engagement_rate'].median()
        max_rate = df_filtered['engagement_rate'].max()
        min_rate = df_filtered['engagement_rate'].min()

        # Add histogram + boxplot using Plotly
        fig = px.histogram(
            df_filtered,
            x="engagement_rate",
            nbins=30,
            title="Engagement Rate Distribution",
            labels={"engagement_rate": "Engagement Rate"},
            marginal="box",  # Adds a boxplot
            hover_data=df_filtered.columns,
        )

        # Customize layout for better readability
        fig.update_layout(
            xaxis_title="Engagement Rate",
            yaxis_title="Frequency",
            title_font_size=20,
            title_x=0.5,  # Center the title
            margin=dict(l=20, r=20, t=50, b=20),
        )

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)

        # Display summary statistics
        st.subheader("Summary Statistics")
        st.write(f"**Mean Engagement Rate:** {mean_rate:.2f}")
        st.write(f"**Median Engagement Rate:** {median_rate:.2f}")
        st.write(f"**Minimum Engagement Rate:** {min_rate:.2f}")
        st.write(f"**Maximum Engagement Rate:** {max_rate:.2f}")

        # Highlight outliers (beyond 1.5 IQR)
        Q1 = df_filtered['engagement_rate'].quantile(0.25)
        Q3 = df_filtered['engagement_rate'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df_filtered[(df_filtered['engagement_rate'] < Q1 - 1.5 * IQR) | (df_filtered['engagement_rate'] > Q3 + 1.5 * IQR)]

        if not outliers.empty:
            st.subheader("Outliers")
            st.write("The following posts have unusually high or low engagement rates:")
            st.dataframe(outliers[['caption', 'engagement_rate']])
        else:
            st.write("No significant outliers detected.")

    with tab6:
        st.header("Hashtag Analysis")

        # Ensure the 'hashtags' column exists
        if 'hashtags' in df.columns:
            # Flatten all hashtags into a single list
            all_hashtags = [hashtag for hashtags in df['hashtags'] for hashtag in hashtags]
            
            # Count the frequency of each hashtag
            hashtag_counts = pd.Series(all_hashtags).value_counts().head(10)

            # Create a bar chart for the top 10 hashtags
            fig = px.bar(
                hashtag_counts,
                x=hashtag_counts.index,
                y=hashtag_counts.values,
                title="Top 10 Hashtags",
                labels={"index": "Hashtag", "value": "Frequency"}
            )

            # Display the plot
            st.plotly_chart(fig, use_container_width=True)

            # Optional: Display the list of top hashtags
            st.write(f"Top Hashtags: {hashtag_counts.index.tolist()}")
        else:
            # Show an error message if the 'hashtags' column is missing
            st.error("The 'hashtags' column is missing from the dataset. Please check your data.")
            
    with tab8:
        st.header("Posting Time Analysis (12-Hour Format)")

        # Ensure 'timestamp' is in datetime format
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        except Exception as e:
            st.error(f"Error parsing timestamps: {e}")
            st.stop()

        # Filter valid rows and ensure engagement_rate is numeric
        df['engagement_rate'] = pd.to_numeric(df['engagement_rate'], errors='coerce')
        df_cleaned = df.dropna(subset=['timestamp', 'engagement_rate'])

        # Extract hour in 12-hour format and AM/PM
        df_cleaned['hour'] = df_cleaned['timestamp'].dt.hour % 12
        df_cleaned['hour'] = df_cleaned['hour'].replace({0: 12})  # Replace 0 with 12 for midnight/noon
        df_cleaned['ampm'] = df_cleaned['timestamp'].dt.strftime('%p')

        # Group by hour and AM/PM, then calculate average engagement rate
        posting_data = df_cleaned.groupby(['hour', 'ampm'])['engagement_rate'].mean().reset_index()

        # Create a combined column for plotting
        posting_data['hour_ampm'] = posting_data['hour'].astype(str) + posting_data['ampm']

        # Check if posting_data is empty
        if posting_data.empty:
            st.warning("No data available for Posting Time Analysis.")
        else:
            # Create a bar chart for 12-hour format
            fig = px.bar(
                posting_data,
                x="hour_ampm",
                y="engagement_rate",
                title="Best Time to Post (12-Hour Format)",
                labels={"hour_ampm": "Hour (12-Hour Format)", "engagement_rate": "Average Engagement Rate"},
                text_auto=True
            )

            # Enhance chart aesthetics
            fig.update_layout(
                xaxis=dict(
                    title="Hour (12-Hour Format)",
                    categoryorder="array",
                    categoryarray=[f"{h}{ap}" for ap in ['AM', 'PM'] for h in range(1, 13)]
                ),
                yaxis=dict(
                    title="Average Engagement Rate"
                ),
                title_x=0.5,
                margin=dict(l=20, r=20, t=50, b=20)
            )

            # Display the chart
            st.plotly_chart(fig, use_container_width=True)

            # Insights
            st.subheader("Insights")
            best_row = posting_data.loc[posting_data['engagement_rate'].idxmax()]
            st.write(f"The best time to post is around **{best_row['hour']}{best_row['ampm']}**, "
                    f"with the highest average engagement rate of **{best_row['engagement_rate']:.2f}**.")

    with tab9:
        st.header("User Engagement Ratios")
        
        # Ensure numeric columns and handle potential division by zero
        df['likesCount'] = pd.to_numeric(df['likesCount'], errors='coerce')
        df['commentsCount'] = pd.to_numeric(df['commentsCount'], errors='coerce')
        df = df.dropna(subset=['likesCount', 'commentsCount'])
        df = df[df['likesCount'] > 0]  # Avoid division by zero
        
        # Calculate the ratio
        df['comments_to_likes'] = df['commentsCount'] / df['likesCount']
        
        # Scatter plot with size representing engagement rate
        fig = px.scatter(
            df,
            x="likesCount",
            y="comments_to_likes",
            size="engagement_rate",
            color="engagement_rate",
            hover_data=["caption"],
            title="Comments to Likes Ratio",
            labels={
                "likesCount": "Likes Count",
                "comments_to_likes": "Comments to Likes Ratio",
                "engagement_rate": "Engagement Rate"
            },
        )
        
        # Customize layout for better aesthetics
        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color='DarkSlateGrey')))
        fig.update_layout(
            title_font_size=20,
            title_x=0.5,
            xaxis=dict(title="Likes Count", showgrid=True),
            yaxis=dict(title="Comments to Likes Ratio", showgrid=True),
            legend_title="Engagement Rate",
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.subheader("Insights")
        avg_ratio = df['comments_to_likes'].mean()
        max_ratio_post = df.loc[df['comments_to_likes'].idxmax()]
        st.write(f"**Average Comments to Likes Ratio:** {avg_ratio:.2f}")
        st.write(f"The post with the highest ratio is:")
        st.write(f"**Caption:** {max_ratio_post['caption']}")
        st.write(f"**Likes Count:** {max_ratio_post['likesCount']}, **Comments Count:** {max_ratio_post['commentsCount']}, **Ratio:** {max_ratio_post['comments_to_likes']:.2f}")

    with tab10:
        st.header("Trend-Based Insights")
        st.write("Analyze trends based on the content of posts and their captions.")
        
        # Extract captions and engagement rates
        trend_data = df[["caption", "engagement_rate"]].dropna()

        # Main Page for user-defined keywords (moved from Sidebar)
        st.subheader("Trend-Based Analysis")
        st.write("Enter keywords or themes to analyze trends:")
        keywords = st.text_input("Keywords (comma-separated)", "fitness, family, love")

        # Process keywords
        if keywords:
            keyword_list = [kw.strip().lower() for kw in keywords.split(",")]
            keyword_pattern = "|".join(keyword_list)

            # Filter data based on keywords
            filtered_data = trend_data[trend_data["caption"].str.contains(keyword_pattern, case=False, na=False)]

            if not filtered_data.empty:
                # Group by keywords and calculate average engagement rate
                keyword_engagement = (
                    filtered_data["caption"]
                    .str.extract(f"({'|'.join(keyword_list)})", expand=False)
                    .str.lower()
                    .value_counts()
                    .reset_index()
                )
                keyword_engagement.columns = ["Keyword", "Frequency"]
                keyword_engagement["Average Engagement Rate"] = keyword_engagement["Keyword"].apply(
                    lambda x: filtered_data[filtered_data["caption"].str.contains(x, case=False)]["engagement_rate"].mean()
                )

                # Display results
                st.subheader("Keyword Performance")
                st.dataframe(keyword_engagement)

                # Visualize the trends
                fig = px.bar(
                    keyword_engagement,
                    x="Keyword",
                    y="Average Engagement Rate",
                    color="Frequency",
                    text="Frequency",
                    title="Trend-Based Engagement Insights",
                    labels={"Keyword": "Keyword/Theme", "Average Engagement Rate": "Avg. Engagement Rate"},
                )
                fig.update_layout(xaxis_title="Keyword/Theme", yaxis_title="Avg. Engagement Rate")
                st.plotly_chart(fig, use_container_width=True)

                # Insights
                st.subheader("Insights")
                best_keyword = keyword_engagement.loc[keyword_engagement["Average Engagement Rate"].idxmax()]
                st.write(
                    f"The most engaging trend is **'{best_keyword['Keyword']}'**, "
                    f"with an average engagement rate of **{best_keyword['Average Engagement Rate']:.2f}**."
                )
            else:
                st.warning("No captions matched the specified keywords. Try different keywords.")
        else:
            st.info("Enter keywords in the main section to start analyzing trends.")

        