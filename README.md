# Installation on WUT laboratory machines
Requirements:
* git
* Python 3.9 or newer

1. Boot Windows on the machine.
2. Open Andaconda Powershell Prompt. The binary shortcut should be located in
```
C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)
```
You can ensure that python is available in your terminal by issuing a command:
```bash
PS C:\> python --version
```

If you have sources of the program already downloaded you can navigate to the source directory and skip steps 3 to 6 in this instruction.

3. Navigate to the directory you want to download the package to:
```bash
PS C:\> cd path/to/the/directory
# or
PS C:\> Set-Location path/to/the/directory
```
4. Clone the repository
```bash
PS C:\> git clone https://github.com/AlexFelicytaNovak/Multigraphs
```
5. Go inside the project directory
```bash
PS C:\...\> cd ./Multigraphs
# or
PS C:\...\> Set-Location ./Multigraphs
```
6. Switch to branch dedicated for running on WUT machines
```bash
PS C:\> git switch wut-labs
```
7. When in project directory, install dependencies.
```bash
$ python -m pip install -r requirements.txt
```
8. After that you should be able to run the application.

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
