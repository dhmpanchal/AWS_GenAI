import boto3
import json

MODEL_ID = "amazon.nova-micro-v1:0"
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId=MODEL_ID,
    guardrailVersion="DRAFT",
    body=json.dumps({
        "schemaVersion": "messages-v1",
        "messages": [{"role": "user", "content": [{"text": "Rewrite this sentence for me in a formal tone: You are very good at your job."}]}],
        "inferenceConfig": {"maxTokens": 500, "topK": 20, "temperature": 0.7}
    })
)

result = response['body'].read()
print(result)