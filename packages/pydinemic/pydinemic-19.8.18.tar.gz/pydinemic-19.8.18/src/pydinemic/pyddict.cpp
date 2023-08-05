/**
Copyright (c) 2016-2019 cloudover.io ltd.

Licensee holding a valid commercial license for dinemic library may use it with
accordance to terms of the license agreement between cloudover.io ltd. and the
licensee, or on GNU Affero GPL v3 license terms.

Licensee not holding a valid commercial license for dinemic library may use it
under GNU Affero GPL v3 license.

Terms of GNU Affero GPL v3 license are available on following site:
https://www.gnu.org/licenses/agpl-3.0.en.html
*/

#include "pyddict.h"

#define PREPARE_MODELS Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL, NULL);   \
    Dinemic::DModel *caller = NULL;                                                         \
    if (get_caller_id() != "") {                                                            \
        caller = new Dinemic::DModel(get_caller_id(), py_store, py_sync, NULL, NULL);       \
        model.set_caller(caller);                                                           \
    }

#define CLEANUP_MODELS if (caller != NULL) delete caller;

using namespace std;

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

string PyDDict::get_caller_id() {
    // Get object_id property of this field. Should be set by map_fields of
    // PyDModel class, which is called by each constructor
    PyObject *caller_id = PyObject_GetAttrString(self, "_caller_id");
    if (!caller_id)
        throw Dinemic::DException(string("Caller_id is not set for this field ") + name);

    // Convert value of object to ascii string
    PyObject *caller_id_unicode = PyUnicode_AsASCIIString(caller_id);
    if (!caller_id_unicode)
        throw Dinemic::DException("Failed to decode unicode object id");

    // Convert Ascii string to std::string
    string caller_id_str = PyBytes_AsString(caller_id_unicode);

    // Release python objects
    Py_XDECREF(caller_id_unicode);
    Py_XDECREF(caller_id);

    return caller_id_str;
}

string PyDDict::get_my_id() {
    // Get object_id property of this field. Should be set by map_fields of
    // PyDModel class, which is called by each constructor
    PyObject *object_id = PyObject_GetAttrString(self, "_object_id");
    if (!object_id)
        throw Dinemic::DException(string("Object_id is not set for this field ") + name);

    // Convert value of object to ascii string
    PyObject *object_id_unicode = PyUnicode_AsASCIIString(object_id);
    if (!object_id_unicode)
        throw Dinemic::DException("Failed to decode unicode object id");

    // Convert Ascii string to std::string
    string object_id_str = PyBytes_AsString(object_id_unicode);

    // Release python objects
    Py_XDECREF(object_id_unicode);
    Py_XDECREF(object_id);

    return object_id_str;
}
