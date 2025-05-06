import asyncio
import sys
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from contextlib import asynccontextmanager
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import os
import getpass
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_ibm import ChatWatsonx


model_id = os.getenv('MODEL_ID')
project_id=os.getenv('WATSONX_PROJECT_ID')
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 8000,
    "min_new_tokens": 1,
    "repetition_penalty": 1.1
}
model = ChatWatsonx(
	model_id = model_id,
    url =  os.getenv('WATSONX_URL'),
    apikey = os.getenv('WATSONX_APIKEY'),
	params = parameters,
	project_id = project_id)

python_path = sys.executable

@asynccontextmanager
async def setup_agent():
    async with MultiServerMCPClient(
        {   
            "product_search": {
                "command": "python",
                "args": ["Product_Recommendation_System/product_search_server.py"],
                "transport": "stdio",
            },
            "price_comparator": {
                "url": "http://0.0.0.0:8002/sse",
                "transport": "sse",
            },
            "review_analyzer": {
                "url": "http://0.0.0.0:8001/sse",
                "transport": "sse",
            }
        }
    ) as client:
        print("Connected to MCP servers.")

        tools = client.get_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")

        system_prompt = """
        You are a helpful product recommendation assistant.
        Your goal is to help users find products that meet their needs.
        1. Use 'find_products' tool first to get candidate products.
        2. Then use 'compare_product_prices' on top products.
        3. Summarize findings into a clear recommendation.
        4. Mention product name, description, price comparison.
        5. If no products found, inform user politely.
        """

        agent = create_react_agent(
            model,
            tools=client.get_tools(),
            prompt=system_prompt,
            debug=True
        )
        yield agent

async def invoke_agent(user_query):
    async with setup_agent() as agent:
        response = await agent.ainvoke({"messages": [HumanMessage(content=user_query)]})
        final_message = response['messages'][-1]

        if isinstance(final_message, AIMessage):
            print("\n===== FINAL RECOMMENDATION =====")
            print(final_message.content)
            print("================================")
        else:
            print("\nCould not extract final AI message cleanly. Full response:")
            print(response)

if __name__ == "__main__":
    user_query = "I need a good laptop for programming, maybe under $1000?"
    asyncio.run(invoke_agent(user_query=user_query))

