# Installation Guide

## Environment Setup

to deploy, there are 2 approaches you can do:
1. Remote Access to EC2 Instance
2. Local Machine.

### Remote Access to EC2 Instance
to do remote access, first you need to create EC2 Instance

1. Open Your AWS Console and go to [EC2 Console](https://ap-southeast-3.console.aws.amazon.com/ec2/home?region=ap-southeast-3#Home:)
2. In Right orange button, click `Launch Instances`
3. Fill the name of your server (Example: `Chatbot EC2 Remote`)
4. Choose the image as `Amazon Linux`
5. in **Amazon Machine Image**, Choose `Amazon Linux 2023 AMI`
6. For your instance type, choose `m5.large`
7. In Key Pair, choose your key pair. If you don't have it, Click `Create new key pair` (Choose `.pem` for Mac users, and choose `.ppk` for Windows users)
8. In Network Settings, Change the **Allow the SSH Traffic from** to `My IP`
9. On Configure Storage, Change the Volume to `20`, and using `gp3` Root volume
10. Once it's done, on the right side, Click `Launch Instance`

You are required to wait several minutes before the EC2 instance ready to be used.

Now, you need to follow the Local machine guide

### Local Machine

If are using a local machine, verify that your environment satisfies the following prerequisites:

You have:

1. An [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)

2. An [IAM User](https://console.aws.amazon.com/iamv2/home?#/users/create) with AdministratorAccess policy granted (for production, we recommend restricting access as needed)

3. [NodeJS 18 or 20](https://nodejs.org/en/download/) installed (NodeJS Version above 20 is not compatible. Please downgrade your NodeJS version if necessary. We recommend to use Virtual Environment to manage the dependencies easier, refer to this link: https://www.dataquest.io/blog/a-complete-guide-to-python-virtual-environments/)

If you are using [nvm](https://github.com/nvm-sh/nvm) you can run the following before proceeding

```
nvm install 18 && nvm use 18
```

or

```
nvm install 20 && nvm use 20
```

4. [AWS CLI](https://aws.amazon.com/cli/) installed and configured to use with your AWS account

5. [AWS CDK CLI](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html) installed

6. [Docker](https://docs.docker.com/get-docker/) installed

 * N.B. [buildx](https://github.com/docker/buildx) is also required. For Windows and macOS `buildx` [is included](https://github.com/docker/buildx#windows-and-macos) in [Docker Desktop](https://docs.docker.com/desktop/)

7. [Python 3+](https://www.python.org/downloads/) installed

## Deployment

**Step 1.** Clone the repository (Using the main branch)

```
git clone https://github.com/id-unicorn-gyms/aws-genai-llm-chatbot.git
```

**Step 2.** Move into the cloned repository.

```
cd aws-genai-llm-chatbot
```

**Step 3.** Install the project dependencies and build the project.

```
npm ci && npm run build
```

**Step 4.** (Optional) Run the unit tests

```
npm run test && pip install -r pytest_requirements.txt && pytest tests
```

**Step 5.** Once done, run the configuration command to help you set up the solution with the features you need:

```
npm run config
```

You'll be prompted to configure the different aspects of the solution, such as:

* The LLMs or MLMs to enable (we support all models provided by Bedrock that [were enabled](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) along with SageMaker hosted Idefics, FalconLite, Mistral and more to come).
* Setup of the RAG system: engine selection (i.e. Aurora w/ pgvector, OpenSearch, Kendra).
* Embeddings selection.
* Limit accessibility to website and backend to VPC (private chatbot).
* Add existing Amazon Kendra indices as RAG sources
* For SageMaker Model, make sure you have the capacity to Deploy the instance. Please check your **Service Quota for Number of Inferences.**

When done, answer `Y` to create or update your configuration, depends on what you'd like to have.

Your configuration is now stored under `bin/config.json`. You can re-run the `npm run config` command as needed to update your `config.json`

**Step 6.** (Optional) Bootstrap AWS CDK on the target account and region

Note: 
* This is required if you have never used AWS CDK on this account and region combination. ([More information on CDK bootstrapping](https://docs.aws.amazon.com/cdk/latest/guide/cli.html#cli-bootstrap)).
* Please change the AccountID and Region below.

```
npm run cdk bootstrap aws://{targetAccountId}/{targetRegion}
```

You can now deploy by running:

```
npm run cdk deploy
```

Note: This step duration can vary greatly, depending on the Constructs you are deploying.

You can view the progress of your CDK deployment in the [CloudFormation console](https://console.aws.amazon.com/cloudformation/home) in the selected region.

**Step 7.** Once deployed, take note of the `User Interface`, `User Pool` and, if you want to interact with [3P models providers](https://aws-samples.github.io/aws-genai-llm-chatbot/guide/deploy.html#3p-models-providers), the `Secret` where to store `API_KEYS` to access 3P model providers.

```
...
Outputs:
GenAIChatBotStack.UserInterfaceUserInterfaceDomanNameXXXXXXXX = dxxxxxxxxxxxxx.cloudfront.net
GenAIChatBotStack.AuthenticationUserPoolLinkXXXXX = https://xxxxx.console.aws.amazon.com/cognito/v2/idp/user-pools/xxxxx_XXXXX/users?region=xxxxx
GenAIChatBotStack.ApiKeysSecretNameXXXX = ApiKeysSecretName-xxxxxx
...
```

**Step 8.** Open the generated Cognito User Pool Link from outputs above i.e. `https://xxxxx.console.aws.amazon.com/cognito/v2/idp/user-pools/xxxxx_XXXXX/users?region=xxxxx`

**Step 9.** Add a user that will be used to log into the web interface.

**Step 10.** Open the `User Interface` Url for the outputs above, i.e. `dxxxxxxxxxxxxx.cloudfront.net`.

**Step 11.** Login with the user created in **Step 8** and follow the instructions.

Your Application is ready to use!
