import boto3
import json
import datetime
from IPython.display import display, JSON

# Task 2: Initialize Bedrock and Set Defaults
bedrock_agent = boto3.client("bedrock-agent")
bedrock_runtime = boto3.client("bedrock-runtime")
bedrock_agent_runtime = boto3.client("bedrock-agent-runtime")

model_id = "amazon.nova-micro-v1:0"

prompt_name = f"job-description-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

template_text = '''
You are an HR assistant.

Write a professional, inclusive job description using the following inputs:

Job title: {{job_title}}
Responsibilities: {{responsibilities}}
Requirements: {{requirements}}
Location: {{location}}
Work type: {{work_type}}

- Start with a clear summary
- Use concise, inclusive language
- Keep it under 250 words
'''


# Task 3: Create a Prompt Template
# 1. Create a prompt with the specified template and input variables
response = bedrock_agent.create_prompt(
    name=prompt_name,
    description="Generates inclusive job descriptions from structured inputs",
    defaultVariant="v1",
    variants=[
        {
            "name": "v1",
            "modelId": model_id,
            "templateType": "TEXT",
            "templateConfiguration": {
                "text": {
                    "inputVariables": [
                        {"name": "job_title"},
                        {"name": "responsibilities"},
                        {"name": "requirements"},
                        {"name": "location"},
                        {"name": "work_type"}
                    ],
                    "text": template_text
                }
            },
            "inferenceConfiguration": {
                "text": {
                    "maxTokens": 500,
                    "temperature": 0.7,
                    "topP": 0.9,
                    "stopSequences": []
                }
            }
        }
    ]
)
print("\n==================== Response Object ====================\n")
display(JSON(response))

print("\n==================== Prompt ARN ====================\n")
print(response['arn'])

# Task 4: Create a New Version of the Prompt
# Create a prompt version for the newly created prompt
response = bedrock_agent.create_prompt_version(
    description='Initial prompt for creating job description documents.',
    promptIdentifier="arn:aws:bedrock:us-east-1:938176218293:prompt/GH8CTU1R7O"
)

print("\n==================== PROMPT VERSION ARN ====================\n")
print(response["arn"])

# Task 5: Invoke a Model Using the Versioned Prompt Template
# Use the prompt version ARN to call the prompt with input variables with converse API
prompt_arn_with_version = "arn:aws:bedrock:us-east-1:938176218293:prompt/GH8CTU1R7O:1"

response = bedrock_runtime.converse(
    modelId=prompt_arn_with_version,
    promptVariables={
        "job_title": {"text": "UX Designer"},
        "responsibilities": {"text": "Design user interfaces, run usability testing, collaborate with product teams"},
        "requirements": {"text": "3+ years experience, Figma, HTML/CSS knowledge, communication skills"},
        "location": {"text": "New York or remote"},
        "work_type": {"text": "Full-time"}
    }
)

print("\n==================== Response Text ====================\n")
print(response['output']['message']['content'][0]['text'])

# Task 6: Optimize the Prompt
# optimize the prompt with the prompt optimizer API
def handle_response_stream(response):
    try:
        event_stream = response['optimizedPrompt']
        for event in event_stream:
            if 'optimizedPromptEvent' in event:
                print("\n==================== OPTIMIZED PROMPT ====================\n")
                print(event['optimizedPromptEvent']['optimizedPrompt']['textPrompt']['text'])
    except Exception as e:
        raise e


prompt_input = {
    "textPrompt": {
        "text": template_text
    }
}

response = bedrock_agent_runtime.optimize_prompt(
            input=prompt_input,
            targetModelId=model_id
        )

print("\n==================== ORIGINAL PROMPT ====================\n")
print(template_text)
handle_response_stream(response)

# Task 7: Update Prompt and Create New Prompt Version
# Update Prompt and Create New Prompt Version
prompt_identifier = "arn:aws:bedrock:us-east-1:938176218293:prompt/GH8CTU1R7O"

existing_prompt = bedrock_agent.get_prompt(promptIdentifier=prompt_identifier)
print("\n==================== ORIGINAL PROMPT ====================\n")
print(existing_prompt["variants"][0]["templateConfiguration"]["text"]["text"])


