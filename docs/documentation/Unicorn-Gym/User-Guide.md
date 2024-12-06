# User Guide

We are going to explain the features and things you are able to do in the application.

## Prerequisites
You need to follow [installation](./Installation.md) guide before proceeding to this guide

# Features
## Chatbot - Playground
1. On the right menu, click `Playground` on the Chatbot menu
2. You will find the page like the screen below

<img src="./image/ChatbotPlayground/2.png" alt="Playground Page"/>

3. Change your preferred model, by clicking the dropdown list of model
4. Enter your inquiries/prompts in the textbox message
5. Click `Enter` on your keyboard, or you can click `Send`

<img src="./image/ChatbotPlayground/5.png" alt="Chatbot Model selection Page"/>

6. You will be able to read the result

<img src="./image/ChatbotPlayground/2.png" alt="Chatbot Result"/>

If you have followed the `RAG - Workspaces` Guidance, you can also integrate your RAG in this chatbot

7. Please specify your model and Workspaces for your RAG.
8. do as step 4 and 5 (Enter your prompt, and click `Enter` or `Send`)

<img src="./image/ChatbotPlayground/8.png" alt="RAG Chatbot"/>

9. It will answer your question, based on the retrieved result.

<img src="./image/ChatbotPlayground/9.png" alt="RAG Result"/>

You can also change your Inference Parameters

10. Click the settings icon below the textbox

<img src="./image/ChatbotPlayground/10.png" alt="Parameter changes Page"/>

11. Please change the parameter based on your preferences, and click `Save Changes`

<img src="./image/ChatbotPlayground/11.png" alt="List of parameters"/>

---

## Chatbot - Multi-chat Playground
You need to create a Workspace in order to leverage this feature.

1. On the right menu, click `Multi-chat Playground` on the Chatbot menu
2. You will find the page like the screen below

<img src="./image/ChatbotMultichatPlayground/2.png" alt="Multi-chat Playground Page"/>

Same as Playground, Multi-Chat playground also generated the result from model. However, you are able to compare two models, to decide which Model/RAG strategy you would like to pursue further.

3. Please specify your model and Workspaces for your RAG, you need to choose the different combination.
4. Change your preferred model on both sides, by clicking the dropdown list of model.
5. Enter your inquiries/prompts in the textbox message

<img src="./image/ChatbotMultichatPlayground/5.png" alt="RAG Chatbot"/>

6. It will answer your question, based on the retrieved result.

<img src="./image/ChatbotMultichatPlayground/6.png" alt="RAG Result"/>

7. You can also clear your messages, by click `Clear messages` on the right side.

<img src="./image/ChatbotMultichatPlayground/7.png" alt="Clear Messages Button"/>

You can also change your Inference Parameters

8. Click the settings icon besides the name of the model, you can only change 1 model inference parameter one at a time.

<img src="./image/ChatbotMultichatPlayground/8.png" alt="Parameter changes Page"/>

9. Please change the parameter based on your preferences, and click `Save Changes`

<img src="./image/ChatbotMultichatPlayground/9.png" alt="List of parameters"/>

---

## Chatbot - Sessions
1. On the right menu, click `Sessions` on the Chatbot menu
2. You will find the page like the screen below

<img src="./image/ChatbotSessions/2.png" alt="List of Histories"/>

These are lists of Questions history that has been entered to the system

---

## Chatbot - Models
1. On the right menu, click `Models` on the Chatbot menu
2. You will find the page like the screen below

<img src="./image/ChatbotModels/2.png" alt="List of Models"/>

These are lists of models that is available to be used for your chatbot.

---

## RAG - Dashboard
1. On the right menu, click `Dashboard` on the RAG menu
2. You will find the page like the screen below

<img src="./image/RAGDashboard/2.png" alt="RAG Dashboard Page"/>

These are lists of Workspaces, total vectors, and size of the data. Please follow `RAG - Workspaces` guide to create Workspace

---

## RAG - Semantic Search
You need to create Workspaces first in order to follow this guide

1. On the right menu, click `Semantic Search` on the RAG menu
2. You will find the page like the screen below

<img src="./image/RAGSemanticSearch/2.png" alt="RAG Semantic Search Page"/>

3. Choose your workspace
4. Fill out the search query, and click `Search`

<img src="./image/RAGSemanticSearch/4.png" alt="RAG Semantic Search Page"/>

5. You will see the result below

<img src="./image/RAGSemanticSearch/5.png" alt="RAG Semantic Search Result Page"/>

The result is based on 2 things, Ranking Score and Vector Search Score.

---

## RAG - Workspaces
1. On the right menu, click `Workspaces` on the RAG menu
2. Click `Create Workspace` button at the top left page

<img src="./image/RAGWorkspaces/2.png" alt="RAG Workspace Page"/>

3. Please choose your Workspace Engine, and fill out the name, Model, and also the language that you will process

<img src="./image/RAGWorkspaces/3.png" alt="RAG Workspace config Page"/>

You can also do more additional settings, such as indexing the vector database, metrics, searching, and chunking configuration

4. Click `Additional settings`, and choose the configuration you would like to do
5. Click `Create Workspace`

<img src="./image/RAGWorkspaces/5.png" alt="RAG Workspace config Page"/>

It takes several minutes to create. Once the status of your workspace is Ready, now you can upload the file that you'd like to upload.

6. in files tab on your Workspace, Click `Upload File`

<img src="./image/RAGWorkspaces/6.png" alt="RAG Workspace config Page"/>

7. you can drag and drop your file, or simply by clickling `Choose Files`. It has a limit of file size by up to 100 MB.

<img src="./image/RAGWorkspaces/7.png" alt="RAG Workspace config Page"/>

8. Click `Upload files`

Once uploaded, the file will have status as `Processing`. You need to wait, until the file is `Processed`. Please keep refreshing the page to keep update with the status.

Now, you are ready to use your workspace!

---

## RAG - Embeddings
1. On the right menu, click `Embeddings` on the RAG menu

<img src="./image/RAGEmbeddings/1.png" alt="RAG Embeddings Page"/>

2. Fill out the model that you would like to use (You can use multiple Models)
3. Fill out the input that will be vectorized. You can also add more input by clicking `Add new Input`
4. Click Generate

<img src="./image/RAGEmbeddings/4.png" alt="RAG Embeddings Page"/>

You will see the generated vector from the embeddings model.

<img src="./image/RAGEmbeddings/4-2.png" alt="RAG Embeddings Result Page"/>

---

## RAG - Cross-encoders
Cross-Encoders enables pre-determined the value of similarity between 2 pairs of sentences. Please read [this link](https://www.sbert.net/examples/applications/cross-encoder/README.html) to understand deeper about this concept
1. On the right menu, click `Cross-Encoders` on the RAG menu
2. Fill out The input and passages of the text. These will determine the similarities between multiple pairs of sentences.

<img src="./image/RAGCrossEncoders/2.png" alt="RAG RAG Cross Encoders Filled Page"/>

3. Scroll down and click `Rank passages`

The result will rank what will be the closest passages, based on the input.

<img src="./image/RAGCrossEncoders/3.png" alt="RAG RAG Cross Encoders Result Page"/>

---

## RAG - Engines
1. On the right menu, click `Engines` on the RAG menu
2. You will find the page like the screen below

<img src="./image/RAGEngines/2.png" alt="RAG Engines Page"/>

These are lists of Vector Database Engines that can be supported on this system. Currently, only Amazon Aurora and Bedrock Knowledge Base that is enabled. You can modify this by changing the config on [Installation Guide](./Installation.md) on Step 5.