# dep2latex

dep2latex is a Python script that converts dependencies output by natural language parsers into nice graphs in LaTeX.

This script is currently *very* custom, i.e. it was built for my own needs, but it could still be very useful to others.

## Requirements

- TikZ
- LuaTeX

You will need to compile your TeX document with `lualatex`.

## Usage

The script accepts output files from three parsers as input.

- C++ C&C parser: output file from `bin/candc --models models --input INPUTFILE`
- Stanford parser: output file using switch `-outputFormat "penn,typedDependencies"`
- Berkeley parser: output file from `java ... edu.stanford.nlp.trees.EnglishGrammaticalStructure -treeFile TREEFILE`, where `TREEFILE` is the output file from the Berkeley parser. The Stanford parser is used to convert the trees into dependencies.

Run `./dep2latex.py DEPSFILE`, with a `data` folder already created in the same directory. The following files will be generated:

- `DEPSFILE.tree` containing *all* the LaTeX code
- `data/sentXYY.tex` for each sentence in `DEPSFILE`; `X` is the sentence number and `YY` is the code for the parser

The individual TeX files are for easier management; it is wise to use something like `\input{data/sent2cc.tex}` in your TeX document, which will also need the following:

```
\usepackage{tikz}
\usetikzlibrary{graphdrawing}
\usetikzlibrary{graphs}
\usetikzlibrary{quotes}
\usegdlibrary{layered}
```

The generated graphs will not be perfect. Fortunately, you can shift the positions of the nodes and labels with `nudge` and `pos` respectively:

```
...
\node (can-8) [nudge left=80mm] {can};
\node (savings-15) [nudge right=20mm] {savings};
...
(see-30) edge["dobj", ->, pos=0.3] (trusts-36)
(responsibility-46) edge["nmod:for", ->, pos=0.2] (the-48)
...
```
