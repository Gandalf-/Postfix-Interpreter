# Postfix-Interpreter
Postfix language interpreter implemented in Python

**Running the interpreter**
- Put *interpreter.py* and *commands.py* in the same directory.
- Run *python interpreter.py*
- Quit the interpreter by pressing *return* on an empty line

**Example Postfix Programs**
- (postfix 2 add)
- (postfix 1 1 nget mul) 
- (postfix 1 1 nget 0 lt (0 swap sub) () sel exec)
- (postfix 0 (swap exec swap exec) (1 sub) swap (2 mul) swap 3 swap exec)