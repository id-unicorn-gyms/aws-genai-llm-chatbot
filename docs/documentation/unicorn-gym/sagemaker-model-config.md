# Adding HuggingFace and Sagemaker Jumpstart model to config file

To add Sagemaker Jumpstart or Huggingface model, you need to edit config.json file located in `aws-genai-llm-chatbot/bin` directory
Model can be add by inserting model description inside following json block

```
"llms": {
    "sagemaker": [
    //insert your sagemaker jumpstart and huggingface model descriptions here
    
    
    ]
}
```

Following is example of a Sagemaker model description
```
    {
        "name": "LLamaV3_1_8B_Instruct",
        "endpointName": "meta-LLama3-1-8b-instruct",
        "jumpstart": {
          "model": "META_TEXTGENERATION_LLAMA_3_1_8B_INSTRUCT_2_1_0"
        },
        "instanceType": "ml.g5.4xlarge"
    }
   ```
In the example above, value "name" and "endpointName" can be defined freely by you as long as they are unique. "model" can be looked up from the file `jumpstart-model.d.ts` located in `aws-genai-llm-chatbot/node_modules/@cdklabs/generative-ai-cdk-constructs/lib/patterns/gen-ai/aws-model-deployment-sagemaker` folder. This file is generated during build time and will contain all sagemaker jumpstart models at the time the build is run. 
"InstanceType" can be checked in Sagemaker Jumpstart console when you choose menu deploy for the model.

Following is example of a HuggingFace model description
```
{
        "name": "Llama3_8B_sahabatai_v1_instruct",
        "huggingface": {
          "modelId": "GoToCompany/llama3-8b-cpt-sahabatai-v1-instruct",
          "container": {
            "repositoryName": "huggingface-pytorch-tgi-inference",
            "tag": "2.4.0-tgi2.4.0-gpu-py311-cu124-ubuntu22.04"
          }
        },
        "instanceType": "ml.g5.2xlarge",
        "startupHealthCheckTimeoutInSeconds": 300,
        "environments": {
          "SM_NUM_GPUS": "1",
          "MAX_INPUT_LENGTH": "1024",
          "MAX_BATCH_PREFILL_TOKENS": "2048",
          "MAX_BATCH_TOTAL_TOKENS": "8192"
        }
      }
```

HuggingFace model description have more information that must be defined in the config compared to Sagemaker Jumpstart model.
Here are how to fill the value for the HuggingFace model descriptions fields:

| Field                    | Value                                                                                            |
|--------------------------|--------------------------------------------------------------------------------------------------|
| modelId                  | ModelID can be checked from Model Card at HuggingFace website                                    |
| repositoryName           | Look repository name from https://github.com/aws/deep-learning-containers/releases?q=tgi+AND+gpu |
| tag                      | Look Image tag from https://github.com/aws/deep-learning-containers/releases?q=tgi+AND+gpu       |
| instanceType             | Check required instance type in HuggingFace deployment instructions for AWS                      |
| SM_NUM_GPUS              | Number of GPU used per replica, check model card at HuggingFace                                  |
| MAX_INPUT_LENGTH         | Maximum length of input text, check model card at HuggingFace                                    |
| MAX_BATCH_PREFILL_TOKENS | Limits the number of tokens in the prefill (input tokenizations) operations                      |
| MAX_BATCH_TOTAL_TOKENS   | Limits the number of tokens that can be processed in parallel during the generation.             |

Number of parameters required for model configurations can vary between HuggingFace models.

__Important Note:__ HuggingFace and Sagemaker Jumpstart models are deployed during solution deployment and will be charged despite it is used or not. Remove the models from configurations and redeploy solutions to delete the models if not used for a long time to save cost.

