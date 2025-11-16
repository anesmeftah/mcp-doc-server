from sklearn.feature_extraction.text import TfidfVectorizer

def sliding_windows(tokens : str , window_size = 150 , step = 100 , min_tokens = 10):
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

    embeddings = [result[i].toarray().astype('float32') for i in range(result.shape[0])]

    return embeddings
