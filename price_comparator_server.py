from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
from typing import List, Dict
import random
load_dotenv(override=True)
mcp = FastMCP("price_comparator")
mcp = FastMCP(
    name="price_comparator",
    host="0.0.0.0", 
    port=8002, 
)
VENDORS = ["ElectroMart", "GadgetGalaxy", "TechHub", "OnlineDeals"]
@mcp.tool()
async def compare_product_prices(product_name: str) -> List[Dict]:
    """Compares prices for a product across simulated vendors.
    Args:
        product_name: The name of the product to compare prices for.

    Returns:
        A list of dictionaries, each containing a vendor name and a simulated price.
    """
    print(f"Price Comparator Server: Received request for '{product_name}'")
    prices = []
    try:
        base_price = 50 + len(product_name) * 25
        num_vendors_to_check = random.randint(2, len(VENDORS))
        selected_vendors = random.sample(VENDORS, num_vendors_to_check)

        for vendor in selected_vendors:
            price = round(base_price * random.uniform(0.9, 1.15), 2)
            prices.append({"vendor": vendor, "price": f"${price:.2f}"})
        print(f"Price Comparator Server: Found {len(prices)} prices for '{product_name}'.")
        return prices
    except Exception as e:
        print(f"Price Comparator Server: Error - {e}")
        return [{"error": f"An error occurred during price comparison: {e}"}]

if __name__ == "__main__":
    mcp.run(transport="sse")