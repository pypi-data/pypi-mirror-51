#include "pydlist.h"
#include "pydmodel.h"

using namespace std;

PyDList::PyDList(PyObject *self_ptr, const string &list_name, const bool &is_encrypted)
    : name(list_name),
      encrypted(is_encrypted),
      self(self_ptr)
{

}

PyDList::PyDList(PyObject *self_ptr, const PyDList &f)
    : name(f.name),
      encrypted(f.encrypted),
      self(self_ptr)
{

}

string PyDList::get_my_id() {
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

void PyDList::append(const string &value) {
    Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL);

    if (encrypted) {
        model.list_append(name, model.encrypt(value));
    } else {
        model.list_append(name, value);
    }
}

void PyDList::insert(long position, string value) {
    Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL);

    if (encrypted) {
        model.list_insert(name, position, model.encrypt(value));
    } else {
        model.list_insert(name, position, value);
    }
}

void PyDList::set(long position, string value) {
    Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL);

    if (encrypted) {
        model.list_set(name, position, model.encrypt(value));
    } else {
        model.list_set(name, position, value);
    }
}

void PyDList::del(long position) {
    Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL);
    model.list_delete(name, position);
}

long PyDList::length() {
    Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL);
    return model.list_length(name);
}

long PyDList::index(string value) {
    Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL);
    for (int i = 0; i < length(); i++) {
        string item;
        if (encrypted) {
            item = model.decrypt(model.list_at(name, i));
        } else {
            item = model.list_at(name, i);
        }
        if (item == value) {
            return i;
        }
    }
    return -1;
}

string PyDList::at(long index) {
    Dinemic::DModel model(get_my_id(), py_store, py_sync, NULL);
    if (encrypted) {
        return model.decrypt(model.list_at(name, index));
    } else {
        return model.list_at(name, index);
    }
}
