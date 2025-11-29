import requests
import webbrowser
from datetime import datetime

def get_random_cat():
    """
    Gets a random cat image from The Cat API
    Returns the image URL or None if request fails
    """
    print("🐱 Fetching a random cat picture...")
    
    try:
        # The Cat API - completely free, no key needed!
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            return data[0]['url']  # The image URL is in the first result
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Cat API: {e}")
        return None

def get_cat_fact():
    """
    Gets a random cat fact from the Cat Facts API
    Returns the fact text or None if request fails
    """
    print("📚 Fetching a cat fact...")
    
    try:
        # Cat Facts API - also completely free!
        response = requests.get('https://catfact.ninja/fact')
        
        if response.status_code == 200:
            data = response.json()
            # The fact is directly in 'fact' field
            return data['fact']
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Cat Facts API: {e}")
        return None

def main():
    """
    Main function that runs the cat picture & fact generator
    """
    print("=" * 50)
    print("😺 RANDOM CAT PICTURE & FACT GENERATOR 😺")
    print("=" * 50)
    print()
    
    # Get a random cat picture
    cat_image_url = get_random_cat()
    
    # Get a random cat fact
    cat_fact = get_cat_fact()
    
    print()
    print("-" * 50)
    
    # Display results
    if cat_image_url:
        print(f"✅ Cat Picture URL: {cat_image_url}")
        print(f"😸 Ready to see an adorable cat!")
    else:
        print("❌ Could not fetch cat picture")
    
    print()
    
    if cat_fact:
        print(f"💡 Cat Fact: {cat_fact}")
    else:
        print("❌ Could not fetch cat fact")
    
    print()
    print("-" * 50)
    
    # Ask if user wants to open the image in browser
    if cat_image_url:
        print()
        choice = input("Would you like to open the cat picture in your browser? (yes/no): ").lower()
        
        if choice in ['yes', 'y']:
            print("🌐 Opening image in browser...")
            webbrowser.open(cat_image_url)
        else:
            print("👋 Thanks for using the Cat Generator!")
    
    # Ask if user wants to see another cat
    print()
    again = input("\nWant to see another cat? (yes/no): ").lower()
    
    if again in ['yes', 'y']:
        print("\n" * 2)
        main()  # Run the program again!
    else:
        print("\n🐾 Thanks for playing! See you next time! 🐾")

# Run the program
if __name__ == "__main__":
    main()