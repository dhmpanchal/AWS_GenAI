import boto3
import json
import random

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
bedrock = boto3.client(service_name="bedrock", region_name="us-east-1")  
s3 = boto3.client("s3")
model_id = "amazon.nova-reel-v1:0"
bucket_name = "gen-ai-exercise-fs-938176218293-us-east-1-an"

# prompt = "A person dancing on a mountain."
prompt = "A wakinng cat in a forest, cinematic lighting, 4k, ultra realistic, trending on artstation, octane render, unreal engine, hyper detailed, volumetric lighting, cinematic lighting, photorealistic, 8k, high quality, sharp focus"

seed = random.randint(0, 2147483646)

model_input = {
    "taskType": "TEXT_VIDEO",
    "textToVideoParams": {"text": prompt},
    "videoGenerationConfig": {
        "fps": 24,
        "durationSeconds": 6,
        "dimension": "1280x720",
        "seed": seed,
    },
}

output_config = {
    "s3OutputDataConfig": {
        "s3Uri": f"s3://{bucket_name}/video/"
    }
}

response = bedrock_runtime.start_async_invoke(
    modelId=model_id,
    modelInput=model_input,
    outputDataConfig=output_config,
)

invocation_arn = response["invocationArn"]
print("✅ Job submitted!")
print("Invocation ARN:", invocation_arn)

job_status = bedrock_runtime.get_async_invoke(invocationArn=invocation_arn)
print("Current Status:", job_status["status"])
