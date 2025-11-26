# ============================================================================
# CRYPTOCURRENCY PRICE TRACKER
# A free, real-time crypto price monitor using CoinGecko's public API
# No API key required | No web scraping | Completely legal and safe
# ============================================================================

import requests  # For making HTTP requests to the API
import json      # For handling JSON data (though not heavily used here)
from datetime import datetime  # For displaying current timestamp
import time      # For sleep() function in live tracker

# ============================================================================
# FUNCTION 1: GET MULTIPLE CRYPTO PRICES
# ============================================================================
def get_crypto_prices():
    """
    Fetches live prices for multiple cryptocurrencies simultaneously.
    
    Returns:
        dict: Price data for all requested cryptocurrencies, or None if error
    
    Features:
        - Gets prices in USD and INR
        - Shows 24-hour price change percentage
        - Displays market capitalization
        - Highlights significant price movements (>10%)
    """
    try:
        # ----------------------------------------------------------------
        # API ENDPOINT SETUP
        # ----------------------------------------------------------------
        # CoinGecko's free public API - no authentication needed
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # ----------------------------------------------------------------
        # REQUEST PARAMETERS
        # ----------------------------------------------------------------
        params = {
            # List of cryptocurrency IDs (must match CoinGecko's naming)
            'ids': 'bitcoin,ethereum,cardano,solana,dogecoin,shiba-inu,polygon,ripple,litecoin,polkadot,chainlink,stellar,tron,avalanche-2,uniswap',
            
            # Currencies to display prices in (can add more like 'eur', 'gbp')
            'vs_currencies': 'usd,inr',
            
            # Include 24-hour percentage change (true/false)
            'include_24hr_change': 'true',
            
            # Include market capitalization data (true/false)
            'include_market_cap': 'true'
        }
        
        # ----------------------------------------------------------------
        # LOADING MESSAGES
        # ----------------------------------------------------------------
        print("💰 Fetching live crypto prices...") 
        print("⏳ Please wait...\n")
        
        # ----------------------------------------------------------------
        # MAKE API REQUEST
        # ----------------------------------------------------------------
        # Send GET request with 30-second timeout to prevent hanging
        response = requests.get(url, params=params, timeout=30)
        
        # ----------------------------------------------------------------
        # HANDLE SUCCESSFUL RESPONSE (Status Code 200)
        # ----------------------------------------------------------------
        if response.status_code == 200:
            # Parse JSON response into Python dictionary
            data = response.json()
            
            # ----------------------------------------------------------------
            # DISPLAY HEADER WITH TIMESTAMP
            # ----------------------------------------------------------------
            print("╔" + "═" * 70 + "╗")
            print("║" + "  LIVE CRYPTOCURRENCY PRICES".center(70) + "║")
            print("║" + f"  Updated: {datetime.now().strftime('%I:%M:%S %p, %d %b %Y')}".center(70) + "║")
            print("╚" + "═" * 70 + "╝\n")
            
            # ----------------------------------------------------------------
            # LOOP THROUGH EACH CRYPTOCURRENCY
            # ----------------------------------------------------------------
            for crypto_id, crypto_data in data.items():
                # Convert ID format: 'shiba-inu' becomes 'Shiba Inu'
                crypto_name = crypto_id.replace('-', ' ').title()
                
                # Extract price data from API response
                usd_price = crypto_data['usd']           # Price in US Dollars
                inr_price = crypto_data['inr']           # Price in Indian Rupees
                change_24h = crypto_data['usd_24h_change']  # 24hr percentage change
                market_cap = crypto_data['usd_market_cap']  # Total market value
                
                # ----------------------------------------------------------------
                # FORMAT MARKET CAP (Billions or Millions)
                # ----------------------------------------------------------------
                if market_cap > 1_000_000_000:  # If over 1 billion
                    market_cap_str = f"${market_cap / 1_000_000_000:.2f}B"
                else:  # If under 1 billion, show in millions
                    market_cap_str = f"${market_cap / 1_000_000:.2f}M"
                
                # ----------------------------------------------------------------
                # DETERMINE TREND INDICATOR (Green up or Red down)
                # ----------------------------------------------------------------
                if change_24h > 0:  # Price went up
                    trend = "🟢 ↗"
                    change_color = "+"  # Show '+' sign for positive change
                else:  # Price went down
                    trend = "🔴 ↘"
                    change_color = ""  # Negative sign already included
                
                # ----------------------------------------------------------------
                # DISPLAY CRYPTO INFORMATION
                # ----------------------------------------------------------------
                print(f"━━━ {crypto_name} ━━━")
                print(f"  💵 USD: ${usd_price:,.2f}")  # :,. adds thousand separators
                print(f"  💰 INR: ₹{inr_price:,.2f}")
                print(f"  {trend} 24h Change: {change_color}{change_24h:.2f}%")
                print(f"  📊 Market Cap: {market_cap_str}")
                print()  # Blank line for readability
            
            # ----------------------------------------------------------------
            # ALERT SECTION - Highlight Big Movers
            # ----------------------------------------------------------------
            print("🚨 ALERTS:")
            for crypto_id, crypto_data in data.items():
                change = crypto_data['usd_24h_change']
                name = crypto_id.replace('-', ' ').title()
                
                # Alert if price moved more than 10% in either direction
                if change > 10:
                    print(f"   🚀 {name} is UP {change:.2f}% today!")
                elif change < -10:
                    print(f"   📉 {name} is DOWN {change:.2f}% today!")
            
            return data  # Return the full data dictionary for further use
        
        # ----------------------------------------------------------------
        # HANDLE RATE LIMITING (Status Code 429)
        # ----------------------------------------------------------------
        elif response.status_code == 429:
            print("❌ Error: Too many requests. Wait a minute and try again.")
            return None
        
        # ----------------------------------------------------------------
        # HANDLE OTHER HTTP ERRORS
        # ----------------------------------------------------------------
        else:
            print(f"❌ Error: Could not fetch data (Status: {response.status_code})")
            return None
    
    # ----------------------------------------------------------------
    # EXCEPTION HANDLING
    # ----------------------------------------------------------------
    except requests.exceptions.Timeout:
        # Request took longer than 30 seconds
        print("❌ Error: Request timed out. Check your internet connection.")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"❌ Error: {e}")
        return None


