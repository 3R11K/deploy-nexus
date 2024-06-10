import pandas as pd
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

nlp = spacy.load("en_core_web_sm")

# Função para carregar o csv e devolvê-lo como dataframe
def carrega_dados(caminho_arquivo, coluna_texto):
    """
    retorna os dados do arquivo csv, mais em especifico a coluna de texto

    Args:
        caminho_arquivo: str - O caminho para o arquivo CSV.
        coluna_texto: str - O nome da coluna no CSV que contém os textos.

    Returns:
        list: Uma lista que representa o dataframe com os textos
    """
    dados = pd.read_csv(caminho_arquivo)
    dados.dropna(subset=[coluna_texto], inplace=True)  # Remove NaN values from the specified column
    return dados[coluna_texto].to_list()


# Função para remover 'https' ou 'http'
def remove_http(texto):
    '''
    Função que remove palavras que começam com http ou https
    
    Args:
        texto : str -> texto que será processado
    
    Returns:
        texto : str -> texto sem as palavras que começam com http ou https
    '''
    
    # Expressão regular para identificar palavras que começam com http ou https
    padrao = r'\b(?:https?://\S+)\b'
    
    # Substitui as palavras que correspondem ao padrão por uma string vazia
    texto_sem_http = re.sub(padrao, '', texto)
    
    return texto_sem_http


# Função para tokenizar
def tokenizar(texto, ):
    """
    Tokeniza um texto em palavras usando um modelo de processamento de linguagem.

    Args:
        texto: str - O texto a ser tokenizado em palavras.
        : Modelo de processamento de linguagem.
    Returns:
        list: Uma lista de palavras tokenizadas.
    """
    # Processa o texto usando o modelo SpaCy

    doc = nlp(texto)
    # Extrai os tokens do documento e retorna como lista de textos de tokens em minúsculas
    tokens = [token.text.lower() for token in doc if not token.is_punct and not token.is_space]
    return tokens


# Função para remover stop-words
def remove_stop_words(tokens):
    """
    Remove as stop words de uma lista de tokens.

    Args:
        tokens: list - Uma lista de tokens.

    Returns:
        list: Uma lista de tokens sem as stop words.
    """
    # Carrega as stop words do modelo SpaCy
    stop_words = nlp.Defaults.stop_words

    # Remove as stop words dos tokens
    return [token for token in tokens if token not in stop_words]


# Função para lematizar as palavras
def lematizacao(tokens):
    """
    Transforma cada palavra para sua base usando um lematizador.

    Args:
        tokens: list - Uma lista de palavras a serem lematizadas.
        : Language - Modelo SpaCy carregado para processamento de linguagem.

    Returns:
        list: Uma lista das palavras lematizadas.
    """

    # Processa a string obtida pela junção dos elementos da lista
    doc = nlp(' '.join(tokens))

    # Extrai o lema de cada token no documento e armazena na nova lista
    frase_lematizada = [token.lemma_ for token in doc]
    
    # Retorna a lista lematizada
    return frase_lematizada


def pipeline(texto):
    """
    Executa um pipeline de processamento de texto.

    Args:
        : Language - Modelo SpaCy carregado para processamento de linguagem.
        texto: str - O texto a ser processado.

    Returns:
        list: Uma lista de frases segmentadas.
        list: Uma lista de tokens.
        list: Uma lista de tokens sem stop words.
        list: Uma lista de tokens lematizados.
        list: Uma lista de tuplas com as entidades e tipos.
    """


    #remove os links
    newTexto = remove_http(texto)

    # Tokeniza o texto
    tokens = tokenizar(newTexto)

    # Remove as stop words
    tokens_sem_stop_words = remove_stop_words(tokens)
    
    tokens_lematizados = lematizacao(tokens_sem_stop_words)


    return " ".join(tokens_lematizados)



