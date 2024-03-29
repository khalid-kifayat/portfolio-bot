from itertools import zip_longest
import streamlit as st

from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
openapi_key = st.secrets["OPENAI_API_KEY"]

# Set streamlit page configuration 
# Set streamlit page configuration
st.set_page_config(page_title="Portfolio-Bot")
st.title("Portfolio-Bot")
hide_streamlit_style = """
            <style>

            background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
            background-size: cover;
            
            [data-testid="stToolbar"] {visibility: hidden;}
            .reportview-container {
            margin-top: -2em;
        }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            #stDecoration {display:none;}
            footer {visibility: hidden;}
            div.embeddedAppMetaInfoBar_container__DxxL1 {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Initialize session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []  # Store AI generated responses

if 'past' not in st.session_state:
    st.session_state['past'] = []  # Store past user inputs

if 'entered_prompt' not in st.session_state:
    st.session_state['entered_prompt'] = ""  # Store the latest user input

# Initialize the ChatOpenAI model
chat = ChatOpenAI(
    temperature=1,
    model_name="gpt-3.5-turbo",
    openai_api_key=openapi_key, 
    max_tokens=200
)


def build_message_list():
    """
    Build a list of messages including system, human and Ai chatbot of Portfolio-Bot it company messages.
    """
    # Start zipped_messages with the SystemMessage
    zipped_messages = [SystemMessage(
        # content="You are a helpful AI assistant talking with a human. If you do not know an answer, just say 'I don't know', do not make up an answer.")]
        content = """ when the user ask  hi  tell him Welcome to the Portfolio-Bot developed by Khalid Kifayat, you can ask any question about khalid kifayat. His education, skills, experience, projects etc I am here to assist you as a knowledgeable consultant. 

---
**About Portfolio-Bot:**
Portfolio-Bot is digital chatbot which answer questions about khalid kifayat, his education, his skills, his experience, projects delivered.
---
**About Khalid Kifayat:**
Hello, I'm Khalid kifayat, Skillful Generative Ai-Engineer with working experience in Cloud computing (AWS, GCP), Infrastructure deployment, testing, monitoring, scripting, automation, Version control, documentation & system's support.
I also work as a proficient working in Python, Langchain, OpenAI, Gemini Ultra, Google Dialogflow & Amazon Alexa with a keen eye for design, coding finesse, and a knack for creating intelligent chatbots using Rule based and Generative AI mechanism's. I bring a holistic approach to crafting dynamic and user-centric digital solutions.
---
**Education**
* Master's in Computer Sciences - Iqra University Karachi - 2004.
* Bachelor's in Computer Sciences - University of Peshawar - 2001
---
**Skills**
* Chatbot Development in python, OpenAI, Gemini Ultra LLMs, Voiceflow, Zapier, Make, CRMs, API Integrations etc.
* Git, GitHub, GitLab for version control and collaboration.
* SonarQube/JFrog for code testing.
* CI/CD: Jenkins ArgoCD, GitLab CI/CD for automation.
* Containerization: Docker and Kubernetes.
* Infrastructure as Code: Terraform, Ansible, Cloud-Formation
* Monitoring: AWS Cloud-Watch, Google Cloud Ops-Agent Monitoring, or tools like Prometheus Grafana.
* Security: IAM, Cloud Armor, Active Directory (AD)
---
**Certifications**
* done ✍ Google Cloud Digital Cloud Leader Certification  (Feb 2024 - Feb 2027)
Accredible Certificate URL: https://www.credential.net/b541e2f9-4c50-4902-98b7-fbf1de34f30a
---
**Projects - Cloud/DevOps**
* CICD Pipeline for Java Application to deploy on Kubernetes Cluster using Jenkins.
* Automated Cl/CD Pipeline for Django Web Application using AWS, Docker, Jenkins and Kubernetes.
* Assimilation of VPC, NAT, API GATEWAY, Route53, Load Balancers & AWS Lambda along with DATA Migration from S3 to Glacier.
* Manage, Secure, Validate, Debug, Monitor & Prevent Misconfiguration of Kubernetes.
* MongoExpress/MongoDB Application deployment using Kubernetes.
* Deploying App using GiT-Maven-Jenkins & Tomcat Server.
---
**Projects - Ai Chatbot Datascience**
* Personalized Diet and Workout Recommender
https://dietplan-app.streamlit.app/
* Gemini Health App
https://health-application.streamlit.app/
* Youtube Video Transcriber
https://yt-transcriber-app.streamlit.app/
* ATS System (Resume)
https://cv-app.streamlit.app/
* ChatwithPDF
https://pdf-chating.streamlit.app/
* MultiLanguage Invoice Extractor
https://invoice-info.streamlit.app/
* Q&A - Saving Chat History
https://builtautomations.streamlit.app/
* Project Ideas & Custom Project Description Generator
https://project-ideas.streamlit.app/
* Question-Paper Solver Application
https://exam-paper-solver.streamlit.app/
---
**Communication skills**
khalid kifayat possesses the following skills,
* Effective communicator
* Teamwork & Leadership
* Customer focused
* Active licensing
---
**Job Experience**
* IT Technical Analyst (Pakistan Tobacco Company (PTC), Location: Akora Khattak Factory, KPK, Pakistan (Client: HRSPL)) July 19 - Sept 20
* IT Officer, Rural Livelihood & Community Infrastructure Project (RLCIP), Location: Peshawar, Pakistan , May 2013 - Mar 2018
* IT Admin, Area Development Project for Frontier Regions (ADP-FRs), Location: Peshawar, Pakistan, July 2010 - Apr 2013
* IT Admin, South FATA Development Project (SFDP) , Location: Peshawar, Pakistan, June 2007 - June 2010
* Assistant Network Engineer, Warid Telecom (Telecom Company) , Location: Peshawar, Pakistan, Oct 2004 - May 2007

Thank you for choosing khalid kifayat Portfolio-Bot. If you have any questions or require assistance, feel free to ask! """
    )]


    # Zip together the past and generated messages
    for human_msg, ai_msg in zip_longest(st.session_state['past'], st.session_state['generated']):
        if human_msg is not None:
            zipped_messages.append(HumanMessage(
                content=human_msg))  # Add user messages
        if ai_msg is not None:
            zipped_messages.append(
                AIMessage(content=ai_msg))  # Add AI messages

    return zipped_messages


def generate_response():
    """
    Generate AI response using the ChatOpenAI model.
    """
    # Build the list of messages
    zipped_messages = build_message_list()

    # Generate response using the chat model
    ai_response = chat(zipped_messages)

    return ai_response.content


# Define function to submit user input
def submit():
    # Set entered_prompt to the current value of prompt_input
    st.session_state.entered_prompt = st.session_state.prompt_input
    # Clear prompt_input
    st.session_state.prompt_input = ""


# Create a text input for user
st.text_input('Hi, I am AI Assistant - Ask anything about Khalid Kifayat: ', key='prompt_input', on_change=submit)


if st.session_state.entered_prompt != "":
    # Get user query
    user_query = st.session_state.entered_prompt

    # Append user query to past queries
    st.session_state.past.append(user_query)

    # Generate response
    output = generate_response()

    # Append AI response to generated responses
    st.session_state.generated.append(output)


# Display the chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # Display AI response
        message(st.session_state["generated"][i], key=str(i))
        # Display user message
        message(st.session_state['past'][i],
                is_user=True, key=str(i) + '_user')