# ============================================================================
# FUNCTION 2: GET DETAILED INFO FOR ONE CRYPTO
# ============================================================================
def get_single_crypto(crypto_name):
    """
    Fetches comprehensive details for a specific cryptocurrency.
    
    Args:
        crypto_name (str): Name or symbol of the crypto (e.g., 'bitcoin' or 'btc')
    
    Returns:
        dict: Detailed crypto data, or None if not found
    
    Features:
        - Current price in USD and INR
        - All-time high (ATH) price and date
        - Percentage down from ATH
    """
    try:
        # ----------------------------------------------------------------
        # CRYPTO NAME MAPPING
        # ----------------------------------------------------------------
        # Maps common abbreviations to CoinGecko's official IDs
        crypto_map = {
            'bitcoin': 'bitcoin', 'btc': 'bitcoin',
            'ethereum': 'ethereum', 'eth': 'ethereum',
            'dogecoin': 'dogecoin', 'doge': 'dogecoin',
            'shiba': 'shiba-inu', 'shib': 'shiba-inu',
            'cardano': 'cardano', 'ada': 'cardano',
            'solana': 'solana', 'sol': 'solana'
        }
        
        # Convert input to lowercase and look up in map
        # If not in map, use the input as-is (assumes it's already correct ID)
        crypto_id = crypto_map.get(crypto_name.lower(), crypto_name.lower())
        
        # ----------------------------------------------------------------
        # BUILD API URL FOR SPECIFIC COIN
        # ----------------------------------------------------------------
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
        
        print(f"\n🔍 Fetching detailed info for {crypto_name}...\n")
        
        # ----------------------------------------------------------------
        # MAKE API REQUEST
        # ----------------------------------------------------------------
        response = requests.get(url, timeout=30)
        
        # ----------------------------------------------------------------
        # PROCESS SUCCESSFUL RESPONSE
        # ----------------------------------------------------------------
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            
            # ----------------------------------------------------------------
            # EXTRACT DATA FROM NESTED JSON STRUCTURE
            # ----------------------------------------------------------------
            name = data['name']  # Full name (e.g., 'Bitcoin')
            symbol = data['symbol'].upper()  # Ticker symbol (e.g., 'BTC')
            
            # Current prices (nested under 'market_data' -> 'current_price')
            current_price_usd = data['market_data']['current_price']['usd']
            current_price_inr = data['market_data']['current_price']['inr']
            
            # All-time high data
            ath_usd = data['market_data']['ath']['usd']  # ATH price
            ath_date = data['market_data']['ath_date']['usd'][:10]  # ATH date (first 10 chars = YYYY-MM-DD)
            
            # ----------------------------------------------------------------
            # DISPLAY DETAILED INFORMATION
            # ----------------------------------------------------------------
            print(f"╔{'═' * 50}╗")
            print(f"║  {name} ({symbol})".ljust(51) + "║")  # .ljust() pads with spaces
            print(f"╚{'═' * 50}╝")
            
            # Current prices with thousand separators
            print(f"\n💵 Current Price (USD): ${current_price_usd:,.2f}")
            print(f"💰 Current Price (INR): ₹{current_price_inr:,.2f}")
            
            # All-time high info
            print(f"🏆 All-Time High: ${ath_usd:,.2f} (on {ath_date})")
            
            # Calculate percentage down from ATH
            # Formula: ((current - ath) / ath) * 100
            print(f"📉 Down from ATH: {((current_price_usd - ath_usd) / ath_usd * 100):.2f}%\n")
            
            return data  # Return full data dictionary
        
        # ----------------------------------------------------------------
        # HANDLE CRYPTO NOT FOUND
        # ----------------------------------------------------------------
        else:
            print(f"❌ Could not find crypto: {crypto_name}")
            return None
    
    # ----------------------------------------------------------------
    # EXCEPTION HANDLING
    # ----------------------------------------------------------------
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# ============================================================================
# FUNCTION 3: LIVE PRICE TRACKER (AUTO-REFRESH)
# ============================================================================
def live_tracker(seconds=60):
    """
    Continuously monitors crypto prices with automatic refresh.
    
    Args:
        seconds (int): Time between updates (default: 60 seconds)
    
    WARNING: 
        - Don't set refresh rate too low (< 10 seconds) or API will rate-limit you
        - Press Ctrl+C to stop the tracker
    
    Rate Limits:
        - CoinGecko free tier: ~10-50 calls/minute depending on endpoint
        - Recommended minimum: 30-60 seconds between refreshes
    """
    print("\n🔴 LIVE TRACKER MODE")
    print(f"Updating every {seconds} seconds...")
    print("Press Ctrl+C to stop\n")
    
    try:
        # ----------------------------------------------------------------
        # INFINITE LOOP - Runs until user stops it
        # ----------------------------------------------------------------
        while True:
            # Fetch and display current prices
            get_crypto_prices()
            
            # Show countdown message
            print(f"\n⏳ Refreshing in {seconds} seconds...\n")
            
            # Wait before next update (this is blocking - script pauses here)
            time.sleep(seconds)
            
            # Visual separator between updates
            print("\n" + "="*70 + "\n")
    
    # ----------------------------------------------------------------
    # HANDLE KEYBOARD INTERRUPT (Ctrl+C)
    # ----------------------------------------------------------------
    except KeyboardInterrupt:
        print("\n\n✋ Tracker stopped by user. Goodbye!")


