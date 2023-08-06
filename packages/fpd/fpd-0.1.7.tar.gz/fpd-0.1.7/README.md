News
====
1 September 2019 - Release 0.1.7: new Airy disc diameter and a 7-smooth number functions, and a new module for io featuring a NanoMegas Topspin app5 file converter for SPED data. 

24 March 2019 - Release 0.1.6: improvements to MerlinBinary class, speed optimisations in synthetic_images, 'Uniform' colourmap renamed to 'MLP', additional conversion functions in mag_tools, and improvements to the single image SNR function.

18 February 2019 - Release 0.1.5 with improvements to or new lattice functions 
(lattice_from_inliers, blob_log_detect, lattice_resolver), 
new SNR and gun noise correction tools in a new fpd.utils module, and many other improvements.

27 October 2018 - Release 0.1.4 with new CubicImageInterpolator and VirtualAnnularImages classes, 
several lattice finding, ctf and image alignment functions, and many other improvements.

31 July 2018 - Release 0.1.3 with new MerlinBinary class and other improvements.

25 Mar 2018 - Notebook demos are now available at https://gitlab.com/fpdpy/fpd-demos


FPD package
===========
The fpd package provides code for the storage, analysis and visualisation
of data from fast pixelated detectors. The data storage uses the hdf5 based 
EMD file format, and the conversion currently supports the Merlin readout from 
Medipix3 detectors. Differential phase contrast imaging and several other common
data analyses, like radial distributions, virtual apertures, and lattice analysis,
are also implemented, along with many utilities.

The package is relatively lightweight, with most of its few dependencies being
standard scientific libraries. All calculations run on CPUs and many use 
out-of-core processing, allowing data to be visualised and processed on anything
from very modest to powerful hardware.

A degree of optimisation through parallelisation has been implemented. The 
development environment is Linux; your mileage may vary on Windows because
of how forking works, but the Windows 10 Linux subsystem has been reported to
work well.

Installation
------------
The package currently supports both python versions 2.7 and 3.x. Hyperspy is
used in a few places but most of the fpd module can be used without it being 
installed (simply install the package dependencies manually and ignore them when
using pip by adding ``--no-deps`` to the install command).

Installation from source:

```bash
pip3 install --user .
```

Instalation from PyPI (https://pypi.org/project/fpd/):

```bash
pip3 install --user fpd
```

``-U`` can be added to force an upgrade / reinstall; in combination with ``--no-deps``,
only the ``fpd`` package will be reinstalled.

The package can be removed with:

```bash
pip3 uninstall fpd
```


Usage
-----
In python or ipython:

```python
import fpd
d = fpd.DPC_Explorer(-64)
```

```python
import fpd.fpd_processing as fpdp
rtn = fpdp.phase_correlation(data, 32, 32)
```
where `data` is any array-like object. For example, this can be an in-memory 
numpy array, an hdf5 object on disk, or a dask array, such as that used in 
'lazy' hyperspy signals.

All functions and classes are documented and can be read, for example, in `ipython`
by appending a `?` to the object. E.g.:

```python
import fpd
fpd.DPC_Explorer?
```

Documentation
-------------
Release: https://fpdpy.gitlab.io/fpd/

Development version: https://gitlab.com/fpdpy/fpd/builds/artifacts/master/file/pages_development/index.html?job=pages_development

Notebook demos: https://gitlab.com/fpdpy/fpd-demos.

Further documentation and examples will be made available over time.


Related projects
----------------

https://www.gla.ac.uk/schools/physics/research/groups/mcmp/researchareas/pixstem/

http://quantumdetectors.com/stem/

https://gitlab.com/fast_pixelated_detectors/merlin_interface

https://gitlab.com/fast_pixelated_detectors/fpd_live_imaging

https://gitlab.com/pixstem/pixstem

https://emdatasets.com/format

http://hyperspy.org/

http://gwyddion.net/

More packages will be added to the https://gitlab.com/fast_pixelated_detectors
group as they develop.

