import streamlit as st
import os
import base64
import io
from PIL import Image

# Import dependencies from the provided notebook
from langchain_ibm import ChatWatsonx
from ibm_watsonx_ai import APIClient
from langchain_core.messages import HumanMessage, AIMessage

# --- Configuration ---
# You can find your API key, project ID, and service URL in your IBM Cloud account
# and within the Watsonx.ai console.
# Hardcoded API Key and Project ID (as per your request in the previous turn)
from dotenv import load_dotenv
load_dotenv()

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", "your_api_key_here")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "your_project_id_here")
WATSONX_SERVICE_URL = os.getenv("WATSONX_SERVICE_URL", "https://api.watsonx.ai")

# Choose a vision-enabled foundation model.
# 'meta-llama/llama-3-2-90b-vision-instruct' or 'ibm/granite-vision-3-2-2b' are examples.
# Verify available models in your Watsonx.ai instance.
WATSONX_MODEL_ID = "meta-llama/llama-3-2-90b-vision-instruct"

# Defining model parameters
WATSONX_MODEL_PARAMETERS = {
    "decoding_method": "greedy",
    "max_new_tokens": 500,
    "min_new_tokens": 1,
    "temperature": 0.0,
    "top_p": 1
}

# --- Helper Functions ---

def encode_image_to_base64(image_file) -> str:
    """
    Reads an uploaded image file-like object, converts it to PNG format,
    and encodes it to a base64 string.
    """
    try:
        # Streamlit's file_uploader gives a BytesIO object directly for opened files
        img = Image.open(image_file).convert("RGB")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    except Exception as e:
        st.error(f"Error encoding image: {e}")
        return None

@st.cache_resource
def initialize_watsonx_chat_model(api_key: str, project_id: str, service_url: str, model_id: str, parameters: dict):
    """
    Initializes and returns a ChatWatsonx instance using the provided credentials and model details.
    This function is cached to avoid re-initializing the model on every Streamlit rerun.
    """
    try:
        credentials = {
            "url": service_url,
            "apikey": api_key
        }
        client = APIClient(credentials=credentials, project_id=project_id)

        chat_model = ChatWatsonx(
            model_id=model_id,
            url=credentials["url"],
            project_id=project_id,
            params=parameters,
            watsonx_client=client,
            apikey=credentials["apikey"]
        )
        st.success(f"Successfully initialized Watsonx Chat Model: {model_id}")
        return chat_model
    except Exception as e:
        st.error(f"Error initializing Watsonx Chat Model: {e}. Please check your API key and project ID.")
        return None

def load_knowledge_file(file_path) -> str:
    """Load knowledge text file into memory."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading knowledge file: {e}")
        return ""

knowledge_text=load_knowledge_file("urban_terrace_farming_knowledge.txt")

custom_instruction = """
This is a fantastic space for an urban farm! Based on the image, I see a terrace with great potential for plants that need a lot of sunlight. Here is a simple, structured guide to help you get started:

Step 1: Assess and Prepare the Space

Sunlight: This area gets plenty of sun, which is perfect for many vegetables and herbs.

Drainage: Before adding pots, ensure there's a plan for water runoff to protect your terrace. Consider placing pots on trays or using self-draining containers.

Water Source: Think about the closest water source to make watering easy.

Step 2: Choose Your Plants

For this amount of sun, I recommend sun-loving vegetables like tomatoes, peppers, and eggplants.

You can also grow a wide range of herbs such as rosemary, basil, and mint.

Step 3: Select Your Containers and Soil

Containers: Use large, sturdy pots or grow bags. The size of the container directly affects how large your plants can grow.

Soil: Use a lightweight, high-quality potting mix specifically designed for containers. It should have good drainage. Avoid using regular garden soil, which can be too heavy.

Step 4: Start Planting!

Fill your containers with soil, plant your seeds or seedlings, and water them gently.

