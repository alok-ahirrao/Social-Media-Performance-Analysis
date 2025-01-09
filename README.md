# Social Media Performance Analysis for Hackathon Submission  

## Overview  
This project is designed to address the pre-hackathon assignment for the Level Supermind Hackathon. It focuses on building an analytics module to evaluate real-world social media performance data, leveraging LangFlow for GPT-based insights and DataStax Astra DB for data storage and querying.

---

## Demo Output  

![Output Demo](output.gif)  

---

## Objective  
Develop a streamlined solution to analyze social media engagement data, generate insights, and integrate a chatbot for user interaction. The assignment includes the following key deliverables:  

### Data Storage:  
- Store real-world engagement data from Instagram in DataStax Astra DB.  

### Performance Analysis:  
- Use LangFlow workflows to process real data and provide average engagement metrics for different post types (e.g., images, videos, carousels).  

### GPT Integration:  
- Employ GPT models via LangFlow to generate actionable insights based on real-world trends and patterns.  

---

## Real Data Integration  
We enhanced the realism and relevance of this project by utilizing real-world Instagram engagement data from the official account of Indian cricketer Virat Kohli. The dataset includes metrics such as:  

- **Post Type**: Images, videos, and carousels.  
- **Engagement Metrics**: Likes, comments, and engagement rates.  
- **Captions**: Actual captions used in posts.  
- **Timestamps**: Real posting dates for time-based analysis.  

**Example entry**:  
```json
{
    "id": 1667540652629609216,
    "type": "Image",
    "caption": "Today we have promised each other to be bound in love...",
    "likesCount": 4425400,
    "commentsCount": 128798,
    "engagement_rate": 4554198,
    "timestamp": 1513006358000,
    "ownerUsername": "virat.kohli"
}
```

By leveraging authentic engagement data, we ensure the analysis is accurate, practical, and directly applicable to real-world scenarios.  

---

## Features  

### Instagram Insights  
- **Engagement Trends**: Visualize trends in likes, comments, and engagement rates over time using real data.  
- **Content-Type Analysis**: Evaluate performance based on post types (e.g., image vs. video) and generate actionable comparisons.  
- **Hashtag Analysis**: Identify and analyze the effectiveness of top-performing hashtags.  
- **Posting Time Analysis**: Pinpoint optimal times for posting.  
- **User Engagement Ratios**: Explore the relationship between likes and comments.  
- **Trend-Based Insights**: Analyze thematic trends based on captions and engagement rates.  

### Chatbot Integration  
- AI-powered chatbot to handle user queries about social media trends and performance.  
- Integrated with LangFlow API for natural language responses and insights.  

---

## Tools Used  
- **LangFlow**: Workflow creation and GPT integration for generating insights.  
- **DataStax Astra DB**: Cloud database used to store and query the engagement data.  
- **Streamlit**: Interactive web application for data visualization and chatbot interaction.  
- **Plotly**: For dynamic data visualizations such as line charts, histograms, and scatter plots.  

---

## Installation  

### Prerequisites  
- Python 3.7+  
- Required libraries:  
  ```bash
  pip install -r requirements.txt
  ```  

### Steps  
1. Clone this repository:  
   ```bash
   git clone https://github.com/alok-ahirrao/Social-Media-Performance-Analysis.git
   ```  
2. Install the dependencies.  
3. Place the dataset (`refined_dataset.json`) in the project root directory.  
4. Run the Streamlit app:  
   ```bash
   streamlit run app.py
   ```  

---

## Functionality  

### Chatbot Workflow  
- Accepts user input and queries the LangFlow API.  
- Provides insights about the social media dataset or assists with other queries.  

### Insights Tabs  
- **Engagement Trends**: Analyze likes, comments, and engagement over time using authentic data.  
- **Top Posts**: View the top 10 posts sorted by engagement rates.  
- **Hashtag Analysis**: Discover the most frequently used and effective hashtags.  
- **Content-Type Analysis**: Compare average performance metrics (likes, comments, engagement) across content types.  
- **Posting Time Analysis**: Identify the best times to post for maximum engagement.  

---

## LangFlow API Integration  

### Workflow  
- **Input**: Post type or query.  
- **Output**: Average metrics or insights.  
- **API**: `run_flow()` function integrates LangFlow to fetch and process results.  

**Example Insight**:  
- "Carousel posts have 20% higher engagement than static posts."  
- "Reels drive 2x more comments compared to other formats."  

---

## Real-World Impact  
By using real data from Virat Kohli's Instagram account, the project ensures:  
- **Practical Application**: Insights generated are based on real-world scenarios.  
- **Enhanced Credibility**: Demonstrates the ability to process and analyze authentic datasets.  
- **Improved Engagement**: Generates relevant, actionable insights for professionals and brands.  

---

## Submission Links  

- **Streamlit App**: [AstraVision Streamlit Dashboard](https://astravision.streamlit.app)  
- **YouTube Demo Video**: [Watch the Project Demo](https://youtu.be/hQ28vmPKF-E)  
- **FindCoder Project Page**: [FindCoder Submission](https://www.findcoder.io/projects/social-media-insights-astravision/67800e128015401a98a17289)  

---

## File Structure  
```plaintext
.
├── app.py                # Main application
├── refined_dataset.json  # Social media data
├── requirements.txt      # Dependencies
├── output.gif            # Demo output
├── README.md             # Documentation
```

---

## Acknowledgments  
- **LangFlow**  
- **DataStax Astra DB**  
- **Streamlit**  

For more details, visit the official hackathon page: **Level Supermind Hackathon**.  

---

## License  
**Copyright (c) 2025, Alok Ahirrao**  

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.  
You may use and modify this project for personal or educational purposes, but commercial use is prohibited without explicit permission.  

For more details, see the LICENSE file or contact [alokahirrao.ai@gmail.com](mailto:alokahirrao.ai@gmail.com).  

--- 

This updated README includes all the necessary links and references the `output.gif` file for showcasing the project output. Let me know if further edits are needed!
