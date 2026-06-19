import streamlit as st
import re
import tiktoken
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="LLM Text Pipeline Visualizer", layout="wide")
st.title("🔹 LLM Text Pipeline Visualizer")
st.caption("Visualize text extraction, custom sliding chunk sizes, overlaps, and tokenization.")

# Simple sentence splitting without spaCy
@st.cache_resource
def split_sentences(text: str) -> list[str]:
    pattern = re.compile(r'(?<=[.!?])\s+')
    return [sentence.strip() for sentence in pattern.split(text) if sentence.strip()]

# Sidebar Configurations
st.sidebar.header("⚙️ Chunking Configuration")

chunk_size = st.sidebar.slider(
    "Max Chunk Size (in Words)", 
    min_value=5, 
    max_value=100, 
    value=20, 
    step=5,
    help="The maximum number of words allowed inside a single chunk."
)

chunk_overlap = st.sidebar.slider(
    "Chunk Overlap (in Words)", 
    min_value=0, 
    max_value=50, 
    value=5, 
    step=1,
    help="How many words should be carried over from the end of the previous chunk to the start of the next."
)

# Guard rail validation to ensure overlap is strictly less than size
if chunk_overlap >= chunk_size:
    st.sidebar.error("❌ Error: Overlap must be strictly smaller than the Chunk Size!")
    st.stop()

# User Input Section
user_text = st.text_area(
    "Enter your source text here:",
    value="Artificial Intelligence is changing the world. Machine learning models analyze huge amounts of data. "
          "Deep learning simulates the human brain's neural networks. Tokenization is the foundational step "
          "where sentences turn into pieces. Pieces turn into vectors. Vectors turn into intelligence.",
    height=150
)

if user_text.strip():
    # ---------------------------------------------------------
    # 1. SENTENCE EXTRACTION
    # ---------------------------------------------------------
    sentences = split_sentences(user_text)
    
    # ---------------------------------------------------------
    # 2. CUSTOM CHUNKING WITH OVERLAP (Sliding Window over Words)
    # ---------------------------------------------------------
    words = user_text.split()
    chunks = []
    
    start_idx = 0
    while start_idx < len(words):
        # Determine the window end bounds
        end_idx = start_idx + chunk_size
        chunk_words = words[start_idx:end_idx]
        chunks.append(" ".join(chunk_words))
        
        # Move forward by (chunk_size - chunk_overlap)
        start_idx += (chunk_size - chunk_overlap)
        
        # Infinite loop brake guard
        if chunk_size <= chunk_overlap:
            break

    # ---------------------------------------------------------
    # 3. TOKENIZATION PROCESS
    # ---------------------------------------------------------
    encoder = tiktoken.get_encoding("cl100k_base") 
    all_tokens_raw = encoder.encode(user_text)
    token_strings = [encoder.decode([t]) for t in all_tokens_raw]

    # Create UI Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Sentence Extraction", 
        "🧩 Custom Overlap Chunks", 
        "🎟️ Tokenization Process", 
        "📊 Analytics Dashboard"
    ])

    # TAB 1: SENTENCES
    with tab1:
        st.subheader("Extracted Sentences")
        for idx, sentence in enumerate(sentences):
            st.info(f"**Sentence {idx + 1}:** {sentence}")

    # TAB 2: CHUNKS WITH OVERLAP VISUALIZATION
    with tab2:
        st.subheader("Generated Sliding Window Chunks")
        st.write("Notice how the ending phrases overlap into the beginning of subsequent blocks:")
        for idx, chunk in enumerate(chunks):
            st.success(f"**Chunk {idx + 1} (Size: {len(chunk.split())} words):** {chunk}")

    # TAB 3: TOKENIZATION
    with tab3:
        st.subheader("Tokenized View")
        st.write("Each colored box represents an individual token read by the LLM model:")
        
        html_tokens = ""
        colors = ["#FFD1DC", "#C1FFC1", "#D6F5D6", "#D1E8FF", "#E6E6FA", "#FFE4E1"]
        for idx, token in enumerate(token_strings):
            color = colors[idx % len(colors)]
            display_token = token.replace(" ", "&nbsp;").replace("\n", "↵")
            html_tokens += f'<span style="background-color: {color}; padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline-block; font-family: monospace; color: black;">{display_token}</span>'
        
        st.markdown(html_tokens, unsafe_allow_html=True)

    # TAB 4: REAL-TIME ANALYTICS
    with tab4:
        st.subheader("Real-Time Pipeline Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Character Count", len(user_text))
        col2.metric("Total Sentences", len(sentences))
        col3.metric("Total Chunks (With Overlap)", len(chunks))
        col4.metric("Total Tokens", len(all_tokens_raw))

        st.subheader("Structure Distribution Breakdown")
        
        chunk_lengths = [len(c.split()) for c in chunks]
        df_chunks = pd.DataFrame({
            "Chunk Index": [f"Chunk {i+1}" for i in range(len(chunks))],
            "Word Count": chunk_lengths
        })
        
        fig = px.bar(df_chunks, x="Chunk Index", y="Word Count", title="Words Per Sliding Window Chunk", color="Word Count")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please type or paste some text above to start the pipeline validation.")
