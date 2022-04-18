import os
import sys

module_path = os.path.abspath(os.path.join("../.."))
if module_path not in sys.path:
    sys.path.append(module_path)

import numpy as np
import c2qa
import qiskit
import numpy as np
import c2qa.util as util


def h1h2h3(circuit, qma, qmb, qb, theta_1, theta_2, theta_3):
    # Work out the hermitian version of the H1 and H2 beamsplitters
    # H1 should have a plus but it has a minus
    circuit.cv_cpbs(theta_1, qmb, qma, qb)
    # H2 is a copy of cpbs for now. It needs an i.
    circuit.cv_cpbs_z2vqe(theta_2, qmb, qma, qb)
    circuit.rx(theta_3, qb)
    return circuit

def vary_Z2LGT(circuit, numberofmodes, qmr, qbr, theta_1, theta_2, theta_3):
    # print("initial state ")
    # stateop, _ = c2qa.util.simulate(circuit)
    # util.stateread(stateop, qbr.size, numberofmodes, cutoff)

    # brickwork format
    for j in range(0,numberofmodes-1,2):
        h1h2h3(circuit, qmr[j+1], qmr[j], qbr[j], theta_1, theta_2, theta_3)
    for j in range(1,numberofmodes-1,2):
        h1h2h3(circuit, qmr[j+1], qmr[j], qbr[j], theta_1, theta_2, theta_3)

def measureE_fieldterm(circuit, qbr, i):
    circuit.x(qbr[i])
    # figure out which qubit corresponds to i in the small endian format etc. Or just make the measure function.
    circuit.measure(-i, 0)

def measureE_hoppingterm(circuit, numberofmodes, numberofqubits, qmr, qbr, i):
    occs=[np.zeros((numberofmodes,numberofqubits))]

    # print("initial state ")
    # stateop, _ = c2qa.util.simulate(circuit)
    # util.stateread(stateop, qbr.size, numberofmodes, cutoff)

    circuit.cv_bs(np.pi/4, qmr[i], qmr[i+1])
    # what will be the best way to measure photon number parity?
    circuit.cv_snap(1, 0, qmr[i])
    circuit.cv_snap(1, 0, qmr[i+1])
    # figure out which qubit corresponds to i in the small endian format etc. Or just make the measure function.
    circuit.measure(-i, 0)


    # stateop, result = c2qa.util.simulate(circuit)
    # occupation = util.stateread(stateop, qbr.size, numberofmodes, 4)
    # occs[0][i]=np.array(list(occupation[0]))
    # occs[1][i]=np.array(list(occupation[1]))

    # return occs