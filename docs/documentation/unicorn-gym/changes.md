# Changes to the baseline repository #

During the unicorn gym we are making several changes to the baseline repository to make the solutions more extensible and can utilize newer models available in Sagemaker Jumpstart and HuggingFace. This will benefit regions who does not have Bedrock yet and to showcase to customer who must use in country services.
We also change the UI and some backend to make it more open for user that choose not to use Cognito user pool

## Model Selection ##
To make the solutions able to adapt new models easily we decide to externalize both HuggingFace model configurations and Sagemaker Jumpstart model configurations to `config.json` located in `aws-genai-llm-chatbot/bin`
Benefit of this changes is that the code become easier to read and it is easier to add new models.
We still need to redeploy the solutions every time we add or remove models from the configuration file.

## New endpoint ##
Existing endpoint does not separate between Admin UI and user UI so only have single endpoint that enforce the use Cognito user pool for authentication and use of Amplify for client application.
We are adding a second endpoint that can be utilize by user who wants to have their own authentication mechanism for user UI
The new endpoint is using common REST API that currently is easier to adopt. The trade off is this solution will not support streaming output

## New Client Application ##
We are adding reference implementation client applications that will connect to the new endpoint.

## Architecture Changes ##

In the following diagram, new components are light red rectangles, changed components are light green rectangles and existing components are using white rectangle 


