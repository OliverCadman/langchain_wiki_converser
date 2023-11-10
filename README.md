# Langchain Exercise - Create a Wikipedia QA Application


This repo contains the finished code for a group code-along workshop, and should serve as reference for any trainers involved in leading workshops for future Xander cohorts.

  

## The 'Problem' defining the purpose of the application


As many of you might know already, OpenAI's ChatGPT 3.5 LLM is trained on data until 2021.

Since this is the case, if we were to ask the LLM the following question,

  

"Who starred in the new Oppenheimer film, directed by Christopher Nolan?"

  

The LLM would not know the answer. This is because it's not been trained on this film.

  

The Question/Answer application we will be building today will be designed to 'teach' the LLM this information, using Wikipedia as the information source. The user should be able to then use the application to 'chat' with the LLM, and find correct information about the given subject.

  

## The Application Lifecycle

  

In the case of our query regarding the new Christopher Nolan film 'Oppenheimer', the application would flow as follows:

  

1. The user types the following command into the terminal: `python -m wiki_converser --chat`

2. The chatbot runs, and the user asks the question, receiving an incorrect response.

  

[Screenshot of Chatbot failure](./assets/readme_images/chat-fail.png)

  

3. The user exits the application, and runs the following command: `python -m wiki_converser --load 'Oppenheimer (film)'`

  

4. The application searches wikiepedia for the desired article, and loads the text of that article to the vector store.

  

[Screenshot of Load Success](./assets/readme_images/chat-success.png)

  

5. The user types the initial command into the terminal: `python -m wiki_converser --chat`

  

6. The chatbut runs, and returns a correct response when prompted by the user.

  

[Screenshot of Chat Success](./assets/readme_images/chat-success.png)

  
  

## Prerequisites

  

In order for this application to run, consultants need the following:

  

- Pinecone API Key, Index and Environment Region: [https://www.pinecone.io/](https://www.pinecone.io/)

  

- OpenAI API Key: https://platform.openai.com/docs/overview

  

NOTE: Consultants will need to register to both of these platforms in order to complete these steps.

  

- Dependencies (all dependencies are outlined in the requirements.txt file.)

  

- .env file: Should contain the following variables:

    - PINECONE_API_KEY

    - PINECONE_INDEX_NAME

   - PINECONE_ENVIRONMENT_REGION

   - OPENAI_API_KEY