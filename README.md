# 🚀 Docling Batch Processor

Um processador em lote para converter documentos diversos (PDF, DOCX, PPTX, etc.) para formato Markdown usando a biblioteca Docling.

## 📋 Descrição

Este projeto automatiza a conversão de documentos em lote para Markdown, oferecendo suporte a GPU para processamento acelerado. É ideal para processar grandes volumes de documentos acadêmicos, relatórios, apresentações e outros arquivos de texto.

## ✨ Funcionalidades

- 🔄 **Conversão em Lote**: Processa múltiplos arquivos simultaneamente
- 🎮 **Suporte GPU**: Acelera o processamento com CUDA (quando disponível)
- 📄 **Múltiplos Formatos**: Suporta PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS, etc  
- 📊 **Divisão Automática**: Divide PDFs grandes automaticamente para evitar erros de memória
- 📈 **Barra de Progresso**: Interface visual com tqdm para acompanhar o progresso
- 📝 **Log de Erros**: Registra detalhadamente qualquer falha na conversão
- 🔗 **Mesclagem**: Combina todos os arquivos Markdown em um documento final

## 🛠️ Requisitos

### Sistema
- Python <= 3.12.10
- Windows 10/11 (testado)
- GPU NVIDIA com CUDA (opcional, mas recomendado)

### Dependências Principais
- `docling==2.36.1` - Biblioteca principal de conversão
- `torch>=2.6.0` - Suporte a machine learning e GPU
- `PyPDF2==3.0.1` - Processamento de PDFs
- `tqdm==4.67.1` - Barra de progresso

## 🚀 Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/convert_files_to_markdown.git
cd convert_files_to_markdown
```

2. **Instale as dependências:**
```bash
2.1 - Criar um ambiente virtual (venv)

2.2 - Instalar as dependências: 
      pip install -r requirements.txt
      pip install --upgrade pip
```

3. **Verifique a configuração da GPU (opcional):**
```bash
python gpu_setup_check.py
```

## 📁 Estrutura do Projeto

```
convert_files_to_markdown/
├── main.py                 # Script principal
├── extraction_functions.py # Funções de processamento
├── gpu_setup_check.py     # Verificação de GPU
├── requirements.txt       # Dependências
└── README.md             # Este arquivo
```

## 🎯 Como Usar

### 1. Preparar os Arquivos
Crie uma pasta de entrada com os documentos que deseja converter:
```
C:\Users\[seu-usuario]\OneDrive\Desktop\input\
├── documento1.pdf
├── apresentacao.pptx
├── relatorio.docx
└── ...

```

### 2. Executar o Processamento
```bash
python main.py
```

### 3. Resultados
Os arquivos convertidos serão salvos em:
```
output_folder = r"C:\\Users\\adema\\OneDrive\\Desktop\\Test\\output"

├── documento1.md
├── apresentacao.md
├── relatorio.md
├── documento_final.md    # Arquivo mesclado
└── conversion_errors.log # Log de erros (se houver)
```

## ⚙️ Configuração

### Personalizar Pastas
Edite o arquivo `main.py` para alterar os caminhos:

```python
# Linhas 16-17
 input_folder = r"C:\\Users\\adema\\OneDrive\\Desktop\\input"
 output_folder = r"C:\\Users\\adema\\OneDrive\\Desktop\\Test\\output"
```

### Configurações de Processamento
- **Tamanho de Chunk**: PDFs maiores que 50MB são divididos automaticamente
- **Páginas por Chunk**: 10 páginas por arquivo (configurável em `extraction_functions.py`)
- **Limpeza de Memória**: Automática após cada arquivo processado

## 🔧 Solução de Problemas

### GPU não Detectada
Se a GPU não for detectada, execute:
```bash
python gpu_setup_check.py
```

### Erros de Memória
- O sistema divide automaticamente PDFs grandes
- Para arquivos muito grandes, reduza o `pages_per_chunk` em `extraction_functions.py`

### Erros de Conversão
- Verifique o arquivo `conversion_errors.log` na pasta de saída
- Certifique-se de que os arquivos não estão corrompidos
- Alguns formatos podem não ser totalmente suportados

## 📊 Formatos Suportados

| Formato | Extensão | Status |
|---------|----------|--------|
| PDF | `.pdf` | ✅ Completo |
| Word | `.docx`, `.doc` | ✅ Completo |
| PowerPoint | `.pptx`, `.ppt` | ✅ Completo |
| Excel | `.xlsx`, `.xls` | ✅ Completo |
| HTML | `.html` | ✅ Completo |

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- [Docling](https://github.com/docling-ai/docling) - Biblioteca principal de conversão
- [PyTorch](https://pytorch.org/) - Framework de machine learning
- [tqdm](https://github.com/tqdm/tqdm) - Barra de progresso

## 📞 Suporte

Se encontrar problemas ou tiver dúvidas:
1. Verifique a seção de solução de problemas
2. Consulte o arquivo `conversion_errors.log`
3. Abra uma issue no GitHub

---

**Desenvolvido com ❤️ para facilitar a conversão de documentos**
