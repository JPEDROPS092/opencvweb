# EdTETI Web App

Aplicação web para processamento de imagens e vídeos utilizando Django no backend e Vue.js no frontend.

## Estrutura do Projeto

```
EdTETI_webapp/
├── backend/             # Aplicação Django
│   └── edteti_project/  # Projeto Django
│       ├── processor/   # App para processamento de imagens e vídeos
│       └── ...
└── frontend/            # Aplicação Vue.js
    ├── public/          # Arquivos públicos
    └── src/             # Código-fonte Vue.js
```

## Requisitos

- Python 3.8+
- Node.js 14+
- npm ou yarn

## Como Executar

### Backend (Django)

1. Navegue até o diretório do backend:
   ```bash
   cd EdTETI_webapp/backend
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install django djangorestframework django-cors-headers opencv-python numpy Pillow
   ```

4. Aplique as migrações do banco de dados:
   ```bash
   cd edteti_project
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Inicie o servidor Django:
   ```bash
   python manage.py runserver
   ```

   O backend estará disponível em: http://localhost:8000/

### Frontend (Vue.js)

1. Navegue até o diretório do frontend:
   ```bash
   cd EdTETI_webapp/frontend
   ```

2. Instale as dependências:
   ```bash
   npm install
   # ou
   yarn install
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run serve
   # ou
   yarn serve
   ```

   O frontend estará disponível em: http://localhost:8080/

## Funcionalidades

### Processamento de Imagens
- Upload de imagens
- Aplicação de filtros: Blur, Sharpen, Emboss, Laplacian, Canny, Sobel
- Conversão para escala de cinza e binarização
- Detecção de objetos com YOLO
- Extração de regiões de interesse (ROI)

### Processamento de Vídeos
- Upload de vídeos
- Aplicação de filtros em vídeos
- Segmentação de vídeos
- Detecção de objetos em vídeos

## Tecnologias Utilizadas

- **Backend**: Django, Django REST Framework, OpenCV, NumPy, Pillow
- **Frontend**: Vue.js 3, Vuex, Vue Router, Axios
