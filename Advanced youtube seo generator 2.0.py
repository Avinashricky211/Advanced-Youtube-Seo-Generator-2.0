import requests
from collections import Counter
import re
import random
from typing import List, Tuple, Optional, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from textblob import TextBlob
import spacy

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

API_KEY = "Enter Your Youtube Data Api Here"  # Replace with your actual YouTube Data API key

# Updated YouTube categories and their corresponding emotional trigger words
YOUTUBE_CATEGORIES = {
    "Film & Animation": ["unbelievable", "groundbreaking", "must-watch", "incredible", "stunning", "amazing", "breathtaking", "epic", "masterpiece", "awesome"],
    "Autos & Vehicles": ["unbelievable", "groundbreaking", "must-see", "incredible", "amazing", "shocking", "revolutionary", "top", "best", "ultimate"],
    "Music": ["unbelievable", "groundbreaking", "must-listen", "incredible", "amazing", "epic", "breathtaking", "awesome", "top", "best"],
    "Pets & Animals": ["adorable", "heartwarming", "must-see", "incredible", "amazing", "cute", "unbelievable", "awesome", "top", "best"],
    "Sports": ["unbelievable", "shocking", "amazing", "incredible", "ultimate", "insane", "must-see", "top", "crazy", "best"],
    "Travel & Events": ["breathtaking", "unbelievable", "must-see", "incredible", "amazing", "stunning", "awesome", "top", "best", "ultimate"],
    "Gaming": ["unbelievable", "groundbreaking", "must-play", "incredible", "amazing", "epic", "awesome", "top", "best", "ultimate"],
    "People & Blogs": ["heartwarming", "inspiring", "must-watch", "incredible", "amazing", "unbelievable", "awesome", "top", "best", "emotional"],
    "Comedy": ["hilarious", "funny", "unbelievable", "must-watch", "incredible", "amazing", "laugh-out-loud", "awesome", "top", "best"],
    "Entertainment": ["hilarious", "shocking", "unbelievable", "crazy", "amazing", "insane", "must-see", "incredible", "top", "best"],
    "News & Politics": ["shocking", "unbelievable", "must-see", "incredible", "breaking", "exclusive", "urgent", "top", "best", "critical"],
    "Howto & Style": ["life-changing", "transformative", "essential", "amazing", "unmissable", "ultimate", "proven", "incredible", "must-try", "fantastic"],
    "Education": ["proven", "unbelievable", "essential", "amazing", "ultimate", "must-know", "top", "effective", "secret", "best"],
    "Science & Technology": ["unbelievable", "groundbreaking", "shocking", "incredible", "amazing", "secret", "ultimate", "must-see", "top", "best"],
    "Nonprofits & Activism": ["inspiring", "heartwarming", "must-see", "incredible", "amazing", "unbelievable", "awesome", "top", "best", "uplifting"],
    "Movies": ["unbelievable", "must-watch", "incredible", "stunning", "epic", "masterpiece", "awesome", "groundbreaking", "top", "best"],
    "Shows": ["binge-worthy", "must-watch", "incredible", "amazing", "addictive", "unbelievable", "awesome", "top", "best", "unmissable"]
}

DEFAULT_CATEGORY = "Entertainment"

def get_top_videos(api_key: str, query: str, max_results: int = 50) -> Optional[List[dict]]:
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults={max_results}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.RequestException as e:
        print(f"Error fetching videos: {e}")
        return None

def preprocess_text(text: str) -> str:
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return ' '.join(text.lower().split())

def identify_category(keyword: str) -> str:
    max_similarity = 0
    best_category = DEFAULT_CATEGORY
    
    for category, trigger_words in YOUTUBE_CATEGORIES.items():
        similarity = len(set(keyword.lower().split()) & set(map(str.lower, trigger_words)))
        if similarity > max_similarity:
            max_similarity = similarity
            best_category = category
    
    return best_category

def generate_titles(keyword: str, category: str) -> List[str]:
    emotional_triggers = YOUTUBE_CATEGORIES.get(category, YOUTUBE_CATEGORIES[DEFAULT_CATEGORY])
    titles = []
    for _ in range(5):
        title_structure = [
            random.choice(emotional_triggers),
            keyword.title(),
            random.choice(["Secrets", "Adventures", "Discoveries", "Explorations"]),
            f"({random.choice(emotional_triggers)} Tips)"
        ]
        new_title = ' '.join(title_structure)
        titles.append(new_title[:70].strip())
    return titles