# ============================================================================
# MAIN PROGRAM EXECUTION
# ============================================================================
if __name__ == "__main__":
    """
    This block only runs when script is executed directly (not imported).
    It's the entry point of the program.
    """
    
    # ----------------------------------------------------------------
    # DISPLAY WELCOME BANNER
    # ----------------------------------------------------------------
    print("=" * 70)
    print("  CRYPTOCURRENCY PRICE TRACKER".center(70))
    print("  (Powered by CoinGecko API - 100% Free!)".center(70))
    print("=" * 70)
    print()
    
    # ----------------------------------------------------------------
    # FETCH AND DISPLAY CRYPTO PRICES
    # ----------------------------------------------------------------
    crypto_data = get_crypto_prices()  # Call main function
    
    # ----------------------------------------------------------------
    # SHOW USAGE TIPS (Only if data fetch was successful)
    # ----------------------------------------------------------------
    if crypto_data:
        print("\n" + "=" * 70)
        print("\n💡 WHAT YOU CAN DO:")
        print("   • This uses CoinGecko's FREE public API")
        print("   • NO web scraping - official API endpoint")
        print("   • NO API key needed for basic use")
        print("   • Updates are real-time!")
        print()
        print("🎯 NEXT STEPS:")
        print("   1. Uncomment line below to get detailed Bitcoin info")
        print("   2. Track your favorite coins by editing the 'ids' list")
        print("   3. Set up alerts for specific price targets")
        print("   4. Save price history to a CSV file")
        print("   5. Uncomment live_tracker() for auto-refresh mode")
        print()
        print("📝 RAM Usage: ~30-40MB - Completely safe!")
        print()
        
        # ----------------------------------------------------------------
        # OPTIONAL FEATURES (Commented out by default)
        # ----------------------------------------------------------------
        # Uncomment the line below to get detailed Bitcoin information:
        # get_single_crypto('bitcoin')
        
        # Uncomment the line below to enable LIVE tracking mode:
        # WARNING: Don't set seconds too low or API will block you!
        # Recommended: Keep at 60 seconds or higher
        # live_tracker(seconds=60)
    
    # ----------------------------------------------------------------
    # CLOSING BANNER
    # ----------------------------------------------------------------
    print("=" * 70)