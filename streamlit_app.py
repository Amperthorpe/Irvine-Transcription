import streamlit as st
import openai as ai
import json
import io
from oai_models import transcribe_audio

st.set_page_config("LunaTranscribe", page_icon="🌙", layout="wide")
AUDIO_FILE_TYPES = ["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"]


def main():
    # Set up session variables to be used later.
    if "output_text" not in st.session_state:
        st.session_state.output_text = "Transcription will show here."
    if "file_name" not in st.session_state:
        st.session_state.file_name = "transcription_file"

    # Site layout
    st.header("Irvine AI Transcription (DEMO)")
    uploader_container = st.container()  # Holds the file upload widget, and settings.
    output_container = st.container()  # Holds the file output, and downloader.
    with output_container:
        text_placeholder = st.markdown(st.session_state.output_text)

    def form_callback():
        """Called when pressing the "Submit" button."""
        prompt = st.session_state.text_prompt
        file = st.session_state.audio_upload

        st.session_state.file_name = file.name
        result_dict = transcribe_audio(file, prompt)
        st.session_state.output_text = result_dict["text"]
        with output_container:
            st.audio(file)

    with uploader_container:
        with st.form(key="upload_file_form"):
            audio_upload = st.file_uploader(
                f"Upload Audio ({', '.join(AUDIO_FILE_TYPES)}), 25 MB Limit (Larger files WIP)",
                key="audio_upload",
                help=f"Upload an audio file of {', '.join(AUDIO_FILE_TYPES)} format to be transcribed.",
                type=AUDIO_FILE_TYPES,
            )
            with st.expander("Prompt (Optional)"):
                st.text_area(
                    "Concisely describe the topic of the audio. Include words the AI is likely to get wrong, such as acronyms and names. Poor grammar or spelling could affect results.",
                    key="text_prompt",
                )
            st.form_submit_button(on_click=form_callback)

    with output_container:

        def get_download_filename():
            audio_name = st.session_state.file_name
            for ext in AUDIO_FILE_TYPES:
                audio_name = audio_name.removesuffix(ext)
                # Removes the file extension
            return f"{audio_name}txt"

        st.download_button(
            "Download Transcript (.txt)",
            data=st.session_state.output_text,
            file_name=get_download_filename(),
        )


def check_password():
    """Returns `True` if the user had the correct password. From Streamlit documentation."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("Password incorrect")
        return False
    else:
        # Password correct.
        return True


url_params = st.experimental_get_query_params()
if (st.secrets["url_password"] in url_params.get("pass", [])) or check_password():
    # Compares a "pass" URL parameter to the password in the Streamlit secrets.
    # Use a password like example.com/?pass=<password here>
    # If that is not found, requests a password for user to type.
    main()
