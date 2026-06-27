#!/usr/bin/env python3
"""
Script per generare automaticamente nuovi articoli cosplay.
Viene eseguito da GitHub Actions ogni 3 giorni.
"""

import os
import json
import random
import datetime
from pathlib import Path

# Temi degli articoli cosplay da ruotare
TEMI_ARTICOLI = [
    {
        "slug": "cosplay-videogiochi",
        "titolo": "Dal Pixel allo Schermo: Il Cosplay dei Videogiochi in Italia",
        "categoria": "Gaming & Cosplay",
        "categoria_class": "gaming",
        "categoria_color": "#06b6d4",
        "lead": "I personaggi dei videogiochi sono tra i più amati dalla community cosplay italiana. Scopri come i cosplayer italiani portano in vita eroi digitali con costumi di straordinaria precisione.",
        "contenuto": """
                <h3>La Fusione tra Gaming e Cosplay</h3>
                <p>Il mondo dei videogiochi ha sempre avuto un rapporto speciale con il cosplay. I personaggi digitali, con i loro design elaborati e iconici, rappresentano una sfida e un'ispirazione per i cosplayer di tutto il mondo. In Italia, questa passione si è tradotta in alcuni dei costumi più tecnici e dettagliati mai realizzati.</p>
                
                <p>Titoli come <strong>Final Fantasy</strong>, <strong>Dark Souls</strong>, <strong>Genshin Impact</strong> e <strong>League of Legends</strong> dominano le fiere italiane con i loro cosplay. La sfida principale è tradurre in materiali fisici quello che i designer di giochi hanno creato senza preoccuparsi dei limiti della realtà: armature con proporzioni impossibili, armi lunghe quanto una persona, effetti luminosi integrati.</p>

                <h3>La Precisione come Filosofia</h3>
                <p>I cosplayer italiani specializzati in personaggi da videogioco si distinguono per un approccio quasi ingegneristico al crafting. Prima di iniziare a costruire, trascorrono ore ad analizzare ogni angolo del personaggio nel gioco, catturando screenshot, studiando i modelli 3D e confrontando le proporzioni. Questa fase di ricerca è fondamentale: un'armatura sbagliata di pochi centimetri può compromettere l'intera illusione.</p>

                <p>La community italiana ha sviluppato tecniche specifiche per affrontare le sfide dei costumi da videogioco. Il "weathering" (invecchiamento artificiale) è particolarmente importante per i personaggi di giochi come Dark Souls o Elden Ring, dove le armature devono sembrare logorate da secoli di battaglie. Al contrario, per i personaggi di JRPG come Final Fantasy, si punta alla perfezione lucida e ai colori saturi e brillanti.</p>

                <h3>Gli Effetti Luminosi: Il Futuro del Cosplay</h3>
                <p>Una delle tendenze più entusiasmanti nel cosplay da videogioco è l'integrazione di sistemi di illuminazione LED. Personaggi come Jinx di League of Legends, con le sue armi luminose, o i vari personaggi di Genshin Impact con i loro elementi visivi, richiedono sistemi elettronici nascosti nei costumi. I cosplayer italiani più avanzati hanno imparato a programmare microcontrollori Arduino per creare effetti luminosi dinamici e sincronizzati.</p>

                <p>Il cosplay da videogioco in Italia non è solo un hobby: è diventato un settore professionale. Molti cosplayer vengono ingaggiati direttamente dalle case editrici per eventi promozionali, fiere internazionali e campagne marketing. La qualità raggiunta dalla community italiana è tale da essere riconosciuta e valorizzata a livello globale.</p>
        """,
        "immagine_alt": "Cosplayer italiano in costume da videogioco elaborato"
    },
    {
        "slug": "cosplay-principianti-guida",
        "titolo": "Iniziare nel Cosplay: La Guida Completa per Principianti Italiani",
        "categoria": "Guide & Tutorial",
        "categoria_class": "guide",
        "categoria_color": "#10b981",
        "lead": "Vuoi iniziare nel mondo del cosplay ma non sai da dove partire? Questa guida completa ti accompagna passo dopo passo, dal scegliere il tuo primo personaggio fino a presentarti alla tua prima fiera.",
        "contenuto": """
                <h3>Il Primo Passo: Scegliere il Personaggio Giusto</h3>
                <p>La scelta del personaggio è il momento più emozionante e, allo stesso tempo, più delicato per chi si avvicina al cosplay per la prima volta. Il consiglio d'oro è semplice: scegli un personaggio che ami davvero, non uno che pensi sia "facile" o che sia di tendenza in quel momento. La passione per il personaggio è il carburante che ti terrà motivato durante le settimane di lavoro.</p>
                
                <p>Per i principianti, è consigliabile partire da personaggi con costumi relativamente semplici: pochi pezzi, colori chiari, senza armature complesse o acconciature impossibili. Questo non significa scegliere personaggi "brutti": anche i costumi più semplici, realizzati con cura e attenzione, possono risultare straordinari.</p>

                <h3>Il Budget: Quanto Costa un Cosplay?</h3>
                <p>Una delle domande più frequenti dei principianti riguarda il costo. La risposta onesta è: dipende enormemente. Un cosplay semplice può costare tra i 50 e i 150 euro, mentre costumi elaborati con armature e props possono superare i 500 o persino i 1000 euro. Tuttavia, esistono strategie intelligenti per contenere i costi senza sacrificare la qualità.</p>

                <p>Il primo consiglio è di non acquistare tutto in una volta. Inizia con gli elementi più visibili e caratteristici del personaggio, quelli che rendono immediatamente riconoscibile il costume. Poi, con il tempo e l'esperienza, potrai aggiungere dettagli e migliorare i pezzi già realizzati. Il cosplay è un processo iterativo: raramente un costume è "finito" definitivamente.</p>

                <h3>Dove Imparare: La Community è la Tua Migliore Risorsa</h3>
                <p>La community cosplay italiana è straordinariamente accogliente e generosa. I forum online, i gruppi Facebook dedicati e i canali YouTube di cosplayer italiani sono miniere d'oro di tutorial, consigli pratici e supporto morale. Non aver paura di fare domande: i cosplayer esperti ricordano tutti com'era essere principianti e sono quasi sempre disposti ad aiutare.</p>

                <p>Le fiere sono l'occasione perfetta per imparare dal vivo. Avvicinarsi ai cosplayer con costumi che ti ispirano e chiedere loro dei materiali usati o delle tecniche applicate è non solo accettato, ma incoraggiato. È così che nasce e si perpetua la cultura del cosplay: attraverso la condivisione della conoscenza e la celebrazione collettiva della creatività.</p>
        """,
        "immagine_alt": "Principiante cosplay che lavora al suo primo costume"
    },
    {
        "slug": "fiere-cosplay-italia-calendario",
        "titolo": "Il Calendario delle Fiere Cosplay Italiane: Dove e Quando Andare",
        "categoria": "Fiere & Eventi",
        "categoria_class": "fiere",
        "categoria_color": "#f59e0b",
        "lead": "Dall'alba dell'anno fino all'autunno inoltrato, l'Italia è costellata di eventi dedicati alla cultura pop e al cosplay. Ecco la guida definitiva alle fiere imperdibili per ogni appassionato.",
        "contenuto": """
                <h3>Il Panorama delle Fiere Italiane</h3>
                <p>L'Italia vanta uno dei calendari fieristici più ricchi d'Europa per quanto riguarda la cultura pop e il cosplay. Ogni regione ha i suoi eventi di riferimento, creando un circuito che permette ai cosplayer più appassionati di essere praticamente in fiera ogni mese dell'anno. Questo ecosistema vibrante è il risultato di decenni di crescita della community e dell'interesse crescente del grande pubblico verso anime, manga, videogiochi e cosplay.</p>
                
                <p>La stagione fieristica italiana inizia già a febbraio con eventi invernali e si conclude in novembre con le grandi manifestazioni autunnali. Il periodo più intenso è senza dubbio la primavera e l'autunno, quando si concentrano le fiere più importanti e i cosplayer italiani danno il meglio di sé.</p>

                <h3>Lucca Comics & Games: Il Re delle Fiere</h3>
                <p><strong>Lucca Comics & Games</strong>, che si tiene ogni anno alla fine di ottobre nella splendida città medievale toscana, è senza dubbio l'evento più importante d'Italia e uno dei più significativi d'Europa. Con oltre 300.000 visitatori in quattro giorni, Lucca è il palcoscenico dove i cosplayer italiani più talentuosi si esibiscono davanti a un pubblico enorme. La città stessa diventa parte del costume: le mura medievali, le piazze storiche e i vicoli acciottolati creano sfondi fotografici unici al mondo.</p>

                <p>Partecipare a Lucca come cosplayer richiede preparazione logistica oltre che creativa. I biglietti vanno acquistati con mesi di anticipo, gli alloggi si esauriscono rapidamente e il costume deve essere progettato per resistere a ore di cammino su sampietrini. Ma lo spettacolo che si crea è impagabile: migliaia di cosplayer che si muovono tra le mura medievali creano un'atmosfera magica e irripetibile.</p>

                <h3>Romics, Napoli Comicon e le Fiere Regionali</h3>
                <p><strong>Romics</strong> a Roma e <strong>Napoli Comicon</strong> sono le altre due grandi manifestazioni nazionali, ciascuna con la propria identità e il proprio pubblico. Romics, con le sue due edizioni annuali (primavera e autunno), è particolarmente importante per le competizioni cosplay ufficiali, mentre Napoli Comicon si distingue per l'atmosfera festosa e la forte identità culturale del Sud Italia.</p>

                <p>Non bisogna però sottovalutare le fiere regionali e locali. Manifestazioni come <strong>Cartoomics</strong> a Milano, <strong>Etna Comics</strong> in Sicilia, <strong>Modena Fiere</strong> e decine di altri eventi minori distribuiti su tutto il territorio nazionale offrono opportunità preziose per i cosplayer locali di farsi conoscere e per i principianti di fare le prime esperienze in un ambiente più raccolto e meno caotico delle grandi fiere nazionali.</p>
        """,
        "immagine_alt": "Fiera cosplay italiana con cosplayer in costumi colorati"
    },
    {
        "slug": "cosplay-sostenibile-riciclo",
        "titolo": "Cosplay Sostenibile: Come Creare Costumi Incredibili con Materiali Riciclati",
        "categoria": "Eco Cosplay",
        "categoria_class": "eco",
        "categoria_color": "#10b981",
        "lead": "Il cosplay sostenibile è una tendenza in crescita nella community italiana. Scopri come creare costumi straordinari riducendo l'impatto ambientale e risparmiando denaro grazie al riciclo creativo.",
        "contenuto": """
                <h3>La Rivoluzione Verde del Cosplay</h3>
                <p>Il cosplay è tradizionalmente un hobby che richiede l'acquisto di molti materiali nuovi: foam, termoplastici, tessuti, vernici. Negli ultimi anni, però, una parte sempre più consapevole della community italiana ha iniziato a esplorare approcci più sostenibili, dimostrando che la qualità e la creatività non devono necessariamente andare di pari passo con un elevato impatto ambientale.</p>
                
                <p>Il cosplay sostenibile non è solo una questione etica: è anche una sfida creativa stimolante. Trovare il modo di trasformare materiali di scarto in elementi di costume richiede ingegno, problem-solving e una visione artistica fuori dagli schemi. Molti cosplayer italiani che hanno abbracciato questa filosofia riferiscono che ha reso il loro processo creativo ancora più soddisfacente.</p>

                <h3>Materiali Riciclati: Un Tesoro Nascosto</h3>
                <p>I materiali riciclabili più utili per il cosplay sono spesso quelli che buttiamo ogni giorno senza pensarci. Le bottiglie di plastica, una volta tagliate e scaldate, possono essere modellate in forme sorprendenti per creare dettagli di armature. I cartoni ondulati, stratificati e trattati con colla vinilica, diventano sorprendentemente rigidi e leggeri. I vecchi abiti possono essere trasformati, tinti e modificati in costumi completamente nuovi.</p>

                <p>Particolarmente prezioso è il materiale espanso (polistirolo) che si trova negli imballaggi di elettrodomestici. Questo materiale, normalmente destinato alla spazzatura, può essere scolpito, verniciato e trattato per creare props e dettagli di costume di ottima qualità. I cosplayer più esperti hanno sviluppato tecniche specifiche per lavorare il polistirolo in modo sicuro e ottenere risultati professionali.</p>

                <h3>Il Mercato dell'Usato: Opportunità e Comunità</h3>
                <p>Un altro pilastro del cosplay sostenibile è il mercato dell'usato. La community italiana ha sviluppato un fiorente ecosistema di scambio e vendita di costumi usati, materiali avanzati e props non più necessari. Gruppi Facebook dedicati, marketplace online e gli stessi stand delle fiere sono luoghi dove trovare pezzi di qualità a prezzi accessibili, dando nuova vita a costumi che altrimenti rimarrebbero inutilizzati.</p>

                <p>Questa cultura dello scambio ha anche un valore sociale importante: rafforza i legami all'interno della community, crea reti di supporto tra cosplayer e promuove un modello di consumo più consapevole. Il cosplay sostenibile è, in definitiva, anche un cosplay più comunitario.</p>
        """,
        "immagine_alt": "Cosplayer che lavora con materiali riciclati per creare un costume"
    },
    {
        "slug": "cosplay-competizioni-gare",
        "titolo": "Competizioni Cosplay in Italia: Come Prepararsi e Vincere",
        "categoria": "Competizioni",
        "categoria_class": "competizioni",
        "categoria_color": "#e91e8c",
        "lead": "Le gare cosplay sono il palcoscenico dove i migliori cosplayer italiani si confrontano. Scopri come funzionano le competizioni, cosa cercano i giudici e come prepararsi per salire sul podio.",
        "contenuto": """
                <h3>Il Sistema delle Competizioni Cosplay</h3>
                <p>Le competizioni cosplay in Italia seguono un sistema strutturato che va dalle gare locali fino alle selezioni per i campionati mondiali. Capire questa gerarchia è fondamentale per chi aspira a competere ad alto livello. Le gare locali, organizzate nelle fiere minori, sono il punto di partenza ideale: meno pressione, giudici spesso più accessibili e un'atmosfera più rilassata che permette di fare esperienza senza troppa ansia.</p>
                
                <p>Le competizioni nazionali, come quelle di Lucca Comics e Romics, rappresentano il livello successivo. Qui i partecipanti vengono valutati non solo per la qualità del costume, ma anche per la performance sul palco, la fedeltà al personaggio e la capacità di comunicare con il pubblico. I migliori classificati nelle gare nazionali possono qualificarsi per competizioni internazionali come il <strong>World Cosplay Summit</strong> in Giappone o l'<strong>EuroCosplay</strong> in Gran Bretagna.</p>

                <h3>Cosa Cercano i Giudici</h3>
                <p>I criteri di valutazione nelle competizioni cosplay sono più complessi di quanto possa sembrare. La maggior parte delle gare italiane valuta il costume su tre assi principali: la qualità costruttiva (craftsmanship), la fedeltà al personaggio originale e la performance sul palco. Ognuno di questi aspetti richiede un tipo diverso di preparazione e abilità.</p>

                <p>La qualità costruttiva è l'aspetto più tecnico: i giudici esaminano da vicino le cuciture, le finiture, i dettagli delle armature, la qualità delle vernici e la solidità complessiva del costume. Spesso i cosplayer devono presentare un "making of" fotografico che documenti il processo di costruzione, dimostrando che il costume è stato realizzato interamente da loro.</p>

                <h3>La Performance: L'Arte di Essere il Personaggio</h3>
                <p>La performance sul palco è spesso l'elemento che distingue i vincitori dai semplici partecipanti. Non basta avere un costume perfetto: bisogna saper interpretare il personaggio, muoversi come lui, comunicare la sua essenza al pubblico in pochi minuti. I cosplayer italiani più competitivi investono tanto nella preparazione della performance quanto nella costruzione del costume.</p>

                <p>Molti si avvalgono di coreografi, insegnanti di recitazione o semplicemente di amici disposti a fare da pubblico critico durante le prove. La scelta della musica, la struttura della performance (spesso una mini-storia di 2-3 minuti), le pose e i movimenti vengono studiati e ripetuti fino alla perfezione. Sul palco, ogni secondo conta.</p>
        """,
        "immagine_alt": "Cosplayer sul palco di una competizione cosplay italiana"
    },
    {
        "slug": "cosplay-fotografia-scatti-perfetti",
        "titolo": "Fotografia Cosplay: Come Ottenere Scatti Perfetti alle Fiere",
        "categoria": "Fotografia",
        "categoria_class": "foto",
        "categoria_color": "#7c3aed",
        "lead": "Una bella foto può immortalare mesi di lavoro e far conoscere il tuo cosplay al mondo intero. Ecco i segreti della fotografia cosplay, dai consigli per i cosplayer ai trucchi per i fotografi.",
        "contenuto": """
                <h3>L'Importanza della Fotografia nel Cosplay Moderno</h3>
                <p>Nell'era dei social media, la fotografia è diventata parte integrante del cosplay tanto quanto la costruzione del costume stesso. Una foto straordinaria può trasformare un cosplay eccellente in un fenomeno virale, portando visibilità internazionale al cosplayer e ispirando migliaia di persone in tutto il mondo. Non è un caso che molti dei cosplayer italiani più seguiti sui social abbiano anche una forte sensibilità fotografica o collaborino stabilmente con fotografi professionisti.</p>
                
                <p>La relazione tra cosplayer e fotografo è una delle più creative e produttive nel panorama artistico contemporaneo. Non si tratta di una semplice sessione fotografica: è una collaborazione artistica dove entrambi contribuiscono con la propria visione per creare qualcosa di unico. I migliori scatti cosplay nascono da una comunicazione aperta, da una preparazione condivisa e da una fiducia reciproca.</p>

                <h3>Location: Il Terzo Elemento del Cosplay</h3>
                <p>La scelta della location è cruciale per la fotografia cosplay. L'ambiente giusto può amplificare enormemente l'impatto visivo di un costume, creando un contesto narrativo che trasporta lo spettatore direttamente nell'universo del personaggio. I cosplayer italiani hanno a disposizione un patrimonio architettonico e paesaggistico unico al mondo: castelli medievali, borghi storici, paesaggi naturali spettacolari.</p>

                <p>Molti cosplayer italiani pianificano sessioni fotografiche in location specifiche scelte per la loro compatibilità con il personaggio. Un cavaliere medievale fotografato nelle mura di un castello toscano, una maga fotografata tra le rovine di un tempio greco in Sicilia, un ninja fotografato tra i bambù di un giardino giapponese in Veneto: queste scelte creative elevano la fotografia cosplay a un livello artistico superiore.</p>

                <h3>Tecnica Fotografica per il Cosplay</h3>
                <p>Dal punto di vista tecnico, la fotografia cosplay presenta sfide specifiche. I costumi spesso includono elementi molto chiari (armature bianche, ali luminose) e molto scuri (mantelli neri, capelli scuri) nella stessa inquadratura, richiedendo una gestione attenta dell'esposizione. I dettagli del costume devono essere visibili, ma il soggetto non deve sembrare piatto: la luce deve modellare le forme tridimensionali del costume.</p>

                <p>L'illuminazione artificiale, usata in modo creativo, può trasformare completamente l'atmosfera di uno scatto. Luci colorate, flash modificati e pannelli LED sono strumenti sempre più usati dai fotografi specializzati in cosplay. La post-produzione gioca anch'essa un ruolo importante: ritocchi mirati, effetti di luce e compositing digitale possono aggiungere elementi fantastici che completano l'illusione del personaggio.</p>
        """,
        "immagine_alt": "Fotografo che scatta foto a un cosplayer in un ambiente suggestivo"
    }
]

