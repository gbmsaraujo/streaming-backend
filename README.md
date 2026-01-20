# 🎬 Video Streaming Platform

> Plataforma de streaming de vídeo otimizada com Python, focada em performance e técnicas avançadas de otimização de memória.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Sobre o Projeto

Este projeto implementa um servidor de streaming de vídeo HTTP otimizado, construído como base para um sistema mais robusto de streaming de conteúdo. A aplicação demonstra conceitos avançados de Python como `memoryview` para operações zero-copy, generators para streaming eficiente e arquitetura limpa com separação de responsabilidades.

### 🎯 Objetivos

- **Performance**: Otimização de memória usando `memoryview` e técnicas de zero-copy
- **Escalabilidade**: Streaming eficiente com generators e chunked transfer
- **Arquitetura Limpa**: Separação em camadas (drivers, interfaces, factories, utils)
- **Extensibilidade**: Base sólida para features avançadas (Range Requests, WebSocket, Cache)

---

## ✨ Features Implementadas

### ✅ Core

- [x] **Streaming HTTP básico** - Transmissão de vídeos MP4 via HTTP
- [x] **Listagem de vídeos** - Endpoint para listar vídeos disponíveis
- [x] **Otimização com memoryview** - Zero-copy para melhor performance de memória
- [x] **CORS configurado** - Permite requisições do frontend
- [x] **Chunked transfer** - Streaming em chunks de 64KB

### 🏗️ Arquitetura

- [x] **Clean Architecture** - Separação em camadas (drivers, interfaces, factories)
- [x] **Dependency Injection** - Factory pattern para instanciação de dependências
- [x] **Interface-based design** - Abstrações para facilitar testes e manutenção

---

## 🚀 Tecnologias Utilizadas

### Backend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.12+ | Linguagem principal |
| **FastAPI** | 0.128+ | Framework web assíncrono |
| **Uvicorn** | 0.40+ | Servidor ASGI de alta performance |
| **aiofiles** | 25.1+ | I/O de arquivos assíncrono |
| **websockets** | 16.0+ | Suporte a WebSocket (futuro) |

### Dev Tools

| Ferramenta | Uso |
|------------|-----|
| **uv** | Gerenciador de pacotes rápido |
| **ruff** | Linter e formatter ultra-rápido |
| **py-spy** | Profiler de performance |
| **memory-profiler** | Análise de uso de memória |

---

## 📂 Estrutura do Projeto

```
streaming-backend/
├── src/
│   ├── server/
│   │   ├── __init__.py
│   │   └── app.py              # Servidor FastAPI e endpoints
│   │
│   ├── streaming/
│   │   ├── __init__.py
│   │   └── reader.py           # Leitor de vídeo com memoryview
│   │
│   ├── drivers/
│   │   ├── __init__.py
│   │   └── path_driver.py      # Driver de manipulação de paths
│   │
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── video_path_interface.py  # Interface abstrata
│   │
│   ├── factories/
│   │   └── video_reader_factory.py  # Factory para DI
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── fastapi_utils.py    # Utilitários para FastAPI
│   │
│   ├── tests/
│   │   └── benchmark_memoryview.py  # Benchmarks de performance
│   │
│   └── videos/                 # Diretório de vídeos (não versionado)
│
├── run.py                      # Script de inicialização
├── pyproject.toml              # Configuração do projeto e dependências
└── README.md                   # Este arquivo
```

---

## 🔧 Instalação

### Pré-requisitos

- Python 3.12 ou superior
- [uv](https://github.com/astral-sh/uv) (recomendado) ou pip

### Setup Rápido

```bash
# Clone o repositório
git clone <seu-repo>
cd streaming-backend

# Instale dependências com uv (recomendado)
uv sync

# Ou com pip
pip install -e .

# Ative o ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### Adicionar Vídeos de Teste

```bash
# Crie o diretório de vídeos
mkdir -p src/videos

# Baixe um vídeo de exemplo
curl -o src/videos/sample.mp4 "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
```

---

## 🎮 Como Usar

### Iniciar o Servidor

```bash
# Método 1: Usando o script run.py
python run.py

# Método 2: Usando uvicorn diretamente
uvicorn src.server.app:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em: **http://localhost:8000**

### Endpoints Disponíveis

#### 📋 Listar Vídeos

```bash
GET /api/videos

# Resposta:
{
  "videos": ["sample.mp4", "video2.mp4"],
  "status": "ok"
}
```

#### 🎥 Stream de Vídeo

```bash
GET /api/stream/{video_name}

# Exemplo:
curl http://localhost:8000/api/stream/sample.mp4 -o output.mp4
```

#### 🔍 Health Check

```bash
GET /

# Ou acesse no navegador
http://localhost:8000
```

---

## 🧪 Testes e Benchmarks

### Executar Benchmarks de Memoryview

```bash
python src/tests/benchmark_memoryview.py
```

### Profiling com py-spy

```bash
# Flame graph de CPU
py-spy record -o profile.svg -- python -m uvicorn src.server.app:app

# Monitoramento em tempo real
py-spy top -- python -m uvicorn src.server.app:app
```

---

## 📊 Performance

### Otimizações Implementadas

| Técnica | Benefício |
|---------|-----------|
| **memoryview** | ~30% menos uso de memória em operações de slice |
| **Chunked transfer** | Streaming de grandes arquivos sem carregar tudo na RAM |
| **Generators** | Lazy evaluation, memória constante independente do tamanho do arquivo |
| **Async I/O** | Melhor utilização de recursos em múltiplas conexões |

---

## 🎯 Próximas Melhorias

### 🔴 Prioridade Alta

- [ ] **Range Requests** - Suporte completo a HTTP Range para seek no vídeo
- [ ] **Content-Length correto** - Header com tamanho total do arquivo
- [ ] **Sistema de métricas** - Monitoramento de throughput, memória e CPU
- [ ] **Logging estruturado** - Logs profissionais com níveis e formatação
- [ ] **Testes automatizados** - Cobertura com pytest

### 🟡 Prioridade Média

- [ ] **Docker** - Containerização da aplicação
- [ ] **CI/CD** - Pipeline com GitHub Actions
- [ ] **Frontend** - UI para player de vídeo
- [ ] **Cache de chunks** - Sistema de cache para seeks repetidos
- [ ] **WebSocket streaming** - Streaming em tempo real via WebSocket

### 🟢 Futuras Features

- [ ] **Torrent Streaming** - Streaming direto de torrents (stremio-like)
- [ ] **Transcodificação** - Conversão de formatos on-the-fly
- [ ] **Adaptive bitrate** - Múltiplas qualidades dinâmicas
- [ ] **Autenticação** - JWT para controle de acesso
- [ ] **Database** - Histórico e metadados persistentes

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

---

## 📖 Documentação Adicional

- [Tutorial Passo a Passo](TUTORIAL_PASSO_A_PASSO.md) - Guia completo de implementação
- [FastAPI Docs](https://fastapi.tiangolo.com/) - Documentação oficial do FastAPI
- [Python memoryview](https://docs.python.org/3/library/stdtypes.html#memoryview) - Documentação do memoryview

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Gabriel**

- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)

---

## 🙏 Agradecimentos

- Comunidade FastAPI pela excelente documentação
- Astral (uv) pelo gerenciador de pacotes ultra-rápido
- Big Buck Bunny pela licença Creative Commons dos vídeos de teste

---

<div align="center">

⭐ Se este projeto foi útil, considere dar uma estrela!

**[⬆ Voltar ao topo](#-video-streaming-platform)**

</div>
