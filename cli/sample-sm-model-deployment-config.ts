import {
  Modality,
  ModelInterface,
  SagemakerModelDeploymentConf,
} from "../lib/shared/types";

export const SagemakerModelEndpointSelections: {
  [key: string]: SagemakerModelDeploymentConf;
} = {
  "FalconLite [ml.g5.12xlarge]": {
    name: "FalconLite",
    huggingface: {
      modelId: "amazon/FalconLite",
      container: {
        repositoryName: "huggingface-pytorch-tgi-inference",
        tag: "2.0.1-tgi0.9.3-gpu-py39-cu118-ubuntu20.04",
      },
    },
    instanceType: "ML_G5_12XLARGE",
    startupHealthCheckTimeoutInSeconds: 600,
    environments: {
      SM_NUM_GPUS: JSON.stringify(4),
      MAX_INPUT_LENGTH: JSON.stringify(12000),
      MAX_TOTAL_TOKENS: JSON.stringify(12001),
      HF_MODEL_QUANTIZE: "gptq",
      TRUST_REMOTE_CODE: JSON.stringify(true),
      MAX_BATCH_PREFILL_TOKENS: JSON.stringify(12001),
      MAX_BATCH_TOTAL_TOKENS: JSON.stringify(12001),
      GPTQ_BITS: JSON.stringify(4),
      GPTQ_GROUPSIZE: JSON.stringify(128),
      DNTK_ALPHA_SCALER: JSON.stringify(0.25),
    },
  },
  "Idefics_9b (Multimodal) [ml.g5.12xlarge]": {
    name: "IDEFICS9B",
    huggingface: {
      modelId: "HuggingFaceM4/idefics-9b-instruct",
      container: {
        repositoryName: "huggingface-pytorch-tgi-inference",
        tag: "2.0.1-tgi1.1.0-gpu-py39-cu118-ubuntu20.04",
      },
    },
    instanceType: "ML_G5_12XLARGE",
    startupHealthCheckTimeoutInSeconds: 300,
    environments: {
      SM_NUM_GPUS: JSON.stringify(4),
      MAX_INPUT_LENGTH: JSON.stringify(1024),
      MAX_TOTAL_TOKENS: JSON.stringify(2048),
      MAX_BATCH_TOTAL_TOKENS: JSON.stringify(8192),
    },
    inputModalities: [Modality.Text, Modality.Image],
    outputModalities: [Modality.Text],
    interface: ModelInterface.MultiModal,
    ragSupported: false,
  },
  "Idefics_80b (Multimodal) [ml.g5.48xlarge]": {
    name: "IDEFICS80B",
    huggingface: {
      modelId: "HuggingFaceM4/idefics-80b-instruct",
      container: {
        repositoryName: "huggingface-pytorch-tgi-inference",
        tag: "2.0.1-tgi1.1.0-gpu-py39-cu118-ubuntu20.04",
      },
    },
    instanceType: "ML_G5_48XLARGE",
    startupHealthCheckTimeoutInSeconds: 600,
    environments: {
      SM_NUM_GPUS: JSON.stringify(8),
      MAX_INPUT_LENGTH: JSON.stringify(1024),
      MAX_TOTAL_TOKENS: JSON.stringify(2048),
      MAX_BATCH_TOTAL_TOKENS: JSON.stringify(8192),
      // quantization required to work with ml.g5.48xlarge
      // comment if deploying with ml.p4d or ml.p4e instances
      HF_MODEL_QUANTIZE: "bitsandbytes",
    },
    inputModalities: [Modality.Text, Modality.Image],
    outputModalities: [Modality.Text],
    interface: ModelInterface.MultiModal,
    ragSupported: false,
  },
  "Llama2_13b_Chat [ml.g5.12xlarge]": {
    name: "LLamaV2_13B_Chat",
    endpointName: "meta-LLama2-13b-chat",
    jumpstart: {
      model: "META_TEXTGENERATION_LLAMA_2_13B_F_2_0_2",
    },
    instanceType: "ML_G5_12XLARGE",
  },
  "Mistral7b_Instruct 0.1 [ml.g5.2xlarge]": {
    name: "Mistral7BInstruct",
    huggingface: {
      modelId: "mistralai/Mistral-7B-Instruct-v0.1",
      container: {
        repositoryName: "huggingface-pytorch-tgi-inference",
        tag: "2.1.1-tgi2.0.0-gpu-py310-cu121-ubuntu22.04",
      },
    },
    instanceType: "ML_G5_2XLARGE",
    startupHealthCheckTimeoutInSeconds: 300,
    environments: {
      SM_NUM_GPUS: JSON.stringify(1),
      MAX_INPUT_LENGTH: JSON.stringify(2048),
      MAX_TOTAL_TOKENS: JSON.stringify(4096),
    },
  },
  "Mistral7b_Instruct 0.2 [ml.g5.2xlarge]": {
    name: "Mistral7BInstruct2",
    huggingface: {
      modelId: "mistralai/Mistral-7B-Instruct-v0.2",
      container: {
        repositoryName: "huggingface-pytorch-tgi-inference",
        tag: "2.1.1-tgi2.0.0-gpu-py310-cu121-ubuntu22.04",
      },
    },
    instanceType: "ML_G5_2XLARGE",
    startupHealthCheckTimeoutInSeconds: 300,
    environments: {
      SM_NUM_GPUS: JSON.stringify(1),
      MAX_INPUT_LENGTH: JSON.stringify(2048),
      MAX_TOTAL_TOKENS: JSON.stringify(4096),
      MAX_CONCURRENT_REQUESTS: JSON.stringify(4),
    },
  },
  "Mistral7b_Instruct 0.3 [ml.g5.2xlarge]": {
    name: "Mistral7b_Instruct3",
    endpointName: "Mistral-7B-Instruct-v0-3",
    jumpstart: {
      model: "HUGGINGFACE_LLM_MISTRAL_7B_INSTRUCT_3_0_0",
    },
    instanceType: "ML_G5_2XLARGE",
  },
  "Mixtral_8x7B_Instruct 0.1 [ml.g5.48xlarge]": {
    name: "Mixtral8x7binstruct",
    huggingface: {
      modelId: "mistralai/Mixtral-8x7B-Instruct-v0.1",
      container: {
        repositoryName: "huggingface-pytorch-tgi-inference",
        tag: "2.1.1-tgi2.0.0-gpu-py310-cu121-ubuntu22.04",
      },
    },
    instanceType: "ML_G5_48XLARGE",
    startupHealthCheckTimeoutInSeconds: 300,
    environments: {
      SM_NUM_GPUS: JSON.stringify(8),
      MAX_INPUT_LENGTH: JSON.stringify(24576),
      MAX_TOTAL_TOKENS: JSON.stringify(32768),
      MAX_BATCH_PREFILL_TOKENS: JSON.stringify(24576),
      MAX_CONCURRENT_REQUESTS: JSON.stringify(4),
    },
  },
};
