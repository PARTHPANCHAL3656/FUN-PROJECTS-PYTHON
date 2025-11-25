import requests
from datetime import datetime
import json

def fetch_reddit_news(subreddit="worldnews", limit=10):
    """
    Fetch latest news from Reddit - always current and free!
    
    Popular news subreddits: worldnews, news, technology, science, business
    """
    
    print(f"\n🌍 Fetching latest posts from r/{subreddit}...\n")
    print("=" * 70)
    
    # Reddit's JSON API (no auth needed for public posts)
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
    
    # Reddit requires a user agent
    headers = {
        'User-Agent': 'Python News Fetcher Bot 1.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            
            if not posts:
                print("No posts found!")
                return
            
            count = 0
            for post in posts:
                post_data = post['data']
                
                # Skip stickied posts and non-news content
                if post_data.get('stickied'):
                    continue
                
                count += 1
                title = post_data.get('title', 'No title')
                author = post_data.get('author', 'Unknown')
                score = post_data.get('score', 0)
                url_link = post_data.get('url', '')
                permalink = f"https://www.reddit.com{post_data.get('permalink', '')}"
                created = post_data.get('created_utc', 0)
                
                # Format timestamp
                try:
                    pub_date = datetime.fromtimestamp(created)
                    time_ago = get_time_ago(created)
                    formatted_date = pub_date.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_date = "Unknown date"
                    time_ago = ""
                
                # Print formatted post
                print(f"\n📰 Post {count}")
                print(f"Title: {title}")
                print(f"Posted: {time_ago} | Score: {score}↑")
                print(f"Link: {url_link}")
                print(f"Comments: {permalink}")
                print("-" * 70)
                
                if count >= limit:
                    break
            
            print(f"\n✅ Successfully fetched {count} current posts!")
            
        else:
            print(f"❌ Error: Status code {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def get_time_ago(timestamp):
    """Calculate how long ago something was posted"""
    now = datetime.now().timestamp()
    diff = int(now - timestamp)
    
    if diff < 60:
        return f"{diff} seconds ago"
    elif diff < 3600:
        return f"{diff // 60} minutes ago"
    elif diff < 86400:
        return f"{diff // 3600} hours ago"
    else:
        return f"{diff // 86400} days ago"

def fetch_hacker_news(num_stories=15):
    """
    Fetch top stories from Hacker News - tech news that's always current!
    """
    
    print(f"\n💻 Fetching top stories from Hacker News...\n")
    print("=" * 70)
    
    try:
        # Get top story IDs
        top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(top_url, timeout=10)
        
        if response.status_code == 200:
            story_ids = response.json()[:num_stories]
            
            for i, story_id in enumerate(story_ids, 1):
                # Fetch each story details
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_response = requests.get(story_url, timeout=5)
                
                if story_response.status_code == 200:
                    story = story_response.json()
                    
                    title = story.get('title', 'No title')
                    author = story.get('by', 'Unknown')
                    score = story.get('score', 0)
                    url_link = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                    created = story.get('time', 0)
                    
                    time_ago = get_time_ago(created)
                    
                    print(f"\n📰 Story {i}")
                    print(f"Title: {title}")
                    print(f"Posted: {time_ago} | Score: {score}↑ | By: {author}")
                    print(f"Link: {url_link}")
                    print("-" * 70)
            
            print(f"\n✅ Successfully fetched {len(story_ids)} current stories!")
        else:
            print(f"❌ Error: Status code {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    
    print("\n" + "=" * 70)
    print("📱 CURRENT NEWS FETCHER")
    print("=" * 70)
    
    print("\nChoose your news source:")
    print("  1. Reddit World News (r/worldnews)")
    print("  2. Reddit Technology (r/technology)")
    print("  3. Reddit Science (r/science)")
    print("  4. Reddit General News (r/news)")
    print("  5. Hacker News (Tech/Startup news)")
    print("  6. Custom Reddit subreddit")
    
    try:
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            fetch_reddit_news("worldnews")
        elif choice == "2":
            fetch_reddit_news("technology")
        elif choice == "3":
            fetch_reddit_news("science")
        elif choice == "4":
            fetch_reddit_news("news")
        elif choice == "5":
            fetch_hacker_news()
        elif choice == "6":
            custom = input("Enter subreddit name (without r/): ").strip()
            fetch_reddit_news(custom)
        else:
            print("Invalid choice. Using r/worldnews")
            fetch_reddit_news("worldnews")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")