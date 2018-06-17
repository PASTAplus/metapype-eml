# Metapype for EML

#### A light weight metadata generator for the Ecological Metadata Language

<hr />

Metapype is a Python 3 library for building, saving, and exporting
scientific metadata using a flexible metadata content model in a
hierarchical tree-like structure. This version of Metapype is designed
to reflect the content structure of the Ecological Metadata Lanaguage
(EML) XML schema, but is not locked into a specific version of EML.

Metapype is divided into a metadata content model and a set of rules that
enforces compliance to a specific standard. The content model can function
fully independent of compliance rules, but cannot perform node or tree
validation.

### Metadata Content Model

The metadata content model is designed as a hierarchical directed graph with a
root node that spans the tree's children using directional links; similarly,
each child node contains a reverse link to its parent (or root) node. Only the
root node may be without parent link. Node links for either parent or children
are constructed of the nodes respective address in memory. Nodes represent the
primary characteristics of their corresponding XML schema elements, including
attributes, content, and children. Node instances must be generated with at
least the corresponding "rank" name as found in the schema [^1]. All other
content may be accessed through setters and getters.

<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/node.png" /></p>

A complete and compliant EML 2.1.1 tree, albeit not too informative, is found in
the following diagram:

<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/eml_model.png"/></p>

[^1]: Actually, the metadata content model may contain any hierarchical
      content that can be entered into the existing Node data structure,
      but will not validate as an EML metadata content model either at
      the node or the tree level.