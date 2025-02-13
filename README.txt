-- Script di automazione per la simulazione di trasporti eccezionali sul portale TE di Autostrade per l'Italia --

Per la stesura di preventivi e per l'organizzazione di trasporti eccezionali è 
fondamentale eseguire delle ricerche preliminari sulle limitazioni
- di sagoma
- di peso
sui vari percorsi possibili.

Il portale ASPI dedicato alle aziende del settore permette di interrogare il
database. Per questo è necessario
- accettare le condizioni previa lettura
- inserire dati completi dei mezzi
- date e percorsi
L'inserimento manuale di questi dati può consumare molto tempo (fino a 20 minuti) 
e, in molti casi, essere superfluo ai fini della ricerca. Spesso infatti l'unica 
limitazione rilevante è quella di altezza. Inoltre, durante la fase di preventivo 
non sono disponibili i dati specifici del convoglio.

Per ovviare a questo spreco di tempo ho scritto due script di automazione
in Python che lasciano all'utente soltanto la scelta del percorso.

-- ALTEZZA
Vengono inseriti valori realistici e un'altezza esageratamente alta
per attivare tutti gli alert di altezza

-- PESO
Nel caso in cui il convoglio abbia un'eccedenza di peso, il portale ASPI
richiede di fornire i dati completi di distribuzione del peso e di
tiplogia degli assi.
Questo tipo di interrogazione avviene più spesso durante la pianificazione
del viaggio, per cui è fondamentale considerare i dati effettivi
del convoglio. Se il viaggio è già in programmazione, i dati sono
presenti sul gestionale, che ha generato un file xml. Lo script utilizza
tutti i dati di questo xml per compilare il modulo.
ISSUES: nel caso di assi C4V bisogna selezionare manualmente la tipologia.
