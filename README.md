🕷️ Screaming Frog → llms.txt Generator

Este projeto converte automaticamente o arquivo internal_html.csv exportado do Screaming Frog SEO Spider em um arquivo llms.txt formatado em Markdown.

O script organiza todas as URLs internas do site de forma hierárquica, agrupando por subdomínios, rotas principais e categorias especiais (como /blog/, /tags/, etc.).
É ideal para documentar a estrutura de um site, auditar conteúdo ou gerar contextos para modelos de linguagem (LLMs).

⚙️ Funcionalidades

✅ Gera automaticamente o arquivo llms.txt com estrutura organizada
✅ Agrupa URLs por rota principal (ex: /cases-de-sucesso/, /servicos/, /produtos/)
✅ Separa automaticamente:

Posts do blog (/blog/...)
Tags do blog (/blog/tag/...)

✅ Agrupa URLs de subdomínios de forma independente
✅ Adiciona automaticamente a meta description da homepage no início do arquivo
✅ Detecta e usa o nome do site a partir do domínio
✅ Funciona de forma totalmente automática, sem ajustes manuais entre clientes

🧩 Estrutura de saída (llms.txt)

O arquivo final é gerado em formato Markdown, com hierarquia por seções e subdomínios:

# NOME DO SITE

> Descrição (meta description da homepage)

- [Página home do site](https://exemplo.com.br)

## Blog
- [Título do Post 1](https://exemplo.com.br/blog/titulo-post-1/)
- [Título do Post 2](https://exemplo.com.br/blog/titulo-post-2/)

### Tags
- [Nome da Tag](https://exemplo.com.br/blog/tag/nome-da-tag/)

## Cases-de-sucesso
- [Case 1](https://exemplo.com.br/cases-de-sucesso/case-1/)
- [Case 2](https://exemplo.com.br/cases-de-sucesso/case-2/)

📄 Estrutura esperada do CSV

O script utiliza o arquivo internal_html.csv exportado pelo Screaming Frog.
Ele deve conter, no mínimo, as seguintes colunas:

Coluna	Descrição
Address	URL completa da página
Status Code	Código de status HTTP (ex: 200)
Content Type	Tipo de conteúdo (deve conter "text/html")
Title 1	Título da página
Meta Description 1	Meta description (usada para a homepage)

⚠️ Outras colunas são ignoradas, portanto o script pode ser usado mesmo com arquivos simplificados.

🚀 Como usar

Exporte o arquivo internal_html.csv do Screaming Frog

Menu: Bulk Export > Internal > All HTML

Salve o CSV na mesma pasta do script Python

Execute o script:

python gerar_llms.py


O arquivo llms.txt será criado automaticamente no mesmo diretório.

🧠 Regras de agrupamento automáticas
Tipo de URL	Agrupamento
/blog/slug/	Dentro de ## Blog
/blog/tag/...	Dentro de ### Tags
/subpasta/...	Agrupado como ## Subpasta
subdominio.exemplo.com.br	Agrupado como # Subdominio
🧰 Requisitos

Python 3.7 ou superior

Bibliotecas utilizadas:

pip install pandas

🧑‍💻 Autor
Script desenvolvido para automatizar a documentação e análise estrutural de sites a partir dos dados do Screaming Frog.
Pode ser adaptado livremente para projetos de SEO, documentação técnica ou geração de contexto para IA.
