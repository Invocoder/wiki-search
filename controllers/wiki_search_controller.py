from flask import Flask, request, jsonify
import wikipedia
from bs4 import BeautifulSoup
from collections import Counter
import re
from app import app
import nltk
from nltk.corpus import stopwords

# in-memory database(List) for storing search history
search_history = []

# returns wikipedia page content on a given topic
def get_wikipedia_text(topic):
    try:
        page = wikipedia.page(topic)
        return page.content
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"DisambiguationError: {e.options}")
        return list(e.options)
    except wikipedia.exceptions.PageError:
        return None

# returns top n words of a wikipedia content text
def word_frequency_analysis(text, n):
    # Downloading stop words(if not already downloaded)
    nltk.download('stopwords', quiet=True)

    words = re.findall(r'\b\w+\b', text.lower())

    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    # Calculating frequency of filtered words
    word_frequency = Counter(filtered_words)

    # Calculating top n words frequency
    top_words = word_frequency.most_common(n)
    return top_words

# get api that retruns top n words on a topic from wikipedia
@app.route('/wiki_search', methods=['GET'])
def word_frequency_analysis_endpoint():
    topic = request.args.get('topic')
    n = int(request.args.get('n', 10))

    if not topic:
        return jsonify({'error': 'You have not entered any topic, please provide a topic.'}), 400
    
    text = get_wikipedia_text(topic)

    if isinstance(text, list):
        # Handle disambiguation error
        return jsonify({'error': 'DisambiguationError', 'options': text}), 400
    if text is None:
        return jsonify({'error: No wikipedia article found for the given topic'}), 404
    
    if isinstance(text, list):
        return jsonify({'error': 'DisambiguationError', 'options': text}), 400

    top_words = word_frequency_analysis(text, n)

    result = {'topic': topic, 'top_words': [{'word': word, 'frequency': count} for word, count in top_words]}

    # Update the search history
    search_history.append(result)

    return jsonify(result)

# returns previously searched topics and the corresponding top frequent words 
@app.route('/search_history', methods=['GET'])
def search_history_endpoint():
    return jsonify(search_history)




