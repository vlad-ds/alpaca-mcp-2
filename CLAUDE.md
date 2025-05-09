# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This repository contains an MCP (Model-Claude-Pipeline) server implementation for the Alpaca API, providing a convenient interface to interact with Alpaca's various trading and data APIs.

## Architecture

The project is organized into several key components:

1. **MCP Server (`server.py`)**: The main entry point that exposes Alpaca API functionality as MCP tools.

2. **Alpaca SDK Structure**:
   - `alpaca/broker/`: Broker-related functionality for account management
   - `alpaca/trading/`: Trading functionality (orders, positions, assets)
   - `alpaca/data/`: Market data services (historical and live data)
   - `alpaca/common/`: Shared components and utilities

3. **Client Types**:
   - `TradingClient`: For managing orders, positions, and accounts
   - `StockHistoricalDataClient`: For accessing historical market data

## Environment Setup

The application requires Alpaca API credentials to be set as environment variables:
- `ALPACA_API_KEY`: Your Alpaca API key
- `ALPACA_SECRET_KEY`: Your Alpaca API secret key

## Tool Implementation Pattern

When implementing new MCP tools that interface with Alpaca API:

1. Create a new `@mcp.tool()` function in `server.py`
2. Initialize the appropriate client (TradingClient, StockHistoricalDataClient, etc.)
3. Call the corresponding Alpaca SDK method
4. Include proper error handling
5. Return the results in the appropriate format
6. Document the tool with comprehensive docstrings including examples

Example pattern:
```python
@mcp.tool()
def some_alpaca_function(parameter1: Type1, parameter2: Type2) -> Dict[str, Any]:
    """
    Docstring with clear description, parameter docs, return type docs, and usage examples
    """
    # Initialize the client
    client = ClientType(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Create any request objects if needed
        # Call the API
        result = client.some_method(...)
        
        # Return the result
        return result
    except Exception as e:
        # Return error information if the request fails
        return {"success": False, "message": str(e)}
```