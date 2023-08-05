#include "pyddict.h"

PyDDict::PyDDict(PyObject *self_ptr, const string &list_name, const bool &is_encrypted)
    : name(list_name),
      encrypted(is_encrypted),
      self(self_ptr)
{

}

PyDDict::PyDDict(PyObject *self_ptr, const PyDDict &f)
    : name(f.name),
      encrypted(f.encrypted),
      self(self_ptr)
{

}

string PyDDict::get_my_id() {
    // Get object_id property of this field. Should be set by map_fields of
    // PyDModel class, which is called by each constructor
    PyObject *object_id = PyObject_GetAttrString(self, "object_id");
    if (!object_id)
        throw Dinemic::DException(string("Object_id is not set for this field ") + name);

    // Convert value of object to ascii string
    PyObject *object_id_unicode = PyUnicode_AsASCIIString(object_id);
    if (!object_id)
        throw Dinemic::DException("Failed to decode unicode object id");

    // Convert Ascii string to std::string
    string object_id_str = PyBytes_AsString(object_id_unicode);

    // Release python objects
    Py_XDECREF(object_id_unicode);
    Py_XDECREF(object_id);

    return object_id_str;
}
