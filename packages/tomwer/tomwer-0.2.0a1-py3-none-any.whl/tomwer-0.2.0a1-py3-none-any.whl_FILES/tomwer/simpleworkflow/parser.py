
__authors__ = ["Bioinformatics Laboratory, University of Ljubljana", "H.Payno"]
__license__ = "[GNU GPL v3+]: https://www.gnu.org/licenses/gpl-3.0.en.html"
__date__ = "29/05/2017"


import sys
from xml.etree.ElementTree import parse
from collections import namedtuple
import ast
from ast import literal_eval
import importlib
import logging
import pickle
import base64
from .scheme import (_GUIFreeScheme, _GUIFreeNode)

logger = logging.getLogger(__name__)

WIDGETS_TO_CORE_PROC = {
    '.widgets.FtseriesWidget.FtseriesWidget': '.core.ftseries.Ftseries.FtseriesP',
    '.widgets.FolderTransfertWidget.FolderTransfertWidget': '.core.FolderTransfert.FolderTransfertP',
    '.widgets.ScanListWidget.ScanListWidget': '.core.ScanList.ScanListP',
    '.widgets.ScanValidatorWidget.ScanValidatorWidget': '.core.ScanValidator.ScanValidatorP',
    '.widgets.TomoDirWidget.TomoDirWidget': '.core.tomodir.TomoDir.TomoDirP'
}

"""This is a dictionnary to convert an OrangeWidget into a core process.
"""

IGNORED_WIDGETS = [
    'orangecontrib.tomwer.widgets.ImageStackViewerWidget.ImageStackViewerWidget'
]

"""Some widget are only used for visualization, and will be ignored"""

def scheme_load(scheme, stream, error_handler=None):
    desc = parse_ows_stream(stream)

    if error_handler is None:
        def error_handler(exc):
            raise exc

    nodes = []
    nodes_by_id = {}
    links = []

    scheme.title = desc.title
    scheme.description = desc.description

    for node_d in desc.nodes:
        node = _GUIFreeNode(id=node_d.id)
        data = node_d.data
        # properties = loads(data.data, data.format)
        properties = loads(data.data, data.format)
        node.properties = properties
        if ('.widgets.' in node_d.qualified_name):
            new_qualified_name = node_d.qualified_name
            if new_qualified_name in IGNORED_WIDGETS:
                # skip the widget creation
                continue

            for equ in WIDGETS_TO_CORE_PROC:
                if new_qualified_name.endswith(equ):
                    new_qualified_name = new_qualified_name.replace(equ,
                                                                    WIDGETS_TO_CORE_PROC[equ])

            sname = new_qualified_name.rsplit('.')
            assert(len(sname) > 1)
            assert('orangecontrib' == sname[0])
            del sname[0]
            class_name = sname[-1]
            del sname[-1]
            module_name = '.'.join(sname)
            m = importlib.import_module(module_name)
            p = getattr(m, class_name)
            cla = p()
            cla.setProperties(properties)
            cla._scheme_title = desc.title
            nodes_by_id[node_d.id] = cla
        else:
            raise ValueError('not recognized widget')

    for link_d in desc.links:
        source_id = link_d.source_node_id
        sink_id = link_d.sink_node_id
        handler = None
        for slot in nodes_by_id[sink_id].inputs:
            if link_d.sink_channel == link_d.sink_channel:
                handler = slot['handler']
                continue

        if handler is None:
            raise ValueError('no slot found for ...')

        signal = getattr(nodes_by_id[source_id], link_d.source_channel)
        slot = getattr(nodes_by_id[sink_id], handler)
        signal.connect(slot)

    scheme.node_by_id = nodes_by_id
    scheme.links = desc.links

    return scheme


def loads(string, format):
    if format == "literal":
        return literal_eval(string)
    elif format == "json":
        return json.loads(string)
    elif format == "pickle":
        return pickle.loads(base64.decodebytes(string.encode('ascii')))
    else:
        raise ValueError("Unknown format")

# ---- TAKE back from Orange3 ---------

_scheme = namedtuple(
    "_scheme",
    ["title", "version", "description", "nodes", "links", "annotations"])

_node = namedtuple(
    "_node",
    ["id", "title", "name", "position", "project_name", "qualified_name",
     "version", "data"])

_data = namedtuple(
    "_data",
    ["format", "data"])

_link = namedtuple(
    "_link",
    ["id", "source_node_id", "sink_node_id", "source_channel", "sink_channel",
     "enabled"])

_annotation = namedtuple(
    "_annotation",
    ["id", "type", "params"])

_text_params = namedtuple(
    "_text_params",
    ["geometry", "text", "font"])

_arrow_params = namedtuple(
    "_arrow_params",
    ["geometry", "color"])


def tuple_eval(source):
    """
    Evaluate a python tuple literal `source` where the elements are
    constrained to be int, float or string. Raise ValueError if not
    a tuple literal.

    >>> tuple_eval("(1, 2, "3")")
    (1, 2, '3')

    """
    node = ast.parse(source, "<source>", mode="eval")

    if not isinstance(node.body, ast.Tuple):
        raise ValueError("%r is not a tuple literal" % source)

    if not all(isinstance(el, (ast.Str, ast.Num)) or
               # allow signed number literals in Python3 (i.e. -1|+1|-1.0)
               (isinstance(el, ast.UnaryOp) and
                isinstance(el.op, (ast.UAdd, ast.USub)) and
                isinstance(el.operand, ast.Num))
               for el in node.body.elts):
        raise ValueError("Can only contain numbers or strings")

    return literal_eval(source)


