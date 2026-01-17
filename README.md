# viewer_stable_diffusion

![image](Screensample)

Stable Diffusion Metadata Explorer è un'applicazione desktop leggera scritta in Python progettata per facilitare la gestione e l'analisi delle immagini generate tramite intelligenza artificiale. Il software permette di navigare velocemente tra le proprie generazioni, visualizzare i parametri tecnici e filtrare i file in base ai prompt utilizzati.

## Caratteristiche

* Galleria Visuale: Visualizzazione fluida delle miniature (thumbnails) delle immagini presenti in una cartella.
* Estrazione Metadati: Recupero automatico di Prompt Positivo, Negative Prompt, Seed, Sampler e altri parametri tecnici.
* Ricerca Dinamica: Sistema di filtraggio istantaneo che analizza i prompt salvati nei metadati per trovare immagini specifiche.
* Copia Rapida: Funzione dedicata per copiare il prompt negli appunti con un solo click.
* Compatibilità: Supporta immagini generate con le principali interfacce come Automatic1111, Forge, ComfyUI e modelli basati su Pony Diffusion.
* Interfaccia Ottimizzata: Design in modalità scura per una migliore leggibilità dei parametri tecnici.

## Requisiti

Per eseguire questo programma è necessario avere Python installato sul proprio sistema. Il software è stato testato su Python 3.8 e versioni successive.

## Installazione
1. Creare una cartella
    ```
   python -m venv venv
   attivare il virtual environment
   pip install -r requirements.txt
   
3. Clonare il repository o scaricare il file sorgente:
   ```bash
   git clone [https://github.com/tuo-username/nome-repository.git](https://github.com/tuo-username/nome-repository.git)
   cd nome-repository
   python app.py
