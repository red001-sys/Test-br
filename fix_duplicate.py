import re

path = '/data/data/com.termux/files/home/biblia-app/src/BibliaApp.jsx'
content = open(path).read()

matches = [m.start() for m in re.finditer(r'function getFallbackVerses', content)]
print(f"Encontradas {len(matches)} declaracoes")

if len(matches) >= 2:
    # Remove todas as declaracoes a partir da segunda
    for idx in reversed(matches[1:]):
        # Acha o comentario antes (se existir)
        remove_from = idx
        comment_search = content.rfind('\n//', 0, idx)
        if comment_search > 0 and content[comment_search:idx].strip().startswith('//'):
            remove_from = comment_search

        # Acha o fim da funcao
        depth = 0
        found = False
        end_idx = idx
        for i in range(idx, len(content)):
            if content[i] == '{':
                depth += 1
                found = True
            elif content[i] == '}':
                depth -= 1
                if found and depth == 0:
                    end_idx = i + 1
                    break

        print(f"Removendo de {remove_from} ate {end_idx}")
        content = content[:remove_from] + content[end_idx:]

    # Verifica
    matches2 = [m.start() for m in re.finditer(r'function getFallbackVerses', content)]
    print(f"Restantes: {len(matches2)}")

    with open(path, 'w') as f:
        f.write(content)
    print("Arquivo corrigido!")
else:
    print("Nenhuma duplicata encontrada!")
