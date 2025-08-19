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
                        },
                        'promptTemplate': {
                            'textPromptTemplate': "A chat between a curious User and an artificial intelligence Bot. The Bot gives helpful, detailed, and polite answers to the User's questions.\n \nIn this session, the model has access to set of search results and a user's question, your job is to answer the user's question using only information from the search results. You must follow the following guidelines:\n \n- If the search results do not contain information that can answer the question, please respond with \"Sorry I could not find an exact answer to the question\".\n- Always add a citation to the end of your response using markers like %[1]%, %[2]%, %[3]%, etc for the corresponding passage supports the response.\n- Always add a brief explaination to your answer. Make the response concise but comprehensive.\n\nNow, below is a list of texts and/or images retrieved for user's question. Read them carefully and then follow my instructions: \n\n$search_results$\n\nUsing the information from above search results to provide answer to user's question. In your answer make sure to first quote the images (by mentioning image title or image ID) from which you can identify relevant information, then followed by your reasoning steps and answer. \n\n$output_format_instructions$\n\nHere is the user's query to be responded in the languange of the user's query:\n$query$\n\n"
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

















