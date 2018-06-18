# Metapype for EML

#### A light weight metadata generator for the Ecological Metadata Language

<hr />

Metapype is a Python 3 library for building, saving, and exporting
scientific metadata using a flexible metadata content model in a
hierarchical tree-like structure. This version of Metapype is designed
to reflect the content structure of the Ecological Metadata Lanaguage
(EML) XML schema, but is not locked into a specific version of EML.

Metapype is divided into a metadata content model and a set of conditional rules
that enforce model compliance to a specific metadata standard. The content model
is fully independent of the compliance rules, but cannot perform node or
tree validation without the rules; as such, they must operate together to serve
as a metadata generator.

#### Metadata Content Model

The metadata content model is designed as a hierarchical directed graph with a
root node that spans the tree's children using directional links; similarly,
each child node contains a reverse link to its parent (or root) node. Only the
root node may be without parent link. Node links for either parent or children
are constructed of the nodes respective address in memory. Nodes represent the
primary characteristics of their corresponding XML schema elements, including
attributes, content, and children. Node instances must be generated with at
least the corresponding "name" as found in the schema for binding to the
EML rule set*. All other node attributes may be accessed through setters and
getters.

<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/node.png" /></p>

A complete and compliant EML 2.1.1 metadata content model tree (albeit not too
informative) is found in the following diagram:

<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/eml_model.png"/></p>

#### Metadata Standard Compliance Rules

A metadata standard compliance rule is a codified set of constraints that follow
the same (or similar) constraints that are declared within the corresponding
metadata standard. In Metapype for EML, these rules are written in accordance
with the element definition as declared in the EML XML schema. Each
rule supports the presence of XML attributes, content, and if a "complex" XML
element, the sequence or choice of descendant elements, including descendant
cardinality (descendant elements are represented as children in the metadata
content model). Rules do not support all XML schema constructs (e.g., groups or
all).

Rules are broken into three parts: 1) zero or more node specific rules (such as
a datatype constraint) or a context sensitive rule (such as allowing only an
enumerated set of choices); 2) an ordered list of allowable children and their
corresponding cardinality; and 3) an unordered list of allowable attributes and
whether they are required or optional.

A typical rule has the following Python code structure:

1. Conditional statements
2. Ordered list of lists (sublists are lists of children names and cardinality)
3. Dictionary of attributes

There is a processing step after sections 2 and 3, respectively, that evaluates
model node for rule compliance. Not all rules have the three sections described
above. The following is an example of the "access" rule:

```Python
def access_rule(node: Node):
    if 'order' in node.attributes:
        allowed = ['allowFirst', 'denyFirst']
        if node.attributes['order'] not in allowed:
            msg = '"{0}:order" attribute must be one of "{1}"'.format(node.name, allowed)
            raise MetapypeRuleError(msg)
    children = [
        ['allow', 'deny', 1, INFINITY]
    ]
    process_children(children, node)
    attributes = {
        'id': OPTIONAL,
        'system': OPTIONAL,
        'scope': OPTIONAL,
        'order': OPTIONAL,
        'authSystem': REQUIRED
    }
    process_attributes(attributes, node)      
```

<hr/>

*Actually, the metadata content model may contain any hierarchical content that
can be entered into the existing Node data structure, but will not validate as
an EML metadata content model either at the node or the tree level.

