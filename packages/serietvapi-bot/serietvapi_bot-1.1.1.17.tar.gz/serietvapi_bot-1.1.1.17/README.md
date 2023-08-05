# SerieTvITaly_bot_downloader

<h3>Come installo?</h3>
Questo pacchetto è disponibile <b>solo per il Python 3</b>, eseguirlo con Python 2 significherebbe avere errori.<br>
<code>pip install serietvapi_bot</code><br>
Se restituisce errori provate ad eseguire il comando con i privilegi di amministratore (mettendo <code>sudo</code> davanti al comando).<br>
Attualmente è ben testato per il sistema operativo macOS, per Windows non è stato testato mentre per il sistema operativo Raspbian (Raspberry Pi) è ancora da testare e supportare.

<h3>Cosa viene installato?</h3>
Questo è un tool Python che si appoggia ad altri tool python, tutti gratuiti ed open-source.<br>
Ecco tutti i moduli Python che vengono installati quando installate il nostro tool:<br>
<ol>
	<li><a href="https://rg3.github.io/youtube-dl/">youtube-dl</a> per effettuare i download</li>
	<li><a href="https://github.com/LonamiWebs/Telethon/">Telethon</a> permette di creare un Client Telegram e di eseguire delle operazioni al vostro posto, noi lo utilizziamo per effettuare i caricamenti dei file che sono stati scaricati.</li>
	<li><a href="https://github.com/requests/requests">requests</a> è un tool che permette di inviare richieste HTTP con sintassi più umana (quella integrata nel Python è poco umana, prossima a sintasssi Java)</li>
</ol>
Inoltre verrano installati anche altri moduli che sono richiesti da questi moduli.

<h3>Mi vengono chiesti dati che Telegram dice di non fornire, come mai?</h3>
Telethon è a tutti gli effetti un Client Telegram alternativo però senza una GUI (interfaccia utente) e per questo motivo sono richiesti alcuni dati sensibili come numero di telefono, codice di verifica e, se impostata, la password.<br>
Tali dati <b>NON</b> sono memorizzati nè sul vostro computer nè sui nostri server (potete visionare i file e vedere che tali salvataggi non avvengono).<br>
Ci sono due file uno che termina per <b>.json</b> e l'altro che termina per <b>.sessione</b>, il primo memorizza le credenziali per usare le API sia di Telethon (con i valori api_id e api_hash già inseriti, potete inserire delle vostre se avete un Client tutto vostro) sia del nostro Bot Telegram <a href="https://t.me/SerieTvItaly_bot">@SerieTvItaly_bot</a> e queste vengono fornite al momento della creazione dell'account API nel Bot.<br>
Tali dati sono richiesti solo una volta e valgono per tutta la durata del vostro account, quando l'account è scaduto o non più valido verranno chieste nuovamente le credenziali automaticamente.<br>
Il secondo file (.session) ha tutte le informazioni che servono per interagire col vostro profilo (inviare messaggi ed ottenerli, anche media) ma non vi sono riferimenti a numero di telefono o vostra password ma altre informazioni che Telegram fornisce.<br>
Essendo un Client Alternativo potenzialmente è possibile usare Telegram anche con questo script Python, come potete vedere anche dai codici i messaggi e i file vengono inviati solo al nostro Bot e nessuna lettura di messaggi avviene fatto perché non ci interessa perché lo scopo di questo script Python è quello di contribuire al miglioramento del nostro Bot e qunidi attribuire premi maggiori.