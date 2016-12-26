/*******************************************************************************
 * 1. Make sure the path to Graghviz include library is on your system path
 *    "C:/Program Files (x86)/Graphviz2.38/include"
 * 2. Extension procedure is slightly different for Py2 and Py3 so uncomment
 *    #define PY3 for use with Py3
 * 3. Call gvFreeLayout() BEFORE GRAPH MODIFICATIONS (add, delete nodes/edges)
 *    otherwise the module crashes
 ******************************************************************************/

#include <stdio.h>     // for printf
#include <iostream>    // cout
#include <fcntl.h>
#include <Python.h>
#include "graphviz/gvc.h"
#include "graphviz/types.h"

//#define PY3
#define MODULE_NAME "gvzpassage"
#define MODULEINIT_PY3(NAME) PyInit_ ## NAME(void)
#define MODULEINIT_PY2(NAME) init ## NAME(void)

/* non-exposed module variables */
GVC_t* gvc = gvContext();

/* non-exposed procedures */
static Agraph_t *retrieve_graph(PyObject *obj) {
    return (Agraph_t *) PyCapsule_GetPointer(obj, "Agraph");
}

static Agnode_t *retrieve_node(PyObject *obj) {
    return (Agnode_t *) PyCapsule_GetPointer(obj, "Agnode");
}

static Agedge_t *retrieve_edge(PyObject *obj) {
    return (Agedge_t *) PyCapsule_GetPointer(obj, "Agedge");
}

static GVC_t *retrieve_GVC(PyObject *obj) {
    return (GVC_t *) PyCapsule_GetPointer(obj, "GVC");
}

/* core procedures here */
static PyObject *wrap_agraphnew(PyObject *self, PyObject *args, PyObject *kwargs) {
    Agraph_t *ag;
    char* name;
    static char* kwlist[] = {"name", "directed", NULL};
    int directed = 0;
    Agdesc_t gtype;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|b", kwlist, &name, &directed))
        return NULL;
    gtype = Agstrictdirected;
    /* Shitty bug: all Agdesc_t variables are THE SAME...
       therefore will set individual bits manually */
    if (directed == 1) {
        gtype.directed = 1;}
    else {
        gtype.directed = 0;}
    ag = agopen(name, gtype, 0);
    return PyCapsule_New(ag, "Agraph", NULL);
}

static PyObject *wrap_addNode(PyObject *self, PyObject *args) {
    PyObject* gra_ptr;
    char* label;
    Agraph_t* ag;
    Agnode_t* node;
    if (!PyArg_ParseTuple(args, "Os", &gra_ptr, &label)) {
        return NULL;
    }
    if (!(ag = retrieve_graph(gra_ptr))) {
        return NULL;
    }
    gvFreeLayout(gvc, ag);
    node = agnode(ag, label, 1);
    return PyCapsule_New(node, "Agnode", NULL);
}

