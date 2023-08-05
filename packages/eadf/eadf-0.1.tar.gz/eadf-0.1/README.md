[![Build Status](https://travis-ci.com/EMS-TU-Ilmenau/EADF.svg?branch=master)](https://travis-ci.com/EMS-TU-Ilmenau/EADF)
[![Documentation Status](https://readthedocs.org/projects/eadf/badge/?version=latest)](https://eadf.readthedocs.io/en/latest/?badge=latest)

## Motivation

Geometry-based MIMO channel modelling and a high-resolution parameter estimation are applications in which a precise description of the radiation pattern of the antenna arrays is required. In this package we implement an efficient representation of the polarimetric antenna response, which we refer to as the Effective Anerture Distribution Function (EADF). High-resolution parameter estimation are applications in which this reduced description permits us to efficiently interpolate the beam pattern to gather the antenna response for an arbitrary direction in azimuth and elevation. Moreover, the EADF provides a continuous description of the array manifold and its derivatives with respect to azimuth and elevation. The latter is valuable for the performance evaluation of an antenna array as well as for gradient-based parameter estimation techniques.

## References

*Efficient antenna description for MIMO channel modelling and estimation*, M. Landmann, G. Del Galdo; 7th European Conference on Wireless Technology; 2004; Amsterdam; [IEEE Link](https://ieeexplore.ieee.org/document/1394809)
