<html><head><meta http-equiv="content-type" content="text/html; charset=UTF-8"></head><body>
<h1 style="margin:1.3em 0 1em;padding:0;font-weight:bold;font-size:1.6em;border-bottom:1pt solid #ddd;">Metapype for EML</h1>
<h4 style="margin:1.0em 0 1em;padding:0;font-weight:bold;font-size:1.3em;">A light weight metadata generator for the Ecological Metadata Language</h4>
<hr />
<p style="margin:1.2em 0;">Metapype is a Python 3 library for building, saving, and exporting
scientific metadata using a flexible metadata content model in a
hierarchical tree-like structure. This version of Metapype is designed
to reflect the content structure of the Ecological Metadata Lanaguage
(EML) XML schema, but is not locked into a specific version of EML.</p>
<p style="margin:1.2em 0;">Metapype is divided into a metadata content model and a set of rules that
enforces compliance to a specific standard. The content model can function
fully independent of compliance rules, but cannot perform node or tree
validation.</p>
<h3 style="margin:1.0em 0 1em;padding:0;font-weight:bold;font-size:1.4em;">Metadata Content Model</h3>
<p style="margin:1.2em 0;">The metadata content model is designed as a hierarchical directed graph with a
root node that spans the tree's children using directional links; similarly,
each child node contains a reverse link to its parent (or root) node. Only the
root node may be without parent link. Node links for either parent or children
are constructed of the nodes respective address in memory. Nodes represent the
primary characteristics of their corresponding XML schema elements, including
attributes, content, and children. Node instances must be generated with at
least the corresponding &quot;rank&quot; name as found in the schema <sup id="fnref-1"><a class="footnote-ref" href="#fn-1">1</a></sup>. All other
content may be accessed through setters and getters.</p>
<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/node.png" /></p>
<p style="margin:1.2em 0;">A complete and compliant EML 2.1.1 tree, albeit not too informative, is found in
the following diagram:</p>
<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/metapype-eml/master/docs/eml_model.png"/></p>
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
      the node or the tree level.