import re
from collections import Counter

def generate_tags(content):
    
    words = re.findall(r'\b\w+\b', content.lower())

    stop_words = {
        'the', 'and', 'is', 'in', 'to', 'of', 'it', 'for', 'on', 'this', 'that', 
        'with', 'a', 'an', 'as', 'at', 'by', 'be', 'are', 'was', 'were', 'from', 
        'has', 'have', 'or', 'not', 'but', 'so', 'if', 'out', 'about', 'up', 'down', 
        'a', 'b', 'p', 's', 'our', 'like', 'my', 'can', 'also', 'we', 'us', 'they', 'their', 'them', 'its', 'your', 'mine', 'more'
    }, 

    keywords = [word for word in words if word not in stop_words and len(word)>4]

    most_common = Counter(keywords).most_common(5)
    return [word for word, _ in most_common]
