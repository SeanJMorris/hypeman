# import streamlit as st

# # Initialize session state
# if "disabled" not in st.session_state:
#     st.session_state.disabled = False

# # Display chat messages from history
# for message in st.session_state.get("messages", []):
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Only show the input if it's not disabled
# if not st.session_state.disabled:
#     prompt = st.chat_input("Say something")
#     if prompt:
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         # Disable input after submission
#         st.session_state.disabled = True
#         # Show the message in chat
#         with st.chat_message("user"):
#             st.markdown(prompt)
#         # Here you can add logic for assistant response
#         # After processing, you can re-enable the input if needed
#         # st.session_state.disabled = False
# else:
#     # Optionally, show a message indicating input is disabled
#     st.write("Processing your message...")

import streamlit as st

# Create an empty container for the chat input
input_container = st.empty()

# Only show the prompt if no message has been sent yet
if 'message_sent' not in st.session_state:
    prompt = input_container.chat_input("Type your message here...")
    if prompt:
        st.session_state.message_sent = True
        st.session_state.user_message = prompt
        input_container.empty()  # Clear the input and prompt
else:
    # Show a disabled input or nothing after the first message
    input_container.chat_input("Type your message here...", disabled=True)
