"""Check Web Claude's 'dual conservation law' floor for the checksum route (notes/checksum_dual_floor_for_cc.md).

Frequencies k < P = 2^{eta n}; profile pi = empirical law of x(k) on the circle; |J(k)|^2 = 2^{n E_pi[log2 M^2]},
M^2 = 2 + 2 cos(theta).  A profile has 2^{(eta - D(pi||U)) n} frequencies with random phases, so its contribution
to V = P^{-1} sum_k J(k) has size 2^{(n/2)(E_pi log2 M^2 - D(pi||U) - eta)}.

WC's floor uses only pi* = 1 + cos (the maximiser of E log M^2 - D, value 1):  tau >= max(1-eta, eta - D*).
But absolute error O(1) requires handling EVERY profile whose contribution is >= 1, i.e. with
    g(pi) := E_pi log2 M^2 - D(pi||U) >= eta,
and for such a profile direct summation (cost = its size) beats sampling (cost size * contribution^2).
So the heavy side costs  max { eta - D(pi) : g(pi) >= eta }.  By Lagrange the extremal pi are the tilted laws
pi_beta ∝ M^{2 beta}, beta in [0, 1]; g is increasing in beta with g(1) = 1, so the binding profile is the one with
g(pi_beta) = eta exactly.
"""
import numpy as np
from scipy.optimize import brentq, minimize_scalar

th = np.linspace(0, 2 * np.pi, 200001)[:-1]
M2 = 2 + 2 * np.cos(th)
lM2 = np.log2(np.maximum(M2, 1e-300))


def tilt(beta):
    w = np.where(M2 > 0, M2 ** beta, 0.0) if beta > 0 else np.ones_like(M2)
    Z = w.mean(); p = w / Z                      # density w.r.t. uniform
    D = np.mean(np.where(p > 0, p * np.log2(p), 0.0))
    E = np.mean(p * lM2)
    return D, E, E - D


Dstar, Estar, gstar = tilt(1.0)
print(f"pi* = 1+cos:  D* = {Dstar:.6f} (log2 e - 1 = {np.log2(np.e) - 1:.6f}),  E log M^2 = {Estar:.6f},  g = {gstar:.6f}")
print(f"WC floor: min_eta max(1-eta, eta-D*) = {(1 - Dstar) / 2:.5f} at eta = {(1 + Dstar) / 2:.5f}")


def heavy_cost(eta):
    """max eta - D(pi) over profiles with g(pi) >= eta (tilted family)."""
    if eta >= gstar:
        return eta - Dstar
    b = brentq(lambda b: tilt(b)[2] - eta, 0.0, 1.0)
    return eta - tilt(b)[0]


for eta in (0.55, 0.6, 0.65, 0.7, 0.72135, 0.75, 0.8):
    print(f"  eta={eta:.4f}: aliases {1 - eta:.4f}   heavy (WC) {eta - Dstar:.4f}   heavy (all profiles >= 1) {heavy_cost(eta):.4f}")
r = minimize_scalar(lambda e: max(1 - e, heavy_cost(e)), bounds=(0.3, 0.999), method="bounded")
print(f"corrected floor: min_eta max(1-eta, heavy) = {r.fun:.5f} at eta = {r.x:.5f}")
