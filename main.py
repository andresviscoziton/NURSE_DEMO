import streamlit as st
import os
from openai import AzureOpenAI


endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")


st.sidebar.title("AI Nursing Assistant")
st.sidebar.markdown("**Select an option:**")
option = st.sidebar.radio("", ["Admission Assistance", "Clinical History Query"])

if 'client' not in st.session_state:
    st.session_state.client = None


if option == "Admission Assistance":
    if st.session_state.client is None:
        client = AzureOpenAI(
        azure_endpoint=endpoint,#, "https://openaiavisco.openai.azure.com/")
        api_key=subscription_key,
        api_version="2024-05-01-preview",
        )
        #st.write("Client initialized")
    else:
        #st.write("Client already initialized")

        

    # Code for the consulta section
    st.title("Nursing Admission Assistant with Azure OpenAI")
    st.text("Try it using some of the following queries:")
    st.table(
        [
            'What are the steps for admission?',
            'What should I do if the patient has a fever?',
            'What are the steps for a patient with a history of hypertension?',
            'Man, 48 Years Old, Head Pain'
         ]
        ) 
            
    consulta = st.text_input("Ask me question regarding patient admissions:", placeholder="Enter your question here")

    if consulta:
        
        # Make the query to OpenAI model
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI Nursing assistant that helps nurses with admission. Based on nurse_protocol.pdf.\nALWAYS your answers should be only max 10 steps to proceed. No additional text"
                },
                {
                    "role": "user",
                    "content": str(consulta)
                }
            ],
            max_tokens=500,
            temperature=0.08,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False,
            extra_body={
                "data_sources": [{
                    "type": "azure_search",
                    "parameters": {
                        "filter": None,
                        "endpoint": f"{search_endpoint}",
                        "index_name": "vector-1726896547803",
                        "semantic_configuration": "vector-1726896547803-semantic-configuration",
                        "authentication": {
                            "type": "api_key",
                            "key": f"{search_key}"
                        },
                        "query_type": "simple",
                        "in_scope": True,
                        "role_information": "You are an AI Nursing assistant that helps nurses with admission. Based on nurse_protocol.pdf.\nALWAYS your answers should be only max 10 steps to proceed. No additional text",
                        "strictness": 3,
                        "top_n_documents": 5
                    }
                }]
            }
        )
        import re
        # Extract the content of the message in the JSON
        message_content = completion.choices[0].message.content
        # Display the result in the Streamlit app
        st.subheader("Assistant Response:")
        st.markdown(message_content)

    # ... your code for the consulta section ...
elif option == "Clinical History Query":
    if st.session_state.client is None:
        client = AzureOpenAI(
        azure_endpoint=endpoint,#, "https://openaiavisco.openai.azure.com/")
        api_key=subscription_key,
        api_version="2024-05-01-preview",
        )
        #st.write("Client initialized")
    else:
        #st.write("Client already initialized")
    # Code for the empty section
    st.title("Clinical History Query")
    st.text("Try it using some of the following patient names:")
    st.table(
        [
            'María Fernandez',
            'Jorge Ramírez',
            'Pablo Lopez',
            'Ana García'
         ]
        ) 
    consulta_ch = st.text_input("Enter the name of a ptient to find the history: ", placeholder="Patient name")
    if consulta_ch:
        
    # Initialize Azure OpenAI client with key-based authentication
        client = AzureOpenAI(
            azure_endpoint = endpoint,
            api_key = subscription_key,
            api_version = "2024-05-01-preview",
        )

        completion = client.chat.completions.create(
            model=deployment,
            messages= [
            {
                "role": "system",
                "content": "You are an AI nursing assistant that helps people find information about clinic history in retrieved data.\nALWAYS your answers should be only a resume of the clinic history.\nAll traslated to English.\n No additional text"
            },
            {
                "role": "user",
                "content": "Necesito busques la historía clínica del patiente: "+str(consulta_ch)+""
            }
            ],
            max_tokens=800,
            temperature=0.11,
            top_p=0.78,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        ,
            extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "filter": None,
                    "endpoint": f"{search_endpoint}",
                    "index_name": "great-nut-723ncdwd3g",
                    "semantic_configuration": "azureml-default",
                    "authentication": {
                    "type": "api_key",
                    "key": f"{search_key}"
                    },
                    "embedding_dependency": {
                    "type": "endpoint",
                    "endpoint": "https://openaiavisco.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-07-01-preview",
                    "authentication": {
                        "type": "api_key",
                        "key": "70eccac0e4ed42409ac26781cfff474a"
                    }
                    },
                    "query_type": "vector_simple_hybrid",
                    "in_scope": True,
                    "role_information": "You are an AI nursing assistant that helps people find information about clinic history in retrieved data.\nALWAYS your answers should be only a resume of the clinic history.\nAll traslated to English.\n No additional text",
                    "strictness": 3,
                    "top_n_documents": 6
                }
                }]
            })

        message_content = completion.choices[0].message.content
        st.subheader("Assistant Response:")
        st.markdown(message_content)
        
    # ... your code for the empty section ...
else:
    st.warning("Please select an option from the sidebar.")

# Get environment variables or default values

# Initialize Azure OpenAI client

# Streamlit app interface
