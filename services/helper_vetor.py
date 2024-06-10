from gensim.models import KeyedVectors
import numpy as np
import pandas as pd

model_path = './models/GoogleNews-vectors-negative300.bin'

model = KeyedVectors.load_word2vec_format(model_path, binary=True)

def get_average_word2vec(tokens_list, model, generate_missing=False, k=300):
    """
    Obtém o vetor médio de um texto usando um modelo Word2Vec.
    
    Args:
        tokens_list (list): Lista de tokens.
        model (KeyedVectors): Modelo Word2Vec treinado.
        generate_missing (bool): Se True, gera vetores para palavras ausentes no modelo.
        k (int): Dimensão do vetor.
    
    Returns:
        np.array: Vetor médio do texto.
    """
    if len(tokens_list) < 1:
        return np.zeros(k)
    vectorized = [model[word] if word in model else np.zeros(k) for word in tokens_list]
    avg_vec = np.mean(vectorized, axis=0)
    return avg_vec

def vectorize_text(df):
    """
    Vetoriza um texto usando um modelo Word2Vec.
    
    Args:
        df (DataFrame): DataFrame contendo os textos.
        model (KeyedVectors): Modelo Word2Vec treinado.
        
    Returns:
        np.array: Vetores dos textos.
    """
    
    #se df for uma string, transforma num df onde a coluna com os textos é chamada 'text'
    if isinstance(df, str):
        df = pd.DataFrame({'text': [df]})     
    vectorized_texts = []
    for text in df["text"].values.tolist():
        print(text)
        tokens = text.split()
        vectorized_texts.append(get_average_word2vec(tokens, model))
    return np.array(vectorized_texts)