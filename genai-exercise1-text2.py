import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
model_id = 'amazon.nova-micro-v1:0'

payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "text": "Tell me what type of dances people do."
                }
            ]
        }
    ]
}

payload_json = json.dumps(payload)

response = bedrock.invoke_model_with_response_stream(
    modelId=model_id,
    body=payload_json,
    contentType='application/json',
    accept='application/json'
)

stream = response['body']
full_text = ""

print("Receiving response stream:")
for event in stream:
    chunk = event['chunk']
    chunk_str = chunk.get('bytes', b'').decode('utf-8')

    try:
        json_chunk = json.loads(chunk_str)

        if "contentBlockDelta" in json_chunk:
            delta = json_chunk["contentBlockDelta"]["delta"]
            text = delta.get("text", "")
            full_text += text
            print(text, end='') 

    except json.JSONDecodeError:
        continue