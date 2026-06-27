#!/usr/bin/env python3
"""
Script per aggiornare la homepage e il sitemap con il nuovo articolo.
Viene eseguito da GitHub Actions dopo genera_articolo.py.
"""

import json
import datetime
import re
from pathlib import Path

def get_date_iso():
    return datetime.date.today().isoformat()

def get_all_articles():
    """Recupera tutti gli articoli esistenti in ordine."""
    articles = []
    for i in range(1, 100):
        f = Path(f"articolo{i}.html")
        if not f.exists():
            break
        articles.append(i)
    return articles

def aggiorna_sitemap(articles):
    """Aggiorna il sitemap.xml con tutti gli articoli."""
    base_url = "https://paradisoantonio789-sketch.github.io/cosplay-ita-blog"
    today = get_date_iso()
    
    urls = [f"""    <url>
        <loc>{base_url}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>"""]
    
    for num in articles:
        urls.append(f"""    <url>
        <loc>{base_url}/articolo{num}.html</loc>
        <lastmod>{today}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>""")
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap)
    
    print(f"✅ Sitemap aggiornato con {len(articles)} articoli")

def aggiorna_homepage(info):
    """Aggiunge la card del nuovo articolo alla homepage."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Crea la nuova card
    nuova_card = f"""
            <article class="post-card">
                <a href="{info['filename']}">
                    <div class="post-image-wrap">
                        <img src="assets/images/articolo1/evento.jpg" alt="{info['titolo']}">
                        <span class="category" style="background:{info['categoria_color']};color:white;">{info['categoria']}</span>
                    </div>
                    <div class="post-info">
                        <h3>{info['titolo']}</h3>
                        <p>{info['lead'][:180]}...</p>
                        <div class="post-meta">
                            <span>{info['data']}</span>
                            <span>8 min di lettura</span>
                        </div>
                        <span class="read-more">Leggi tutto &rarr;</span>
                    </div>
                </a>
            </article>
"""
    
    # Inserisce la nuova card prima della chiusura della griglia
    marker = '</div>\n    </section>\n\n    <section class="stats-section">'
    if marker in content:
        content = content.replace(marker, nuova_card + '\n        </div>\n    </section>\n\n    <section class="stats-section">')
    
    # Aggiorna il contatore articoli
    content = re.sub(
        r'(<div class="stat-number">)(\d+)(\+</div>\s*<div class="stat-label">Articoli)',
        lambda m: f'{m.group(1)}{info["numero"]}+{m.group(3)}',
        content
    )
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Homepage aggiornata con il nuovo articolo: {info['titolo']}")

def main():
    # Carica info del nuovo articolo
    try:
        with open('scripts/ultimo_articolo.json', 'r', encoding='utf-8') as f:
            info = json.load(f)
    except FileNotFoundError:
        print("❌ File ultimo_articolo.json non trovato. Esegui prima genera_articolo.py")
        return
    
    # Aggiorna sitemap
    articles = get_all_articles()
    aggiorna_sitemap(articles)
    
    # Aggiorna homepage
    aggiorna_homepage(info)
    
    print(f"✅ Aggiornamento completato! Articolo #{info['numero']} pubblicato.")

if __name__ == "__main__":
    main()
