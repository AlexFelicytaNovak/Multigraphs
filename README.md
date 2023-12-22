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
### Maximal subgraph
```cmd
.\main.exe -g1 path/to/graph -g2 path/to/graph -s
```
### Maximal subgraph approximation
```cmd
.\main.exe -g1 path/to/graph -g2 path/to/graph -as
```
