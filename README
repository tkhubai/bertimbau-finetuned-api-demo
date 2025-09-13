# BERTimbau Fine-tuned API - Docker Implementation - Demo

## 📋 Sobre o Projeto

Demo de API para inferência de modelos BERTimbau fine-tuned, containerizada com Docker e otimizada para CPU.

## 🚀 Características Principais

- **✅ 100% Offline** - Não requer conexão com Hugging Face Hub
- **⚡ Otimizado para CPU** - Configuração específica para melhor performance
- **🐳 Dockerizado** - Fácil deploy e reprodução de ambiente
- **🔧 FastAPI** - API moderna com documentação automática
- **📊 Monitoramento** - Endpoints de health check e métricas

## 🏗️ Estrutura do Projeto

```
bertimbau-app/
├── app/
│   ├── api.py              # FastAPI application
│   ├── model.py           # Classe do modelo BERTimbau
│   ├── requirements.txt    # Dependências Python
│   └── test.py            # Scripts de teste
├── models/
│   └── seu-modelo-finetuned/  # Modelo fine-tuned
│       ├── config.json
│       ├── pytorch_model.bin
│       ├── vocab.txt
│       ├── tokenizer_config.json
│       └── special_tokens_map.json
├── Dockerfile             # Configuração do container
└── README.md             # Este arquivo
```

## 📦 Dependências

### Python Packages (requirements.txt)
```txt
# torch==2.2.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
transformers==4.45.2      # Hugging Face Transformers
protobuf==3.20.3          # Protocol Buffers
fastapi==0.115.2          # Framework API moderno
uvicorn==0.32.0           # ASGI server
pydantic==2.9.2           # Validação de dados
numpy==1.26.4             # Computação numérica
torch==2.2.2+cpu          # PyTorch para CPU
```

## 🐳 Configuração Docker

### Dockerfile
```dockerfile
FROM python:3.9-slim

# Variáveis de ambiente para CPU
ENV CUDA_VISIBLE_DEVICES=""
ENV TF_FORCE_GPU_ALLOW_GROWTH="false"
ENV TF_CPP_MIN_LOG_LEVEL="2"

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Instalar PyTorch para CPU
RUN pip install torch==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu

# Instalar demais dependências
COPY app/requirements.txt /workspace/app/requirements.txt
RUN pip install --no-cache-dir -r /workspace/app/requirements.txt

# Copiar código e modelos
COPY app/ /workspace/app/
COPY models/ /workspace/models/

EXPOSE 8000
ENV PYTHONPATH=/workspace

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🚀 Como Executar

### 1. Build da Imagem Docker
```bash
docker buildx build -t bertimbau-api .
```

### 2. Executar em Docker
```bash
docker run -p 8000:8000 \
  -v $(pwd)/models:/workspace/models \
  -v $(pwd)/app:/workspace/app \
  bertimbau-api
```

### 3. Executar localmente
```bash
> pip install --no-cache-dir -r requirements.txt
> PYTHONPATH=/app uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 Endpoints da API

### Health Check
```bash
GET http://localhost:8000/health
```
**Resposta:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "offline": true
}
```

### Informações do Modelo
```bash
GET http://localhost:8000/model-info
```

### Predição (POST)
```bash
POST http://localhost:8000/predict
Content-Type: application/json

{
  "text": "Este é um texto de exemplo para classificação.",
  "max_length": 128
}
```

**Resposta:**
```json
{
  "prediction": [0],
  "probabilities": [[0.1, 0.9]],
  "model_loaded": true
}
```

## 🧪 Testes

### Testar o Modelo Localmente
```bash
docker exec bertimbau-api python app/test.py
```

### Testar Configuração CPU
```bash
docker exec bertimbau-api python app/test_cpu.py
```

### Testar via curl
```bash
# Health check
curl http://localhost:8000/health

# Predição
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text":"O modelo está funcionando perfeitamente!"}'
```

## ⚙️ Configurações de Otimização

### Variáveis de Ambiente para CPU
```bash
CUDA_VISIBLE_DEVICES=""          # Desabilita CUDA
TF_FORCE_GPU_ALLOW_GROWTH="false" # Previne alocação de GPU
TF_CPP_MIN_LOG_LEVEL="2"         # Reduce TensorFlow logging
PYTHONPATH="/workspace"          # Python path configuration
```

### Otimizações no Código
- `torch.set_grad_enabled(False)` - Desabilita gradientes
- `model.eval()` - Modo de avaliação
- `with torch.no_grad():` - Inference sem gradientes

## 🔧 Troubleshooting

### Erro: Module not found
```bash
# Verificar PYTHONPATH
docker exec bertimbau-api echo $PYTHONPATH

# Verificar estrutura de arquivos
docker exec bertimbau-api ls -la /workspace/app/
```

### Erro: Modelo não carrega
```bash
# Verificar se os arquivos do modelo estão presentes
docker exec bertimbau-api ls -la /workspace/models/seu-modelo-finetuned/
```

### Performance Lenta
```bash
# Aumentar número de threads CPU
docker run -e OMP_NUM_THREADS=4 -e MKL_NUM_THREADS=4 ...
```

## 📊 Monitoramento

### Logs da Aplicação
```bash
docker logs bertimbau-api -f
```

### Uso de Recursos
```bash
docker stats bertimbau-api
```

### Health Check Automático
```bash
# Verificar status periodicamente
watch -n 5 curl -s http://localhost:8000/health
```

## 🛠️ Desenvolvimento

### Modo Desenvolvimento com Hot Reload
```bash
# Modificar o CMD no Dockerfile para:
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Testar Alterações sem Rebuild
```bash
# O volume ./app mapeado permite alterações em tempo real
# Edite os arquivos em ./app/ e a API recarregará automaticamente
```

## 📈 Performance Tips

1. **Batch Processing**: Processar múltiplos textos de uma vez
2. **Tokenization Cache**: Cache de tokens para textos repetidos
3. **Model Quantization**: Usar torch.quantization para melhor performance
4. **Thread Optimization**: Ajustar OMP_NUM_THREADS baseado no CPU

## 🔒 Considerações de Segurança

- ✅ API roda localmente (127.0.0.1)
- ✅ Sem dependências externas
- ✅ Modelos locais apenas
- ✅ Sem exposição desnecessária de ports

## 📝 Próximos Passos

1. [ ] Adicionar autenticação à API
2. [ ] Implementar rate limiting
3. [ ] Adicionar monitoring com Prometheus
4. [ ] Criar testes unitários completos
5. [ ] Implementar batch processing

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas changes (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Para issues e dúvidas:
1. Verifique os logs: `docker logs bertimbau-api`
2. Teste a configuração: `docker exec bertimbau-api python app/test_cpu.py`
3. Verifique se todos os arquivos do modelo estão presentes

---

**⭐ Se este projeto foi útil, deixe uma star no repositório!**