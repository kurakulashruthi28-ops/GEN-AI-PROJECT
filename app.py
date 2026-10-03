import os
import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Generative AI Chatbot",
    page_icon="✨",
    layout="centered"
)


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# BACKGROUND IMAGE
# =========================================================

BASE_DIR = Path(__file__).parent
BACKGROUND_PATH = BASE_DIR / "background.jpg"

if BACKGROUND_PATH.exists():

    image_bytes = BACKGROUND_PATH.read_bytes()

    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    background = (
        f'url("data:image/jpeg;base64,{image_base64}")'
    )

else:

    background = "linear-gradient(135deg, #f8d8e8, #e9d9f5)"


# =========================================================
# CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* ================================
       REMOVE DEFAULT STREAMLIT UI
       ================================ */

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        visibility: hidden;
    }}


    /* ================================
       BACKGROUND
       ================================ */

    .stApp {{

        background-image:
            linear-gradient(
                rgba(255, 220, 238, 0.68),
                rgba(235, 218, 246, 0.75)
            ),
            {background};

        background-size: cover;

        background-position: center;

        background-repeat: no-repeat;

        background-attachment: fixed;

        min-height: 100vh;
    }}


    /* ================================
       MAIN CONTAINER
       ================================ */

    .block-container {{

        max-width: 850px;

        padding-top: 45px;

        padding-bottom: 100px;
    }}


    /* ================================
       TITLE
       ================================ */

    .title {{

        text-align: center;

        font-size: 46px;

        font-weight: 800;

        color: #713c70;

        text-shadow:
            0px 2px 8px white,
            0px 5px 20px rgba(120,60,110,0.25);

        margin-bottom: 8px;
    }}


    /* ================================
       SUBTITLE
       ================================ */

    .subtitle {{

        text-align: center;

        font-size: 17px;

        font-weight: 600;

        color: #453b48;

        margin-bottom: 30px;

        text-shadow: 0px 2px 8px white;
    }}


    /* ================================
       TEXT AREA CONTAINER
       ================================ */

    div[data-testid="stTextArea"] {{

        background: rgba(255,255,255,0.82);

        padding: 8px;

        border-radius: 25px;

        box-shadow:
            0px 10px 35px
            rgba(80,40,70,0.22);
    }}


    /* ================================
       TEXT AREA
       ================================ */

    div[data-testid="stTextArea"] textarea {{

        background: rgba(255,228,239,0.96) !important;

        color: #000000 !important;

        border: 2px solid #c8789e !important;

        border-radius: 18px !important;

        font-size: 17px !important;

        padding: 16px !important;
    }}


    div[data-testid="stTextArea"] textarea:focus {{

        border: 2px solid #c94f91 !important;

        box-shadow:
            0px 0px 20px
            rgba(200,80,145,0.30) !important;
    }}


    div[data-testid="stTextArea"] textarea::placeholder {{

        color: #806878 !important;

        opacity: 1 !important;
    }}


    div[data-testid="stTextArea"] label {{

        display: none !important;
    }}


    /* ================================
       BUTTON
       ================================ */

    div.stButton {{

        display: flex;

        justify-content: center;

        margin-top: 18px;
    }}


    div.stButton > button {{

        background:
            linear-gradient(
                135deg,
                #e85c9f,
                #c94f91
            );

        color: white;

        border: none;

        border-radius: 18px;

        padding: 13px 34px;

        font-size: 17px;

        font-weight: 700;

        box-shadow:
            0px 9px 24px
            rgba(180,65,125,0.35);

        transition: 0.3s;
    }}


    div.stButton > button:hover {{

        transform: translateY(-3px);

        background:
            linear-gradient(
                135deg,
                #d94c91,
                #b94182
            );

        box-shadow:
            0px 13px 30px
            rgba(180,65,125,0.45);
    }}


    /* ================================
       AI RESPONSE HEADING
       ================================ */

    .response-heading {{

        background: rgba(255,238,247,0.96);

        border: 2px solid #d99ab9;

        border-radius: 20px 20px 0px 0px;

        padding: 18px 24px 10px 24px;

        margin-top: 30px;

        color: #713c70;

        font-size: 21px;

        font-weight: 700;

        box-shadow:
            0px 5px 20px
            rgba(80,40,70,0.15);
    }}


    /* ================================
       PLAIN TEXT RESPONSE
       ================================ */

    div[data-testid="stText"] {{

        background: rgba(255,238,247,0.96);

        border-left: 2px solid #d99ab9;

        border-right: 2px solid #d99ab9;

        border-bottom: 2px solid #d99ab9;

        border-radius: 0px 0px 20px 20px;

        padding: 5px 24px 24px 24px;

        color: #000000 !important;

        font-size: 17px !important;

        line-height: 1.7 !important;

        box-shadow:
            0px 10px 30px
            rgba(80,40,70,0.20);

        white-space: pre-wrap !important;
    }}


    div[data-testid="stText"] * {{

        color: #000000 !important;

        font-size: 17px !important;
    }}


    /* ================================
       MOBILE
       ================================ */

    @media (max-width: 600px) {{

        .title {{

            font-size: 34px;
        }}

        .subtitle {{

            font-size: 15px;
        }}

        .block-container {{

            padding-left: 15px;

            padding-right: 15px;
        }}

        div[data-testid="stTextArea"] textarea {{

            font-size: 16px !important;
        }}

        div.stButton > button {{

            font-size: 15px;

            padding: 12px 25px;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    """
    <div class="title">
        ✨ Generative AI Chatbot
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SUBTITLE
# =========================================================

st.markdown(
    """
    <div class="subtitle">
        Ask anything • Think creatively • Generate intelligently
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# QUESTION BOX
# =========================================================

prompt = st.text_area(
    "Question",
    placeholder="Type your question here...",
    height=170,
    label_visibility="collapsed"
)


# =========================================================
# BUTTON
# =========================================================

generate = st.button(
    "✨ Generate Response"
)


# =========================================================
# AI RESPONSE
# =========================================================

if generate:

    if not prompt.strip():

        st.warning(
            "💭 Please type your question first."
        )

    elif not API_KEY:

        st.error(
            "🔑 Gemini API key not found. "
            "Please check your .env file."
        )

    else:

        try:

            # ---------------------------------------------
            # CONNECT TO GEMINI
            # ---------------------------------------------

            with st.spinner(
                "✨ AI is thinking..."
            ):

                client = genai.Client(
                    api_key=API_KEY
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                answer = response.text


            # ---------------------------------------------
            # IF EMPTY RESPONSE
            # ---------------------------------------------

            if not answer:

                answer = (
                    "Sorry, I could not generate "
                    "a response."
                )


            # ---------------------------------------------
            # RESPONSE TITLE
            # ---------------------------------------------

            st.markdown(
                """
                <div class="response-heading">
                    💗 AI Response
                </div>
                """,
                unsafe_allow_html=True
            )


            # ---------------------------------------------
            # IMPORTANT:
            # DISPLAY ANSWER AS PLAIN TEXT
            # NO HTML
            # NO CODE BLOCK
            # ---------------------------------------------

            st.text(answer)


        except Exception as error:

            st.error(
                "⚠️ Something went wrong."
            )

            st.text(
                str(error)
            )