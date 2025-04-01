# Controle de Validade

Sistema web desenvolvido como parte do Projeto Integrador III da UNIVESP, com foco na gestão de estoque e validade de produtos para pequenos e médios comércios.

## 🎯 Objetivo

Facilitar o controle de entrada, saída e validade dos produtos em estoque, evitando perdas e otimizando a gestão de mercadorias.

---

## ✅ Funcionalidades

- Cadastro de produtos com validade
- Edição e exclusão de itens
- Visualização de estoque
- Controle de entrada e saída de produtos
- Alertas de produtos vencidos ou próximos do vencimento
- Geração de relatórios
- Responsividade para dispositivos móveis
- Acessibilidade com alto contraste, Libras (VLibras) e ajuste de fonte

---

## 🧰 Tecnologias Utilizadas

### 🔧 Backend
- **Python 3**
- **Flask** (framework web)
- **Flask SQLAlchemy** (ORM)
- **Flask Migrate** (migrações de banco de dados)
- **SQLite** (ambiente local) / **PostgreSQL** (produção)
- **APIs com Flask** (`/api/produtos`, `/iot/sensor`)

### 🌐 Frontend
- **HTML5 + CSS3**
- **JavaScript** (scripts para acessibilidade, filtros e alertas)
- **Bootstrap** (responsividade)

### ☁️ Nuvem
- **Render.com** (deploy do backend com PostgreSQL)
- **GitHub** (controle de versão e repositório)
- **Vercel** (opcional, para frontend)
- **GitHub Actions** (integração contínua)

### ♿ Acessibilidade
- Botão de **Alto Contraste**
- Botão para **Aumentar/Diminuir Fonte**
- Integração com **VLibras**
- Compatibilidade com leitores de tela e teclados
- Layout responsivo e com foco em boas práticas do [Lighthouse](https://developers.google.com/web/tools/lighthouse/)

---

## 🔁 Integração Contínua

- CI com **GitHub Actions** para verificar push/pull requests
- Testes automatizados de funcionalidades essenciais

---

## 🔬 Testes

- Testes de rotas com Flask
- Testes de banco de dados SQLite
- Testes manuais de interface e responsividade

---

## 🔗 API & IoT

- Rota `/api/produtos`: fornece todos os dados do estoque em JSON
- Rota `/iot/sensor`: simula recebimento de dados de sensores externos (ex: temperatura, validade)

---

## 🧪 Scripts Web (JavaScript)

- Filtros de produtos por categoria
- Controle de contraste e fonte
- Validação de campos de formulário
- Contador de produtos vencidos

---

## 🌍 Acesso ao Projeto

- [Projeto online no Render](https://projetointegrador2-r303.onrender.com)
- [Repositório GitHub](https://github.com/Alunos-univesp/projetointegrador2)

---

## 👨‍💻 Integrantes do Grupo

- Brenda Raimundo da Silva  
- Dinalva Crisostomo Barbosa  
- Douglas Henrique Rasse  
- Marques dos Santos  
- Thais Baldo de Oliveira

---

## 📁 Estrutura do Projeto

```bash
projetointegrador2/
├── app/
│   ├── __init__.py            # Criação e configuração da aplicação Flask
│   ├── models.py              # Definição do modelo Produto (SQLAlchemy)
│   ├── routes.py              # Rotas principais e lógica da aplicação
│
├── static/
│   ├── css/                   # Estilos customizados
│   ├── js/                    # Scripts de acessibilidade, filtro, alerta
│
├── templates/
│   ├── index.html             # Tela inicial (login/redirecionamento)
│   ├── home.html              # Página principal (painel)
│   ├── estoque.html           # Tabela de produtos
│   ├── cadastro-mercadoria.html # Formulário de cadastro
│   ├── lista_produtos_proximo_vencimento.html
│   ├── analise.html           # Dashboard de gráficos com Plotly
│   ├── pdf_analise.html       # Template HTML para geração de PDF
│
├── tests/
│   └── test_app.py            # Testes automatizados com pytest
│
├── run.py                     # Arquivo principal para executar a aplicação
├── requirements.txt           # Dependências do projeto
├── Procfile                  # Configuração para deploy no Render
├── README.md                 # Documentação do projeto

📦 Requisitos
Python 3.10+

Pip

Ambiente virtual (venv)

Editor de código (VS Code recomendado)

🚀 Execução Local
bash
Copiar
# Clonar o repositório
git clone https://github.com/Alunos-univesp/projetointegrador2.git
cd projetointegrador2

# Criar ambiente virtual e ativar
python -m venv venv
venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar o projeto
python run.py

📅 Entrega
Projeto desenvolvido de acordo com as diretrizes do Projeto Integrador III da UNIVESP, atendendo aos critérios obrigatórios:

Framework web

Banco de dados

Script Web (JavaScript)

Nuvem (Render.com)

Acessibilidade

Controle de versão (GitHub)

Integração contínua (GitHub Actions)

Testes

API e IoT