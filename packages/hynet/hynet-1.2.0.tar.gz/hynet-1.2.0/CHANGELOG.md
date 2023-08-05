# Change Log

All notable changes to this project are documented in this file.

## [1.2.0] - 2019-08-19
- Revised the internal structure to simplify the implementation of extensions.
    * The former class ``SystemModel`` was split into the class ``OPFModel`` and an abstract base class ``SystemModel``. The new ``SystemModel`` class implements the system model equations and serves as an interface class for optimization-problem-generating models. The class ``OPFModel`` specializes the new ``SystemModel`` to the formulation of the optimal power flow problem and replaces the former ``SystemModel`` class.
    * The class ``OPFResult`` was split into a specialization ``OPFResult`` and an abstract base class ``SystemResult``. The ``SystemResult`` class implements a common framework for the representation and evaluation of a system model based optimization result. The new implementation of ``OPFResult`` specializes the ``SystemResult`` to the representation of an optimal power flow solution.
    * Some associated internal code revision and refactoring was performed. Changes that affect the user interface are documented below.
- Added an extension for the maximum loadability problem. Please refer to the tutorial "Maximum Loadability" for more information.
- Added a monitoring and automatic correction of the converter loss error: In problem formulations that incentivize a load increase at some buses, a loss error may emerge in lossy and bidirectional converters due to noncomplementary modes in the model. While this is typically not observed in OPF problems, it often emerges in the maximum loadability problem of hybrid systems. In the automatic correction, the converter mode is fixed according to the net active power flow in the initial solution and the problem is solved again, where a zero loss error is guaranteed.
- Added the properties ``is_valid``, ``has_valid_power_balance``, and ``has_valid_converter_flows`` to ``SystemResult`` (and ``OPFResult``) and updated the property ``is_physical`` to improve and simplify the check of the result validity. Please refer to the updated tutorial "Analysis of the Optimal Power Flow Result" for more information.
- Added the methods ``add_bus``, ``add_branch``, ``add_converter``, ``add_injector``, and ``get_relative_loading`` to ``Scenario``.
- Added the functions ``convert_ac_line_to_hvdc_system`` and ``convert_transformer_to_b2b_converter``. Please refer to the tutorial "Construction of Hybrid AC/DC Grid Models" for more information.
- Added an argument to ``Scenario.verify`` to control its log output.
- Updated all internally issued scenario verifications to suppress any log output.
- Changed ``Scenario.has_hybrid_architecture`` to ``Scenario.verify_hybrid_architecture_conditions``.
- Changed the attributes ``total_injection_cost``, ``dynamic_losses``, and ``total_losses`` of ``SystemResult`` (and ``OPFResult``) to the methods ``get_total_injection_cost``, ``get_dynamic_losses``, and ``get_total_losses``.
- Changed the columns ``dv_cap_src_p_min``, ``dv_cap_dst_p_min``, ``dv_cap_src_p_max``, and ``dv_cap_dst_p_max`` of the ``converter`` data frame of ``OPFResult`` to ``dv_p_fwd_min``, ``dv_p_bwd_min``, ``dv_p_fwd_max``, and ``dv_p_bwd_max``, respectively.
- Changed the minimum version requirement for pandas from v0.23 to v0.24.
- Changed the default tolerance of the CPLEX SOCR solver interface to ``5e-8``.
- Changed the default amalgamation of the MOSEK chordal SDR solver interface: The amalgamation improved the performance for many problem instances, but in some cases it led to numerical issues or less accurate results. In favor of robustness, the amalgamation is now disabled by default.
- Fixed some compatibility and deprecation issues with pandas v0.25 and NumPy v1.17.
- Removed ``SystemModel.has_hybrid_architecture`` and ``SystemModel.islands``.

## [1.1.4] - 2019-06-24
- Extended the OPF result summary for cases that are not solved successfully.
- Updated the MATPOWER import to support test cases with missing ``gencost`` data.
- Updated the MATPOWER import to detect and replace infinite (``Inf``) active/reactive power limits.
- Changed the automatic solver selection to *always* select a QCQP solver by default.
- Added ``OPFResult.get_branch_utilization``.

## [1.1.3] - 2019-06-13
- Revised the ampacity constraint generation to improve performance.

## [1.1.2] - 2019-06-07
- Added a chordal conversion to the SDR solver interface for MOSEK.
- Added the suppression of the activity output of the clients in ``OptimizationServer.start_clients``.
- Changed the progress bar of the ``OptimizationServer`` to ``tqdm``.
- Updated the OPF summary (total losses in percent of the active power load).
- Updated the code to address the deprecation of ``numpy.asscalar``.
- Updated the SOCR and SDR solver interface for MOSEK with a scaling of the coupling constraints for duplicate variables to improve the numerical accuracy of the duplication.
- Updated the SOCR solver interface for MOSEK to use a default of ``1e-9`` for ``MSK_DPAR_INTPNT_CO_TOL_DFEAS`` with versions prior to MOSEK v9.0.

## [1.1.1] - 2019-05-17
- Added an IBM CPLEX based SOCR solver interface.
- Added an object-oriented design to the initial point generators and added their support in ``calc_opf``.
- Updated the PICOS solver interface to support PICOS v1.2.0.
- Updated the MOSEK solver interface to support MOSEK v9.0.

## [1.1.0] - 2019-03-28
- Added a feature- and structure-preserving network reduction method for large-scale grids.

## [1.0.8] - 2019-02-26
- Added a setter for the grid name and description of a database (``DBConnection.grid_name`` and ``DBConnection.description``).
- Changed the default tolerance of the IPOPT QCQP solver to ``1e-6`` (was ``1e-7``).

## [1.0.7] - 2019-02-05
- Added average branch utilization statistics to the OPF summary.
- Added a local mode to the optimization server (replaces ``num_local_workers``).
- Added a marginal price property to the ``PWLFunction`` class.
- Changed the automatic solver selection to require a QCQP solver for systems without the *hybrid architecture*.

## [1.0.6] - 2019-01-10
- Fixed an issue in the MATPOWER import with optional data columns of the MATPOWER format.

## [1.0.5] - 2019-01-10
- Added ``Scenario.has_hybrid_architecture``, ``Scenario.get_ac_branches``, ``Scenario.get_dc_branches``, ``Scenario.add_compensator``, ``CapRegion.copy``, ``show_power_balance_error``, and ``show_branch_reconstruction_error``.
- Added an object-oriented design to the rank-1 approximation methods (to avoid the need of closures for their configuration).
- Added the detection of omitted ramping limits in the MATPOWER import.
- Extended the physical validity assessment that underlies ``OPFResult.is_physical``.
- Updated the automatic solver selection and OPF result summary with the consideration of the *hybrid architecture*.
- Changed the default rank-1 approximation to the graph traversal method.
- Removed ``SystemModel.is_acyclic``, ``SystemModel.ac_subgrids``, and ``SystemModel.dc_subgrids``.

## [1.0.4] - 2018-12-28
- Revised the constraint scaling to improve performance.

## [1.0.3] - 2018-12-11
- Extended the scenario verification to detect lines that connect buses with different base voltages.

## [1.0.2] - 2018-12-07
- Revised the management of worker processes to improve performance, especially under Windows.

## [1.0.1] - 2018-11-29
- Updated the README with solver installation instructions for Windows.
- Excluded support for CVXPY.

## [1.0.0] - 2018-11-27
- Official release.

## [0.9.9] - 2018-11-26
- Initial commit to GitLab.com.

## [0.9.8] - 2018-10-19
- Pre-release of *hynet* on PyPI.
