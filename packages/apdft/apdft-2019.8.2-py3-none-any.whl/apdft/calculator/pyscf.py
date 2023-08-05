#!/usr/bin/env python

import basis_set_exchange as bse
import apdft.calculator as apc
import os
import jinja2 as j
import numpy as np
from apdft import log


class PyscfCalculator(apc.Calculator):
    _methods = {"CCSD": "CCSD", "HF": "HF"}

    @staticmethod
    def _format_coordinates(nuclear_numbers, coordinates):
        """ Converts the vector representation into the atomspec format for PySCF."""
        ret = []
        for z, pos in zip(nuclear_numbers, coordinates):
            ret.append("%d %f %f %f" % (z, *pos))
        return ";".join(ret)

    @staticmethod
    def _format_basis(nuclear_numbers):
        basis = {}
        for nuclear_number in set(nuclear_numbers):
            basis[nuclear_number] = bse.get_basis("6-31G", "N", fmt="nwchem")
        return str(basis)

    @staticmethod
    def _format_list(values):
        return ",".join([str(_) for _ in values])

    def get_input(
        self, coordinates, nuclear_numbers, nuclear_charges, grid, iscomparison=False
    ):
        basedir = os.path.dirname(os.path.abspath(__file__))
        with open("%s/templates/pyscf.py" % basedir) as fh:
            template = j.Template(fh.read())

        env = {}
        env["atoms"] = PyscfCalculator._format_coordinates(nuclear_numbers, coordinates)
        env["basisset"] = PyscfCalculator._format_basis(nuclear_numbers)
        env["includeonly"] = PyscfCalculator._format_list(range(len(nuclear_numbers)))
        env["deltaZ"] = PyscfCalculator._format_list(
            np.array(nuclear_charges) - np.array(nuclear_numbers)
        )
        env["method"] = self._methods[self._method]
        return template.render(**env)

    @staticmethod
    def _read_value(folder, label, multiple):
        lines = open("%s/run.log" % folder).readlines()
        res = []
        for line in lines:
            parts = line.strip().split()
            if parts[0] == label:
                res.append([float(_) for _ in parts[1:]])
                if not multiple:
                    return np.array(res[0])
        return np.array(res)

    @staticmethod
    def get_total_energy(folder):
        return PyscfCalculator._read_value(folder, "TOTAL_ENERGY", False)

    def get_runfile(self, coordinates, nuclear_numbers, nuclear_charges, grid):
        basedir = os.path.dirname(os.path.abspath(__file__))
        with open("%s/templates/pyscf-run.sh" % basedir) as fh:
            template = j.Template(fh.read())
        return template.render()

    @staticmethod
    def get_epn(folder, coordinates, includeatoms, nuclear_charges):
        epns = PyscfCalculator._read_value(folder, "ELECTRONIC_EPN", True)

        # check that all included sites are in fact present
        included_results = epns[:, 0].astype(np.int)
        if not set(included_results) == set(includeatoms):
            log.log(
                "Atom selections do not match. Likely the configuration has changed in the meantime.",
                level="error",
            )

        included_results = list(included_results)
        return epns[[included_results.index(_) for _ in includeatoms], 1]
