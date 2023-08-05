#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2017-2019 Airinnova AB and the PyTornado authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Authors:
# * Alessandro Gastaldi
# * Aaron Dettmann

"""
Data structures for VLM-related data: grid and results.

Developed for Airinnova AB, Stockholm, Sweden.
"""

from collections import defaultdict, namedtuple

from pytornado.objects.utils import FixedNamespace, FixedOrderedDict

BookKeepingEntry = namedtuple('BookKeepingEntry', ['subarea', 'pan_idx', 'num_chordwise_panels', 'mirror'])


class VLMLattice(FixedNamespace):
    """
    Data structure for the PyTornado VLM lattice.

    VLMLATTICE contains the lattice data required for VLM analysis
    The data is stored in pre-allocated, contiguous-memory C-arrays

    Attributes:
        :p: (numpy) panel corner points (N x 4 x 3)
        :v: (numpy) panel vortex points (N x 4 x 3)
        :c: (numpy) panel collocation points (N x 3)
        :bound_leg_midpoints: (numpy) midpoint of the bound leg (N x 3)
        :n: (numpy) panel normal vectors (N x 3)
        :a: (numpy) panel surface areas (N x 1)
        :info: (dict) lattice statistics (quantity, quality)
    """

    def __init__(self):
        """
        Initialises instance of VLMLATTICE.

        Upon initialisation, attributes of VLMLATTICE are created and fixed
        Only existing attributes may be modified afterwards
        """

        super().__init__()

        self.reset()
        self._freeze()

    def reset(self):
        """Re-initialise VLMLATTICE properties and data"""

        self.p = None
        self.v = None
        self.c = None
        self.n = None
        self.a = None
        self.bound_leg_midpoints = None

        self.epsilon = None

        self.len_bound_leg = None

        self.panel_bookkeeping = []
        self.bookkeeping_by_wing_uid = defaultdict(list)
        self.bookkeeping_by_wing_uid_mirror = defaultdict(list)

        self.info = FixedOrderedDict()
        self.info['num_wings'] = 0
        self.info['num_segments'] = 0
        self.info['num_controls'] = 0
        self.info['num_panels'] = 0
        self.info['num_strips'] = 0
        self.info['aspect_min'] = 0.0
        self.info['aspect_max'] = 0.0
        self.info['aspect_avg'] = 0.0
        self.info['area_min'] = 0.0
        self.info['area_max'] = 0.0
        self.info['area_avg'] = 0.0
        self.info._freeze()

    def update_control_panels(self, control_uid, hinge_points, panel_range, deflection):
        """
        Update the book keeping of the control panels

        :control_uid: (str) name of the control surface
        :hinge_points: (tuple) inner and outer hinge point
        :panel_range: (gen-obj) generator with range of panel indices
        :deflection: (float) deflection of panels in degrees
        """

        self.control_panels[control_uid].append([hinge_points[0], hinge_points[1], panel_range, deflection])

    def update_bookkeeping(self, entry):

        self.panel_bookkeeping.append(entry)

        if entry.mirror:
            self.bookkeeping_by_wing_uid_mirror[entry.subarea.parent_wing.uid].append(entry)
        else:
            self.bookkeeping_by_wing_uid[entry.subarea.parent_wing.uid].append(entry)


class VLMData(FixedNamespace):
    """
    Data structure for the PyTornado VLM analysis data.

    VLMDATA contains the data produced during VLM analysis. .
    The data is stored in pre-allocated, contiguous-memory C-arrays.

    Attributes:
        :panelwise: (dict) dictionary of panel-wise properties (NP)
        :stripwise: (dict) dictionary of strip-wise properties (NS)
        :forces: (dict) dictionary of aero forces (1)
        :coeffs: (dict) dictionary of aero coefficients (1)
    """

    def __init__(self):
        """
        Initialise instance of VLMDATA.

            * VLMDATA inherits from FIXEDNAMESPACE.
            * Upon initialisation, attributes of VLMDATA are created and fixed.
            * Only existing attributes may be modified afterwards.
        """

        super().__init__()

        self.reset()
        self._freeze()

    def reset(self):
        """Re-initialise VLMDATA."""

        self.matrix_downwash = None
        self.array_rhs = None

        self.matrix_lu = None
        self.array_pivots = None

        # On unit of panelwise results:
        # Circulation [gamma] = m²/s
        # Velocity v{x,y,z} [m/s]
        # Panel forces f{x,y,z} [Newton] (NOT force per length)
        self.panelwise = FixedOrderedDict()
        self.panelwise['gamma'] = None
        self.panelwise['vx'] = None
        self.panelwise['vy'] = None
        self.panelwise['vz'] = None
        self.panelwise['vmag'] = None
        self.panelwise['fx'] = None
        self.panelwise['fy'] = None
        self.panelwise['fz'] = None
        self.panelwise['fmag'] = None
        self.panelwise['cp'] = None
        self.panelwise._freeze()

        self.stripwise = FixedOrderedDict()
        self.stripwise['cl'] = None
        self.stripwise._freeze()

        self.forces = FixedOrderedDict()
        self.forces['x'] = 0.0
        self.forces['y'] = 0.0
        self.forces['z'] = 0.0
        self.forces['D'] = 0.0
        self.forces['C'] = 0.0
        self.forces['L'] = 0.0
        self.forces['l'] = 0.0
        self.forces['m'] = 0.0
        self.forces['n'] = 0.0
        self.forces._freeze()

        self.coeffs = FixedOrderedDict()
        self.coeffs['x'] = 0.0
        self.coeffs['y'] = 0.0
        self.coeffs['z'] = 0.0
        self.coeffs['D'] = 0.0
        self.coeffs['C'] = 0.0
        self.coeffs['L'] = 0.0
        self.coeffs['l'] = 0.0
        self.coeffs['m'] = 0.0
        self.coeffs['n'] = 0.0
        self.coeffs._freeze()
