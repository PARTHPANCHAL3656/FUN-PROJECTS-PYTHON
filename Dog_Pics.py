import requests
import webbrowser
from datetime import datetime

def get_random_dog():
    """
    Gets a random dog image from the Dog API
    Returns the image URL or None if request fails
    """
    print("🐕 Fetching a random dog picture...")
    
    try:
        # Dog API - completely free, no key needed!
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            return data['message']  # The image URL is in 'message'
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Dog API: {e}")
        return None

def get_dog_fact():
    """
    Gets a random dog fact from the Dog Facts API
    Returns the fact text or None if request fails
    """
    print("📚 Fetching a dog fact...")
    
    try:
        # Dog Facts API - also completely free!
        response = requests.get('https://dogapi.dog/api/v2/facts')
        
        if response.status_code == 200:
            data = response.json()
            # The fact is nested in the response
            return data['data'][0]['attributes']['body']
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Dog Facts API: {e}")
        return None

def main():
    """
    Main function that runs the dog picture & fact generator
    """
    print("=" * 50)
    print("🐶 RANDOM DOG PICTURE & FACT GENERATOR 🐶")
    print("=" * 50)
    print()
    
    # Get a random dog picture
    dog_image_url = get_random_dog()
    
    # Get a random dog fact
    dog_fact = get_dog_fact()
    
    print()
    print("-" * 50)
    
    # Display results
    if dog_image_url:
        print(f"✅ Dog Picture URL: {dog_image_url}")
        
        # Extract breed from URL (the URL structure includes breed name)
        # Example: https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg
        try:
            breed_part = dog_image_url.split('/breeds/')[1].split('/')[0]
            breed = breed_part.replace('-', ' ').title()
            print(f"🐕 Breed: {breed}")
        except:
            print("🐕 Breed: Unknown")
    else:
        print("❌ Could not fetch dog picture")
    
    print()
    
    if dog_fact:
        print(f"💡 Dog Fact: {dog_fact}")
    else:
        print("❌ Could not fetch dog fact")
    
    print()
    print("-" * 50)
    
    # Ask if user wants to open the image in browser
    if dog_image_url:
        print()
        choice = input("Would you like to open the dog picture in your browser? (yes/no): ").lower()
        
        if choice in ['yes', 'y']:
            print("🌐 Opening image in browser...")
            webbrowser.open(dog_image_url)
        else:
            print("👋 Thanks for using the Dog Generator!")
    
    # Ask if user wants to see another dog
    print()
    again = input("\nWant to see another dog? (yes/no): ").lower()
    
    if again in ['yes', 'y']:
        print("\n" * 2)
        main()  # Run the program again!
    else:
        print("\n🐾 Thanks for playing! See you next time! 🐾")

# Run the program
if __name__ == "__main__":
    main()