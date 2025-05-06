---

# Product Recommendation System with Model Context Protocol (MCP) and IBM watsonx

This project demonstrates a **product recommendation system** built using the **Model Context Protocol (MCP)** with a **multi-server architecture**. It integrates functionalities like product search, price comparison, and review analysis, using **Server-Sent Events (SSE)** and **Standard Input/Output (STDIO)** for inter-server communication. The **review analysis** is powered by **IBM watsonx**.

---

## 🧱 Architecture

The system comprises the following independent servers:

### 1. **Product Search Server** (`product_search_server.py`)

* Tool: `find_products`
* Searches for products based on a user query.
* Uses an in-memory simulated product database (e.g., laptops, headphones, cameras).
* Communicates via **STDIO** with the MCP client.

### 2. **Price Comparator Server** (`price_comparator_server.py`)

* Tool: `compare_product_prices`
* Simulates fetching and comparing product prices from various vendors.
* Communicates via **SSE** on `http://0.0.0.0:8002/sse`.

### 3. **Review Analyzer Server** (`review_analyzer_server.py`)

* Tool: `analyze_product_reviews`
* Summarizes positive and negative reviews for a product using IBM Watsonx.
* Communicates via **SSE** on `http://0.0.0.0:8001/sse`.

### 4. **Recommendation Agent** (`recommendation_agent.py`)

* Central orchestrator using LangChain's `create_react_agent` and `MultiServerMCPClient`.
* Coordinates interactions with all three servers.
* Generates a recommendation based on product findings, prices, and reviews.


## 🚀 Getting Started

### 1. Set up the virtual environment:

```bash
uv venv
source .venv/bin/activate
```

### 2. Initialize the uv project:

```bash
uv init
```

### 3. Install required package:

```bash
uv add fastmcp
```

---

## 🖥️ Running the Servers

### 1. Start the Product Search Server (STDIO)

```bash
uv run mcp dev product_search_server.py
```

### 2. Start the Price Comparator Server (SSE)

```bash
python price_comparator_server.py
```

### 3. Start the Review Analyzer Server (SSE)

```bash
python review_analyzer_server.py
```

Each server will log incoming requests and responses to the console.

---

## 🤖 Running the Recommendation Agent

Once all servers are running, start the agent:

```bash
python recommendation_agent.py
```

### Default Query:

```
I need a good laptop for programming, maybe under $1000?
```

---
