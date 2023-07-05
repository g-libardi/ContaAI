# ContaAI

O objetivo desse projeto é desenvolver um editor de texto assistido por inteligência artificial capaz de gerar trechos de textos narrativos com base no contexto da história digitada pelo usuário. Para tal foi realizado o processo de fine-tuning do modelo pierreguillou/gpt2-small-portuguese, uma versão do GPT-2 da OpenAI treinada em português.

## Instalação e execução

1. Descompactar as partes dos arquivos .rar dentro da pasta ./src
2. Criar um ambiente virtual(venv) do python na pasta ./src com o comando "python -m venv venv"
3. Instalar as dependências disponíveis em ./src/requirements.txt no venv com o comando "pip install -r requirements.txt"
4. Executar o arquivo ./src/main.py

## Uso

Digite sua história na caixa de texto, ao clicar em Run Model(Ctrl + R) será gerada uma predição pela IA após o trecho final da sua história. Você pode mudar a quantidade de texto gerada na caixa de input numérico que fica acima do botão Run Model. O botão Undo(Ctrl + U) irá desfazer a última predição gerada.

## Arquitetura

A arquitetura do modelo escolhido é o GPT2.

## Conjunto de dados

Livros e texto literários obtidos por meio do webscrapping de sites de literatura.

## Video do projeto
https://youtu.be/vL4wgCAb4E4 

## Contribuição

Guilherme Libardi e Francine Franco

## Contato

Francine Franco - francinegfranco@gmail.com

Guilherme Libardi - guilhermelibardi@hotmail.com
