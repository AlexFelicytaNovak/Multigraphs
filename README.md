# Installation
Requirements:
* Python 3.10 or newer

Install dependencies:

When in the root project directory
```bash
$ python -m pip install -r requirements.txt
```

# Usage
Run with one graph to find maximal cliques, approximate maximal cliques, and maximum clique
```bash
$ python main.py -g1 path/to/graph
```
Run with two graphs to find maximal subgraphs or distance between these graphs.
### Distance using L1 norm
```bash
$ python main.py -g1 path/to/graph -g2 path/to/graph -d1
```
### Distance using L1 norm approximation
```bash
$ python main.py -g1 path/to/graph -g2 path/to/graph -ad1
```
### Distance using L2 norm
```bash
$ python main.py -g1 path/to/graph -g2 path/to/graph -d2
```
### Distance using L2 norm approximation
```bash
$ python main.py -g1 path/to/graph -g2 path/to/graph -ad2
```
### Maximal subgraph
```bash
$ python main.py -g1 path/to/graph -g2 path/to/graph -s
```
### Maximal subgraph approximation
```bash
$ python main.py -g1 path/to/graph -g2 path/to/graph -as
```