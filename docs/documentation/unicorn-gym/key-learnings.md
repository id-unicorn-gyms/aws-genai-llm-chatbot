# Key Learnings during Project Implementation

## 1. CloudFormation takes too long to execute/Iterate on changes
While using IaC approach, CloudFormation takes a relatively long time to deploy a stack. Not to mentioned, during any changes of deployed stack, to re-deploy it also takes a very long time (~10-20 minutes to deploy, and ~30 minutes to rollback.)

## 2. Baseline project doesn't have GraphQL API Documentation for deploying client app
While deploying the app using the baseline project, GraphQL is being used. However, there is not a documentation on a baseline to explain about GraphQL part, causing the developer to interpret based on the code itself. This creates a longer time to undestand the code.

## 3. Baseline project has combined GraphQL for admin and client. Not a best practice.
Inside the code, Admin and Client side has been combined in 1 single GraphQL. This cause the security risk, and also management issue if this project is going to be up in production. This is not following the best practice of security and operations on AWS.

## 4. When deploying baseline project, process marked as completed, but some components are not ready yet.
While deploying, The status changed as completed. However, several components such as ECR Image is not successfully uploaded, and is not being marked as incomplete. This impacts during RAG process, when file is being uploaded to system, but it calls step functions that calls ECR Image to run AWS Batch job to upload data to S3. This ECR Image is not fully downloaded, causing the upload file to fail.

## 5. Baseline project doesn't support ARM based compute
As to build the project requires the compute, the baseline project doesn't mentioned that ARM-based compute is possible to be run. Thus, while deploying the CDK, the error message doesn't explicitly mentioned that ARM-based can't be used.

## 6. To Support GraphQL APIKey, schema need to be modified a lot
Not everyone is using Cognito to authenticate to the system. Thus, APIKey is more generally being used. While APIKey wants to be integrated with GraphQL, the effort is very high, as the modification of schema is required based on [this link](https://docs.aws.amazon.com/appsync/latest/devguide/security-authz.html#using-additional-authorization-modes)

## 7. Client iFrame and GraphQL is not extendable
in baseline project While the iFrame HTML Tags being used to create a pluggable UI, GraphQL is not compatible to be embedded due to tight integration with Cognito.
 
## 8. RAG Performance depends on Retrieval Methods and Embedding models
As the RAG being developed in multiple Embeddings model, (intfloat/multilingual-e5-large - size 1024, sentence-transformers/all-MiniLM-L6-v2 - size 384) and the approach to retrieve the similarity varies (Negative Inner Product, Cosine, and Eucledian), the performance of RAG also varies.

Conclusion:
* sentence-transformers/all-MiniLM-L6-v2 works best with Cosine > Eucledian > Negative Inner Product
* intfloat/multilingual-e5-large works best with Eucledian > Cosine > Negative Inner Product

If want to approach using metrices, [RAGAS](https://docs.ragas.io/en/stable/) might be the solution to do so

## 9. Front End Baseline project needs improvement on bedrock configuration
During the config file in deployment, when the bedrock is not being used on baseline project, The UI is still displaying Bedrock Models. While being tested, the bedrock models couldn't be used. This requires an Improvement from front-end side to not display the bedrock models, while bedrock is not being chosen as a model provider.

## 10. /doc in Q Developer failed to create README file, as the folder is "Too Large"
While creating the documentation using Q Developer /doc feature to create README file, the Q Developer display the error as "Folder too large", even though the account has used pro license. This requires manual README file creation.

## 11. Service Quota limit on SageMaker for larger instances to deploy LLM is required prior deployment
As the LLM models required to use relatively larger model, Increasing service quota is required. Thus, not all models can be deployed in 1 single account.