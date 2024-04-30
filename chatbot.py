import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
import io
import base64
import time


def get_pdf_file_as_base64(data):
    base64_pdf = base64.b64encode(data.read()).decode('utf-8')
    return f"data:application/pdf;base64,{base64_pdf}"

questions_answers = {
    "What types of appliances and systems are included in the property?": "The property includes a range of appliances and systems such as a microwave, dishwasher, garbage disposal, central heating, central air conditioning, and a water heater, among others.",
    "Are there any known significant defects or malfunctions in the structural components of the property?": "Yes, the Seller Disclosures report known significant defects or malfunctions in various structural components such as the interior walls, ceilings, floors, exterior walls, insulation, roof, windows, doors, foundation, and other structural components.",
    "Has the property undergone any renovations or repairs without necessary permits as disclosed by the seller?": "Yes, the disclosures indicate that there have been unpermitted renovations, including a kitchen remodel done without necessary permits."
}

def show_typing_animation(message, container):
    displayed_message = ''
    for char in message:
        displayed_message += char
        container.markdown(f"<p style='text-align: justify;'>{displayed_message}</p>", unsafe_allow_html=True)
        time.sleep(0.05)
def scroll_to_last_message():
    st.session_state.last_response = st.empty()  # This will create a new placeholder
    st.session_state.last_response.write("")  # Write an empty string to create a visual element
    st.experimental_rerun()
    
def main():
    load_dotenv()
    st.set_page_config(layout="wide")
    
    with st.sidebar:
        st.title('💬 EstateSpace 📝')
        st.markdown('### About\nThis App helps you upload your contract and ask specific questions.')
        pdf_file = st.file_uploader("Upload your Contract", type='pdf')
        if pdf_file is not None:
            st.sidebar.success("Contract Uploaded!")
        add_vertical_space(5)
        st.write('Made with ❤️ by [Krutika Bhalla](http://krutika-bhalla.github.io/)')
    
    col1, col2 = st.columns([3, 2], gap="small")

    with col1:
        st.header("📄 🔍 EstateCarousel")
        if pdf_file is not None:
            base64_pdf = get_pdf_file_as_base64(pdf_file)
            st.markdown(f'<iframe src="{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>', unsafe_allow_html=True)
        else:
            st.write("Please upload your Contract to view it here.")

    with col2:
        st.header("🤖 EstateTalk")
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        
    
        chat_container = st.container()
        
        
        if pdf_file is not None:
            # question_select = st.selectbox('Choose a question:', [""] + list(questions_answers.keys()))
            question_select = st.selectbox("Choose a common question or select 'Custom' to type your own:", ["Custom"] + list(questions_answers.keys()))
            custom_question = ""
            if question_select == "Custom":
                custom_question = st.text_input("Type your custom question here:")
            if st.button('Ask'):
                
                question = question_select
                if question != "Custom":
                    response = questions_answers.get(question, "Sorry, I don't have an answer to that question.")
                    st.session_state.chat_history.append(("You: " + question, "Bot is typing..."))
                    with chat_container:
                        for q, a in st.session_state.chat_history:
                            st.markdown(f"**{q}**")
                            if a == "Bot is typing...":
                                st.session_state.chat_history[-1] = (q, response)
                                show_typing_animation(response, st.empty())
                            else:
                                st.markdown(f"<p style='text-align: justify;'>{a}</p>", unsafe_allow_html=True)
                            st.markdown("---")
                elif custom_question:
                    response = questions_answers.get(custom_question, "Sorry, I don't have an answer to that question.")
                    st.session_state.chat_history.append(("You: " + question, "Bot is typing..."))
                    with chat_container:
                        for q, a in st.session_state.chat_history:
                            st.markdown(f"**{q}**")
                            if a == "Bot is typing...":
                                st.session_state.chat_history[-1] = (q, response)
                                show_typing_animation(response, st.empty())
                            else:
                                st.markdown(f"<p style='text-align: justify;'>{a}</p>", unsafe_allow_html=True)
                            st.markdown("---")
                else:
                    chat_container.write("Please select a question to get an answer.")
        else:
            st.write("Please upload your Contract to ask questions.")
    
if __name__ == '__main__':
    main()
