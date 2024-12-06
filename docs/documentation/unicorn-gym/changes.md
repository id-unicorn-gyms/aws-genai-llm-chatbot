# Changes to the baseline repository #

During the unicorn gym we are making several changes to the baseline repository to make the solutions more extensible and can utilize newer models available in Sagemaker Jumpstart and HuggingFace. 
This will benefit regions who does not have Bedrock yet and to showcase to customer who must use in country services.

We also add separate endpoint for client application to consume the Gen AI APIs for users that prefer not to use Cognito user pool.

## Deployable in Jakarta region
As of now (Dec 2024), [original repo](https://github.com/aws-samples/aws-genai-llm-chatbot) can't be deployed to Jakarta region.

Necessary changes, including in the dependency libraries, are made to make it deployable in Jakarta region.

## Model Selection
As of now (Dec 2024), in [original repo](https://github.com/aws-samples/aws-genai-llm-chatbot) support several Sagemaker model deployments.
Any new models to be added, code change needed in this [file](https://github.com/aws-samples/aws-genai-llm-chatbot/blob/main/lib/models/index.ts).

In order to make the solution able to adapt new models easily we decide to externalize both HuggingFace model configurations and Sagemaker Jumpstart model configurations to `config.json` located in `aws-genai-llm-chatbot/bin`
Benefit of this changes is that the code become easier to read and it is easier to add new models.
We still need to redeploy the solutions every time we add or remove models from the configuration file.

## Prompt Template Management
As of now (Dec 2024), in [original repo](https://github.com/aws-samples/aws-genai-llm-chatbot), template for `prompt`, `prompt Q&A`, and `prompt condensed Q&A` are hardcoded for every model adapter.

We improve the implementation so admin are allows to configure those templates from DynamoDB. Prompt templates update are applied without any code rebuilding and redeployment.


## New Endpoint for Gen AI API to be Consumed by Client App
Existing endpoint does not separate between Admin UI and user UI so only have single endpoint that enforce the use Cognito user pool for authentication and use of Amplify for client application.
We are adding a second endpoint that can be utilize by user who wants to have their own authentication mechanism for user UI
The new endpoint is using common REST API that currently is easier to adopt. The trade off is this solution will not support streaming output

## New Client Application
We are adding reference implementation client applications that will connect to the new endpoint.

## Architecture Changes

In the following diagram, new components are light red rectangles, changed components are light green rectangles and existing components are using white rectangle 
![Architecture Diagram](./image/General%20TAP-unicorn-Page-1.drawio.png)

UI for enduser will connect to Load Balancer that will forward to two Lambda, Lambda Incoming and Lambda Outgoing). Lambda incoming will connect to SNS then SQS, bypassing the Appsync and Lambda Resolver for Admin UI. This changes enables clent app to use other authentication than Cognito user pool.
Existing lambda langchain is modified to externalize the configuration of Sagemaker Jumpstart and HuggingFace models to configuration files.
Another changes is providing DynamoDB to store prompt template.


