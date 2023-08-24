# yeplang
Yep is a toy programming language to use as a testbed for ideas on parsers, interpreters, just in time compilation, and ahead of time compilation.  Initially we'll implement a tree-walk interpreter with a scanner and lexer as well as an interpreter. Once that is working we intend to experiment with backends for LLVM, Webasm, and or C.

We'll be starting with ideas for Lox from *Crafting Interpreters* by Robert Nystrom, but will be using Python and C++ instead of Java and C.

## Getting Started
```
python -m venv venv
venv\scripts\activate
cd src\yep
pip install -r requirements.txt
pip install -e .
```

## Running tests
```
cd src\yep
python -m unittest discover
```