def parse_ows_etree_v_2_0(tree):
    scheme = tree.getroot()
    nodes, links, annotations = [], [], []

    # First collect all properties
    properties = {}
    for property in tree.findall("node_properties/properties"):
        node_id = property.get("node_id")
        format = property.get("format")
        if "data" in property.attrib:
            data = property.get("data")
        else:
            data = property.text
        properties[node_id] = _data(format, data)

    # Collect all nodes
    for node in tree.findall("nodes/node"):
        node_id = node.get("id")
        node = _node(
            id=node_id,
            title=node.get("title"),
            name=node.get("name"),
            position=tuple_eval(node.get("position")),
            project_name=node.get("project_name"),
            qualified_name=node.get("qualified_name"),
            version=node.get("version", ""),
            data=properties.get(node_id, None)
        )
        nodes.append(node)

    for link in tree.findall("links/link"):
        params = _link(
            id=link.get("id"),
            source_node_id=link.get("source_node_id"),
            sink_node_id=link.get("sink_node_id"),
            source_channel=link.get("source_channel"),
            sink_channel=link.get("sink_channel"),
            enabled=link.get("enabled") == "true",
        )
        links.append(params)

    for annot in tree.findall("annotations/*"):
        if annot.tag == "text":
            rect = tuple_eval(annot.get("rect", "(0.0, 0.0, 20.0, 20.0)"))

            font_family = annot.get("font-family", "").strip()
            font_size = annot.get("font-size", "").strip()

            font = {}
            if font_family:
                font["family"] = font_family
            if font_size:
                font["size"] = int(font_size)

            annotation = _annotation(
                id=annot.get("id"),
                type="text",
                params=_text_params(rect, annot.text or "", font),
            )
        elif annot.tag == "arrow":
            start = tuple_eval(annot.get("start", "(0, 0)"))
            end = tuple_eval(annot.get("end", "(0, 0)"))
            color = annot.get("fill", "red")
            annotation = _annotation(
                id=annot.get("id"),
                type="arrow",
                params=_arrow_params((start, end), color)
            )
        annotations.append(annotation)

    return _scheme(
        version=scheme.get("version"),
        title=scheme.get("title", ""),
        description=scheme.get("description"),
        nodes=nodes,
        links=links,
        annotations=annotations
    )


def parse_ows_stream(stream):
    doc = parse(stream)
    scheme_el = doc.getroot()
    version = scheme_el.get("version", None)
    if version is None:
        # Fallback: check for "widgets" tag.
        if scheme_el.find("widgets") is not None:
            version = "1.0"
        else:
            log.warning("<scheme> tag does not have a 'version' attribute")
            version = "2.0"

    if version == "1.0":
        return parse_ows_etree_v_1_0(doc)
    elif version == "2.0":
        return parse_ows_etree_v_2_0(doc)
    else:
        raise ValueError()


def resolve_replaced(scheme_desc, registry):
    widgets = registry.widgets()
    nodes_by_id = {}  # type: Dict[str, _node]
    replacements = {}
    replacements_channels = {}  # type: Dict[str, Tuple[dict, dict]]
    # collect all the replacement mappings
    for desc in widgets:  # type: WidgetDescription
        if desc.replaces:
            for repl_qname in desc.replaces:
                replacements[repl_qname] = desc.qualified_name

        input_repl = {}
        for idesc in desc.inputs or []:  # type: InputSignal
            for repl_qname in idesc.replaces or []:  # type: str
                input_repl[repl_qname] = idesc.name
        output_repl = {}
        for odesc in desc.outputs:  # type: OutputSignal
            for repl_qname in odesc.replaces or []:  # type: str
                output_repl[repl_qname] = odesc.name
        replacements_channels[desc.qualified_name] = (input_repl, output_repl)

    # replace the nodes
    nodes = scheme_desc.nodes
    for i, node in list(enumerate(nodes)):
        if not registry.has_widget(node.qualified_name) and \
                node.qualified_name in replacements:
            qname = replacements[node.qualified_name]
            desc = registry.widget(qname)
            nodes[i] = node._replace(qualified_name=desc.qualified_name,
                                     project_name=desc.project_name)
        nodes_by_id[node.id] = nodes[i]

    # replace links
    links = scheme_desc.links
    for i, link in list(enumerate(links)):  # type: _link
        nsource = nodes_by_id[link.source_node_id]
        nsink = nodes_by_id[link.sink_node_id]

        _, source_rep = replacements_channels.get(
            nsource.qualified_name, ({}, {}))
        sink_rep, _ = replacements_channels.get(
            nsink.qualified_name, ({}, {}))

        if link.source_channel in source_rep:
            link = link._replace(
                source_channel=source_rep[link.source_channel])
        if link.sink_channel in sink_rep:
            link = link._replace(
                sink_channel=sink_rep[link.sink_channel])
        links[i] = link

    return scheme_desc._replace(nodes=nodes, links=links)


def main(ows_file):
    scheme = _GUIFreeScheme()
    with open(ows_file, "rb") as f:
        scheme_load(scheme, f)

    scheme.node_by_id['0'].start()


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].lower().endswith('.ows'):
        raise ValueError('need a .ows file to process the scheme')

    main(sys.argv[1])
