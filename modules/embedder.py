from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import hashlib

def sliding_windows(text : str , window_size = 150 , step = 100 , min_tokens = 10):
    assert step <= window_size, "Step cannot be larger than window_size, otherwise no overlap happens."
    tokens = nltk.word_tokenize(text)
    windows = []
    for i in range(0,len(tokens),step):
        window = tokens[i:i+window_size]
        if len(window) < min_tokens:
            break
        windows.append(window)
    return windows


def window_vect(windows : list):
    result = []
    windows_str = [" ".join(w) for w in windows]
    tfidf = TfidfVectorizer()
    result = tfidf.fit_transform(windows_str)
    
    embeddings = [result[i].toarray().flatten().astype('float32') for i in range(result.shape[0])]

    return embeddings


def Compute_Hash(text : str) -> str:
    hash_object = hashlib.sha256(text.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig