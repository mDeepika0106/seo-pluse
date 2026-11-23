
import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/audit"


st.set_page_config(
    page_title="SEO Pulse",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Marketing Intelligence Assistant")
st.subheader("Website SEO Audit & AI Insights")

st.write(
    "Enter a website URL to analyze its SEO performance "
    "and receive AI-powered recommendations."
)

url = st.text_input(
    "Enter website URL",
    placeholder="https://example.com"
)

if st.button("🔍 Audit Website", use_container_width=True):

    if not url.strip():
        st.warning("Please enter a website URL.")

    else:

        with st.spinner("Auditing website... Please wait."):

            try:
                response = requests.post(
                    API_URL,
                    json={"url": url.strip()},
                    timeout=300
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("SEO Audit Completed!")

                    # Overall score
                    score = data["score"]["overall_score"]

                    st.metric(
                        "Overall SEO Score",
                        f"{score}/100" if score is not None
                        else "Unavailable"
                    )

                    st.write(
                        f"**Pages crawled:** "
                        f"{data['pages_crawled']}"
                    )

                    # Metric scores
                    st.subheader("SEO Metric Scores")

                    metric_scores = data["score"]["metric_scores"]

                    col1, col2, col3, col4, col5 = st.columns(5)

                    columns = [
                        col1, col2, col3, col4, col5
                    ]

                    names = [
                        "title_meta",
                        "broken_links",
                        "h1",
                        "image_alt",
                        "indexability"
                    ]

                    labels = [
                        "Title & Meta",
                        "Broken Links",
                        "H1",
                        "Image Alt",
                        "Indexability"
                    ]

                    for column, name, label in zip(
                        columns, names, labels
                    ):

                        value = metric_scores.get(name)

                        with column:
                            st.metric(
                                label,
                                f"{value}%" if value is not None
                                else "N/A"
                            )

                    # Detailed findings
                    st.subheader("Detailed SEO Findings")

                    metrics = data["metrics"]

                    with st.expander(
                        "Title & Meta Description"
                    ):
                        st.json(metrics["title_meta"])

                    with st.expander("Broken Internal Links"):
                        st.json(metrics["broken_links"])

                    with st.expander("H1 Headings"):
                        st.json(metrics["h1"])

                    with st.expander("Image Alt Text"):
                        st.json(metrics["image_alt"])

                    with st.expander("Indexability"):
                        st.json(metrics["indexability"])

                    # AI recommendations
                    st.subheader("🤖 AI Recommendations")

                    st.markdown(
                        data["recommendations"]
                    )

                else:

                    st.error(
                        f"Audit failed: {response.text}"
                    )

            except requests.RequestException as error:

                st.error(
                    "Could not connect to the API. "
                    "Please make sure the backend is running."
                )

                st.caption(str(error))
