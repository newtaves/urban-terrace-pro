

### Urban Terrace Farming Expert Chatbot

This is an AI-powered conversational assistant built to help you with all your terrace gardening and urban farming needs. Powered by a multimodal Large Language Model (LLM) from Watsonx.ai, the chatbot can provide detailed, step-by-step advice based on both text descriptions and uploaded images of your space.

-----

### Key Features

  * **Multimodal Capabilities:** The chatbot can analyze images of your terrace or balcony to give you tailored advice on plant selection, sunlight assessment, and space preparation.
  * **Knowledge-Augmented Generation (RAG):** The bot is pre-loaded with a knowledge base on urban terrace farming, so it can provide accurate and specific guidance on topics like drainage, soil types, and plant care.
  * **Conversational Interface:** The app features a clean and intuitive chat interface, allowing for a natural and engaging user experience.
  * **Secure API Handling:** API credentials for the Watsonx.ai model are handled securely using a **`.env` file** and environment variables, keeping sensitive information out of the codebase.

-----

### Technologies Used

  * **Streamlit:** The web framework used to build the interactive and user-friendly front end.
  * **IBM Watsonx.ai:** The powerful AI platform that provides the underlying Large Language Model (`meta-llama/llama-3-2-90b-vision-instruct`).
  * **LangChain:** A framework used to build and manage the connection to the LLM and handle the conversational flow.
  * **Python:** The core programming language for the entire application.

-----

### How to Run Locally

To get this application up and running on your local machine, follow these simple steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

      * **Note:** The `requirements.txt` file should include `streamlit`, `langchain_ibm`, `ibm-watsonx-ai`, `python-dotenv`, `Pillow`, etc.

4.  **Set up your `.env` file:**

      * Create a file named **`.env`** in the root directory of the project.
      * Add your IBM Cloud API key and Watsonx.ai project ID. You can find these credentials in your IBM Cloud account.
      * The file should look like this:
        ```ini
        WATSONX_API_KEY="your_api_key_here"
        WATSONX_PROJECT_ID="your_project_id_here"
        ```

5.  **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

    The app will open in your web browser, and you can start interacting with the chatbot\!

-----

### Project Structure

```
.
├── app.py                      # Main Streamlit application file
├── urban_terrace_farming_knowledge.txt # The RAG knowledge base
├── requirements.txt            # Python dependencies
└── .env.example                # Example file for environment variables
```

-----

### Future Enhancements

  * Integration with more specialized models for pest identification or soil analysis.
  * The ability to save and retrieve past conversations.
  * User accounts and personalization.
  * A dedicated knowledge base management system.