def get_next_article_number():
    """Determina il numero del prossimo articolo da creare."""
    existing = list(Path('.').glob('articolo*.html'))
    # Filtra solo i file con numero (articolo1.html, articolo2.html, ecc.)
    nums = []
    for f in existing:
        name = f.stem  # es. "articolo1"
        try:
            num = int(name.replace('articolo', ''))
            nums.append(num)
        except ValueError:
            pass
    return max(nums) + 1 if nums else 4

def get_next_theme(article_num):
    """Seleziona il tema per il nuovo articolo in modo ciclico."""
    idx = (article_num - 4) % len(TEMI_ARTICOLI)
    return TEMI_ARTICOLI[idx]

def get_date_str():
    """Restituisce la data corrente formattata in italiano."""
    mesi = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
            'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
    oggi = datetime.date.today()
    return f"{oggi.day} {mesi[oggi.month - 1]} {oggi.year}"

def genera_html_articolo(num, tema, data_str):
    """Genera l'HTML completo per un nuovo articolo."""
    nav_links = ""
    for i in range(1, num + 1):
        active = ' class="active"' if i == num else ''
        nav_links += f'<li><a href="articolo{i}.html"{active}>Articolo {i}</a></li>\n                    '

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{tema['lead'][:155]}">
    <title>{tema['titolo']} | Cosplay ITA Blog</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="logo">Cosplay ITA <span>Blog</span></h1>
            <nav class="nav">
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="articolo1.html">Anime & Fiere</a></li>
                    <li><a href="articolo2.html">Crafting</a></li>
                    <li><a href="articolo3.html">Makeup</a></li>
                    {nav_links}
                </ul>
            </nav>
        </div>
    </header>

    <main class="container article-container">
        <article class="post full-post">
            <header class="post-header">
                <span class="category" style="background:{tema['categoria_color']};color:white;">{tema['categoria']}</span>
                <h2>{tema['titolo']}</h2>
                <div class="meta">Pubblicato il {data_str} &bull; Lettura: 8 min</div>
            </header>

            <img src="assets/images/articolo1/evento.jpg" alt="{tema['immagine_alt']}" class="featured-image">

            <div class="post-content">
                <p class="lead">{tema['lead']}</p>
                {tema['contenuto']}
            </div>
        </article>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 Cosplay ITA Blog. Tutti i diritti riservati.</p>
            <p>Aggiornato automaticamente ogni 3 giorni con nuovi articoli!</p>
        </div>
    </footer>
</body>
</html>"""

def main():
    num = get_next_article_number()
    tema = get_next_theme(num)
    data_str = get_date_str()
    
    html = genera_html_articolo(num, tema, data_str)
    
    filename = f"articolo{num}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Creato: {filename} - {tema['titolo']}")
    
    # Salva info per lo script di aggiornamento index
    info = {
        "numero": num,
        "slug": tema['slug'],
        "titolo": tema['titolo'],
        "categoria": tema['categoria'],
        "categoria_class": tema['categoria_class'],
        "categoria_color": tema['categoria_color'],
        "lead": tema['lead'],
        "data": data_str,
        "filename": filename
    }
    
    with open('scripts/ultimo_articolo.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Info salvate in scripts/ultimo_articolo.json")

if __name__ == "__main__":
    main()
