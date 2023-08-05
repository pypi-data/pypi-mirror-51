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

#ifndef PYDMODEL_H
#define PYDMODEL_H

#include <string>
#include <boost/python.hpp>
#include <libdinemic/dmodel.h>
#include <libdinemic/store/redisdriver.h>
#include <libdinemic/sync/zeromqsync.h>

#include "module.h"

struct PyDModel
{
    PyObject *self;
    Dinemic::DModel obj;
    Dinemic::DModel *caller;

    PyDModel(PyObject *self_ptr, std::string model_name, boost::python::list authorized_objects);
    PyDModel(PyObject *self_ptr, std::string db_id, std::string caller_id);
    PyDModel(PyObject *self_ptr, std::string db_id);
    PyDModel(PyObject *self_ptr, const PyDModel &o);

    std::string get_id();
    std::string get_db_id();
    std::string get_model();

    std::vector<std::string> object_list_owned(std::string filter="");
    std::vector<std::string> object_list(std::string filter="");

    void set(std::string key, std::string value);
    std::string get(std::string key, std::string default_value="");
    void del(std::string key);

    std::string encrypt(const std::string &value);
    std::string decrypt(const std::string &value);

    /// Map all fields from derived classes to instance of this object. Crypto-
    /// graphic credentials of this object will be used to encrypt/devrypt
    /// data of the field. This method is used only internally, by PyDModel
    void map_fields();
};

#endif // PYDMODEL_H
