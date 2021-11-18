import io
import requests
# from requests_toolbelt.multipart.encoder import MultipartEncoder
import streamlit as st
import requests
from requests.structures import CaseInsensitiveDict
from textblob import TextBlob
import pandas as pd


@st.cache
def convert_to_df(sentiment_result):
    sentiment_dict = {'polarity': sentiment_result.polarity,
                      'subjectivity': sentiment_result.subjectivity}
    sentiment_df = pd.DataFrame(
        sentiment_dict.items(), columns=['metric', 'value'])
    return sentiment_df

@st.cache
def process_summary(input_text: str, server_url: str):
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    # m = MultipartEncoder(fields={"text": (text)})
    # data_dict = {}
    # data_dict["text"] = input_text.text
    # data = str(data_dict)
    # input_text = Text(text=text)
    valid_text = {
            'text': input_text
        }
    # data = '{"text":'+input_text+'}'
    # data = '{"text":"'+text+'"}'

    resp = requests.post(server_url, headers=headers, json=valid_text, verify=False, timeout=8000)
    result = resp.json()
    result_list = result['Summary from transformers']
    valid_result = result_list[0]["summary_text"]
    return valid_result

@st.cache
def process_ner(input_text: str, server_url: str):
    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    # m = MultipartEncoder(fields={"text": (text)})
    # data_dict = {}
    # data_dict["text"] = input_text.text
    # data = str(data_dict)
    # input_text = Text(text=text)
    valid_text = {
            'text': input_text
        }
    # data = '{"text":'+input_text+'}'
    # data = '{"text":"'+text+'"}'

    resp = requests.post(server_url, headers=headers, json=valid_text, verify=False, timeout=8000)
    result = resp.json()
    result_list = result['NER from Spacy']
    # valid_result = result_list
    return result_list


def main():
    st.title("Streamlit app for Text Analysis")
    menu = ["Home", "NER", "Summarization"]
    choice = st.sidebar.selectbox("Menu",    menu)

    if choice == "Home":
        st.subheader("Home")
        with st.form(key="HomeForm"):
            raw_text = st.text_area("Enter text here:")
            submit_button = st.form_submit_button(label='Analyze')

        if submit_button:
            
            st.info("Results")
            sentiment = TextBlob(raw_text).sentiment
            st.write(sentiment)

            # Emoji
            if sentiment.polarity > 0:
                st.markdown("Sentiment: Positive :smiley: ")
            elif sentiment.polarity < 0:
                st.markdown("Sentiment: Negative :angry: ")
            else:
                st.markdown("Sentiment: Neutral 😐 ")

            # st.write(type(sentiment))
            result_df = convert_to_df(sentiment)
            st.dataframe(result_df)

    elif choice=="Summarization":
        st.subheader("Text summarizer")
        with st.form(key="SummaryForm"):
            raw_text = st.text_area("Enter text here:")
            submit_button = st.form_submit_button(label='Get Summary')

        if submit_button:
            backend = "https://fastapi-image-jvlhy6khda-ue.a.run.app/summary"
            summary = process_summary(raw_text, backend)
            st.write("Summary:")
            st.write(summary)

    elif choice=="NER":
        st.subheader("NER")
        with st.form(key="NERForm"):
            raw_text = st.text_area("Enter text here:")
            submit_button = st.form_submit_button(label='Get Entities')

        if submit_button:
            backend = "https://fastapi-image-jvlhy6khda-ue.a.run.app/ner"
            ner = process_ner(raw_text, backend)
            st.write("NER:")
            st.write(ner)

    # st.write(
    #     """Perform summarization and NER"""
    # )  # description and instructions

    # raw_text = st.text_area("Enter text here:")
    # # print(raw_text)
    # if st.button("Get summary"):

    #     col1, col2 = st.columns(2)

    #     if raw_text:
    #         summary = process(raw_text, backend)
    #         # col1.header("Original")
    #         # col1.text(raw_text, use_column_width=True)
    #         # col2.header("Summary")
    #         # col2.text(summary, use_column_width=True)
    #         st.write("Summary:")
    #         st.write(summary)

    # else:
    #     # handle case with no image
    #     st.write("Insert Text!")


if __name__ == '__main__':
    main()
