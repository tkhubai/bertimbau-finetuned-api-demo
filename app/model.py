import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.consts import classes_result

class BertModel:
    def __init__(self, model_path="models/bertimbau"):
        # Verifica se o dispositivo CUDA está disponível
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Carrega o tokenizador e o modelo
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        # Move o modelo para o dispositivo apropriado
        self.model.to(self.device)
        # Define o modelo em modo de avaliação (sem treinamento, em produção)
        self.model.eval()
    
    def predict(self, text, max_length=128):
        # Adicionar [CLS] e [SEP] ao texto de entrada
        # text = f"[CLS] {text} [SEP]"
        # Tokeniza o texto de entrada
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=max_length
        )
        # Move os inputs para o dispositivo apropriado
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        # Executa o modelo em modo de avaliação (sem treinamento, em produção)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Calcula as probabilidades das classes
        logits = outputs.logits
        # definir a classe
        predicted_class_id = logits.argmax().item()
        # calcular as probabilidades
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        # prediction = torch.argmax(probabilities, dim=-1)
        # Retorna a predição e as probabilidades (em CPU para evitar transferência de GPU)
        # return prediction.cpu().numpy().tolist(), probabilities.cpu().numpy()
        return {
            "class": classes_result[predicted_class_id],
            "class_id": predicted_class_id,
            "probabilities": probabilities.cpu().numpy().tolist()
        }