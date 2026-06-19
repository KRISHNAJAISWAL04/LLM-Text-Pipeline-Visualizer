import html
import re

import plotly.express as px
import streamlit as st


st.set_page_config(page_title="LLM Text Pipeline Visualizer", layout="wide")
st.title("LLM Text Pipeline Visualizer")
st.caption("Visualize sentence extraction, sliding-window chunks, overlaps, and tokenization.")


@st.cache_data(show_spinner=False)
def split_sentences(text: str) -> list[str]:
    pattern = re.compile(r"(?<=[.!?])\s+")
    return [sentence.strip() for sentence in pattern.split(text) if sentence.strip()]


st.sidebar.header("Chunking Configuration")

chunk_size = st.sidebar.slider(
    "Max Chunk Size (in Words)",
    min_value=5,
    max_value=100,
    value=20,
    step=5,
    help="The maximum number of words allowed inside a single chunk.",
)

chunk_overlap = st.sidebar.slider(
    "Chunk Overlap (in Words)",
    min_value=0,
    max_value=50,
    value=5,
    step=1,
    help="How many words should be carried over from the previous chunk.",
)

if chunk_overlap >= chunk_size:
    st.sidebar.error("Overlap must be strictly smaller than the chunk size.")
    st.stop()

user_text = st.text_area(
    "Enter your source text here:",
    value=(
        "Artificial Intelligence is changing the world. Machine learning models analyze huge amounts of data. "
        "Deep learning simulates the human brain's neural networks. Tokenization is the foundational step "
        "where sentences turn into pieces. Pieces turn into vectors. Vectors turn into intelligence."
    ),
    height=150,
)

if user_text.strip():
    sentences = split_sentences(user_text)
    words = user_text.split()
    chunks = []

    start_idx = 0
    step_size = chunk_size - chunk_overlap
    while start_idx < len(words):
        end_idx = start_idx + chunk_size
        chunk_words = words[start_idx:end_idx]
        chunks.append(" ".join(chunk_words))
        start_idx += step_size

    token_strings = re.findall(r"\w+|[^\w\s]", user_text, re.UNICODE)

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Sentence Extraction",
            "Custom Overlap Chunks",
            "Tokenization Process",
            "Analytics Dashboard",
        ]
    )

    with tab1:
        st.subheader("Extracted Sentences")
        for idx, sentence in enumerate(sentences):
            st.info(f"**Sentence {idx + 1}:** {sentence}")

    with tab2:
        st.subheader("Generated Sliding Window Chunks")
        st.write("Notice how ending phrases overlap into the beginning of later chunks:")
        for idx, chunk in enumerate(chunks):
            st.success(f"**Chunk {idx + 1} ({len(chunk.split())} words):** {chunk}")

    with tab3:
        st.subheader("Tokenized View")
        st.write("Each colored box represents an individual token read by the LLM model:")

        colors = ["#FFD1DC", "#C1FFC1", "#D6F5D6", "#D1E8FF", "#E6E6FA", "#FFE4E1"]
        html_tokens = ""
        for idx, token in enumerate(token_strings):
            color = colors[idx % len(colors)]
            display_token = html.escape(token).replace(" ", "&nbsp;").replace("\n", "\\n")
            html_tokens += (
                f'<span style="background-color: {color}; padding: 2px 6px; margin: 2px; '
                f'border-radius: 4px; display: inline-block; font-family: monospace; '
                f'color: black;">{display_token}</span>'
            )

        st.markdown(html_tokens, unsafe_allow_html=True)

    with tab4:
        st.subheader("Real-Time Pipeline Metrics")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Character Count", len(user_text))
        col2.metric("Total Sentences", len(sentences))
        col3.metric("Total Chunks", len(chunks))
        col4.metric("Total Tokens", len(token_strings))

        st.subheader("Structure Distribution Breakdown")

        chunk_lengths = [len(chunk.split()) for chunk in chunks]
        chunk_labels = [f"Chunk {idx + 1}" for idx in range(len(chunks))]

        fig = px.bar(
            x=chunk_labels,
            y=chunk_lengths,
            title="Words Per Sliding Window Chunk",
            color=chunk_lengths,
            labels={"x": "Chunk Index", "y": "Word Count"},
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please type or paste some text above to start the pipeline validation.")
