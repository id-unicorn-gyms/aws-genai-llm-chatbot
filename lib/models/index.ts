import * as ssm from "aws-cdk-lib/aws-ssm";
import { Construct } from "constructs";
import * as iam from "aws-cdk-lib/aws-iam";
import * as secretsmanager from "aws-cdk-lib/aws-secretsmanager";
import { Shared } from "../shared";
import {
  Modality,
  ModelInterface,
  SageMakerModelEndpoint,
  SystemConfig,
} from "../shared/types";
import {
  HuggingFaceSageMakerEndpoint,
  JumpStartSageMakerEndpoint,
  SageMakerInstanceType,
  DeepLearningContainerImage,
  JumpStartModel,
} from "@cdklabs/generative-ai-cdk-constructs";
import { NagSuppressions } from "cdk-nag";
import { createStartSchedule, createStopSchedule } from "./sagemaker-schedule";

export interface ModelsProps {
  readonly config: SystemConfig;
  readonly shared: Shared;
}

export class Models extends Construct {
  public readonly models: SageMakerModelEndpoint[];
  public readonly modelsParameter: ssm.StringParameter;

  constructor(scope: Construct, id: string, props: ModelsProps) {
    super(scope, id);

    const models: SageMakerModelEndpoint[] = [];

    let hfTokenSecret: secretsmanager.Secret | undefined;
    if (props.config.llms.huggingfaceApiSecretArn) {
      hfTokenSecret = secretsmanager.Secret.fromSecretCompleteArn(
        this,
        "HFTokenSecret",
        props.config.llms.huggingfaceApiSecretArn
      ) as secretsmanager.Secret;
    }

    for (const sagemakerEndpoint of props.config.llms.sagemaker) {
      if (sagemakerEndpoint.jumpstart) {
        const js = sagemakerEndpoint.jumpstart;
        const endpointName =
          sagemakerEndpoint.endpointName ?? sagemakerEndpoint.name;

        const modelEndpoint = new JumpStartSageMakerEndpoint(
          this,
          sagemakerEndpoint.name,
          {
            model: JumpStartModel.of(js.model),
            instanceType: SageMakerInstanceType.of(
              sagemakerEndpoint.instanceType.toUpperCase()
            ),
            vpcConfig: {
              securityGroupIds: [props.shared.vpc.vpcDefaultSecurityGroup],
              subnets: props.shared.vpc.privateSubnets.map(
                (subnet) => subnet.subnetId
              ),
            },
            endpointName: endpointName,
          }
        );
        this.suppressCdkNagWarningForEndpointRole(modelEndpoint.role);
        models.push({
          name: endpointName,
          endpoint: modelEndpoint.cfnEndpoint,
          responseStreamingSupported:
            sagemakerEndpoint.responseStreamingSupported ?? false,
          inputModalities: sagemakerEndpoint.inputModalities
            ? sagemakerEndpoint.inputModalities.map(
                (a) => Modality[a as keyof typeof Modality]
              )
            : [Modality.Text],
          outputModalities: sagemakerEndpoint.outputModalities
            ? sagemakerEndpoint.outputModalities.map(
                (a) => Modality[a as keyof typeof Modality]
              )
            : [Modality.Text],
          interface: sagemakerEndpoint.interface
            ? ModelInterface[
                sagemakerEndpoint.interface as keyof typeof ModelInterface
              ]
            : ModelInterface.LangChain,
          ragSupported: sagemakerEndpoint.ragSupported ?? true,
        });
      } else if (sagemakerEndpoint.huggingface) {
        const hf = sagemakerEndpoint.huggingface;
        const endpointName =
          sagemakerEndpoint.endpointName ??
          hf.modelId.split("/").join("-").split(".").join("-");
        const modelEndpoint = new HuggingFaceSageMakerEndpoint(
          this,
          sagemakerEndpoint.name,
          {
            modelId: hf.modelId,
            vpcConfig: {
              securityGroupIds: [props.shared.vpc.vpcDefaultSecurityGroup],
              subnets: props.shared.vpc.privateSubnets.map(
                (subnet) => subnet.subnetId
              ),
            },
            container: hf.container
              ? DeepLearningContainerImage.fromDeepLearningContainerImage(
                  hf.container.repositoryName,
                  hf.container.tag
                )
              : DeepLearningContainerImage.HUGGINGFACE_PYTORCH_TGI_INFERENCE_2_1_1_TGI2_0_0_GPU_PY310_CU121_UBUNTU22_04,
            instanceType: SageMakerInstanceType.of(
              sagemakerEndpoint.instanceType.toUpperCase()
            ),
            startupHealthCheckTimeoutInSeconds:
              sagemakerEndpoint.startupHealthCheckTimeoutInSeconds ?? 600,
            endpointName: endpointName,
            environment: sagemakerEndpoint.environments
              ? {
                  ...sagemakerEndpoint.environments,
                  HF_TOKEN:
                    hfTokenSecret?.secretValue?.unsafeUnwrap()?.toString() ||
                    "",
                }
              : {
                  HF_TOKEN:
                    hfTokenSecret?.secretValue?.unsafeUnwrap()?.toString() ||
                    "",
                },
          }
        );

        this.suppressCdkNagWarningForEndpointRole(modelEndpoint.role);
        models.push({
          name: endpointName!,
          endpoint: modelEndpoint.cfnEndpoint,
          responseStreamingSupported:
            sagemakerEndpoint.responseStreamingSupported ?? false,
          inputModalities: sagemakerEndpoint.inputModalities
            ? sagemakerEndpoint.inputModalities.map(
                (a) => Modality[a as keyof typeof Modality]
              )
            : [Modality.Text],
          outputModalities: sagemakerEndpoint.outputModalities
            ? sagemakerEndpoint.outputModalities.map(
                (a) => Modality[a as keyof typeof Modality]
              )
            : [Modality.Text],
          interface: sagemakerEndpoint.interface
            ? ModelInterface[
                sagemakerEndpoint.interface as keyof typeof ModelInterface
              ]
            : ModelInterface.LangChain,
          ragSupported: sagemakerEndpoint.ragSupported ?? true,
        });
      }
    }

    const modelsParameter = new ssm.StringParameter(this, "ModelsParameter", {
      stringValue: JSON.stringify(
        models.map((model) => ({
          name: model.name,
          endpoint: model.endpoint.endpointName,
          responseStreamingSupported: model.responseStreamingSupported,
          inputModalities: model.inputModalities,
          outputModalities: model.outputModalities,
          interface: model.interface,
          ragSupported: model.ragSupported,
        }))
      ),
    });

    this.models = models;
    this.modelsParameter = modelsParameter;

    if (models.length > 0 && props.config.llms?.sagemakerSchedule?.enabled) {
      const schedulerRole: iam.Role = new iam.Role(this, "SchedulerRole", {
        assumedBy: new iam.ServicePrincipal("scheduler.amazonaws.com"),
        description: "Role for Scheduler to interact with SageMaker",
      });

      schedulerRole.addManagedPolicy(
        iam.ManagedPolicy.fromAwsManagedPolicyName("AmazonSageMakerFullAccess")
      );
      this.suppressCdkNagWarningForEndpointRole(schedulerRole);

      models.forEach((model) => {
        createStartSchedule(
          this,
          id,
          model.endpoint,
          schedulerRole,
          props.config
        );
        createStopSchedule(
          this,
          id,
          model.endpoint,
          schedulerRole,
          props.config
        );
      });
    }
  }

  private suppressCdkNagWarningForEndpointRole(role: iam.Role) {
    NagSuppressions.addResourceSuppressions(
      role,
      [
        {
          id: "AwsSolutions-IAM4",
          reason:
            "Gives user ability to deploy and delete endpoints from the UI.",
        },
        {
          id: "AwsSolutions-IAM5",
          reason:
            "Gives user ability to deploy and delete endpoints from the UI.",
        },
      ],
      true
    );
  }
}
