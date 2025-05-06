from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
from typing import Dict
import os
import getpass
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GP
from ibm_watsonx_ai.foundation_models import ModelInference
def get_credentials():
	return {
		"url" :  os.getenv('WATSONX_URL'),
		"apikey" :  os.getenv('WATSONX_APIKEY')
	}
model_id = os.getenv('MODEL_ID')  
project_id= os.getenv('WATSONX_PROJECT_ID')
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 8000,
    "min_new_tokens": 1,
    "repetition_penalty": 1.1
}
model = ModelInference(
	model_id = model_id,
	params = parameters,
	credentials = get_credentials(),
	project_id = project_id)
mcp = FastMCP(
    name="review_analyzer",
    host="0.0.0.0",
    port=8001,
)
@mcp.tool()
async def analyze_product_reviews(product_name: str) -> Dict:
    """Analyzes and summarizes hypothetical reviews for a given product.

    Args:
        product_name: The name of the product to analyze reviews for.

    Returns:
        A dictionary containing a summary of positive and negative points based on simulated reviews.
    """
    print(f"Review Analyzer Server: Received request for '{product_name}'")
    try:
        prompt = f"""
        Generate a brief, plausible review summary for a product named "{product_name}".
        Imagine what typical customer feedback might be.
        Focus on 1-2 positive points and 1-2 negative points or caveats.
        Format the output as a dictionary with keys "positive_summary" and "negative_summary".
        Example format: {{"positive_summary": "Customers love the battery life and screen quality.", "negative_summary": "Some users find it a bit heavy and the webcam quality is average."}}
        Output only the JSON dictionary.
        """
        ai_msg = model.generate_text(prompt=prompt, guardrails=False)
        ai_msg = ai_msg.replace('```', '').replace('json', '')
        summary_dict = eval(ai_msg.strip())
        
        print(f"Review Analyzer Server: Generated summary for '{product_name}'.")
        return summary_dict

    except Exception as e:
        print(f"Review Analyzer Server: Error - {e}")
        return {"error": f"An error occurred while analyzing reviews: {e}"}

if __name__ == "__main__":
    mcp.run(transport="sse")