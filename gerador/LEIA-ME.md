# Como editar o site

O conteúdo fica em `gerador/paginas.py` (áreas de atuação e tecnologia) e `gerador/dados.py` (endereço, telefones, CRO).
A home, Sobre e Contato estão em `gerador/gerar.py`. A política de privacidade está em `gerador/privacidade-texto.html`.

Depois de editar, rode na raiz do repositório:

    python3 gerador/gerar.py

e publique os arquivos gerados (`index.html`, as pastas de cada página, `sitemap.xml`).
