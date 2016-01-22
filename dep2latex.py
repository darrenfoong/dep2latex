#!/usr/bin/python

import os
import sys
from collections import defaultdict

FILE = sys.argv[1]

with open(FILE, "r") as input_file, \
     open(os.path.basename(FILE)+".tree", "w") as output_file:

    start_pos = input_file.tell()
    first_line = input_file.readline()
    input_file.seek(start_pos)

    if first_line[0] == "#":
        FORMAT = "cc"
        PARSER = "cc"
        sents = input_file.read().split("\n\n")[1:]
        sents = map(lambda lines: lines.splitlines()[:-1], sents)
        sents = sents[:-1]
    elif first_line[0] == "(":
        FORMAT = "sp"
        PARSER = "sp"
        sents = input_file.read().split("\n\n")[1::2]
        sents = map(lambda lines: lines.splitlines(), sents)
    else:
        FORMAT = "sp"
        PARSER = "bp"
        sents = input_file.read().split("\n\n")
        sents = map(lambda lines: lines.splitlines(), sents)
        sents = sents[:-1]

    nodes = None
    adj_list = None

    def parse_edge(edge):
        if FORMAT == "sp":
            label = edge.split("(")[0]
            start_end = edge.split("(")[1].split(")")[0].split(", ")
            start = start_end[0]
            end = start_end[1]
        elif FORMAT == "cc":
            label_start_end = edge.split("(")[1].split(")")[0].split(" ")
            label = label_start_end[0]
            if label == "ncsubj":
                start = label_start_end[1]
                end = label_start_end[2]
                if label_start_end[-1] != "_":
                    label += ":" + label_start_end[-1]
            else:
                start = label_start_end[-2]
                end = label_start_end[-1]
                if len(label_start_end) == 4 and label_start_end[1] != "_":
                    if label == "ncmod":
                        label += ":" + label_start_end[1]
                    else:
                        label += ":" + sanitise_ext(label_start_end[1])
        return start, end, label

    def sanitise_inner(node):
        node = node.replace("#", "_HASH")
        node = node.replace(",", "_COMMA")
        node = node.replace(":", "_COLON")
        return node

    def sanitise_ext(node):
        node = node.replace("#", "\#")
        if FORMAT == "sp":
            delimit = "-"
        elif FORMAT == "cc":
            delimit = "_"
        return delimit.join(node.split(delimit)[:-1])

    def sanitise_label(label):
        label = label.replace("_", "\_")
        return label

    def get_index(node):
        if FORMAT == "sp":
            delimit = "-"
        elif FORMAT == "cc":
            delimit = "_"
        return int(node.split(delimit)[-1])

    def build_tree(sent, num):
        global nodes
        global adj_list
        global output_file
        nodes = set()
        adj_list = defaultdict(dict)
        for edge in sent:
            start, end, label = parse_edge(edge)
            adj_list[start][end] = label
            nodes.add(start)
            nodes.add(end)

        output = ""

        output += "\\begin{figure}[h]\n"
        output += "\\begin{center}\n"
        output += "\\scalebox{1.0}{\n"
        output += "\\centering\n"
        output += "\\tikz [layered layout, rounded corners, >=stealth, sibling distance=20mm, level distance=15mm, every edge quotes/.style={fill=white,font=\\tiny,inner sep=1pt}] {\n"

        for node in sorted(nodes, key=get_index):
           output += "\\node (" + sanitise_inner(node) + ") {" + sanitise_ext(node) + "};\n"

        output += "\\draw\n"

        for node in sorted(adj_list, key=get_index):
           for child in adj_list[node]:
               output += "(" + sanitise_inner(node) + ") edge[\"" + sanitise_label(adj_list[node][child]) + "\", ->, pos=0.7] (" + sanitise_inner(child) + ")\n"

        output += ";}\n"
        output += "}\n"
        output += "\\end{center}\n"
        output += "\\caption{Sentence " + str(num) + " (" + PARSER + ").} \\label{fig:sent" + str(num) + PARSER + "}\n"
        output += "\\end{figure}\n\n"

        with open("data/sent" + str(num) + PARSER + ".tex", "w") as sub_output_file:
            sub_output_file.write(output)

        output_file.write(output)

    for num, sent in enumerate(sents, start=1):
        build_tree(sent, num)
