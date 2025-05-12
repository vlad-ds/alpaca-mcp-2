# Alpaca MCP

A Model-Claude-Pipeline (MCP) wrapper over the Alpaca API, enabling Claude to interact with Alpaca's trading and market data APIs through simple tool calls.

## Features

The MCP currently provides the following functionality:

- `get_latest_quotes`: Get the latest quotes for stock symbols
- `get_stock_bars`: Get historical stock bars (candles)
- `get_account`: Get account details from your Alpaca account
- `get_all_positions`: Get all open positions
- `get_open_position`: Get details for a specific position
- `get_orders`: Get orders with various filters
- `cancel_orders`: Cancel all open orders
- `cancel_order_by_id`: Cancel a specific order by ID
- `place_limit_order`: Place a limit order
- `close_position`: Close a position by symbol
- `get_asset`: Get details for a specific asset
- `get_clock`: Get current market clock information
- `get_calendar`: Get market calendar for a date range

## Installation

### Prerequisites

Make sure you have uv installed:

```bash
curl -fsSL https://astral.sh/uv/install.sh | bash
# or
brew install uv
```

### Manual Installation

Clone this repository and install locally:

```bash
gh repo clone vlad-ds/alpaca-mcp-2
cd alpaca-mcp-2
pip install -e .
```

## Setup

1. Create an [Alpaca](https://app.alpaca.markets/signup) paper trading account
2. Generate and save your API key and secret

## Usage

Add the following to your `claude_desktop_config.json`:

```json
"alpaca": {
  "command": "uv",
  "args": [
    "run",
    "--directory",
    "/Users/{USERNAME}/alpaca-mcp-2", # add your username and path to the repository
    "mcp",
    "run",
    "server.py"
  ],
  "env": {
    "ALPACA_API_KEY": "{YOUR_ALPACA_API_KEY}",
    "ALPACA_SECRET_KEY": "{YOUR_ALPACA_SECRET_KEY}"
  }
}
```
