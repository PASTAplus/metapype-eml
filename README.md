<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head><body>
<h1 style="margin:1.3em 0 1em;padding:0;font-weight:bold;font-size:1.6em;border-bottom:1pt solid #ddd;">Metapype for EML</h1>
<h4 style="margin:1.0em 0 1em;padding:0;font-weight:bold;font-size:1.3em;">A light weight metadata generator for the Ecological Metadata Language</h4>
<hr />
<p style="margin:1.2em 0;">Metapype is a Python 3 library for building, saving, and exporting
scientific metadata using a flexible metadata content model in a
hierarchical tree-like structure. This version of Metapype is designed
to reflect the content structure of the Ecological Metadata Lanaguage
(EML) XML schema, but is not locked into a specific version of EML.</p>
<p style="margin:1.2em 0;">Metapype is divided into a metadata content model and a set of conditional rules
that enforce model compliance to a specific metadata standard. The content model
is fully independent of the compliance rules, but cannot perform node or
tree validation without the rules; as such, they must operate together to serve
as a metadata generator.</p>
<h4 style="margin:1.0em 0 1em;padding:0;font-weight:bold;font-size:1.3em;">Metadata Content Model</h4>
<p style="margin:1.2em 0;">The metadata content model is designed as a hierarchical directed graph with a
root node that spans the tree's children using directional links; similarly,
each child node contains a reverse link to its parent (or root) node. Only the
root node may be without parent link. Node links for either parent or children
are constructed of the nodes respective address in memory. Nodes represent the
primary characteristics of their corresponding XML schema elements, including
attributes, content, and children. Node instances must be generated with at
least the corresponding &quot;rank&quot; name as found in the schema for binding to the
EML rule set<sup id="fnref-1"><a class="footnote-ref" href="#fn-1">1</a></sup>. All other node attributes may be accessed through setters and
getters.</p>
<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/node.png" /></p>
<p style="margin:1.2em 0;">A complete and compliant EML 2.1.1 metadata content model tree (albeit not too
informative) is found in the following diagram:</p>
<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/eml_model.png"/></p>
<h4 style="margin:1.0em 0 1em;padding:0;font-weight:bold;font-size:1.3em;">Metadata Standard Compliance Rules</h4>
<p style="margin:1.2em 0;">A metadata standard compliance rule is a codified set of constraints that follow
the same (or similar) constraints that are declared within the corresponding
metadata standard. In Metapype for EML, these rules are written in accordance
with the rank of the element definition as declared in the EML XML schema. Each
rule supports the presence of XML attributes, content, and if a &quot;complex&quot; XML
element, the sequence or choice of descendant elements, including descendant
cardinality (descendant elements are represented as children in the metadata
content model). Rules do not support all XML schema constructs (e.g., groups or
all).</p>
<p style="margin:1.2em 0;">Rules are broken into three parts: 1) zero or more rank specific rules (such as
a datatype constraint) or a context sensitive rule (such as allowing only an
enumerated set of choices); 2) an ordered list of allowable children and their
corresponding cardinality; and 3) an unordered list of allowable attributes and
whether they are required or optional.</p>
<p style="margin:1.2em 0;">A typical rule has the following Python code structure:</p>
<ol style="margin-left:1em;padding-left:0.5em;text-indent:0;">
  <li>Conditional statements</li>
  <li>Ordered list of lists (sublists are lists of children rank and cardinality)</li>
  <li>Dictionary of attributes</li>
</ol>
<p style="margin:1.2em 0;">There is a processing step after sections 2 and 3, respectively, that evaluates
model node for rule compliance. Not all rules have the three sections described
above. The following is an example of the &quot;access&quot; rule:</p>
<pre style="font-family:Consolas,Inconsolata,Courier,monospace;font-size:1em;line-height:1.3em;margin:1.2em 0;"><code class="Python" style="background-color:#f8f8f8;border-radius:3px;border:1px solid #ccc;display:block;font-family:Consolas,Inconsolata,Courier,monospace;font-size:0.9em;margin:0 0.15em;overflow:auto;padding:0.5em 0.7em;white-space:pre;color:#444;">def access_rule(node: Node):
    if 'order' in node.attributes:
        allowed = ['allowFirst', 'denyFirst']
        if node.attributes['order'] not in allowed:
            msg = '&quot;{0}:order&quot; attribute must be one of &quot;{1}&quot;'.format(node.rank, allowed)
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
</code></pre>
<div class="footnotes">
  <hr />
  <ol>
    <li id="fn-1">
      <p style="margin:1.2em 0;">Actually, the metadata content model may contain any hierarchical
      content that can be entered into the existing Node data structure,
      but will not validate as an EML metadata content model either at
      the node or the tree level.</p>
      <a href="#fnref-1" class="footnote-backref">&#8617;</a>
    </li>
  </ol>
</div>

</body></html>
