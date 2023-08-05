#include <pybind11/pybind11.h>
#include <fwdpy11/types/Diploid.hpp>
#include <fwdpy11/genetic_values/GeneticValueToFitness.hpp>

void test_GSSmo_linkage(const fwdpy11::GSSmo & g)
{
    fwdpy11::DiploidMetadata m;
    g(m);
}


PYBIND11_MODULE(cpptests, m)
{
    pybind11::object o = (pybind11::object) pybind11::module::import("fwdpy11").attr("GSSmo");
    m.def("test_GSSmo_linkage",&test_GSSmo_linkage);
}
