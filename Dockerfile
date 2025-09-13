FROM python:3.9-slim

# Definir variáveis de ambiente para CPU
ENV CUDA_VISIBLE_DEVICES=""
ENV TF_FORCE_GPU_ALLOW_GROWTH="false"
ENV TF_CPP_MIN_LOG_LEVEL="2"

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copiar requirements primeiro para aproveitar cache do Docker
COPY app/requirements.txt /workspace/app/requirements.txt
# RUN pip install torch==2.2.2+cpu torchvision==0.17.2+cpu torchaudio==0.10.1+cpu --index-url https://download.pytorch.org/whl/cpu
RUN pip install torch==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r /workspace/app/requirements.txt

# Copiar o código da aplicação
COPY app/ /workspace/app/

# Copiar o modelo (você pode montar como volume também)
COPY models/ /workspace/models/

# Expor a porta
EXPOSE 8000

ENV PYTHONPATH=/workspace

# Comando para rodar a aplicação
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
