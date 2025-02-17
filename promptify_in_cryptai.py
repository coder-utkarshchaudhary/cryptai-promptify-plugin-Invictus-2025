import streamlit as st
import requests

st.set_page_config(page_title="Prompt Hacking  - Promptify Level 3", layout="centered")
st.title("PROMPT HACKING!!!")
# st.markdown('[CLICK HERE! CLICK HERE! CLICK HERE! CLICK HERE! CLICK HERE! CLICK HERE! CLICK HERE! CLICK HERE!](https://unstop.com/hackathons/promptify-invictus-2025-technical-council-dtu-1387638)')

api_key = st.secrets["GPT_API_KEY"]
external_user_id = 'user'

create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
headers = {
    'apikey': api_key
}
create_session_body = {
    "pluginIds": [],
    "externalUserId": external_user_id
}

response = requests.post(create_session_url, headers=headers, json=create_session_body)

# if response.status_code == 201:
#     session_id = response.json()['data']['id']
#     print(f"Session created with ID: {session_id}")

#     submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
#     submit_query_body = {
#         "endpointId": "predefined-openai-gpt4o",
#         "role" : "system",
#         "query": SYSTEM_PROMPT,
#         "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
#         "responseMode": "sync"
#     }

#     response = requests.post(submit_query_url, headers=headers, json=submit_query_body)

#     if response.status_code == 200:
#         print("Query submitted successfully.")
#         print(response.text)
#     else:
#         print("Failed to submit query:", response.status_code)
# else:
#     print("Failed to create session:", response.status_code)

if response.status_code == 201:
    session_id = response.json()['data']['id']
else:
    st.error("Failed to create session. Please try again.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask the Whispering Oracle..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
    submit_query_body = {
        "endpointId": "predefined-openai-gpt4o",
        "role": "system",
        "query": st.secrets["SYSTEM_PROMPT"] + f"\nUser Input: {user_input}",
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }

    response = requests.post(submit_query_url, headers=headers, json=submit_query_body)
    if response.status_code == 200:
        # print(response.text)
        # print(response.json())
        oracle_response = response.json()["data"]["answer"]
        st.session_state.messages.append({"role": "assistant", "content": oracle_response})
        with st.chat_message("assistant"):
            st.markdown(oracle_response)
    else:
        st.error("Failed to get a response from the Oracle.")
