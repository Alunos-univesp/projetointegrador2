Controle de Mercadorias
Este projeto é um sistema de controle de mercadorias destinado a pequenas e médias empresas. Ele permite aos usuários gerenciar o inventário de produtos, incluindo funcionalidades para adicionar, editar, excluir e visualizar itens. O sistema também suporta o rastreamento de vendas e controle de estoque em tempo real.

Requisitos do Sistema
Para executar o sistema de controle de mercadorias, você precisará dos seguintes requisitos:

Python 3.x: Certifique-se de ter o Python 3.x instalado em seu sistema. Você pode baixar e instalar a versão mais recente do Python no site oficial: python.org.

Flask: O sistema utiliza o framework Flask para desenvolvimento web em Python. Instale o Flask usando o pip, o gerenciador de pacotes do Python, com o comando:

bash
Copiar código
pip install Flask
MySQL: O sistema utiliza o MySQL como banco de dados. Instale o MySQL e crie um banco de dados para o sistema de controle de mercadorias. Certifique-se de configurar as credenciais de acesso no arquivo de configuração do projeto.

Cloud Firestore: O sistema também usa o Cloud Firestore, um banco de dados NoSQL do Firebase e Google Cloud Platform, para armazenar e sincronizar dados em tempo real e offline. Certifique-se de configurar o Firebase para usar o Firestore antes de prosseguir com a instalação.

Certifique-se de que todos esses requisitos estejam instalados corretamente em seu sistema antes de prosseguir com a instalação e execução do sistema de controle de mercadorias.

Instalação
Clone o repositório:

bash
Copiar código
git clone https://github.com/Alunos-univesp/projeto-integrador-univesp.git
Navegue até a pasta do projeto:

bash
Copiar código
cd projeto-integrador-univesp
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Configure o MySQL:

Certifique-se de que o MySQL está instalado e em execução.
Crie um banco de dados para o sistema:
sql
Copiar código
CREATE DATABASE controle_estoque;
Atualize as configurações de conexão ao MySQL no arquivo de configuração do projeto (app.py ou o arquivo de configuração correspondente) com suas credenciais, por exemplo:
python
Copiar código
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:senha@localhost/controle_estoque'
Inicialize o banco de dados:

Execute o arquivo create_db.py para criar as tabelas no banco de dados MySQL.
bash
Copiar código
python create_db.py
Inicie o servidor local:

bash
Copiar código
python app.py
Acesse o sistema: Após iniciar o servidor, abra seu navegador e acesse o seguinte endereço:

arduino
Copiar código
http://127.0.0.1:5000/login
Dicas adicionais:
Certifique-se de que o MySQL está configurado corretamente e que as credenciais estão corretas no código.
Verifique se todas as dependências estão instaladas corretamente. Em caso de erros ao iniciar o servidor, revise as dependências e os logs no terminal.
Consulte a documentação do projeto ou entre em contato com a equipe de suporte para obter assistência adicional.
Uso
Acessando o Sistema
Após concluir a instalação, abra o navegador e acesse:

arduino
Copiar código
http://127.0.0.1:5000/login
Adicionando um Novo Produto ao Inventário
Faça login no sistema.
Navegue até a seção "Adicionar Produto".
Preencha o formulário com informações do novo produto, incluindo nome, marca, código, custo, quantidade, data de inclusão e data de validade.
Clique em "Adicionar" ou "Salvar" para registrar o produto no inventário.
Visualizando Produtos no Inventário
Após adicionar novos produtos, acesse a página de "Estoque" para visualizar a lista completa de produtos.
A lista exibe todos os produtos disponíveis, incluindo os recentemente adicionados.
Utilize as funcionalidades de filtro ou pesquisa para encontrar produtos específicos, caso necessário.
Dicas Adicionais para o Inventário
Revise todas as informações antes de adicionar um novo produto para garantir precisão.
Para editar ou remover um produto existente, acesse a página de detalhes do produto e utilize as opções disponíveis.
Mantenha seu inventário atualizado regularmente para refletir os produtos disponíveis.
Contribuindo
Contribuições são sempre bem-vindas! Para contribuir:

Faça um fork do projeto:

No GitHub, clique no botão "Fork" no canto superior direito da página do projeto para criar uma cópia do repositório em sua conta.
Crie uma nova branch para suas modificações:

bash
Copiar código
git checkout -b nome-da-sua-branch
Faça commit das suas alterações:

Após fazer as modificações no código, confirme-as localmente usando o comando:
bash
Copiar código
git commit -m "Descrição das alterações"
Faça push para a branch:

bash
Copiar código
git push origin nome-da-sua-branch
Abra um Pull Request:

No GitHub, acesse o repositório do seu fork, clique em "New Pull Request" e selecione a branch principal do projeto original para solicitar a mesclagem.
Depois de abrir o PR, outros colaboradores poderão revisar suas alterações, fazer comentários e sugerir modificações. Uma vez revisado e aprovado, seu PR poderá ser mesclado ao projeto original pelo mantenedor do projeto.

Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para detalhes.