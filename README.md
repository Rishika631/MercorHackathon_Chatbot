# MercorHackathon_Chatbot
# Job Interview Preparation Bot 
## Video demo link
https://drive.google.com/file/d/1HVCtzKhq5MU3_k2IL1b_D8a2iISfHYHI/view?usp=sharing

## Overview
The Job Interview Preparation Bot is a Python-based chatbot designed to simulate a job interview preparation experience. The bot interacts with users, asks questions to understand the job they are preparing for, and then conducts a simulated job interview based on the provided information. It utilizes the OpenAI GPT-3.5 Turbo model to generate responses and provides personalized feedback to improve interview skills.

## Dependencies
Before using the chatbot, ensure the following Python libraries are installed:

textbase
langchain
pydantic
pandas
rich
Also, you need to obtain an API key for the OpenAI GPT-3.5 Turbo model.
## Installation
1. Clone the repository:

Open your terminal or command prompt and navigate to the directory where you want to clone the project. 
Clone the repository and install the dependencies using Poetry (you might have to install Poetry first).

  ```ruby
git clone https://github.com/Rishika631/MercerHackathon_Chatbot.git
cd textbase
poetry install
```

2. Install the required dependencies:
 
Install the required Python packages by running the following command in your terminal or command prompt:
```ruby
pip install textbase langchain pydantic openai pandas rich
```

3. Set up the secret key:
In the project directory, find the main.py file and open it with a code editor. Replace the placeholder API keys with your actual API keys:
```ruby
openai.api_key = 'YOUR_OPENAI_API_KEY'
```
4. Run the following command:
```ruby
poetry run python textbase/textbase_cli.py test main.py
```
Now go to http://localhost:4000 and start chatting with your job interview preparation bot!

## Features
Collects and processes candidate details such as full name, education background, working experience, and interview motivation.
Simulates a job interview experience with random sample interview questions.
Generates responses using the GPT-3.5 Turbo model for realistic interactions.
Provides personalized feedback to candidates based on interview performance.

## Conclusion
The Job Interview Preparation Bot is a powerful tool for job seekers to practice and improve their interview skills in a personalized and interactive manner. With the help of the OpenAI GPT-3.5 Turbo model, the chatbot offers an effective preparation experience to boost candidates' confidence and readiness for real job interviews.
