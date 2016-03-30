# Postfix-Interpreter
Postfix language interpreter implemented in Python

**Running the interpreter**
- Put *interpreter.py* and *commands.py* in the same directory.
- Run *python interpreter.py*
- Quit the interpreter by pressing *return* on an empty line

**Example Postfix Programs**
- In the form "program" -> "arguments" -> "output"
- (postfix 2 add) -> 1 2 -> 3
- (postfix 1 1 nget mul) -> 5 -> 25
- (postfix 1 1 nget 0 lt (0 swap sub) () sel exec) -> -10 -> 10