updated_variants = existing_prompt["variants"]
for variant in updated_variants:
    if variant["templateType"] == "TEXT":
        variant["templateConfiguration"]["text"]["text"] = "## Role\nYou are an expert HR assistant specializing in crafting compelling, inclusive job descriptions that attract diverse talent.\n\n## Task\nCreate a professional job description that is clear, engaging, and accessible to all candidates.\n\n## Input Information\n\n### Job Title\n{{job_title}}\n\n### Responsibilities\n{{responsibilities}}\n\n### Requirements\n{{requirements}}\n\n### Location\n{{location}}\n\n### Work Type\n{{work_type}}\n\n## Instructions\n\nFollow these guidelines to create an effective job description:\n\n1. **Opening Summary**: Begin with a compelling 2-3 sentence summary that captures the essence of the role and its impact on the organization.\n\n2. **Structure**: Organize the job description into clear sections:\n   - Role Overview\n   - Key Responsibilities (use bullet points for clarity)\n   - Required Qualifications\n   - Location and Work Arrangement\n\n3. **Inclusive Language**: \n   - Use gender-neutral terms and avoid gendered pronouns\n   - Focus on essential qualifications only\n   - Avoid unnecessary jargon or exclusionary phrases\n   - Use \"you will\" instead of passive voice to engage candidates\n   - Replace phrases like \"rockstar\" or \"ninja\" with professional descriptors\n\n4. **Conciseness**: Keep the entire description under 250 words while maintaining clarity and completeness.\n\n5. **Tone**: Maintain a professional yet welcoming tone that reflects organizational values and encourages diverse applicants.\n\nProvide your job description immediately without any preamble, introduction, or additional commentary."


response = bedrock_agent.update_prompt(
    promptIdentifier=prompt_identifier,
    name=existing_prompt["name"],
    description=existing_prompt["description"],
    defaultVariant=existing_prompt["defaultVariant"],
    variants=updated_variants
)

print("\n==================== UPDATED PROMPT ====================\n")

updated_prompt = bedrock_agent.get_prompt(promptIdentifier=prompt_identifier)
print(updated_prompt["variants"][0]["templateConfiguration"]["text"]["text"])

response = bedrock_agent.create_prompt_version(
    description='Optimized prompt for creating job description documents.',
    promptIdentifier=prompt_identifier
)

print("\n==================== PROMPT VERSION ARN ====================\n")
print(response["arn"])

# Task 8: Compare Versions
prompt_arn = "arn:aws:bedrock:us-east-1:938176218293:prompt/GH8CTU1R7O:1"

response = bedrock_runtime.converse(
    modelId=prompt_arn,
    promptVariables={
        "job_title": {"text": "UX Designer"},
        "responsibilities": {"text": "Design user interfaces, run usability testing, collaborate with product teams"},
        "requirements": {"text": "3+ years experience, Figma, HTML/CSS knowledge, communication skills"},
        "location": {"text": "New York or remote"},
        "work_type": {"text": "Full-time"}
    }
)

print("\\n==================== Response Text ====================\\n")
print(response['output']['message']['content'][0]['text'])

prompt_arn = "arn:aws:bedrock:us-east-1:938176218293:prompt/GH8CTU1R7O:2"
response = bedrock_runtime.converse(
    modelId=prompt_arn,
    promptVariables={
        "job_title": {"text": "UX Designer"},
        "responsibilities": {"text": "Design user interfaces, run usability testing, collaborate with product teams"},
        "requirements": {"text": "3+ years experience, Figma, HTML/CSS knowledge, communication skills"},
        "location": {"text": "New York or remote"},
        "work_type": {"text": "Full-time"}
    }
)

print("\\n==================== Response Text ====================\\n")
print(response['output']['message']['content'][0]['text'])

# Task 9: Clean Up
response = bedrock_agent.list_prompts()

for prompt in response['promptSummaries']:
    prompt_id = prompt['id']  # The correct key is 'id', not 'promptId'
    print(f"Deleting prompt: {prompt['name']} (ID: {prompt_id})")
    bedrock_agent.delete_prompt(promptIdentifier=prompt_id)

print("All prompts deleted successfully")