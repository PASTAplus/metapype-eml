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
EML rule set\*. All other node attributes may be accessed through setters and
getters.

<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/node.png" /></p>

A complete and compliant EML 2.1.1 metadata content model tree (albeit not too
informative) is found in the following diagram:

<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/eml_model.png"/></p>

#### Metadata Standard Compliance Rules

A metadata standard compliance rule is a codified set of constraints that follow
the same (or similar) requirements that are declared within the
corresponding metadata standard. In Metapype for EML, in particular, these rules
are written in accordance with the element definitions as declared in the EML
XML schema. Each rule enforces the presence of XML attributes, content
requirements, and if a "complex" XML element is being modeled, the sequence or choice of
descendant elements, including descendant cardinality (descendant elements are
represented as children in the metadata content model). Rules do not support all
XML schema constructs (e.g., groups or all), but they can also enforce
constraints or practices that fall outside of the XML schema.

Rules are broken into three parts: 1) zero or more node specific constraints
(such as data type or enumerations; constraints do not have to be XML schema
dependent); 2) an ordered list of allowable children nodes and their
corresponding cardinality; and 3) an non-ordered list of allowable attributes
and whether they are required or optional.

In general, node specific constraints are written as Python conditional
statements (e.g., `if`, `else`, or `elif`) and provide a "fail fast" method
for node validation. Node specific constraints are best used for enforcing
content types or enumerations as declared in the XML schema, but they can also
encode more qualitative assessments, such as whether the content meets
requirements of community best practices. To satisfy complex situations,
multiple conditional statements may be chained depending on need.

Following the section of conditional statements, if any, is the declaration of
allowable children (children correspond to sub-elements or sub-trees declared in
"complex" XML elements). This list of allowable children must declare not only
the sequence or choice of acceptable descendants, but also their correct
cardinality. The list of allowable children is represented as a nested Python
list of lists; the outer list specifies the sequence in which children may
occur, while the inner lists specify what specific children may occur at the
specific step-wise location of the sequence, whether there is a chocie of
children, and their allowed cardinality. This data structure is passed to a
validating function that iterates through both the rule-based list and the list
of children from the node instance to confirm compliance as specified in the
given rule. Failure to comply with the rule at this point indicates that the 
node contains illegal children, children occurring in the wrong sequence, or 
children occurring too few or too many times.

The last section of the rule declares allowable node attributes (node attributes
are equivalent to attributes specified in the XML schema). Allowable attributes
are represented as a Python dictionary, where attribute names are the "keys" and
their cardinality (i.e., optional or required) the "values". Similar to the
validating function found for node children, the attributes of the node instance
are checked against those of the rule dictionary of allowable attributes. Errors
during this processing step include the presence of illegal attributes or
missing attributes that are required. The literal values of node attributes are 
not currently evaluated during this step of validation, but can be codified as
a node specific constraint described above (see following example).

The following is an example of the "access" rule as codified in Python:

```Python
def access_rule(node: Node):
    # Node specific constraint section
    if 'order' in node.attributes:
        allowed = ['allowFirst', 'denyFirst']
        if node.attributes['order'] not in allowed:
            msg = '"{0}:order" attribute must be one of "{1}"'.format(node.name, allowed)
            raise MetapypeRuleError(msg)

    # Children rule section
    children = [
        ['allow', 'deny', 1, INFINITY]
    ]
    process_children(children, node)

    # Attribute rule section
    attributes = {
        'id': OPTIONAL,
        'system': OPTIONAL,
        'scope': OPTIONAL,
        'order': OPTIONAL,
        'authSystem': REQUIRED
    }
    process_attributes(attributes, node)
```

The `access_rule` example demonstrates all three rule sections: 1) The node
specific constraint validates the value of a specific node attribute. In this
case, the `order` attribute, if defined, must have a value of either
`allowFirst` or `denyFirst` only. 2) The allowable children rule defines a
single descendant node choice of either an `allow` or `deny` child, along with
the cardinality of 1 to infinity. And finally, 3) the allowable attributes rule
defines the set of acceptable attributes to be `id`, `system`, `order`, and
`authSystem`; all defined attributes are optional with the exception of
`authSystem`, which is required.

<hr/>

\*Actually, the metadata content model may contain any hierarchical content that
can be entered into the existing Node data structure, but will not validate as
an EML metadata content model either at the node or the tree level.

