import pandas as pd
from urllib.parse import urlparse
import re

# === 1. Ler o CSV exportado do Screaming Frog ===
df = pd.read_csv("internal_html.csv", encoding="utf-8")

# === 2. Filtrar apenas URLs válidas (status 200 e HTML) ===
df = df[
    (df["Status Code"] == 200)
    & (df["Content Type"].str.contains("text/html", na=False))
]

# === 3. Descobrir domínio principal ===
primeira_url = df["Address"].iloc[0]
parsed = urlparse(primeira_url)
dominio_principal = f"{parsed.scheme}://{parsed.netloc}"

# === 4. Gerar nome do projeto (ex: meusite.com.br → NOME DO SITE) ===
nome_site = re.sub(r"https?://(www\.)?", "", dominio_principal)
nome_site = nome_site.split(".")[0].replace("-", " ").upper()

# === 5. Obter meta description da homepage ===
meta_col = next((c for c in df.columns if "meta description" in c.lower()), None)
descricao_home = ""

if meta_col:
    home_row = df[df["Address"].str.rstrip("/") == dominio_principal.rstrip("/")]
    if not home_row.empty:
        descricao_home = home_row.iloc[0][meta_col]
        if not isinstance(descricao_home, str) or not descricao_home.strip():
            descricao_home = ""
    if not descricao_home:
        descs = df[meta_col].dropna()
        if not descs.empty:
            descricao_home = descs.iloc[0]

# === 6. Criar dicionário de categorias ===
categorias = {}

for _, row in df.iterrows():
    url = row["Address"]
    titulo = row.get("Title 1", "")
    if not isinstance(titulo, str) or not titulo.strip():
        titulo = url.split("/")[-2].replace("-", " ").title()

    parsed_url = urlparse(url)
    path = parsed_url.path.strip("/")

    # Detectar subdomínio
    host = parsed_url.netloc
    dominio_base = dominio_principal.split("//")[-1]
    subdominio = host.replace(dominio_base, "").strip(".")
    grupo_subdominio = subdominio.capitalize() if subdominio else "Site principal"

    # Inicializar dicionário do subdomínio
    if grupo_subdominio not in categorias:
        categorias[grupo_subdominio] = {}

    # --- Agrupamento inteligente por rota principal ---
    if not path:
        categoria = "Home"
        subcategoria = None

    else:
        partes = path.split("/")

        # === BLOG (tratamento especial) ===
        if partes[0] == "blog":
            if len(partes) > 1 and partes[1] == "tag":
                categoria = "Blog"
                subcategoria = "Tags"
            elif len(partes) > 2 and partes[1] not in ["tag"]:
                categoria = "Blog"
                subcategoria = partes[1].capitalize()
            else:
                categoria = "Blog"
                subcategoria = "_raiz"

        # === Outros diretórios principais (agrupamento automático) ===
        else:
            categoria = partes[0].capitalize()
            subcategoria = None

    # Adicionar ao dicionário final
    if categoria not in categorias[grupo_subdominio]:
        categorias[grupo_subdominio][categoria] = {}

    categorias[grupo_subdominio][categoria].setdefault(subcategoria or "_raiz", []).append((titulo, url))

# === 7. Montar o conteúdo do llms.txt ===
conteudo = f"# {nome_site}\n\n"

# Adicionar descrição, se existir
if descricao_home:
    conteudo += f"> {descricao_home.strip()}\n\n"

conteudo += f"- [Página home do site]({dominio_principal})\n\n"

# Loop por subdomínio
for subdominio, cats in categorias.items():
    if subdominio != "Site principal":
        conteudo += f"# {subdominio}\n\n"
    for cat, subs in cats.items():
        conteudo += f"## {cat}\n"
        for sub, links in subs.items():
            if sub != "_raiz":
                conteudo += f"### {sub}\n"
            for titulo, url in sorted(links):
                conteudo += f"- [{titulo}]({url})\n"
            conteudo += "\n"

# === 8. Salvar o resultado ===
with open("llms.txt", "w", encoding="utf-8") as f:
    f.write(conteudo)

print("✅ Arquivo llms.txt gerado automaticamente com sucesso!")
