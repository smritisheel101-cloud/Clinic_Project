from langchain_aws import BedrockEmbeddings , ChatBedrockConverse

embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
llm = ChatBedrockConverse(model_id="global.anthropic.claude-haiku-4-5-20251001-v1:0")