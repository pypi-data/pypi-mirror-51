**0.8.24 - 08/20/19**

 - Bugfix to prevent component list from not including setup components during setup phase.
 - Bugfix to dot diagram of state machine.

**0.8.23 - 08/09/19**

 - Move handle_exceptions() up to vivarium to eliminate duplication

**0.8.22 - 07/16/19**

 - Bugfix for lookup table input validation.
 - Event subsytem documentation.

**0.8.21 - 06/14/19**

 - Add names and better reprs to some of the managers.
 - ConfigTree documentation
 - Yaml load bugfix.
 - Documentation for ``simulate run`` and the interactive context.
 - Tutorials for running a simulation interactively and from the command line.
 - Headers for API documentation.
 - Component management documentation.
 - Enforce all components have a unique name.
 - Add ``get_components_by_type`` and ``get_component(name)`` to
   the component manager.
 - Bugfix in the lookup table.

**0.8.20 - 04/22/19**

 - Add simulation lifecycle info to the simulant creator.
 - Bugfix in simulate profile.

**0.8.19 - 03/27/19**

 - Update results writer to write new hdfs instead of overwriting.

**0.8.18 - 02/13/19**

 - Fix numerical issue in rate to probability calculation
 - Alter randomness manager to keep track of randomness streams.

**0.8.17 - 02/13/19**

 - Fix branch/version synchronization

**0.8.16 - 02/11/19**

 - Remove combined sexes from the "build_table".

**0.8.15 - 01/03/19**

 - Add doctests to travis
 - Update population initializer error message

**0.8.14 - 12/20/18**

 - Standardize the population getter from the the interactive interface.
 - Added "additional_key" argument to randomness.filter for probability and for rate.
 - Added a profile subcommand to simulate.
 - Separated component configuration from setup.
 - Vectorize python loops in the interpolation implementation.

**0.8.13 - 11/15/18**

 - Fix broken doc dependency

**0.8.12 - 11/15/18**

 - Remove mean age and year columns

**0.8.11 - 11/15/18**

 - Bugfix where transitions were casting pandas indices to series.
 - Add better error message when a none is found in the configuration.

**0.8.10 - 11/5/18**

 - Added ``add_components`` method to simulation context.
 - Added typing info to interactive interface.

**0.8.9 - 10/23/18**

 - Accept ``.yml`` model specifications
 - Redesign interpolation. Order zero only at this point.

**0.8.8 - 10/09/18**

 - Raise error if multiple components set same default configuration.
 - Loosen error checking in value manager

**0.8.7 - 09/25/18**

 - Distinguish between missing and cyclic population table dependencies.
 - Initial draft of tutorial documentation

**0.8.6 - 09/07/18**

 - Workaround for hdf metadata limitation when writing dataframes with a large
   number of columns

**0.8.5 - 08/22/18**

 - Add integration with Zenodo to produce DOIs
 - Added default get_components implementation for component manager

**0.8.4 - 08/02/18**

 - Standardized a bunch of packaging stuff.

**0.8.2 - 07/24/18**

 - Added ``test`` command to verify and installation
 - Updated ``README`` with installation instructions.


**0.8.1 - 07/24/18**

 - Move to source layout.
 - Set tests to install first and then test installed package.
 - Renamed ``test_util`` to resolve naming collision during test.

**0.8.0 - 07/24/18**

 - Initial release
