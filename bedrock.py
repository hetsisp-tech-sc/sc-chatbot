import boto3
import json
import streamlit as st

aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
aws_session_token = st.secrets["AWS_SESSION_TOKEN"]
aws_region = st.secrets.get("AWS_REGION", "us-east-2")

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token, region_name="us-east-2")
bedrock_agent_runtime = session.client(
    service_name='bedrock-agent-runtime', region_name='us-east-2')


def call_bedrock_service(question):
    user_question = question
    knowledge_base_id = 'HES75UX1JQ'
    model_arn = 'arn:aws:bedrock:us-east-2:885798945027:inference-profile/us.amazon.nova-micro-v1:0'

    try:
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={
                'text': user_question
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'generationConfiguration': {
                        'guardrailConfiguration': {
                            'guardrailId': '07hsgjdh0xn3',
                            'guardrailVersion': 'DRAFT'
                        }
                    },
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn
                }
            }
        )

        generated_text = response['output']['text']
        return generated_text
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


# def main():
#     while True:
#         q = input("Write your Query:")
#         resp = call_bedrock_service(q)
#         print(resp)
#         print()


# if __name__ == '__main__':
#     main()