What are you interested in growing first? I can provide more specific advice on those plants!
"""


# --- Streamlit Application ---

st.set_page_config(page_title="Urban terrace farming pro", layout="centered")
st.title("💬 Your terrace farming expert. I stop solution to all terrace gardern problems")
st.markdown("Type a message or upload an image to start a conversation!")

# Initialize the Watsonx Chat Model only once
chat_model = initialize_watsonx_chat_model(
    WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_SERVICE_URL, WATSONX_MODEL_ID, WATSONX_MODEL_PARAMETERS
)

if chat_model:
    # Initialize chat history and current uploaded file in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_uploaded_image" not in st.session_state:
        st.session_state.current_uploaded_image = None
    
    # File uploader for images - always available
    uploaded_file = st.sidebar.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])

    # If a new file is uploaded, update session state
    if uploaded_file is not None:
        st.session_state.current_uploaded_image = uploaded_file
        # Display the uploaded image below the uploader
        st.sidebar.image(uploaded_file, caption="Current Uploaded Image", use_column_width=True)
        st.sidebar.info("Image uploaded. Your next message will include this image.")
    elif uploaded_file is None and st.session_state.current_uploaded_image is not None:
        # If the user clears the uploader, also clear the session state
        st.session_state.current_uploaded_image = None
        st.sidebar.info("Image cleared.")


    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["type"] == "text":
                st.markdown(message["content"])
            elif message["type"] == "image":
                st.image(message["content"], caption="Image from a previous turn", use_column_width=True)
            elif message["type"] == "multimodal":
                st.markdown(message["text_content"])
                st.image(message["image_content"], caption="Image sent in this turn", use_column_width=True)

    # Accept user input - always available
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        # Determine if an image needs to be sent with this prompt
        if st.session_state.current_uploaded_image is not None:
            st.session_state.messages.append(
                {"role": "user", "type": "multimodal", "text_content": prompt, "image_content": st.session_state.current_uploaded_image}
            )
        else:
            st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})

        # Display the user's message in the chat
        with st.chat_message("user"):
            if st.session_state.current_uploaded_image is not None:
                st.image(st.session_state.current_uploaded_image, caption="Your image", use_column_width=True)
            st.markdown(prompt)

        # Prepare the message for the LLM
        messages_for_llm = []

        if st.session_state.current_uploaded_image is not None:
            encoded_image = encode_image_to_base64(st.session_state.current_uploaded_image)
            if encoded_image:
                image_data_url = f"data:image/png;base64,{encoded_image}"
                messages_for_llm.append(
                    HumanMessage(
                        content=[
                            {"type": "text", "text": f"{custom_instruction}\n\nKnowledge:\n{knowledge_text}\n\nUser: {prompt}"},
                            {"type": "image_url", "image_url": {"url": image_data_url, "detail": "high"}}
                        ]
                    )
                )
        else:
            messages_for_llm.append(
                HumanMessage(content=f"{custom_instruction}\n\nKnowledge:\n{knowledge_text}\n\nUser: {prompt}")
            )


        with st.spinner("Thinking..."):
            try:
                response_message = chat_model.invoke(messages_for_llm)
                chatbot_response = response_message.content

                # Add chatbot response to chat history
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": chatbot_response})
                with st.chat_message("assistant"):
                    st.markdown(chatbot_response)

            except Exception as e:
                error_msg = f"An error occurred during chat: {e}. Please ensure your API key, project ID, and model ID are correct and the model supports multimodal input if an image was sent."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "type": "text", "content": f"Error: {error_msg}"})
                with st.chat_message("assistant"):
                    st.markdown(f"Error: {error_msg}")
            finally:
                # Clear the uploaded image from session state after it's been processed
                # This ensures subsequent messages don't automatically re-send the same image
                st.session_state.current_uploaded_image = None
                # Rerun the app to clear the file uploader widget
                st.rerun()
else:
    st.warning("Chatbot not initialized. Please check the console for errors and ensure your Watsonx.ai credentials are correct.")
