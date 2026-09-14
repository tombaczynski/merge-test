import os
import re

# Katalog zawierający pliki źródłowe Markdown
INPUT_DIR = "docs"
# Nazwa pliku wyjściowego
OUTPUT_FILE = "gotowy_dokument.md"

def remove_frontmatter(text):
    """Usuwa blok YAML Front Matter z początku pliku (między potrójnymi myślnikami ---)."""
    pattern = r'^---\s*\n.*?\n---\s*\n'
    return re.sub(pattern, '', text, flags=re.DOTALL)

def adjust_headings(text, depth_shift):
    """Przesuwa nagłówki o określoną liczbę poziomów w dół (np. # na ###)."""
    if depth_shift <= 0:
        return text
    
    lines = text.splitlines()
    adjusted_lines = []
    
    for line in lines:
        # Dopasowuje nagłówki Markdown zaczynające się od #
        match = re.match(r'^(#{1,6})(\s+.*)', line)
        if match:
            hashes, content = match.groups()
            # Zwiększa liczbę # o głębokość folderu (maksymalnie do 6 poziomów)
            new_level = min(len(hashes) + depth_shift, 6)
            adjusted_lines.append("#" * new_level + content)
        else:
            adjusted_lines.append(line)
            
    return "\n".join(adjusted_lines)

def merge_markdown():
    merged_sections = []
    input_dir_abs = os.path.abspath(INPUT_DIR)

    # Przechodzi po katalogach i plikach w kolejności alfabetycznej
    for root, dirs, files in os.walk(input_dir_abs):
        dirs.sort()
        files.sort()
        
        # Oblicza poziom zagłębienia folderu względem INPUT_DIR
        rel_path = os.path.relpath(root, input_dir_abs)
        if rel_path == ".":
            depth = 0
        else:
            depth = len(rel_path.split(os.sep))

        for file in files:
            # Pomija pliki index.md oraz wszystko co nie jest .md
            if file.lower() == "index.md" or not file.endswith(".md"):
                continue

            file_path = os.path.join(root, file)
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Czyszczenie z frontmatter Jekylla
            content_clean = remove_frontmatter(content).strip()
            
            # 2. Przesunięcie nagłówków zgodnie z głębokością w drzewie
            content_adjusted = adjust_headings(content_clean, depth)

            if content_adjusted:
                merged_sections.append(content_adjusted)

    # Łączenie wszystkich sekcji separatorami
    final_document = "\n\n---\n\n".join(merged_sections)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(final_document)

    print(f"Pomyślnie scalono dokument do pliku: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_markdown()