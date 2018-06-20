# Metapype for EML

#### A lightweight metadata generator for the Ecological Metadata Language

<hr />

Metapype is a Python 3 library for building, saving, and exporting scientific
metadata using a flexible metadata content model in a hierarchical tree-like
structure. Metapype only provides the primitives (as a Python application
programmable interface) for operating on metadata; it is expected that client
applications will use the Metapype API to build more robust and user friendly
applications.

This version of Metapype is designed to reflect the content
structure of the Ecological Metadata Lanaguage (EML) XML schema, but is not
locked into a specific version of EML.

Metapype is divided into a metadata content model and a set of conditional rules
that enforce model compliance to a specific metadata standard. The content model
is fully independent of the compliance rules, but cannot perform node or
tree validation without the rules; as such, they must operate together to serve
as a metadata generator.

#### Metadata Content Model

The metadata content model is designed as a hierarchical directed graph with a
root node that spans the tree's children using directional links; similarly,
each child node contains a reverse link to its parent (or root) node. Only the
root node may be without a parent link. Node links for either parent or children
are constructed of the node's respective address in memory. Nodes represent the
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

A metadata standard compliance rule is a codified set of constraints that
follow the same (or similar) requirements that are declared within the
corresponding metadata standard. In Metapype for EML, in particular, these
rules are written in accordance with the element definitions as declared in
the EML XML schema and are written as individual Python functions. Each rule
enforces the presence of XML attributes, content requirements, and if a
"complex" XML element is being modeled, the sequence or choice of descendant
elements, including descendant cardinality (descendant elements are
represented as children in the metadata content model). Rules do not support
all XML schema constructs (e.g., groups or all). Rules can, however, enforce
constraints or practices that fall outside of the XML schema.

Rules are divided into three parts: 1) zero or more node specific constraints,
such as data type or enumerations requirements (note that constraints do not
have to be XML schema dependent); 2) an ordered list of allowable descendant
nodes and their corresponding cardinality; and 3) an non-ordered list of
allowable attributes and their corresponding cardinality (optional or
required).

Node specific constraints, if any, are written as Python conditional
statements (e.g., `if`, `else`, or `elif`) and provide a "fail fast" method
for node validation. Node specific constraints are best used for enforcing
content data types or enumerations as declared in the XML schema, but they can also
encode more qualitative assessments, such as whether the content complies with
community best practices. To satisfy complex situations, conditional
statements may be chained together for evaluating multiple or different
requirements.

The rule section for descendant children (children correspond to sub-elements
or sub-trees declared in "complex" XML elements) is declared as a nested
Python list. This data structure is a "list-of-lists": the outer list
specifies the sequence in which children may occur, while the inner list(s)
specifies what child node (or children, if a choice) may occur at the current
sequence location. The cardinality (i.e., minimum and maximum occurrence) of
each child node is always set to the last two positions of the list,
thereby making the values accessible through list slicing (i.e., `rule[-2:]`).
The "list-of-lists" data structure is passed to a validating function, called
`rules.process_children`, that iterates through both the rule-based list and the
list of children from the node instance to evaluate compliance as specified in
the given rule. Compliance failure at this point indicates that the node
contains illegal children, children occurring in the wrong sequence, or
children occurring too few or too many times (a cardinality violation).

The rule section for node attributes (node attributes are equivalent to
attributes specified in the XML schema) is the last part of the rule function.
Allowable attributes are represented as a Python dictionary, where attribute
names are the "keys" and their cardinality (i.e., optional or required) the
"values". Similar to the validating function found for descendant children,
the attributes of the node instance are checked against those of the rule's
attribute dictionary using a function called `rules.process_attributes`. Errors
during this step may result from the presence of illegal attributes or
attributes that are required, but missing from the node. The literal value
of node attributes are not evaluated during this validation phase,
but can be codified as a node-specific constraint described earlier (see
following example).

Rule functions implicitly return `None` unless an exception occurs during the
evaluation process; exceptions are of the class `exceptions.MetapypeRuleError`.

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

This `access_rule` example demonstrates the use of all three rule sections: 1)
The node-specific constraint validates the value of a specific node attribute.
In this case, the `order` attribute, if defined, must have a value of either
`allowFirst` or `denyFirst` only. 2) The descendant children section defines a
single node choice of either an `allow` or `deny` child, along with
the cardinality of 1 to infinity. And finally, 3) the allowable attributes
rule defines the set of acceptable attributes to be `id`, `system`, `order`,
and `authSystem`; all defined attributes are *optional* with the exception of
`authSystem`, which is *required*.

