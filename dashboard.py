
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(page_title="Trauma Translation Dashboard", layout="wide")

st.title("🛡️ Trauma Translation Ethics Dashboard")
st.markdown("""
This dashboard evaluates how well AI models adhere to **Witness-Bearing Ethics** in translation. 
The goal is to avoid 'Beautification' and preserve the raw, fragmented nature of trauma.
""")

# Load data
df = pd.read_csv('evaluation_data.csv')

# --- Sidebar Metrics ---
st.sidebar.header("Global Statistics")
avg_score = df['Score'].mean()
pass_rate = df['Passed'].mean() * 100
st.sidebar.metric("Average Ethics Score", f"{avg_score:.2f}")
st.sidebar.metric("Overall Pass Rate", f"{pass_rate:.1f}%")

# --- Overview Row ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Performance by Model")
    model_perf = df.groupby('Model')['Score'].mean().reset_index().sort_values('Score', ascending=False)
    fig_model = px.bar(model_perf, x='Model', y='Score', color='Score', 
                       color_continuous_scale='RdYlGn', title="Avg Ethics Score per Provider")
    st.plotly_chart(fig_model, use_container_width=True)

with col2:
    st.subheader("Pass/Fail Distribution")
    fig_pie = px.pie(df, names='Passed', color='Passed', 
                     color_discrete_map={True: '#2ecc71', False: '#e74c3c'},
                     title="Percentage of Successfully 'Witnessed' Translations")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- Insight Section: What affected the score? ---
st.divider()
st.header("🔍 Deep Insights: What causes failure?")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Length Expansion (Beautification Proxy)")
    st.markdown("Higher ratios suggest the model is 'adding' words to clarify or soften the text.")
    fig_scatter = px.scatter(df, x='Source_WordCount', y='Output_WordCount', color='Passed',
                             hover_data=['Model'], size='Length_Ratio',
                             title="Source vs Output Word Count")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col4:
    st.subheader("Common Feedback Keywords")
    # Simple extraction of failure keywords from 'Feedback'
    all_feedback = " ".join(df[df['Passed'] == False]['Feedback'].fillna('').tolist()).lower()
    keywords = ['beautify', 'smooth', 'fluent', 'added', 'formatting', 'guillemets', 'soften', 'punctuation']
    counts = {word: all_feedback.count(word) for word in keywords}
    kw_df = pd.DataFrame(list(counts.items()), columns=['Keyword', 'Count']).sort_values('Count', ascending=False)
    
    fig_kw = px.bar(kw_df, x='Keyword', y='Count', title="Why do models fail?")
    st.plotly_chart(fig_kw, use_container_width=True)

# --- Detailed Result Explorer ---
st.divider()
st.header("📋 Detailed Result Explorer")
selected_model = st.selectbox("Filter by Model", options=['All'] + list(df['Model'].unique()))

display_df = df if selected_model == 'All' else df[df['Model'] == selected_model]

for idx, row in display_df.iterrows():
    with st.expander(f"Case {idx+1}: {row['Model']} | Score: {row['Score']} | Passed: {row['Passed']}"):
        c1, c2 = st.columns(2)
        with c1:
            st.info("**Source (English)**")
            st.text(row['Source'])
        with c2:
            st.success("**Output (Arabic/Hybrid)**")
            st.text(row['Output'])
        st.warning(f"**Judge Feedback:** {row['Feedback']}")

st.markdown("""
### Key Takeaways for Ethics Improvement:
1. **The Politeness Trap:** Models with high word-count expansion usually fail the 'Coldness' requirement.
2. **Formatting Fragility:** If the score is high (e.g. 0.85) but 'Passed' is False, check for missing « » or —.
3. **Fluency vs Fidelity:** 'Fluent' Arabic is often a sign of ethical failure in trauma testimony.
""")
