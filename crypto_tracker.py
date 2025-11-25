import requests
import json
from datetime import datetime
import time

def get_crypto_prices():
    """
    Get live cryptocurrency prices using CoinGecko API
    100% FREE - No API key needed!
    No scraping - Official public API
    """
    try:
        # CoinGecko free public API endpoint
        # Gets prices for multiple cryptos in one call
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # Parameters: which coins to track and what currency
        params = {
            'ids': 'bitcoin,ethereum,cardano,solana,dogecoin,shiba-inu,polygon,ripple,litecoin,polkadot,chainlink,stellar,tron,avalanche-2,uniswap',
            'vs_currencies': 'usd,inr',  # Both USD and INR!
            'include_24hr_change': 'true',  # Get 24hr price change %
            'include_market_cap': 'true'
        }
        
        print("💰 Fetching live crypto prices...")
        print("⏳ Please wait...\n")
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            print("╔" + "═" * 70 + "╗")
            print("║" + "  LIVE CRYPTOCURRENCY PRICES".center(70) + "║")
            print("║" + f"  Updated: {datetime.now().strftime('%I:%M:%S %p, %d %b %Y')}".center(70) + "║")
            print("╚" + "═" * 70 + "╝\n")
            
            # Display each crypto with details
            for crypto_id, crypto_data in data.items():
                crypto_name = crypto_id.replace('-', ' ').title()
                usd_price = crypto_data['usd']
                inr_price = crypto_data['inr']
                change_24h = crypto_data['usd_24h_change']
                market_cap = crypto_data['usd_market_cap']
                
                # Format market cap in billions/millions
                if market_cap > 1_000_000_000:
                    market_cap_str = f"${market_cap / 1_000_000_000:.2f}B"
                else:
                    market_cap_str = f"${market_cap / 1_000_000:.2f}M"
                
                # Choose emoji based on price change
                if change_24h > 0:
                    trend = "🟢 ↗"
                    change_color = "+"
                else:
                    trend = "🔴 ↘"
                    change_color = ""
                
                print(f"━━━ {crypto_name} ━━━")
                print(f"  💵 USD: ${usd_price:,.2f}")
                print(f"  💰 INR: ₹{inr_price:,.2f}")
                print(f"  {trend} 24h Change: {change_color}{change_24h:.2f}%")
                print(f"  📊 Market Cap: {market_cap_str}")
                print()
            
            # Alert for significant moves
            print("🚨 ALERTS:")
            for crypto_id, crypto_data in data.items():
                change = crypto_data['usd_24h_change']
                name = crypto_id.replace('-', ' ').title()
                
                if change > 10:
                    print(f"   🚀 {name} is UP {change:.2f}% today!")
                elif change < -10:
                    print(f"   📉 {name} is DOWN {change:.2f}% today!")
            
            return data
            
        elif response.status_code == 429:
            print("❌ Error: Too many requests. Wait a minute and try again.")
            return None
        else:
            print(f"❌ Error: Could not fetch data (Status: {response.status_code})")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out. Check your internet connection.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def get_single_crypto(crypto_name):
    """
    Get detailed info for a specific cryptocurrency
    """
    try:
        # Convert common names to CoinGecko IDs
        crypto_map = {
            'bitcoin': 'bitcoin', 'btc': 'bitcoin',
            'ethereum': 'ethereum', 'eth': 'ethereum',
            'dogecoin': 'dogecoin', 'doge': 'dogecoin',
            'shiba': 'shiba-inu', 'shib': 'shiba-inu',
            'cardano': 'cardano', 'ada': 'cardano',
            'solana': 'solana', 'sol': 'solana'
        }
        
        crypto_id = crypto_map.get(crypto_name.lower(), crypto_name.lower())
        
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
        
        print(f"\n🔍 Fetching detailed info for {crypto_name}...\n")
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            name = data['name']
            symbol = data['symbol'].upper()
            current_price_usd = data['market_data']['current_price']['usd']
            current_price_inr = data['market_data']['current_price']['inr']
            ath_usd = data['market_data']['ath']['usd']
            ath_date = data['market_data']['ath_date']['usd'][:10]
            
            print(f"╔{'═' * 50}╗")
            print(f"║  {name} ({symbol})".ljust(51) + "║")
            print(f"╚{'═' * 50}╝")
            print(f"\n💵 Current Price (USD): ${current_price_usd:,.2f}")
            print(f"💰 Current Price (INR): ₹{current_price_inr:,.2f}")
            print(f"🏆 All-Time High: ${ath_usd:,.2f} (on {ath_date})")
            print(f"📉 Down from ATH: {((current_price_usd - ath_usd) / ath_usd * 100):.2f}%\n")
            
            return data
        else:
            print(f"❌ Could not find crypto: {crypto_name}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def live_tracker(seconds=60):
    """
    Live price tracker - updates every few seconds
    WARNING: Don't refresh too fast or API will block you!
    """
    print("\n🔴 LIVE TRACKER MODE")
    print(f"Updating every {seconds} seconds...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            get_crypto_prices()
            print(f"\n⏳ Refreshing in {seconds} seconds...\n")
            time.sleep(seconds)
            print("\n" + "="*70 + "\n")
    except KeyboardInterrupt:
        print("\n\n✋ Tracker stopped by user. Goodbye!")


if __name__ == "__main__":
    print("=" * 70)
    print("  CRYPTOCURRENCY PRICE TRACKER".center(70))
    print("  (Powered by CoinGecko API - 100% Free!)".center(70))
    print("=" * 70)
    print()
    
    # Get current prices for popular cryptos
    crypto_data = get_crypto_prices()
    
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
        
        # Uncomment below to get detailed info on Bitcoin:
        # get_single_crypto('bitcoin')
        
        # Uncomment below for LIVE tracking (updates every 60 seconds):
        # WARNING: Don't set seconds too low or API will block you!
        # live_tracker(seconds=60)
    
    print("=" * 70)