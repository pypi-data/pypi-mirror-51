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

#include "module.h"

using namespace boost::python;
using namespace std;

Dinemic::Sync::SyncInterface *py_sync = NULL;
Dinemic::Store::StoreInterface *py_store = NULL;

void launch() {
    py_store = new Dinemic::Store::RedisDriver();
    py_sync = new Dinemic::Sync::ZeroMQSync(py_store);
    py_sync->start_agent();
}

void shutdown() {
    py_sync->stop_agent();
}

void dinemic_exception_to_py(Dinemic::DException const &x) {
    PyErr_SetString(PyExc_Exception, x.get_reason().c_str());
}


boost::python::list object_list(const std::string &filter) {
    boost::python::list r;

    for (std::string o : Dinemic::DModel::object_list(filter, py_store)) {
        r.append(o);
    }

    return r;
}

boost::python::list object_list_owned(const std::string &filter) {
    boost::python::list r;

    for (std::string o : Dinemic::DModel::object_list(filter, py_store)) {
        r.append(o);
    }

    return r;
}

void set_loglevel(string loglevel) {
    if (loglevel == "verbose")
        Dinemic::set_loglevel(Dinemic::loglevel_verbose);
    else if (loglevel == "debug")
        Dinemic::set_loglevel(Dinemic::loglevel_debug);
    else if (loglevel == "info")
        Dinemic::set_loglevel(Dinemic::loglevel_info);
    else if (loglevel == "error")
        Dinemic::set_loglevel(Dinemic::loglevel_error);
    else if (loglevel == "action")
        Dinemic::set_loglevel(Dinemic::loglevel_action);
    else if (loglevel == "none")
        Dinemic::set_loglevel(Dinemic::loglevel_none);
    else
        throw Dinemic::DException("Unknown loglevel");
}

namespace boost {
    namespace python {
        template <>
        struct has_back_reference<PyDModel>
          : boost::mpl::true_
        {};
        template <>
        struct has_back_reference<PyDField>
          : boost::mpl::true_
        {};
        template <>
        struct has_back_reference<PyDList>
          : boost::mpl::true_
        {};
        template <>
        struct has_back_reference<PyAction>
          : boost::mpl::true_
        {};
    }
}

BOOST_PYTHON_MODULE(pydinemic) {

    def("launch", &launch);
    def("shutdown", &launch);
    def("set_loglevel", &set_loglevel);
    def("object_list", &object_list);
    def("object_list_owned", &object_list_owned);

    register_exception_translator<Dinemic::DException>(dinemic_exception_to_py);

    class_ <PyDModel>("DModel", init<string, boost::python::list>(args("model_name", "authorized_object_ids"), "Create new object in Dinemic database with authorized objects"))
            .def(init<string, string>(args("db_id", "caller_id"), "Recreate existing in Dinemic database object, from given full dabtabase id"))
            .def("get_id", &PyDModel::get_id)
            .def("get_db_id", &PyDModel::get_db_id)
            .def("get_model", &PyDModel::get_model)
            .def("set", &PyDModel::set)
            .def("get", &PyDModel::get)
            .def("del", &PyDModel::del)
            .def("encrypt", &PyDModel::encrypt)
            .def("decrypt", &PyDModel::decrypt);
    class_<PyAction>("DAction", init<>("Inherit this class to create listener on certain changes being created in database. Use apply and revoke methods to set when listener should be called. For details check dinemic framework documentation.\n\n"
                     "Supported callbacks in DAction object is going to be created:\n"
                     " - on_create(object_id, key)\n"
                     "After object was created:\n"
                     " - on_created(object_id, key)\n"
                     " - on_owned_created(object_id, key)\n\n"
                     "Before field of object will be changed in local database:\n"
                     " - on_update(object_id, field, old_value, new_value)\n"
                     " - on_authorized_update(object_id, field, old_value, new_value)\n"
                     " - on_unauthorized_update(object_id, field, old_value, new_value)\n"
                     " - on_owned_update(object_id, field, old_value, new_value)\n\n"
                     "After field of object will be changed in local database:\n"
                     " - on_updated(object_id, field, old_value, new_value)\n"
                     " - on_authorized_updated(object_id, field, old_value, new_value)\n"
                     " - on_unauthorized_updated(object_id, field, old_value, new_value)\n"
                     " - on_owned_updated(object_id, field, old_value, new_value)\n\n"
                     "Before field will be removed:\n"
                     " - on_delete(object_id, field, value)\n"
                     " - on_authorized_delete(object_id, field, value)\n"
                     " - on_unauthorized_delete(object_id, field, value)\n"
                     " - on_owned_delete(object_id, field, value)\n\n"
                     "After field was removed from database:\n"
                     " - on_deleted(object_id, field, value)\n"
                     " - on_authorized_deleted(object_id, field, value)\n"
                     " - on_unauthorized_deleted(object_id, field, value)\n"
                     " - on_owned_deleted(object_id, field, value)\n\n"
                     "Before whole object is removed from local database:\n"
                     " - on_remove(object_id)\n"
                     " - on_authorized_remove(object_id)\n"
                     " - on_unauthorized_remove(object_id)\n"
                     " - on_owned_remove(object_id)\n\n"
                     "Changes signed by one of authorized keys will call *_authorized_* callbacks.\n"
                     "\n"
                     "Changes requested on locally owned objects (created on this machine, whichs private keys are available) will call *_owned_* callbacks."))
          .def("apply", &PyAction::py_apply)
          .def("revoke", &PyAction::py_revoke);
    class_<PyDField>("DField", init<string, bool>(args("field_name", "is_encrypted")))
          .def("set", &PyDField::set)
          .def("get", &PyDField::get);
    class_<PyDList>("DList", init<string, bool>(args("list_name", "is_encrypted")))
          .def("append", &PyDList::append)
          .def("at", &PyDList::at)
          .def("delete", &PyDList::del)
          .def("index", &PyDList::index)
          .def("insert", &PyDList::insert)
          .def("length", &PyDList::length)
          .def("set", &PyDList::set);
}
