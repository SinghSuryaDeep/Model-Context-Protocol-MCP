# Model-Context-Protocol-


# Product Recommendation System with Model Context Protocol (MCP)

This project demonstrates a product recommendation system built using the Model Context Protocol (MCP) with a multi-server architecture. It integrates different functionalities like product search, price comparison, and review analysis, leveraging both Server-Sent Events (SSE) and Standard Input/Output (STDIO) for communication between components. The review analysis is powered by IBM Watsonx.

## Architecture

The system comprises the following independent servers:

1.  **Product Search Server (`product_search_server.py`):**
    * Provides a tool (`find_products`) to search for products based on a user query.
    * Maintains a simulated in-memory database of products across categories (laptops, headphones, cameras).
    * Communicates with the MCP client via **STDIO**.

2.  **Price Comparator Server (`price_comparator_server.py`):**
    * Offers a tool (`compare_product_prices`) to fetch and compare simulated prices for a given product name from various virtual vendors.
    * Communicates with the MCP client via **Server-Sent Events (SSE)** on `http://0.0.0.0:8002/sse`.

3.  **Review Analyzer Server (`review_analyzer_server.py`):**
    * Provides a tool (`analyze_product_reviews`) to generate a brief summary of hypothetical positive and negative reviews for a given product name.
    * Utilizes **IBM Watsonx** for generating these review summaries based on a prompt.
    * Communicates with the MCP client via **Server-Sent Events (SSE)** on `http://0.0.0.0:8001/sse`.
    * Requires IBM Watsonx API key, URL, Model ID, and Project ID to be set as environment variables.

4.  **Recommendation Agent (`recommendation_agent.py`):**
    * Acts as the central orchestrator, using Langchain's `create_react_agent` and the `MultiServerMCPClient` to interact with the other servers.
    * Defines a system prompt to guide the agent in finding products, comparing prices, and summarizing findings into a recommendation for the user.
    * Leverages the tools exposed by the other servers through the MCP client.

## Prerequisites

Before you begin, ensure you have the following installed:

* **uv:** A fast Python package installer and resolver. Install it using `pip install uv`.
* **Environment Variables:** Set the following environment variables in a `.env` file (create one in the project root):

## Step-by-Step Instructions

Follow these steps to run the product recommendation system:

**1. Set up the Virtual Environment:**
   ```bash
   uv venv
   source .venv/bin/activate


**2. Initialize an uv project:**
   ```bash
   uv init

**2. Initialize an uv project:**
   ```bash
   uv init

**3. Install the fastmcp python library:**
   ```bash
   uv add fastmcp



## Running the Servers

Open three terminals (or use a multiplexer like tmux/tmuxinator).

**1. Start Product Search Server (stdio)**

   ```bash
   uv run mcp dev product_search_server.py

**2. Start Price Comparator Server (SSE)**

   ```bash
   python price_comparator_server.py


**3. Start Review Analyzer Server (SSE)**

   ```bash
   python review_analyzer_server.py


Each server will log incoming requests and responses to the console.


