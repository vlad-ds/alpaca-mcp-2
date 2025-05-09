# server.py
from mcp.server.fastmcp import FastMCP
from typing import Union, List, Dict, Any, Optional
from datetime import datetime, date
import os

from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus, OrderSide
from alpaca.common.enums import Sort


# Create an MCP server
mcp = FastMCP("Demo")


@mcp.tool()
def get_latest_quotes(symbols: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Get the latest quotes for one or multiple stock symbols.
    
    Args:
        symbols: A single stock symbol as string or a list of symbols
    
    Returns:
        Dictionary containing the latest quote data for each requested symbol
    
    Example:
        # Get latest quotes for AAPL
        quotes = get_latest_quotes("AAPL")
        
        # Get latest quotes for multiple symbols
        quotes = get_latest_quotes(["AAPL", "MSFT", "GOOGL"])
        
        # Access specific quote data
        aapl_ask_price = quotes["AAPL"].ask_price
    """
    # Convert single symbol to list for consistent handling
    if isinstance(symbols, str):
        symbols = [symbols]
    
    # Create the request parameters
    request_params = StockLatestQuoteRequest(symbol_or_symbols=symbols)
    
    # Initialize the client
    client = StockHistoricalDataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"))
    
    # Get the latest quotes
    latest_quotes = client.get_stock_latest_quote(request_params)
    
    # Return the data
    return latest_quotes

@mcp.tool()
def get_stock_bars(
    symbols: Union[str, List[str]],
    start_date: Union[str, datetime, date],
    end_date: Union[str, datetime, date],
    timeframe_value: int = 1,
    timeframe_unit: str = "Day",
    limit: int = None,
    sort: str = "asc"
) -> Dict[str, Any]:
    """
    Get historical stock bars (candles) for one or multiple symbols.
    
    Args:
        symbols: A single stock symbol as string or a list of symbols
        timeframe_value: The number of time units for each bar (default: 1)
        timeframe_unit: The unit of time for each bar (default: "Day")
                        Valid values: "Min", "Hour", "Day", "Week", "Month"
        start_date: The start date for the data (string in 'YYYY-MM-DD' format or datetime object)
        end_date: The end date for the data (string in 'YYYY-MM-DD' format or datetime object)
        limit: Maximum number of bars to return (optional)
        sort: Sort direction, either "asc" or "desc" (default: "asc")
    
    Returns:
        Dictionary containing bar data for each requested symbol
    
    Example:
        # Get daily bars for AAPL and MSFT for January 2025
        bars = get_stock_bars(
            symbols=["AAPL", "MSFT"],
            timeframe_value=1,
            timeframe_unit="Day",
            start_date="2025-01-01",
            end_date="2025-01-31"
        )
    """
    # Convert single symbol to list for consistent handling
    if isinstance(symbols, str):
        symbols = [symbols]
    
    # Map the string timeframe unit to Alpaca's TimeFrameUnit enum
    unit_map = {
        "Min": TimeFrameUnit.Minute,
        "Hour": TimeFrameUnit.Hour,
        "Day": TimeFrameUnit.Day,
        "Week": TimeFrameUnit.Week,
        "Month": TimeFrameUnit.Month
    }
    
    # Validate timeframe unit
    if timeframe_unit not in unit_map:
        raise ValueError(f"Invalid timeframe_unit. Must be one of: {', '.join(unit_map.keys())}")
    
    # Create the request parameters
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame(timeframe_value, unit=unit_map[timeframe_unit]),
        start=start_date,
        end=end_date,
        limit=limit,
        sort=sort
    )
    
    # Initialize the client
    client = StockHistoricalDataClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"))
    
    # Get the bars data
    bars = client.get_stock_bars(request_params)
    
    # Return the data as a dictionary
    return bars.data

@mcp.tool()
def get_orders(
    status: Optional[str] = None,
    limit: Optional[int] = None,
    after: Optional[Union[str, datetime]] = None,
    until: Optional[Union[str, datetime]] = None,
    direction: Optional[str] = None,
    nested: Optional[bool] = None,
    side: Optional[str] = None,
    symbols: Optional[Union[str, List[str]]] = None
) -> Dict[str, Any]:
    """
    Get orders from your trading account with various filters.
    
    Args:
        status: Order status to query. Values: "open", "closed", or "all". Defaults to "open".
        limit: Maximum number of orders to return. Defaults to 50, max is 500.
        after: Filter orders submitted after this timestamp (string in format 'YYYY-MM-DD' or datetime).
        until: Filter orders submitted until this timestamp (string in format 'YYYY-MM-DD' or datetime).
        direction: Sort order. Values: "asc" or "desc". Defaults to "desc".
        nested: If true, multi-leg orders will be rolled up under the legs field of primary order.
        side: Filter by order side. Values: "buy" or "sell".
        symbols: Filter by symbol or list of symbols.
    
    Returns:
        Dictionary containing order data
    
    Example:
        # Get all open orders
        orders = get_orders()
        
        # Get closed sell orders for specific symbols
        orders = get_orders(
            status="closed",
            side="sell",
            symbols=["AAPL", "MSFT"]
        )
    """
    # Convert string parameters to proper enums if provided
    status_param = None
    if status:
        status_map = {
            "open": QueryOrderStatus.OPEN,
            "closed": QueryOrderStatus.CLOSED,
            "all": QueryOrderStatus.ALL
        }
        if status.lower() in status_map:
            status_param = status_map[status.lower()]
    
    direction_param = None
    if direction:
        direction_map = {
            "asc": Sort.ASC,
            "desc": Sort.DESC
        }
        if direction.lower() in direction_map:
            direction_param = direction_map[direction.lower()]
    
    side_param = None
    if side:
        side_map = {
            "buy": OrderSide.BUY,
            "sell": OrderSide.SELL
        }
        if side.lower() in side_map:
            side_param = side_map[side.lower()]
    
    # Convert single symbol to list for consistent handling
    symbols_param = None
    if symbols:
        if isinstance(symbols, str):
            symbols_param = [symbols]
        else:
            symbols_param = symbols
    
    # Create the request parameters
    request_params = GetOrdersRequest(
        status=status_param,
        limit=limit,
        after=after,
        until=until,
        direction=direction_param,
        nested=nested,
        side=side_param,
        symbols=symbols_param
    )
    
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    # Get the orders
    orders = trading_client.get_orders(filter=request_params)
    
    # Return the orders data
    return orders

@mcp.tool()
def cancel_orders() -> List[Dict[str, Any]]:
    """
    Cancel all open orders in your trading account.
    
    This function will attempt to cancel all currently open orders. It returns a list of responses
    indicating the success or failure status for each canceled order attempt.
    
    Returns:
        A list of cancellation status responses for each order
    
    Example:
        # Cancel all open orders
        responses = cancel_orders()
        
        # Check the status of each cancellation
        for response in responses:
            print(f"Order cancellation status: {response.status}")
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    # Cancel all orders
    responses = trading_client.cancel_orders()
    
    # Return the response data
    return responses

@mcp.tool()
def cancel_order_by_id(order_id: str) -> Dict[str, Any]:
    """
    Cancel a specific order by its order ID.
    
    Args:
        order_id: The unique identifier (UUID) of the order to cancel
    
    Returns:
        A dictionary with success status and message information
    
    Example:
        # Cancel a specific order
        result = cancel_order_by_id("f1d6dc0e-8d24-4f94-a36d-c1d6b2b8ad77")
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Cancel the specific order
        trading_client.cancel_order_by_id(order_id)
        
        # Since the Alpaca API doesn't return any data on success, we'll create our own response
        return {"success": True, "message": f"Request to cancel order {order_id} was sent to Alpaca. Verify order status to ensure it was cancelled."}
    except Exception as e:
        # Return error information if cancellation fails
        return {"success": False, "message": str(e)}

@mcp.tool()
def get_asset(symbol_or_asset_id: str) -> Dict[str, Any]:
    """
    Get details for a specific asset by its symbol or asset ID.
    
    This function retrieves detailed information about a specific asset such as
    its name, exchange, status, tradability, etc.
    
    Args:
        symbol_or_asset_id: The symbol (e.g. "AAPL") or asset ID (UUID) to retrieve
    
    Returns:
        Dictionary containing the asset information
    
    Example:
        # Get details for Apple stock
        asset = get_asset("AAPL")
        
        # Get details using an asset ID
        asset = get_asset("b0b6dd9d-8b9b-4a32-9b23-c81997b3d06c")
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Get the asset
        asset = trading_client.get_asset(symbol_or_asset_id)
        
        # Return the asset data
        return asset
    except Exception as e:
        # Return error information if the request fails
        return {"success": False, "message": str(e)}

@mcp.tool()
def get_account() -> Dict[str, Any]:
    """
    Get account details from your Alpaca trading account.
    
    This function retrieves detailed information about your account including:
    - Account status
    - Buying power
    - Cash balance
    - Portfolio value
    - Number of day trades
    - Trading restrictions
    - And other account metrics
    
    Returns:
        Dictionary containing the account information
    
    Example:
        # Get your account details
        account = get_account()
        
        # Check your buying power
        print(f"Buying power: ${account.buying_power}")
        
        # Check if account is restricted from trading
        print(f"Trading restricted: {account.trading_blocked}")
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Get the account details
        account = trading_client.get_account()
        
        # Return the account data
        return account
    except Exception as e:
        # Return error information if the request fails
        return {"success": False, "message": str(e)}

@mcp.tool()
def get_all_positions() -> List[Dict[str, Any]]:
    """
    Get all open positions in your Alpaca trading account.
    
    This function retrieves a list of all the current open positions in your account,
    including details such as quantity, market value, unrealized profit/loss, etc.
    
    Returns:
        List of dictionaries containing position information
    
    Example:
        # Get all open positions
        positions = get_all_positions()
        
        # Check the quantity and value of each position
        for position in positions:
            print(f"Symbol: {position.symbol}, Qty: {position.qty}, Market Value: ${position.market_value}")
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Get all positions
        positions = trading_client.get_all_positions()
        
        # Return the positions data
        return positions
    except Exception as e:
        # Return error information if the request fails
        return [{"success": False, "message": str(e)}]

@mcp.tool()
def get_open_position(symbol_or_asset_id: str) -> Dict[str, Any]:
    """
    Get details for a specific open position by its symbol or asset ID.
    
    This function retrieves detailed information about a specific open position
    such as quantity, market value, cost basis, unrealized profit/loss, etc.
    
    Args:
        symbol_or_asset_id: The symbol (e.g. "AAPL") or asset ID (UUID) of the position
    
    Returns:
        Dictionary containing the position information
    
    Example:
        # Get position details for Apple stock
        position = get_open_position("AAPL")
        
        # Check the current market value and P/L
        print(f"Market value: ${position.market_value}")
        print(f"Unrealized P/L: ${position.unrealized_pl}")
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Get the open position
        position = trading_client.get_open_position(symbol_or_asset_id)
        
        # Return the position data
        return position
    except Exception as e:
        # Return error information if the request fails
        return {"success": False, "message": str(e)}

@mcp.tool()
def close_position(symbol_or_asset_id: str, qty: Optional[str] = None, percentage: Optional[str] = None) -> Dict[str, Any]:
    """
    Close a specific open position by its symbol or asset ID.
    
    This function places an order to liquidate a specific position. You can specify
    either a quantity or percentage of the position to close.
    
    Args:
        symbol_or_asset_id: The symbol (e.g. "AAPL") or asset ID (UUID) of the position to close
        qty: The number of shares to liquidate (e.g. "100")
        percentage: The percentage of shares to liquidate (e.g. "50")
    
    Note:
        You must specify either qty OR percentage, not both.
        If neither is specified, the entire position will be closed.
    
    Returns:
        Dictionary containing the order information for the close position request
    
    Example:
        # Close an entire position
        order = close_position("AAPL")
        
        # Close half of a position
        order = close_position("MSFT", percentage="50")
        
        # Close a specific number of shares
        order = close_position("GOOGL", qty="10")
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Create close options if qty or percentage is specified
        close_options = None
        if qty is not None or percentage is not None:
            from alpaca.trading.requests import ClosePositionRequest
            close_options = ClosePositionRequest(qty=qty, percentage=percentage)
        
        # Close the position
        order = trading_client.close_position(symbol_or_asset_id, close_options)
        
        # Return the order data
        return order
    except Exception as e:
        # Return error information if the request fails
        return {"success": False, "message": str(e)}

@mcp.tool()
def get_clock() -> Dict[str, Any]:
    """
    Get the current market clock information.
    
    This function retrieves the current market timestamp, whether or not the market
    is currently open, as well as the times of the next market open and close.
    
    Returns:
        Dictionary containing the following market clock information:
        - timestamp: The current market timestamp (in Eastern Time)
        - is_open: Whether the market is currently open
        - next_open: The timestamp of the next market open (in Eastern Time)
        - next_close: The timestamp of the next market close (in Eastern Time)
    
    Example:
        # Get the current market clock
        clock = get_clock()
        
        # Check if the market is open
        is_market_open = clock["is_open"]
        
        # Get the next market open time
        next_open = clock["next_open"]
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Get the market clock
        clock = trading_client.get_clock()
        
        # Return the clock data
        return clock
    except Exception as e:
        # Return error information if the request fails
        return {"success": False, "message": str(e)}

@mcp.tool()
def get_calendar(
    start: Optional[Union[str, date]] = None,
    end: Optional[Union[str, date]] = None
) -> List[Dict[str, Any]]:
    """
    Get the market calendar for a specified date range.
    
    This function retrieves the market calendar for the specified date range, including
    market open and close times for each trading day. The calendar API serves the full
    list of market days from 1970 to 2029.
    
    Args:
        start: The start date to get the calendar from (string in format 'YYYY-MM-DD' or date object)
        end: The end date to get the calendar until (string in format 'YYYY-MM-DD' or date object)
    
    Returns:
        List of dictionaries containing calendar information for each trading day:
        - date: The date of the trading day
        - open: The timestamp when the market opens on that day (in Eastern Time)
        - close: The timestamp when the market closes on that day (in Eastern Time)
    
    Example:
        # Get the market calendar for January 2025
        calendar = get_calendar(start="2025-01-01", end="2025-01-31")
        
        # Get the first trading day's information
        first_day = calendar[0]
        print(f"Date: {first_day.date}, Open: {first_day.open}, Close: {first_day.close}")
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Create the request parameters if start or end is specified
        from alpaca.trading.requests import GetCalendarRequest
        
        filters = None
        if start is not None or end is not None:
            filters = GetCalendarRequest(start=start, end=end)
        
        # Get the calendar
        calendar = trading_client.get_calendar(filters)
        
        # Return the calendar data
        return calendar
    except Exception as e:
        # Return error information if the request fails
        return [{"success": False, "message": str(e)}]

@mcp.tool()
def place_limit_order(
    symbol: str,
    limit_price: float,
    qty: float,
    side: str,
    time_in_force: str = "day"
) -> Dict[str, Any]:
    """
    Place a limit order to buy or sell an asset at a specified price.
    
    This function submits a limit order for the specified asset. A limit order is an order
    to buy or sell an asset at a specific price or better.
    
    Args:
        symbol: The stock symbol (e.g. "AAPL", "TSLA")
        limit_price: The maximum/minimum price at which you're willing to buy/sell
        qty: The number of shares to trade
        side: The order side, either "buy" or "sell"
        time_in_force: How long the order will remain active before being canceled
                      Options: "day", "gtc" (good till canceled), "opg" (market on open),
                      "cls" (market on close), "ioc" (immediate or cancel), "fok" (fill or kill)
                      Default is "day"
    
    Returns:
        Dictionary containing the order information
    
    Example:
        # Buy 1 share of Tesla at a limit price of $900
        order = place_limit_order(
            symbol="TSLA",
            limit_price=900,
            qty=1,
            side="buy",
            time_in_force="day"
        )
        
        # Sell 5 shares of Apple at a limit price of $195
        order = place_limit_order(
            symbol="AAPL",
            limit_price=195,
            qty=5,
            side="sell",
            time_in_force="gtc"
        )
    """
    # Initialize the client
    trading_client = TradingClient(os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY"), paper=True)
    
    try:
        # Map the string side parameter to the OrderSide enum
        side_param = None
        if side.lower() == "buy":
            side_param = OrderSide.BUY
        elif side.lower() == "sell":
            side_param = OrderSide.SELL
        else:
            return {"success": False, "message": f"Invalid side parameter: {side}. Must be 'buy' or 'sell'."}
        
        # Map the string time_in_force parameter to the TimeInForce enum
        from alpaca.trading.enums import TimeInForce
        
        tif_map = {
            "day": TimeInForce.DAY,
            "gtc": TimeInForce.GTC,
            "opg": TimeInForce.OPG,
            "cls": TimeInForce.CLS,
            "ioc": TimeInForce.IOC,
            "fok": TimeInForce.FOK
        }
        
        if time_in_force.lower() not in tif_map:
            return {
                "success": False, 
                "message": f"Invalid time_in_force parameter: {time_in_force}. Must be one of: {', '.join(tif_map.keys())}"
            }
        
        tif_param = tif_map[time_in_force.lower()]
        
        # Create the limit order request
        from alpaca.trading.requests import LimitOrderRequest
        
        limit_order_data = LimitOrderRequest(
            symbol=symbol,
            limit_price=limit_price,
            qty=qty,
            side=side_param,
            time_in_force=tif_param
        )
        
        # Submit the order
        order = trading_client.submit_order(order_data=limit_order_data)
        
        # Return the order data
        return order
    except Exception as e:
        # Return error information if the request fails
        return {"success": False, "message": str(e)}