### Using Metapype for EML

The Metapype Python API can be used to generate metadata that is compliant with
the Ecological Metadata Language standard. Using Metapype for this purpose is
typically separated into two steps: first, build a Metapype model instance
beginning wtih an "eml" node as the *root* node, followed by validating the
model instance to ensure it complies with the EML standard. Validation can be
performed on a single node using the `validate.node` function or on an entire
model tree beginning with a specified *root* node using the `validate.tree`
function. The following code example demonstrates these two steps:

```Python
from metapype.eml2_1_1.exceptions import MetapypeRuleError
import metapype.eml2_1_1.names as names
import metapype.eml2_1_1.validate as validate
from metapype.model.node import Node

def main():

    eml = Node(names.EML)
    eml.add_attribute('packageId', 'edi.23.1')
    eml.add_attribute('system', 'metapype')

    access = Node(names.ACCESS, parent=eml)
    access.add_attribute('authSystem', 'pasta')
    access.add_attribute('order', 'allowFirst')
    eml.add_child(access)

    allow = Node(names.ALLOW, parent=access)
    access.add_child(allow)

    principal = Node(names.PRINCIPAL, parent=allow)
    principal.content = 'uid=gaucho,o=EDI,dc=edirepository,dc=org'
    allow.add_child(principal)

    permission = Node(names.PERMISSION, parent=allow)
    permission.content = 'all'
    allow.add_child(permission)

    dataset = Node(names.DATASET, parent=eml)
    eml.add_child(dataset)

    title = Node(names.TITLE, parent=dataset)
    title.content = 'Green sea turtle counts: Tortuga Island 20017'
    dataset.add_child(title)

    creator = Node(names.CREATOR, parent=dataset)
    dataset.add_child(creator)

    individualName_creator = Node(names.INDIVIDUALNAME, parent=creator)
    creator.add_child(individualName_creator)

    surName_creator = Node(names.SURNAME, parent=individualName_creator)
    surName_creator.content = 'Gaucho'
    individualName_creator.add_child(surName_creator)

    contact = Node(names.CONTACT, parent=dataset)
    dataset.add_child(contact)

    individualName_contact = Node(names.INDIVIDUALNAME, parent=contact)
    contact.add_child(individualName_contact)

    surName_contact = Node(names.SURNAME, parent=individualName_contact)
    surName_contact.content = 'Gaucho'
    individualName_contact.add_child(surName_contact)

    try:
        validate.tree(eml)
    except  MetapypeRuleError as e:
        logger.error(e)

   return 0

if __name__ == "__main__":
    main()

``` 

In the above example, the "eml" node is created and used as the anchor node for the root of the model tree. Sub-element descendant nodes are created and then added to higher-level nodes as children. Although this example is quite small, it does produce metadata that conforms to EML 2.1.1 standard.

Metapype can convert a model instance tree to either EML-specific *XML* or to
*JSON* Unicode strings by using either the `export.to_xml` or `io.to_json`
functions, respectively. The string value can then be saved directly to the file
system or passed to other functions for additional processing. Metapype can also
convert a Metapype valid JSON Unicode string back into a model instance tree by
using the `io.from_json` function. This is important for saving incomplete or
sub-tree instances to the file system (e.g., for reusable model components),
which can be reloaded at a later time. The following code example demonstrates
using both the *XML* and *JSON* functions:

```Python
import json
import metapype.eml_2_1_1.export
import metapype.model.io

# Write EML XML
xml_str = metapype.eml2_1_1.export.to_xml(eml)
with open('test_eml.xml', 'w') as f:
    f.write(xml_str)

# Write JSON
json_str = metapype.model.io.to_json(eml)
with open('test_eml.json', 'w') as f:
    f.write(json_str)

# Read JSON
with open('test_eml.json', 'r') as f:
    json_str = f.read()
eml = metapype.model.io.from_json(json.loads(json_str))

```

<hr/>

\*Actually, the metadata content model may contain any hierarchical content that
can be entered into the existing Node data structure, but will not validate as
an EML metadata content model either at the node or the tree level.