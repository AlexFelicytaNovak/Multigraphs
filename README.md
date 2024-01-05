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
1. In terminal (either Powershell or cmd on Windows), navigate to the `Exe` directory, containing the program executable.

With both cmd (Command Prompt) and Powershell the command is the same:
```
cd path\to\Exe\directory
```
2. Run the `main.exe` file with a set of desired arguments. For example:
```cmd
.\main.exe -g1 ..\Examples\g3.txt -c
```
The set of parameters from the call above calculates the maximum clique(s) and all maximal cliques for example graph g3.txt (assuming `Examples` directory is located next to `Exe` directory).

The program can also display a summary of available arguments (flags) with:
```cmd
.\main.exe -h
```
**The program works with the .txt files that contain exactly one graph.** If given a file that contains more than one graph, it will display a message `Provide only files with single graph inside!` and exit. Detailed description and visualizations of graphs provided in `Examples` directory is provided in the project report.

Due to the `.exe` of the program being included, Windows Defender may automatically delete the `main.exe` executable and `Exe` directory may appear empty. In such case, an exclusion for the file needs to be set up in Windows, so that the file does not disappear.

# Possible arguments for testing specific functionality

### Maximum & maximal cliques
```cmd
.\main.exe -g1 path/to/graph -c
```
### Maximum clique approximation
```cmd
.\main.exe -g1 path/to/graph -ac
```
### Distance using L1 norm
```cmd
.\main.exe -g1 path/to/graph -g2 path/to/graph -d1
```
### Distance using L1 norm approximation
```cmd
.\main.exe -g1 path/to/graph -g2 path/to/graph -ad1
```
### Distance using L2 norm
```cmd
.\main.exe -g1 path/to/graph -g2 path/to/graph -d2
```
### Distance using L2 norm approximation
```cmd
.\main.exe -g1 path/to/graph -g2 path/to/graph -ad2
```
### Maximum subgraph
```cmd
.\main.exe -g1 path/to/graph -g2 path/to/graph -s
```
### Maximum subgraph approximation
```cmd
.\main.exe -g1 path/to/graph -g2 path/to/graph -as
```
Argument flags can be used in combination with one-another, f.e. using all options
```cmd
.\main.exe -g1 graph1.txt --clique --approx_clique -g2 graph2.txt --distance_l1 --approx_distance_l1 --distance_l2 --approx_distance_l2 --subgraph --approx_subgraph
```
will result in calculating:
* maximum clique (or cliques) as well as its approximation for graph from the file given next to -g1 (here 'graph1.txt')
* common subgraph (or subgraphs) and approximation of maximum common subgraph (or subgraphs), distance and its approximation (with L1 and L2 norms) for graphs from files given next to -g1 and -g2 (here 'graph1.txt' and 'graph2.txt').