def generate_description(keyword: str, category: str, title: str) -> str:
    emotional_triggers = YOUTUBE_CATEGORIES.get(category, YOUTUBE_CATEGORIES[DEFAULT_CATEGORY])
    intro = f"{random.choice(emotional_triggers)}! {title} 🚀"
    content_details = f"Embark on an extraordinary journey into the world of {keyword}. Discover hidden gems, expert insights, and breathtaking experiences that will leave you in awe."
    cta = f"🔔 {random.choice(emotional_triggers)}! SUBSCRIBE now for {random.choice(emotional_triggers)} {keyword} content!"
    engagement = f"👇 Share your {random.choice(emotional_triggers)} thoughts! What's your experience with {keyword}?"
    outro = f"Don't miss out on our upcoming videos about {keyword} and related topics. Stay tuned for more {random.choice(emotional_triggers)} content!"
    
    description = f"{intro}\n\n{content_details}\n\n{cta}\n\n{engagement}\n\n{outro}"
    
    return description[:2000].strip()

def generate_tags(keyword: str, category: str) -> List[str]:
    emotional_triggers = YOUTUBE_CATEGORIES.get(category, YOUTUBE_CATEGORIES[DEFAULT_CATEGORY])
    base_tags = keyword.split()
    related_terms = emotional_triggers[:10]  # Use top 10 emotional triggers as related terms
    
    tags = [keyword] + base_tags + related_terms
    tags += [f"{keyword} {term}" for term in related_terms]
    tags += [f"{term} {keyword}" for term in related_terms]
    
    # Remove duplicates and limit to 30 tags
    return list(dict.fromkeys(tags))[:30]

def generate_hashtags(tags: List[str], keyword: str) -> List[str]:
    hashtags = [f"#{tag.replace(' ', '')}" for tag in tags[:14] if len(tag) > 2]
    keyword_hashtag = f"#{keyword.replace(' ', '')}"
    if keyword_hashtag not in hashtags:
        hashtags.insert(0, keyword_hashtag)
    return list(dict.fromkeys(hashtags))[:15]

def calculate_seo_score(title: str, description: str, tags: List[str], hashtags: List[str]) -> int:
    score = 0
    if len(title) <= 70:
        score += 20
    if 500 <= len(description) <= 2000:
        score += 30
    score += min(len(tags), 30)
    score += min(len(hashtags) * 2, 20)
    return min(score, 100)

def get_mock_analytics() -> Dict[str, int]:
    return {
        "views": random.randint(10000, 1000000),
        "likes": random.randint(1000, 100000),
        "comments": random.randint(100, 10000),
        "shares": random.randint(50, 5000)
    }

def generate_seo_content(query: str) -> Tuple[str, str, List[str], List[str], int, Dict[str, int], str]:
    category = identify_category(query)
    titles = generate_titles(query, category)
    
    print("\nGenerated Titles:")
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")
    
    title_choice = int(input("\nSelect a title (1-5): ")) - 1
    selected_title = titles[title_choice]
    
    new_description = generate_description(query, category, selected_title)
    new_tags = generate_tags(query, category)
    new_hashtags = generate_hashtags(new_tags, query)
    
    seo_score = calculate_seo_score(selected_title, new_description, new_tags, new_hashtags)
    mock_analytics = get_mock_analytics()

    return selected_title, new_description, new_tags, new_hashtags, seo_score, mock_analytics, category

def process_keyword(keyword: str) -> None:
    print(f"\nGenerating SEO Content for '{keyword}'...")
    
    title, description, tags, hashtags, seo_score, analytics, category = generate_seo_content(keyword)

    print(f"\n{'='*80}\nSEO Content\n{'='*80}")
    print(f"\nIdentified Category: {category}")
    print(f"\nSelected Title:\n{title}")
    print(f"\nDescription:\n{description}")
    print(f"\nTags:\n{', '.join(tags)}")
    print(f"\nHashtags:\n{' '.join(hashtags)}")
    print(f"\nSEO Score: {seo_score}/100")
    print("\nEstimated Analytics:")
    for key, value in analytics.items():
        print(f"  {key.capitalize()}: {value:,}")

    # Fetch top 50 videos
    top_videos = get_top_videos(API_KEY, keyword)
    if top_videos:
        print(f"\nTop 5 Related Videos:")
        for i, video in enumerate(top_videos[:5], 1):
            print(f"{i}. {video['snippet']['title']}")

def main():
    print("Welcome to the Enhanced YouTube SEO Generator!")
    while True:
        print("\n1. Generate SEO Content")
        print("2. Exit")
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            keyword = input("Enter a keyword to generate SEO content: ")
            process_keyword(keyword)
        elif choice == '2':
            print("Thank you for using the Enhanced YouTube SEO Generator. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()