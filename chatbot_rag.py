#import streamlit
import streamlit as st
import os
from dotenv import load_dotenv

# import pinecone
from pinecone import Pinecone, ServerlessSpec

# import langchain
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# import the project's own ingestion file
from ingestion import ingest

load_dotenv()
# ingest()

col1, col2 = st.columns(2)

with col1:
    st.markdown("")
    st.title("Sean's Hypeman")

with col2:
    # st.image("/home/scjmorris/projects/hypeman/images/best_ever_sean_golden_020.png")
    st.image("images/best_ever_sean_golden_020.png")

# initialize pinecone database
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# initialize pinecone database
index_name = os.environ.get("PINECONE_INDEX_NAME")  # change if desired
index = pc.Index(index_name)

# initialize embeddings model + vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=os.environ.get("OPENAI_API_KEY"))
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(AIMessage("Hi! I'm Sean's Hypeman Bot. I'm an LLM that has been trained by Sean to answer questions that you might have about him. Heads up -- like any good hypeman, I'm primed to say only positive things about him!"))

    st.session_state.messages.append(SystemMessage("You are an assistant for question-answering tasks. "))

# display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# create the bar where we can type messages
prompt = st.chat_input("Ask anything about Sean! Such as about his work experience, skills, or hobbies!")

# did the user submit a prompt?
if prompt:
    # st.session_state.
    # add the message from the user (prompt) to the screen with streamlit
    with st.chat_message("user"):
        st.markdown(prompt)

        st.session_state.messages.append(HumanMessage(prompt))

    # initialize the llm
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=1
    )

    # creating and invoking the retriever
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 6, "score_threshold": 0.1},
    )

    docs = retriever.invoke(prompt)
    docs_text = "".join(d.page_content for d in docs)

    # creating the system prompt
    system_prompt = """You are an assistant for question-answering tasks.
    Your job is to answer questions specifically about a man named Sean.
    Use the pieces of retrieved context provided below to answer the question.
    Begin every response with a child-like rock star tone, using lots of slang and excitement.
    In your response, you should speak as highly of Sean as possible, highlighting his skills, experience, and positive attributes. You should speak about him as if you are a rock star dude who thinks the world of Sean. Try to bring the conversation back to his technical skills and professional achievements whenever possible.
    If you don't know the answer, speculate based on the information provided in the context, but be clear about the fact that you are speculating and then offer to answer another question and give an example of another question you can answer.
    Use 4 sentences maximum.
    Context: {context}:"""

    # Populate the system prompt with the retrieved context
    system_prompt_fmt = system_prompt.format(context=docs_text)


    print("-- SYS PROMPT --")
    print(system_prompt_fmt)

    # adding the system prompt to the message history
    st.session_state.messages.append(SystemMessage(system_prompt_fmt))

    # invoking the llm
    result = llm.invoke(st.session_state.messages).content
    result += "\n\nOther questions you could ask:"
    # result += st.button("What are Sean's hobbies outside of work?")
    # result += st.button("What is Sean's work experience?")
    # result += st.button("What technical skills does Sean have?")

    # result +=
    # left, middle, right = st.columns(3)
    # if left.button("Plain button", width="stretch"):
    #     left.markdown("You clicked the plain button.")
    # if middle.button("Emoji button", icon="😃", width="stretch"):
    #     middle.markdown("You clicked the emoji button.")
    # if right.button("Material button", icon=":material/mood:", width="stretch"):
    #     right.markdown("You clicked the Material button.")


    # adding the response from the llm to the screen (and chat)
    with st.chat_message("assistant"):
        st.markdown(result)

        # # Add three buttons in a single row
        # col1, col2, col3 = st.columns(3)
        # with col1:
        #     if st.button("First button"):
        #         # st.markdown("You clicked the first button.")
        #         # st.chat_input("Is Sean handsome?")
        #         # first_question = "Is Sean handsome?"
        #             # st.session_state.messages.append(HumanMessage(first_question))
        #         # prompt = st.chat_input("Ask anything about Sean! Such as about his work experience, skills, or hobbies!")
        #         with st.chat_message("user"):
        #             st.chat_input("Is Sean handsome?")
        #             # st.markdown(prompt)
        #             # st.session_state.messages.append(HumanMessage(prompt))
        # with col2:
        #     if st.button("Second button"):
        #         st.markdown("You clicked the second button.")
        # with col3:
        #     if st.button("Third button"):
        #         st.markdown("You clicked the third button.")

        st.session_state.messages.append(AIMessage(result))
