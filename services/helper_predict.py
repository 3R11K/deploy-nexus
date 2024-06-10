import pickle
import pandas as pd
import numpy as np
def load_logistic_model():
    """
    Carrega o modelo de Regressão Logística a partir de um arquivo pickle.
    Returns:
        model: O modelo de Regressão Logística carregado.
    """
    path = './models/logistic_regression_model.pkl'
    with open(path, 'rb') as file:
        model = pickle.load(file)
    print(type(model))
    return model
model = load_logistic_model()
def predict(data):
    """
    Aplica o modelo de Regressão Logística para prever sentimentos.
    Args:
        data (list or np.ndarray): Lista de listas ou array NumPy representando vetores de características de frases.
    Returns:
        np.ndarray: Uma lista de previsões (0 ou 1).
    """
    data = np.array(data).reshape(1, -1)
    predict = model.predict(data)
    return predict