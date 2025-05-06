from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv(override=True)
mcp = FastMCP("product_search")


SIMULATED_DB = {
    "laptop": [
        {"id": "LPT001", "name": "DevBook Pro 14", "description": "Powerful laptop for developers, 16GB RAM, 512GB SSD"},
        {"id": "LPT002", "name": "UltraSlim X1", "description": "Lightweight ultrabook for travel, 8GB RAM, 256GB SSD"},
        {"id": "LPT003", "name": "GamerRig Max", "description": "High-performance gaming laptop, RTX 4070, 32GB RAM"},
    ],
    "headphones": [
        {"id": "HDP001", "name": "NoiseAway Pro", "description": "Active noise-cancelling over-ear headphones"},
        {"id": "HDP002", "name": "SportBuds Lite", "description": "Water-resistant earbuds for workouts"},
    ],
    "camera": [
        {"id": "CAM001", "name": "PhotoMaster Z", "description": "Professional mirrorless camera, 45MP sensor"},
        {"id": "CAM002", "name": "VlogCam Mini", "description": "Compact camera ideal for vlogging"},
 ]
}

@mcp.tool()
async def find_products(query: str) -> List[Dict]:
    """Searches for products based on a query.

    Args:
        query: The user's description of the product they are looking for (e.g., 'laptop for programming', 'noise cancelling headphones').

    Returns:
        A list of dictionaries, where each dictionary represents a matching product with its ID, name, and description.
    """
    print(f"Product Search Server: Received query '{query}'")
    results = []
    query_lower = query.lower()
    try:
        # Basic keyword matching against descriptions and names (can be improved)
        for category, products in SIMULATED_DB.items():
             if category in query_lower: # Basic category match
                 for product in products:
                     results.append(product)
             else: # Match keywords in description/name
                 for product in products:
                     if query_lower in product['name'].lower() or query_lower in product['description'].lower():
                         if product not in results: # Avoid duplicates
                             results.append(product)

        # If still no results, try matching broader terms
        if not results:
             if "laptop" in query_lower: results.extend(SIMULATED_DB.get("laptop", []))
             if "headphone" in query_lower or "earbud" in query_lower: results.extend(SIMULATED_DB.get("headphones", []))
             if "camera" in query_lower: results.extend(SIMULATED_DB.get("camera", []))

        print(f"Product Search Server: Found {len(results)} products.")
        # Limit results for brevity
        return results[:3] # Return top 3 matches
    except Exception as e:
        print(f"Product Search Server: Error - {e}")
        return [{"error": f"An error occurred during product search: {e}"}]

if __name__ == "__main__":
    mcp.run(transport='stdio')
    #mcp.run(transport="sse")