static PyObject *wrap_addEdge(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject* gra_ptr;
    PyObject* node1_ptr;
    PyObject* node2_ptr;
    char* label = "";
    Agraph_t* ag;
    Agnode_t* node1;
    Agnode_t* node2;
    Agedge_t* edge;
    static char* kwlist[] = {"graph", "node1", "node2", "label", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO|s", kwlist, &gra_ptr, &node1_ptr, &node2_ptr, &label))
        return NULL;
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    if (!(node1 = retrieve_node(node1_ptr)))
        return NULL;
    if (!(node2 = retrieve_node(node2_ptr)))
        return NULL;
    edge = agedge(ag, node1, node2, label, 1);
    return PyCapsule_New(edge, "Agedge", NULL);
}

static PyObject *wrap_layout(PyObject *self, PyObject *args) {
    PyObject* gra_ptr;
    Agraph_t* ag;
    if (!PyArg_ParseTuple(args, "O", &gra_ptr))
        return NULL;
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    gvLayout(gvc, ag, "dot");
    boxf bbox = GD_bb(ag);
    double LLx = bbox.LL.x;
    double LLy = bbox.LL.y;
    double URx = bbox.UR.x;
    double URy = bbox.UR.y;
    return Py_BuildValue("{sdsdsdsd}", "LLx", LLx,
                                       "LLy", LLy,
                                       "URx", URx,
                                       "URy", URy);
}

static PyObject *node_geometry(PyObject *self, PyObject *args) {
    PyObject* node_ptr;
    Agnode_t* node;
    if (!PyArg_ParseTuple(args, "O", &node_ptr)) {
        return NULL;
    }
    if (!(node = retrieve_node(node_ptr))) {
        return NULL;
    }
    pointf center = ND_coord(node);
    double x = center.x;
    double y = center.y;
    double width = ND_width(node);
    double height = ND_height(node);
    char* shape = ND_shape(node)->name;
    return Py_BuildValue("{sdsdsdsdss}", "centerX", x,
                                         "centerY", y,
                                         "width", width,
                                         "height", height,
                                         "shape", shape);
}

static PyObject *edge_geometry(PyObject *self, PyObject *args) {
    PyObject* edge_ptr;  // to get incoming PyCapsule
    Agedge_t* edge;      // to retrieve Edge
    int i, j;            // iterate: i = splines; j = points of a spline
    splines* splines;    // collection of all splines of the edge
    PyObject* output;    // to return
    bezier spline;       // for each spline in splines
    PyObject* points;    // all points of a given spline
    pointf tochka;       // a point in points
    PyObject* sppoint;   // same, but in Py dictionary form
    pointf sarrowtip, earrowtip;  // start arrow tip and end arrow tip (see man)
    PyObject *sartpoint, *eartpoint;  // same, but in Py dictionary form
    PyObject* elem;      // ready-to-go spline structure
    /* argument (edge) gathering */
    if (!PyArg_ParseTuple(args, "O", &edge_ptr)) {
        return NULL;
    }
    if (!(edge = retrieve_edge(edge_ptr))) {
        return NULL;
    }
    /* geometry parsing */
    splines = ED_spl(edge);
    output = PyList_New(splines->size);
    for(i = 0; i < splines->size; i++) {
        spline = splines->list[i];
        points = PyList_New(spline.size);
        for(j = 0; j < spline.size; j++) {
            tochka = spline.list[j];
            sppoint = Py_BuildValue("{sdsd}", "x", tochka.x,
                                              "y", tochka.y);
            PyList_SET_ITEM(points, j, sppoint);
        }
        sarrowtip = spline.sp;
        sartpoint = Py_BuildValue("{sdsd}", "x", sarrowtip.x,
                                            "y", sarrowtip.y);
        earrowtip = spline.ep;
        eartpoint = Py_BuildValue("{sdsd}", "x", earrowtip.x,
                                            "y", earrowtip.y);
        elem = Py_BuildValue("{sOsisisOsO}", "points", points,
                                             "sflag", spline.sflag,
                                             "eflag", spline.eflag,
                                             "sarrowtip", sartpoint,
                                             "earrowtip", eartpoint);
        PyList_SET_ITEM(output, i, elem);
    }
    return output;
}

static PyObject *delete_node(PyObject *self, PyObject *args) {
    /* Warning! Delete edges first! */
    PyObject* gra_ptr;
    PyObject* node_ptr;
    Agraph_t* ag;
    Agnode_t* node;
    int result;
    if (!PyArg_ParseTuple(args, "OO", &gra_ptr, &node_ptr)) {
        return NULL;
    }
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    if (!(node = retrieve_node(node_ptr))) {
        return NULL;
    }
    result = agdelete(ag, node);
    return Py_BuildValue("i", result);
}

static PyObject *delete_edge(PyObject *self, PyObject *args) {
    PyObject* gra_ptr;
    PyObject* edge_ptr;
    Agraph_t* ag;
    Agedge_t* edge;
    int result;
    if (!PyArg_ParseTuple(args, "OO", &gra_ptr, &edge_ptr)) {
        return NULL;
    }
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    if (!(edge = retrieve_edge(edge_ptr))) {
        return NULL;
    }
    result = agdelete(ag, edge);
    return Py_BuildValue("i", result);
}

static PyObject *stdout_graph(PyObject *self, PyObject *args) {
    PyObject* gra_ptr;
    Agraph_t* ag;
    if (!PyArg_ParseTuple(args, "O", &gra_ptr)) {
        return NULL;
    }
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    agwrite(ag, stdout);
    Py_RETURN_NONE;
}

static PyObject *wrap_nodeshape(PyObject *self, PyObject *args) {
    PyObject* gra_ptr;
    char* value;
    Agraph_t* ag;
    Agsym_t *sym;
    if (!PyArg_ParseTuple(args, "Os", &gra_ptr, &value)) {
        return NULL;
    }
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    sym = agattr(ag, AGNODE, "shape", value);
    Py_RETURN_NONE;
}

static PyObject *wrap_nodelabel(PyObject *self, PyObject *args) {
    PyObject* node_ptr;
    Agnode_t* node;
    textlabel_t* label;
    if (!PyArg_ParseTuple(args, "O", &node_ptr)) {
        return NULL;
    }
    if (!(node = retrieve_node(node_ptr))) {
        return NULL;
    }
    label = ND_label(node);
    return Py_BuildValue("s", label->text);
}

static PyObject *wrap_agclose(PyObject *self, PyObject *args) {
    PyObject* gra_ptr;
    Agraph_t* ag;
    if (!PyArg_ParseTuple(args, "O", &gra_ptr)) {
        return NULL;
    }
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    agclose(ag);
    Py_RETURN_NONE;
}

/* Methods registration */
static PyMethodDef module_methods[] = {
    {"agraphNew", (PyCFunction)wrap_agraphnew, METH_VARARGS | METH_KEYWORDS, "Creates new Agraph"},
    {"addNode", wrap_addNode, METH_VARARGS, "Add a new node"},
    {"addEdge", (PyCFunction)wrap_addEdge, METH_VARARGS | METH_KEYWORDS, "Add a new edge"},
    {"layout", wrap_layout, METH_VARARGS, "Create layout"},
    {"node_geometry", node_geometry, METH_VARARGS, "Gets node geometry after layout"},
    {"edge_geometry", edge_geometry, METH_VARARGS, "Gets edge geometry after layout"},
    {"delete_node", delete_node, METH_VARARGS, "Delete node. Warning! Delete edges first"},
    {"delete_edge", delete_edge, METH_VARARGS, "Delete edge"},
    {"stdout_graph", stdout_graph, METH_VARARGS, "Writes graph text to stdout"},
    {"set_shape_nodes", wrap_nodeshape, METH_VARARGS, "Sets a default shape for nodes"},
    {"node_label", wrap_nodelabel, METH_VARARGS, "Gets node label"},
    {"agraphClose", wrap_agclose, METH_VARARGS, "Closes the graph"},
    {NULL, NULL, 0, NULL}
};

/* New to Python 3: module description structure */
#ifdef PY3
    static struct PyModuleDef thismodule = {
       PyModuleDef_HEAD_INIT,
       MODULE_NAME,          /* name of module */
       NULL, /* module documentation, may be NULL */
       -1,               /* size of per-interpreter state of the module, */
                      /* or -1 if the module keeps state in global variables. */
       module_methods
    };
#endif

/* When Python imports a C module named 'X' it loads the module */
/* then looks for a method named "PyInit_"+X and calls it.  Hence */
/* for the module "djhuj" the initialization function is */
/* "PyInit_djhuj".  The PyMODINIT_FUNC helps with portability */
/* across operating systems and between C and C++ compilers */
PyMODINIT_FUNC
#ifdef PY3
    /* For Python 3*/
     PyInit_gvzpassage(void)
#else
    /* For Python 2 */
     initgvzpassage(void)
#endif
{
#ifdef PY3
    return PyModule_Create(&thismodule);
#else
    (void) Py_InitModule3(MODULE_NAME, module_methods, "Capsule pointers demo");
#endif
}
