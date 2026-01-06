# Modify Dr. Amparore's et als footprint method to be used with safe petri nets read from PNML
Following are the citations of the paper that are additionally used

- Amparore, Elvio G., Gianfranco Ciardo, and Andrew S. Miner. "The footprint form of a matrix: definition, properties, and an application." Linear Algebra and its Applications 651 (2022): 209-229.

- Amparore, Elvio Gilberto, et al. "i: A Variable Order Metric for DEDS Subject to Linear Invariants." International Conference on Tools and Algorithms for the Construction and Analysis of Systems. Cham: Springer International Publishing, 2019.

- Cayir, Sinan, and Müjgân Uçer. "An algorithm to compute a basis of Petri net invariants." 4th ELECO Int. Conf. on Electrical and Electronics Engineering. UCTEA, Bursa, Turkey. 2005.

The PNML files are from MCC 2025
- https://mcc.lip6.fr/2025/

-----
# ORIGINAL README BELOW

# reduced_row_footprint_form
This repository hosts a simple Python code that computed the *reduced row footprint form of* (RRFF) a matrix.
The RREF is similar to the *reduced row echelon form* (RREF), with the difference that
 * Only values below each row leading entry are zeroed in RRFF, while in RREF every element above and below are zeroed.
 * Values above each trailing entry are zeroed.

The code defines a single function `rrff` that takes in input an arbitrary $N \times M$ matrix and return its RRFF. The canonical form is define dover the integers, i.e. leading entries are not necessarily $1$, but instead the greates common divisor of each row is made to be $1$.

The code implements the theory described in the paper:
```
``The footprint form of a matrix: definition, properties, and an application'',
Amparore, Elvio G. and Ciardo, Gianfranco and Miner, Andrew S., Linear Algebra and its Applications, To appear.
```