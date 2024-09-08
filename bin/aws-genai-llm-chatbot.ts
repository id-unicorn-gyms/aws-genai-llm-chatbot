#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import "source-map-support/register";
import { AwsGenAILLMChatbotStack } from "../lib/aws-genai-llm-chatbot-stack";
import { AwsSolutionsChecks } from "cdk-nag";
import { getConfig } from "./config";
import { Aspects } from "aws-cdk-lib";
import { JumpStartConstants } from "@cdklabs/generative-ai-cdk-constructs/lib/patterns/gen-ai/aws-model-deployment-sagemaker/private/jumpstart-constants";

const app = new cdk.App();

const config = getConfig();

// TODO: fix https://github.com/awslabs/generative-ai-cdk-constructs/blob/main/src/patterns/gen-ai/aws-model-deployment-sagemaker/private/jumpstart-constants.ts
JumpStartConstants.JUMPSTART_LAUNCHED_REGIONS["ap-southeast-3"] = {
  contentBucket: "jumpstart-cache-prod-ap-southeast-3",
  gatedContentBucket: "jumpstart-private-cache-prod-ap-southeast-3",
};

new AwsGenAILLMChatbotStack(app, `${config.prefix}GenAIChatBotStack`, {
  config,
  env: {
    region: process.env.CDK_DEFAULT_REGION,
    account: process.env.CDK_DEFAULT_ACCOUNT,
  },
});

Aspects.of(app).add(new AwsSolutionsChecks({ verbose: true }));
