import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd

# download NLTK stopwords
nltk.download('stopwords')
nltk.download('wordnet')


def clean_doc(doc):
    # Remove HTML tags using regex
    doc = re.sub(r'<[^>]+>', '', doc)

    # Convert text to lowercase
    doc = doc.lower()

    # Split into tokens by white space
    tokens = doc.split()

    # Prepare regex for char filtering
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))

    # Remove punctuation from each word
    tokens = [re_punc.sub('', w) for w in tokens]

    # Remove non-alphabetic tokens
    tokens = [word for word in tokens if word.isalpha()]

    # Initialize the WordNet Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Perform lemmatization on each word
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Filter out stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]

    # Filter out short tokens
    tokens = [word for word in tokens if len(word) > 1]

    # Join the tokens back into a single string
    cleaned_text = ' '.join(tokens)

    return cleaned_text


def decimal_to_percentage(decimal_number):
    percentage = decimal_number * 100
    return round(percentage, 2)


def get_prediction(source, content, model, vectorizer):
    clean_content = clean_doc(content)

    post_df = pd.DataFrame({'source': [source], 'content': [clean_content]})

    X = post_df['source'] + ' ' + post_df['content']
    X_vec = vectorizer.transform(X)
    y_pred = model.predict(X_vec)[0]
    y_pred_prob = model.predict_proba(X_vec)[0]

    if y_pred == 0:
        classification = 'not credible'
    else:
        classification = 'credible'

    result = {
        'classification': classification,
        'prob_negative': decimal_to_percentage(y_pred_prob[0]),
        'prob_positive': decimal_to_percentage(y_pred_prob[1])
    }
    return result
