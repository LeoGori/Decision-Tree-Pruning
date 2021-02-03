# Decision-Tree-Pruning

Nella seguente repository viene implementato un algoritmo per l'apprendimento di alberi di decisione utilizzando l'entropia come misura di impurità (descritto nel libro "Artificial Intelligence: A Modern Approach", P.Norvig, S.Russell, §18.3) e di una strategia di pruning su un insieme di regole estratte dalla struttura dell'albero basata sull'errore sul validation set (descritto nel libro "Machine Learning", T. Mitchell, §3.7.1.2).

# Come usare il codice
Per poter eseguire il test per il confronto dell'accuratezza prima e dopo l'applicazione della strategia di pruning è necessario scaricare il dataset [Nursery](https://archive.ics.uci.edu/ml/datasets/Nursery) e inserire il file 'nursery.data' all'interno della directory nominata 'Data'.

# Descrizione del codice
I file che compongono il progetto sono:
- **_Classification.py_**: classe che raccoglie l'insieme delle possibili classificazioni del dataset, definite nel file 'Classification' all'interno della directory 'Data'. Per comodità il file è inizializzato con le classificazioni del dataset **Nursery** ma può essere sovrascritto per l'utilizzo di altri dataset. **N:B.**: le varie classificazioni devono essere divise da ", " (Es.: 'TRUE, FALSE').
- **_Attribute.py_**: classe che raccoglie i nomi degli attributi e i relativi valori legali, definiti nel file 'Attributes and values' all'interno della directory 'Data'. Per comodità il file è inizializzato con gli attributi seguiti dai relativi valori legali del dataset **Nursery** ma può essere sovrascritto per l'utilizzo di altri dataset. **N:B.**: ogni riga inizia col nominativo dell'attributo, seguito da i relativi valori distinti da "," (Es.: 'colore,rosso,verde,giallo')
- **_Example.py_**: classe che registra coppie (Attributo, Valore) per ogni attributo di un esempio del dataset.
- **_Node.py_**: classe che rappresenta un'entità nodo, per la realizzazione di un albero di decisione, la quale registra i valori di attributo scelto sulla base del guadagno di informazione basato su entropia.
- **_Tree.py_**: classe che raccoglie in una struttura a albero elementi di tipo __Node__.
- **_Rule.py_**: classe che rappresenta una regola di decisione, la quale registra un insieme di coppie (Attributo, Valore) come __Preconditions__ e la relativa classificazione come __Postcondition__.
- **_SetOfRules.py_**: classe che racoglie una lista di elementi di tipo __Rule__ responsabile dell'esecuzione della strategia di pruning e del successivo ordinamento della lista di decisione.
- **_DecisionTreeLearning.py_**: File contenente funzioni per l'apprendimento dell'albero di decisione.
- **_Test.py_**: classe che esegue i test su alberi di decisione generati su porzioni di dataset scelte in modo casuale, e che registra i valori delle accuratezze delle strutture di decisione prima e dopo la strategia di pruning.

# Linguaggio e librerie

Il progetto è stato realizzato utilizzando _Python 3.8_ come linguaggio di programmazione. Sono inoltre state utilizzate le seguenti librerie:
- **random**: per generare numeri casuali, rimuovere casualmente e uniformemente con una data probabilità alcuni valori e per scegliere casualmente degli elementi da una lista.
- **copy**: per eseguire la deepcopy di alcune liste nel main.
- **texttable**: per la generazione di codice Latex per la costruzione di tabelle per raccogliere i valori delle accuratezze.
- **csv**: per la lettura di informazioni quali gli esempi del dataset da file di testo.
- **sklearn**: per lo splitting del dataset e l'estrazione casuale di set di esempi per la generazione di training set, validation set e test set.
