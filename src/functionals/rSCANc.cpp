/*
 * XCFun, an arbitrary order exchange-correlation library
 * Copyright (C) 2020 Ulf Ekström and contributors.
 *
 * This file is part of XCFun.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * For information on the complete list of contributors to the
 * XCFun library, see: <https://xcfun.readthedocs.io/>
 */

#include "SCAN_like_eps.hpp"
#include "constants.hpp"
#include "functional.hpp"

template <class num> static num rSCANC(const densvars<num> & d) {
  num eps_c = SCAN_eps::SCAN_C(d, 1, 1, 0);

  return eps_c;
}

FUNCTIONAL(XC_RSCANC) = {
    "rSCAN correlation functional",
    "rSCAN correlation functional.\n"
    "Regularised SCAN functional\n"
    "A. P. Bartok and J. R. Yates, J. Chem. Phys. 150, 161101 (2019)."
    "Implemented by James Furness (@JFurness1)\n",
    XC_DENSITY | XC_GRADIENT | XC_KINETIC,
    ENERGY_FUNCTION(rSCANC) XC_A_B_GAA_GAB_GBB_TAUA_TAUB,
    XC_PARTIAL_DERIVATIVES,
    1,
    1e-11,
    {0.217, 0.0632, 0.191, 0.0535, 0.015, 0.267, 0.0328},
    {-7.50556494224e-03,
     -1.96870403236e-02,
     -6.41852283218e-02,
     1.09960132228e-02,
     2.19920264457e-02,
     1.09960132228e-02,
     -1.76965520905e-02,
     -1.76965520905e-02}};
