# Decision-Tree-Pruning

Implementazione di una strategia di apprendimento e pruning di alberi di decisione
Nella seguente repository vengono implementati gli algoritmi di apprendimento di alberi di decisione utilizzando l'entropia come misura di impurità (descritto nel libro "Artificial Intelligence: A Modern Approach", P.Norvig, S.Russell, §18.3) e di una strategia di pruning su un insieme di regole estratte dalla struttura dell'albero basata sull'errore sul validation set (descritto nel libro "Machine Learning", T. Mitchell, §3.7.1.2).

# Come usare il codice
Per poter eseguire il test per il confronto dell'accuratezza prima e dopo l'applicazione della strategia di pruning è necessario scaricare il dataset [Nursery](https://archive.ics.uci.edu/ml/datasets/Nursery) e inserire il file 'nursery.data' all'interno della directory nominata 'Data'. Dopo di che per eseguire i test descritti nella relazione è sufficiente eseguire il file Test.py.

# Descrizione del codice
I file che compongono il progetto sono:

- [**_Classification.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Classification.py): classe che raccoglie l'insieme delle possibili classificazioni del dataset, definite nel file 'Classification' all'interno della directory 'Data'. Per comodità il file è inizializzato con le classificazioni del dataset Nursery ma può essere sovrascritto per l'utilizzo di altri dataset. N:B.: le varie classificazioni devono essere divise da ", " (Es.: 'TRUE, FALSE').
- [**_Attribute.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Example.py): classe che raccoglie i nomi degli attributi e i relativi valori legali, definiti nel file 'Attributes and values' all'interno della directory 'Data'. Per comodità il file è inizializzato con gli attributi seguiti dai relativi valori legali del dataset Nursery ma può essere sovrascritto per l'utilizzo di altri dataset. N:B.: ogni riga inizia col nominativo dell'attributo, seguito da i relativi valori distinti da "," (Es.: 'colore,rosso,verde,giallo')
- [**_Example.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Example.py): classe che registra coppie (Attributo, Valore) per ogni attributo di un esempio del dataset.
- [**_Node.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Node.py): classe che rappresenta un'entità nodo, per la realizzazione di un albero di decisione, la quale registra i valori di attributo scelto sulla base del guadagno di informazione basato su entropia.
- [**_Tree.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Tree.py): classe che raccoglie in una struttura a albero elementi di tipo **Node**.
- [**_Rule.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Rule.py): classe che rappresenta una regola di decisione, la quale registra un insieme di coppie (Attributo, Valore) come _Preconditions_ e la relativa classificazione come _Postcondition_.
- [**_SetOfRules.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/SetOfRules.py): classe che raccoglie una lista di elementi di tipo **Rule** responsabile dell'esecuzione della strategia di pruning e del successivo ordinamento della lista di decisione.
- [**DecisionTreeLearning.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/DecisionTreeLearning.py): File contenente funzioni per l'apprendimento dell'albero di decisione.
- [**_Test.py_**](https://github.com/LeoGori/Decision-Tree-Pruning/blob/master/Test.py): classe che esegue i test su alberi di decisione generati su porzioni di dataset scelte in modo casuale, e che registra i valori delle accuratezze delle strutture di decisione prima e dopo la strategia di pruning.
# Linguaggio e librerie
Il progetto è stato realizzato utilizzando _Python 3.8_ come linguaggio di programmazione. Sono inoltre state utilizzate le seguenti librerie:

- **copy**: per eseguire la deepcopy di alcune liste.
- **texttable**: per la generazione di codice Latex per la costruzione di tabelle per raccogliere i valori delle accuratezze.
- **csv e pandas**: per la lettura di informazioni quali gli esempi del dataset da file di testo di tipo csv.
- **sklearn**: per lo splitting del dataset e l'estrazione casuale di set di esempi per la generazione di training set, validation set e test set.
- **math**: per l'utilizzo della funzione log(x) per il calcolo dell'entropia.
