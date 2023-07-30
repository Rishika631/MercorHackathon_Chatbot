import textbase
from textbase.message import Message
from textbase import models
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_tagging_chain_pydantic
from pydantic import BaseModel, Field, conlist
from typing import Optional, List 
import os
import time
import pandas as pd
import random
from rich.console import Console
from rich.table import Table

# Load your OpenAI API key
models.OpenAI.api_key = "YOUR_OPENAI_API_KEY"

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with a Job Interview Preparation Bot. I'll ask you some questions to understand the job you are preparing for, and then I'll simulate a job interview based on that information. Let's get started!
"""

# Initialize Langchain and OpenAI models
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
ask_init = ['full_name', 'school_background', 'working_experience', 'interview_motivation']
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# Define the PersonalDetails class for candidate details
class PersonalDetails(BaseModel):
    full_name: Optional[str] = Field(
        None,
        description="Is the full name of the user.",
    )
    school_background: Optional[conlist(int, min_items=3, max_items=3)] = Field(
        None,
        description="""Qualification level of education background. Range is 1 to 10, the bigger number the higher qualified.
        The first element indicates the level of degree, 10 means master degree or higher, 1 means high school.
        The second element indicates the major relevance, 10 means computer science and its releated major.
        The third element indicates the college ranking, 10 means the Top 50 college of world, 1 means community college.
        0 means indeterminated.
        """,
    )
    working_experience: Optional[conlist(int, min_items=3, max_items=3)] = Field(
        None,
        description="""Qualification status of career background.Range is 1 to 10, the bigger number the higher qualified.
        The first element indicates job level, 10 means senior manager or above, 1 means intern.
        The second element indicates position relevance, 10 means software development positions.
        The third element indicates the company Ranking, 10 means the Top 500 companies of world, 1 means small local company.
        0 means indeterminated.
        """,
    )
    interview_motivation: Optional[int] = Field(
        None,
        description="""The candidate's motivation level to join the interview.
        10 means very interested and enthusiastic about the interview and new role opening. 1 means not interested.
        """,
    )
tagging_chain = create_tagging_chain_pydantic(PersonalDetails, llm)

# Function to generate interview questions
sample_questions = [
    "Tell me about yourself.",
    "What are your strengths?",
    "What are your weaknesses?",
    "Why do you want this job?",
    "Where do you see yourself in 5 years?",
    "How do you handle stress?",
    "Maximum product of 3 numbers?",
    "How to reverse a linkedlist? write code",
    "Tell me about a challenging situation you faced at work and how you handled it.",
    "What do you know about our company?",
]

def generate_interview_questions(message_history):
    num_questions = min(len(sample_questions), 5)  # Limit the number of questions to 5 for simplicity
    return random.sample(sample_questions, num_questions)

def radar_chart(motivation, education, career):
    console = Console()
    table = Table(show_header=False, box=None, show_lines=False)
    table.add_column()
    table.add_column(justify="right")
    table.add_row("Motivation", str(motivation))
    table.add_row("Highest Degree", str(education[0]))
    table.add_row("Academic Major", str(education[1]))
    table.add_row("College Ranking", str(education[2]))
    table.add_row("Job Level", str(career[0]))
    table.add_row("Job Position", str(career[1]))
    table.add_row("Company Ranking", str(career[2]))
    console.print(table)

def on_message(message_history: List[Message], state: dict = None):
    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    if len(message_history) > 0:
        user_message = message_history[-1].content.strip()
    else:
        user_message = ""

    # Generate GPT-3.5 Turbo response
    bot_response = models.OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history,
        model="gpt-3.5-turbo",
    )

    # Check if the conversation is in the interview phase
    if state.get("interview_phase", False):
        interview_questions = generate_interview_questions(message_history)
        if state["counter"] == len(interview_questions):
            # All interview questions have been asked, move to feedback phase
            state["interview_phase"] = False
            state["feedback_phase"] = True
            bot_response = "Thank you for participating! Here is your feedback:\n\n"
        else:
            bot_response = interview_questions[state["counter"]]

    # Process user response and move to the interview phase
    if "user" in bot_response.lower():
        state["interview_phase"] = True
        bot_response = interview_questions[0]

    # If the conversation is in the feedback phase
    elif state.get("feedback_phase", False):
        final_details = state.get("user_details", {}).dict()
        radar_chart(
            final_details["interview_motivation"],
            final_details["school_background"],
            final_details["working_experience"],
        )

    return bot_response, state

# Run the textbase chatbot with the on_message function
if __name__ == "__main__":
    textbase.run(on_message)

