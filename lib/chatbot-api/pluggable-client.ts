import * as path from "path";
import * as cdk from "aws-cdk-lib";
import { SystemConfig } from "../shared/types";
import { Construct } from "constructs";
import * as cognito from "aws-cdk-lib/aws-cognito";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as logs from "aws-cdk-lib/aws-logs";
import * as ssm from "aws-cdk-lib/aws-ssm";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import { ITopic } from "aws-cdk-lib/aws-sns";
import { Shared } from "../shared";
import { readFileSync } from "fs";
import * as s3 from "aws-cdk-lib/aws-s3";

export interface PluggableClientProps {
    readonly shared: Shared;
    readonly config: SystemConfig;
    readonly userPool: cognito.UserPool;
    readonly sessionsTable: dynamodb.Table;
    readonly byUserIdIndex: string;
    readonly filesBucket: s3.Bucket;
    readonly topic: ITopic;
}

export class PluggableClient extends Construct {

    readonly lambdaPluggableClient: lambda.Function;
    constructor(scope: Construct, id: string, props: PluggableClientProps) {
        super(scope, id);

        const lambdaSecurityGroup = new ec2.SecurityGroup(this, "ApiSecurityGroup", {
            vpc: props.shared.vpc,
          });

        const lambdaPluggableClient = new lambda.Function(this, "lambdaPluggableClient", {
            description: "Lambda to accept chat request from pluggable FE",
            code: lambda.Code.fromInline(
                readFileSync(
                    path.join(__dirname, "./functions/pluggable-client/index.py"),
                    "utf8"
                )
            ),
            handler: "index.handler",
            runtime: props.shared.pythonRuntime,
            logRetention: props.config.logRetention ?? logs.RetentionDays.ONE_WEEK,
            timeout: cdk.Duration.minutes(15),
            tracing: props.config.advancedMonitoring
            ? lambda.Tracing.ACTIVE
            : lambda.Tracing.DISABLED,
            securityGroups: [lambdaSecurityGroup],
            vpc: props.shared.vpc,
            vpcSubnets: props.shared.vpc.privateSubnets as ec2.SubnetSelection,
            layers: [props.shared.powerToolsLayer, props.shared.commonLayer],
            environment: {
                SNS_TOPIC_ARN: props.topic.topicArn,
            },
            memorySize: 256,
            architecture: props.shared.lambdaArchitecture,
        });

        this.lambdaPluggableClient = lambdaPluggableClient;

        function addPermissions(clientHandler: lambda.Function) {
            props.shared.configParameter.grantRead(clientHandler);
            props.shared.apiKeysSecret.grantRead(clientHandler);
            props.shared.xOriginVerifySecret.grantRead(clientHandler);
            props.sessionsTable.grantReadWriteData(clientHandler);
            props.shared.kmsKey.grantEncrypt(clientHandler);


        }

        addPermissions(lambdaPluggableClient);
        props.topic.grantPublish(lambdaPluggableClient);

    }
}