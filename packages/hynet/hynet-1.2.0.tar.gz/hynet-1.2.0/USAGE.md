# Tutorial

In the following, some use cases are presented to illustrate the application of *hynet*. In all subsections, it is assumed that a Python shell was started in a directory that contains the [grid databases](https://gitlab.com/tum-msv/hynet-databases) and that the following commands were executed:

```python
import hynet as ht
database = ht.connect('pjm_hybrid.db')
```


## Optimal Power Flow


### Selection and Configuration of a Specific Solver

The [README.md](https://gitlab.com/tum-msv/hynet/blob/master/README.md) illustrates the automatic selection of a QCQP solver and the selection of a solver for a specific OPF formulation (QCQP, SDR, SOCR). However, in certain cases, e.g. for reproducibility, the explicit selection of a specific solver with specific parameters may be desired. To this end, a list of solver classes for the available solvers is provided by

```python
ht.AVAILABLE_SOLVERS
```

For example, to solve the OPF problem with IPOPT, use

```python
solver = ht.solver.ipopt.QCQPSolver()
result = ht.calc_opf(database, solver=solver)
print(result)
```

To change the convergence tolerance of IPOPT to $`10^{-7}`$, extend the ``param`` dictionary accordingly, i.e.,

```python
solver.param['tol'] = 1e-7
print(ht.calc_opf(database, solver=solver))
```

For more information on the parameters of a solver class, please refer to its documentation, e.g. via

```python
help(ht.solver.ipopt.QCQPSolver)
```


### Analysis of the Optimal Power Flow Result

The result of an OPF calculation contains extensive information about the resulting system state, the solution process, as well as the associated optimization problem. An overview of the available data is provided the result object's help, i.e.,

```python
result = ht.calc_opf(database)
help(result)
```

A formatted summary can be printed with

```python
print(result)
```

while detailed information related to the buses, branches, converters, and injectors can be pretty-printed using

```python
print(result.details)
```

The data related to these entities is stored in [pandas](https://pandas.pydata.org/) data frames, which provide extensive support for data analysis. For example, the total active power injection (in MW) and the three buses with the smallest voltage magnitude can be determined with

```python
result.injector['s'].sum().real
result.bus['v'].abs().nsmallest(n=3)
```

For the visual inspection of the data, [Matplotlib](https://matplotlib.org/) may be used, where *hynet* includes some functions for some common plotting tasks, i.e.,

```python
ht.show_voltage_profile(result)
ht.show_dispatch_profile(result)
ht.show_branch_flow_profile(result)
ht.show_converter_flow_profile(result)
```

Furthermore, [in case of exactness of the SDR or SOCR relaxation](http://ieeexplore.ieee.org/document/7997734/), the dual variables of the power balance constraints equal the locational marginal prices (LMPs), which can be illustrated with

```python
ht.show_lmp_profile(result)
```

Finally, to identify congested branches in the system, the dual variables of the ampacity constraint may be investigated via

```python
ht.show_ampacity_dual_profile(result, id_label=True)
```

When processing the result programmatically, it is important to check its validity:

```python
result.is_valid
```

This check ensures the following conditions:

1)  The result contains solution data:

    ```python
    not result.empty
    ```

2)  The solver reported the successful solution of the problem:

    ```python
    result.solver_status == ht.SolverStatus.SOLVED
    ```

3)  The solution complies with the tolerances for a physical solution:

    ```python
    result.is_physical
    ```
    
    The solution is considered physically valid if the power balance and converter flow error complies with the respective tolerances, which can be verified individually by
    
    ```python
    result.has_valid_power_balance, result.has_valid_converter_flows
    ```

The third item is particularly important if the OPF problem was solved via a relaxation (SDR or SOCR), where inexactness of the relaxation can lead to a nonphysical solution. In some cases, it can be appropriate to consider the above conditions individually, e.g., to check only the first and third item to accept also solutions for which the solver obtained a result but reported numerical issues.


### Optimal Power Flow for Different Scenarios

The *hynet* grid database format comprises two major categories of data, i.e., a description of the *grid infrastructure* as well as *scenarios*. The grid infrastructure specifies all physical entities of the grid, i.e., buses, lines, transformers, converters, shunts, and injections, where the latter encompasses conventional as well as renewables-based generation, dispatchable loads, and prosumers. This physical description is complemented by scenario information, which specifies the load, injector capabilities (e.g., for renewable energy sources), and inactivity of certain entities (e.g. decommitment of generators) at particular time instants. To inspect the scenarios provided by the database, type

```python
scenario_info = ht.get_scenario_info(database)
print(scenario_info)
```

For example, assume we want to calculate the OPF for all scenarios of the exemplary winter weekday in this database. We start by extracting these scenarios and sort them by their time stamp:

```python
scenario_info = scenario_info.loc[scenario_info['name'] == 'Winter Weekday']
scenario_info.sort_values(by='time', inplace=True)
```

Now, we calculate the OPF for all these scenarios and store the minimum injection cost in a new column of the data frame:

```python
for id_ in scenario_info.index:
    result = ht.calc_opf(database, scenario_id=id_)
    scenario_info.loc[id_, 'injection_cost'] = result.get_total_injection_cost()
```

Finally, we visualize the cost using [Matplotlib](https://matplotlib.org/):

```python
import matplotlib.pyplot as plt
plt.plot(scenario_info['time'], scenario_info['injection_cost']/1e3)
plt.xlabel('Hour of the Day')
plt.ylabel('Cost in k$')
plt.title('Injection Cost for an Exemplary Winter Weekday')
plt.show()
```


### Distributed Computation of Optimal Power Flows

The calculation of several OPFs, e.g., to analyze different scenarios of a grid, can be computationally demanding. To this end, *hynet* includes support for a distributed solution on a server cluster. Consider again the analysis of the examplary winter weekday, where the hourly injection cost was computed in [Optimal Power Flow for Different Scenarios](#optimal-power-flow-for-different-scenarios). In order to distribute the calculation of these OPFs to several servers, start a *hynet* optimization server via

```python
server = ht.start_optimization_server()
```

To see more options for the server, call ``help(ht.start_optimization_server)``. After starting the server, connect *hynet* optimization clients by logging in to the **client machines** and, in the terminal, run

```sh
python -m hynet client [server_ip]
```

where ``[server_ip]`` is the network IP address of the machine running the *hynet* optimization server. To see more options for the clients, call ``python -m hynet client -h``. Then, back at the Python prompt on the **server machine**, load the scenarios of the exemplary winter weekday into a list using

```python
scenario_info = ht.get_scenario_info(database)
scenario_info = scenario_info.loc[scenario_info['name'] == 'Winter Weekday']
scenario_info.sort_values(by='time', inplace=True)
scenarios = [ht.load_scenario(database, scenario_id=id_) for id_ in scenario_info.index]
```

and distribute their computation to the client machines using

```python
results = server.calc_jobs(scenarios)
```

This call is blocking until all jobs are processed. The obtained OPF results are returned in ``results``, corresponding to the order in ``scenarios``. Finally, the *hynet* optimization server and all clients are shut down via

```python
server.shutdown()
```

**Remarks:**

* If the client machines are unavailable, the optimization server can be operated in a local mode, see the parameter ``local`` of ``ht.start_optimization_server``.
* To automate the start of *hynet* optimization clients, the method ``server.start_clients`` may be utilized. For example, starting *hynet* optimization clients on the machines with the host names ``client1`` and ``client2`` via SSH using the user name ``my_user_name`` (with automated authentication via SSH keys), where the *hynet* optimization server is running on the machine with the IP address ``10.0.0.5``, can be achieved with

```python
server.start_clients(['client1', 'client2'], '10.0.0.5',
                     ssh_user='my_user_name', num_workers=4,
                     log_file='hynet_client.log')
```

In this configuration, every *hynet* optimization client offers 4 worker processes and logs its output to ``hynet_client.log``.


### Optimal Power Flow for a Customized Scenario

A scenario may also serve as the starting point for a further analysis of the grid, e.g., to study the impact of outages. In such cases, the desired scenario can be loaded explicity. For example, the base case is loaded with

```python
scenario = ht.load_scenario(database)
```

Let us first inspect the data of this scenario with

```python
print(scenario)
```

To get more information on the type of data, we can consult the class documentation, i.e.,

```python
help(scenario)
```

Now, assume that we want to study the impact of an outage of the AC/DC converter between bus 5 and 8 on the optimal power flow. To this end, we remove the respective converter with ID 3 from the scenario and initiate an OPF calculation:

```python
scenario.converter.drop(3, inplace=True)
print(ht.calc_opf(scenario))
```

As another example, let us study the hour 6pm to 7pm of the exemplary winter weekday with scenario ID 67, see also [Optimal Power Flow for different Scenarios](#optimal-power-flow-for-different-scenarios).

```python
scenario = ht.load_scenario(database, scenario_id=67)
```

Assume we want to take bus 3 off the grid, including all entities connected to it, and study the OPF. As bus 3 is the reference bus, we move the reference to bus 5. These actions can be implemented by

```python
scenario.remove_buses([3])
scenario.bus.loc[5, 'ref'] = True
print(ht.calc_opf(scenario))
```


### Optimal Power Flow with Loss Minimization

Typically, the OPF is considered with respect to minimum injection cost, but sometimes an OPF with minimum transmission losses is more appropriate - from an engineering as well as mathematical perspective. To illustrate this, consider again the default scenario, i.e.,

```python
scenario = ht.load_scenario(database)
```

This system exhibits the [hybrid architecture](https://ieeexplore.ieee.org/document/7414517) and satisfies the conditions for the related [results on exactness of the SDR and SOCR](https://ieeexplore.ieee.org/document/7997734), which is verified by

```python
scenario.verify_hybrid_architecture_conditions()
```

Thus, the use of an SOCR solver (which we assume to be available on your system) is appropriate:

```python
result = ht.calc_opf(scenario, solver_type=ht.SolverType.SOCR)
print(result)
```

The [theory](https://ieeexplore.ieee.org/document/7997734) guarantees exactness of the relaxation as long as no *pathological price profile* occurs, which is indeed the case:

```python
result.is_physical, result.reconstruction_mse
```

Now, assume all generation in the system is based on renewable energy sources, which are often considered with zero marginal costs. Correspondingly, we set all cost functions to zero and calculate the OPF again, i.e.,

```python
scenario.injector['cost_p'] = None
result = ht.calc_opf(scenario, solver_type=ht.SolverType.SOCR)
```

Pathological price profiles are characterized by a union of linear subspaces in the domain of the dual variables and, as they intersect at the origin, inexactness of the relaxation is more likely if the LMP is (close to) zero at some buses. Indeed, although this system features the hybrid architecture, the relaxation has now become inexact:

```python
print(result)
result.is_physical, result.reconstruction_mse
```

The observation of a pathological price profile can motivate a reconsideration from an engineering perspective: If the LMP for active power is zero at some buses, those locations provide power free of charge and, there, the OPF's cost minimization objective remains without effect. In such cases, it is reasonable to consider transmission losses in the objective to avoid the waste of freely available energy. In *hynet*, the OPF's objective can be augmented with a *loss penalty term* by imposing an (artificial) cost on the electrical losses. For example, this cost is set to $1/MWh using

```python
scenario.loss_price = 1
```

While this penalty term is motivated from an engineering perspective, it also establishes exactness of the relaxation:

```python
result = ht.calc_opf(scenario, solver_type=ht.SolverType.SOCR)
print(result)
result.is_physical, result.reconstruction_mse
```

The recovery of exactness is explained by the impact of the loss term, which [can be shown](https://arxiv.org/abs/1811.10496) to introduce an offset to the marginal prices of the injectors and, therewith, induces a shift of the price profile that potentially avoids the critical subspaces.


### Saving an Optimal Power Flow Result

As OPF results can be reproduced rather easily and as it is often not necessary to store the entirety of an OPF result, the *hynet* grid database format favors simplicity and does not support the storage of results. However, if the necessity of storing an OPF result arises, e.g., to avoid its repeated computation, it can be serialized with [pickle](https://docs.python.org/3/library/pickle.html). Let us calculate an OPF result and store it to the file ``my_result.pickle``:

```python
import pickle
result = ht.calc_opf(database)
with open('my_result.pickle', 'wb') as file:
    pickle.dump(result, file)
```

We can load the result again using

```python
with open('my_result.pickle', 'rb') as file:
    result = pickle.load(file)
```

**Caution:** Note that pickles are not secure against malicious modifications and should only be opened if they were received from a trusted source.


### Tracking the Solution Progress

By default, *hynet* does not show any progress information to avoid cluttering the standard output. However, especially for large grids that involve a significant computation time, such information may be desired to track the solution progress. To this end, the progress within the solver can be tracked by enabling its verbose mode, e.g.,

```python
solver = ht.solver.ipopt.QCQPSolver(verbose=True)
print(ht.calc_opf(database, solver=solver))
```

while the progress within *hynet* may be tracked by enabling its debug log output, i.e.,

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```


## Additional Problem Formulations

The object-oriented design of *hynet* facilitates extensions to OPF-related problem formulations. These extensions consist of an adapted mapping from the scenario data to the QCQP formulation as well as an adjusted result representation, while sharing the other software infrastructure. Correspondingly, many aspects of *hynet* that are documented in the context of OPF problems apply to extensions as well. In the following, the extensions that are included with *hynet* are briefly presented, while further information can be found in the package documentation.


### Maximum Loadability

The *maximum loadability* is an important characteristic of a power system and, e.g., relevant in expansion planning and voltage stability assessment. In *hynet*, the maximum loadability problem as proposed in Section 3 of "[Maximum loadability of power systems using interior point nonlinear optimization method](https://ieeexplore.ieee.org/document/574936)" by Irisarri et al. is included, i.e., the power balance equations are extended with a scaled load increment and the scaling of the increment is maximized. The nodal load increment is defined by the column ``'load_increment'`` in the ``bus`` data frame of the scenario and, if left unspecified, it is set to the nodal load (i.e., a constant power factor is maintained).

The maximum loadability for the default scenario of the grid database can be calculated with

```python
result = ht.calc_loadability(database)
print(result)
```

The load increment is set to the system's load, which is verified with

```python
result.scenario.bus['load_increment']
```

and the maximum load increment scaling can be accessed via

```python
result.load_increment_scaling
```

A custom load increment, e.g., only at bus 2 and 3, can be configured as follows. Load the scenario,

```python
scenario = ht.load_scenario(database)
```

set the load increment accordingly,

```python
scenario.bus['load_increment'] = 0.0
scenario.bus.loc[2:3, 'load_increment'] = scenario.bus.loc[2:3, 'load']
```

and initiate the computation of the maximum loadability,

```python
result = ht.calc_loadability(scenario)
print(result)
```

The identified maximum load is thus given by

```python
scenario.bus['load'] + result.load_increment_scaling * scenario.bus['load_increment']
```

which is also available via the result, which contains a copy of the original scenario with the maximum load:

```python
result.scenario.bus['load']
```


## Management of Grid Databases

The *hynet* grid database format divides the data into two categories, the *grid infrastructure* as well as *scenario information* (see also [Optimal Power Flow for Different Scenarios](#optimal-power-flow-for-different-scenarios)). The data considered as grid infrastructure comprises the system's physical entities as well as their parameters that are assumed to be fixed for the purpose of OPF studies, while scenario information comprises certain OPF-relevant time-dependent parameters. In particular, the latter can capture (with ``scenario`` being a scenario object):

* Changes of the load (``scenario.bus['load']``).
* Selected changes of injectors:
    - Scaling of the cost function for active and reactive power (``scenario.injector[['cost_p', 'cost_q']]``). The scaling must be the same for both cost functions of an injector.
    - Changes of the box constraints of the capability region (``p_min``, ``p_max``, ``q_min``, and ``q_max`` of the objects in ``scenario.injector['cap']``).
* Inactivity of injectors, branches, converters, or buses (captured by dropping the respective rows in ``scenario.injector``, ``scenario.branch``, ``scenario.converter``, and ``scenario.bus``).
* Inactivity of shunt compensation (captured by setting the respective entry in ``scenario.bus['y_tld']`` to zero).

In the following, it is illustrated how grid infrastructure and scenario data can be saved in *hynet* grid databases, while the subsequent sections discuss further aspects of managing *hynet* grid databases.


### Creating a new Database

In this example, some changes are made to a scenario that are considered as modifications of the grid infrastructure and, subsequently, it is saved as a new grid. To this end, let us consider the following scenario.

```python
scenario = ht.load_scenario(database, scenario_id=100)
print(ht.calc_opf(scenario).details)
```

In the injector result, we can observe that two generators operate at a very low power factor. To ensure that the power factor of the injectors is at least 0.9, we can modify their capability regions accordingly (see also [Visualization and Specification of Capability Regions](#visualization-and-specification-of-capability-regions)):

```python
for cap in scenario.injector['cap']:
    cap.add_power_factor_limit(0.9)
print(ht.calc_opf(scenario).details)
```

If we now try to save this scenario (which we'll actually learn [below](#saving-a-customized-scenario)), *hynet* issues an error as this is considered as a change of the grid infrastructure (For the sake of simplicity, scenarios may change capability regions only in size, but not in shape):

```python
scenario.name = 'Nice power factor'
ht.save_scenario(database, scenario)
```

Thus, in order to store this scenario, we have to create a new database with this grid infrastructure. Assume the database shall be stored in ``my_new_database.db`` (which must not exist). We thus connect to this database and initialize it using

```python
database_new = ht.connect('my_new_database.db')
scenario.grid_name = 'Hybrid PJM System with a Power Factor Limit'
ht.initialize_database(database_new, scenario)
```

Therewith, the grid infrastructure is stored to the database and, additionally, a scenario is created that captures the scenario information. Note that during the database initialization, the scenario ID and database URI in ``scenario`` are updated accordingly. If you are curious, you may browse the database, e.g., using the [DB Browser for SQLite](http://sqlitebrowser.org/) or [SqLite Online](https://sqliteonline.com/).


### Saving a Customized Scenario

This example assumes that [Creating a new Database](#creating-a-new-database) was finished before to have an example database at hand. Let us first connect to this database and check the scenarios therein:

```python
database = ht.connect('my_new_database.db')
print(ht.get_scenario_info(database))
```

We see that there is one scenario available, which was created when we initialized the database, and load it using

```python
scenario = ht.load_scenario(database)
```

Now, let's assume we want to create a scenario where injector 3 is decommitted (offline). To this end, we simply remove this injector from the injector data frame, update the scenario's name, and initiate the saving of the scenario, i.e.,

```python
scenario.injector.drop(3, inplace=True)
scenario.name = "Injector 3 offline"
ht.save_scenario(database, scenario)
```

The saving procedure assigns a new ID to the scenario, saves the scenario information to the database, and updates the scenario ID and database URI in ``scenario`` accordingly. For the purpose of illustration, let's add another scenario that considers the outage of converter 2 at 80% of the original load:

```python
scenario = ht.load_scenario(database)
scenario.converter.drop(2, inplace=True)
scenario.bus['load'] *= 0.8
scenario.name = "Outage of converter 2"
ht.save_scenario(database, scenario)
```

We can now see these scenarios when we inspect the database,

```python
print(ht.get_scenario_info(database))
```


### Removing Scenarios from a Database

This example assumes that [Saving a Customized Scenario](#saving-a-customized-scenario) was finished before to have an example database at hand. In this database, we now find three scenarios:

```python
database = ht.connect('my_new_database.db')
print(ht.get_scenario_info(database))
```

Let's assume we are not satisfied with the last two scenarios that we added and we want to remove them from the database. We can achieve this using

```python
ht.remove_scenarios(database, scenario_ids=[1, 2])
```


### Import Grid Data from the MATPOWER Format

*hynet* supports the import of MATPOWER test cases into the *hynet* grid database format, if the test case is stored as a MATPOWER test case struct ``mpc`` in a MATLAB MAT-file. For example, assume we want to import the MATPOWER test case ``case5.m``. With [MATPOWER](http://www.pserc.cornell.edu/matpower/) properly installed, start MATLAB, load the test case, and save it to a MAT-file using

```Matlab
mpc = loadcase('case5.m');
save('case5.mat', 'mpc');
```

Then, open a terminal, navigate to the directory that contains this MAT-file, and perform the import using

```sh
python -m hynet import case5.mat
```

The corresponding *hynet* grid database is then saved as ``case5.db``. To see more options for the import, type

```sh
python -m hynet import -h
```

For example, we can specify the output file name, the grid's name, and a description of the data using

```sh
python -m hynet import case5.mat -o pjm_system.db -g "PJM System" -d "This data was imported from MATPOWER."
```

**Remark:** To perform the import from the Python shell, see ``ht.import_matpower_test_case``.

**Caution:** It is important to be aware of the following particularities of the import:

1) The branch flow limit is interpreted differently in *hynet*, i.e., it is considered as an *ampacity rating* (thermal flow limit) stated as an MVA rating at 1 p.u. compared to the apparent power flow limit in MATPOWER. If the apparent power flow limit shall be enforced, the conservative substitute bounds described in Remark 1 in [this paper](http://ieeexplore.ieee.org/document/7414517/) can be utilized, which are applied to a scenario object ``scenario`` with ``scenario.set_conservative_rating()``.

2) *hynet* exclusively employs *piecewise linear* (PWL) cost functions. Nonlinear polynomial cost functions in the MATPOWER test case are converted to PWL functions by sampling the polynomial equidistantly within the generator's active power bounds. The number of sample points can be specified with the option ``-n``.


## Construction of Hybrid AC/DC Grid Models

The following examples illustrate how HVDC systems may be added to a grid model. Please note that the presented modeling approach is targeted at system-level studies and does not explicitly model the transformer, filter, and phase reactor of VSC stations. The converters are parameterized with conversion loss factors of 1% and a Q/P capability ratio of 35%, which is rather conservative, cf. the brochure "[HVDC Light - It's time to connect](https://search-ext.abb.com/library/Download.aspx?DocumentID=POW-0038&LanguageCode=en&DocumentPartId=&Action=Launch&DocumentRevisionId=H)" of ABB AB (Revision H, 2017).


### Converting AC Lines to DC Operation

For capacity expansion, the [conversion of existing AC lines to DC operation](https://e-cigre.org/publication/583-guide-to-the-conversion-of-existing-ac-lines-to-dc-operation) can be an attractive option, as the construction of new transmission corridors is often difficult and protracted. The conversion can offer a significant increase of transmission capacity within the existing corridor, while the (VSC) converters additionally provide flexible power flow control and reactive power compensation which can additionally enhance the system's effective transmission capacity. In the following, it is illustrated how such a conversion may applied to a model by creating a MT-HVDC variant of the hybrid system presented in [this paper](https://ieeexplore.ieee.org/document/7414517). To this end, we first load the adapted PJM system:

```python
database_acg = ht.connect('pjm_adapted.db')
acg = ht.load_scenario(database_acg)
print(acg)
```

The branches 5 and 6 connect the buses 3-4 and 4-5 and are converted to P2P-HVDC systems in the [aforementioned work](https://ieeexplore.ieee.org/document/7414517). Here, these two AC lines shall be converted to a 3-terminal HVDC system. We start by creating a copy of the original system and updating the meta data:

```python
htg = acg.copy()
htg.grid_name = "Hybrid PJM System"
htg.description = htg.database_uri = ""
```

For the conversion to DC operation, *hynet* offers the following utilities:

```python
help(ht.convert_ac_line_to_hvdc_system)
help(ht.convert_transformer_to_b2b_converter)
```

With the following code, the two AC lines are converted to an HVDC system. Please note that, like in the [aforementioned work](https://ieeexplore.ieee.org/document/7414517), the transmission capacity of the lines is intentionally *not* uprated to illustrate the increase of the effective transmission capacity due to the *flexibilization* of the grid.

```python
ht.convert_ac_line_to_hvdc_system(
    htg,
    branch_id=5,
    loss_fwd=1.0,
    loss_bwd=1.0,
    q_to_p_ratio=0.35,
    base_kv_map={230.0: 325.0},
    capacity_factor=1.0
)

ht.convert_ac_line_to_hvdc_system(
    htg,
    branch_id=6,
    loss_fwd=1.0,
    loss_bwd=1.0,
    q_to_p_ratio=0.35,
    base_kv_map={230.0: 325.0},
    capacity_factor=1.0
)
```

The conversion introduces 3 DC buses and 3 AC/DC converters and updates the branch data, which can be seen by inspecting the scenario data:

```python
print(htg)
```

Finally, let's analyze the impact of the conversion on the system's performance in terms of the following two aspects:

- Economic efficiency: Can this flexibilization measure reduce the injection costs?

    ```python
    cost = []
    for scenario in [acg, htg]:
        result = ht.calc_opf(scenario)
        cost.append(result.get_total_injection_cost())
        print(result.details)
        print(result)
    print("Injection cost reduction: {:.1%}".format(1 - cost[1] / cost[0]))
    ```
    
    We can observe a significant reduction of the injection cost, which is due to the different utilization of injector 3 that exhibits the lowest marginal costs. In the original system, it's utilization is restricted by congestion, while it is operated at maximum capacity in the hybrid system. Note that the total losses in the hybrid system are higher than in the original system, which is not only due to the converter losses but also due to the "power flow routing" enabled by the grid flexibilization, where power may flow along (electrically) longer distances, cf. the branch result and losses for both systems. Here, the cost of the additional losses is outweighed by the improved utilization of the injectors. 
    
- Transmission capacity: Can this flexibilization measure increase the effective capacity?

    ```python
    loadability = []
    for scenario in [acg, htg]:
        result = ht.calc_loadability(scenario)
        loadability.append(1 + result.load_increment_scaling)
        print(result)
    print("Loadability improvement: {:.1%}".format(loadability[1] / loadability[0] - 1))
    ```
    
    We can observe a significant improvement in the maximum loadability and, even more importantly, that the hybrid system is *not* limited by congestion but by the available generation capacity. This is even the case if the generation capacity is increased, e.g., by 20% via

    ```python
    for scenario in [acg, htg]:
        for cap in scenario.injector['cap']:
            cap.scale(1.2)
    ```
    
    If the above experiment is repeated, it can be observed that the loadability improvement is substantially higher and that the hybrid system is still *not* limited by congestion.

These results illustrate that the flexibility introduced by the conversion of AC lines to DC operation may significantly improve the performance of a congested system and confirm the findings in [this paper](https://ieeexplore.ieee.org/document/7414517). Regarding the latter, it shall be mentioned that the results for the adapted PJM system deviate due to different branch flow limits, see "[Import Grid Data from the MATPOWER Format](#import-grid-data-from-the-matpower-format)".


### Adding an HVDC System

In the following, it is illustrated how an HVDC system may be added to a grid model by exchanging the 3-terminal HVDC system by two P2P-HVDC systems. To this end, we first load the scenario from the database

```python
scenario = ht.load_scenario(database)
```

where we can see that the 3-terminal HVDC system comprises the buses 6 to 8

```python
scenario.get_dc_subgrids()
```

which are connected by the branches 5 and 6:

```python
scenario.branch.loc[scenario.branch[['src', 'dst']].isin([6, 7, 8]).any(axis='columns')]
```

To set the scene, we backup the series resistance and rating of branch 6 and remove bus 8, which also removes all the connected entities:

```python
z_bar, rating = scenario.branch.loc[6, ['z_bar', 'rating']]
scenario.remove_buses([8])
print(scenario)
```

We can see that a P2P-HVDC system between the AC buses 3-4 remains and we now introduce a P2P-HVDC system between the AC buses 4-5 by adding 2 DC buses, the respective AC/DC converters, and the DC line:

```python
dc_bus_src = scenario.add_bus(
    type_=ht.BusType.DC,
    base_kv=325.0,
    v_min=0.9,
    v_max=1.1,
    zone=1
)

dc_bus_dst = scenario.add_bus(
    type_=ht.BusType.DC,
    base_kv=325.0,
    v_min=0.9,
    v_max=1.1,
    zone=1
)

cap_src = ht.ConverterCapRegion(
    p_bnd=[-rating, rating],
    q_bnd=[-0.35*rating, 0.35*rating]
)

cap_dst = ht.ConverterCapRegion(
    p_bnd=[-rating, rating]
)

scenario.add_converter(
    src=4,
    dst=dc_bus_src,
    cap_src=cap_src.copy(),
    cap_dst=cap_dst.copy(),
    loss_fwd=1.0,
    loss_bwd=1.0
)

scenario.add_converter(
    src=5,
    dst=dc_bus_dst,
    cap_src=cap_src.copy(),
    cap_dst=cap_dst.copy(),
    loss_fwd=1.0,
    loss_bwd=1.0
)

scenario.add_branch(
    type_=ht.BranchType.LINE,
    src=dc_bus_src,
    dst=dc_bus_dst,
    z_bar=z_bar,
    rating=rating
)

scenario.grid_name += " (P2P-HVDC Systems)"
scenario.description = scenario.database_uri = ""
```

Concluding, let's verify and inspect the resulting scenario and compute an OPF:

```python
scenario.verify()
print(scenario)
print(ht.calc_opf(scenario))
```


## Feature- and Structure-Preserving Network Reduction

For large-scale power systems, repeated optimal power flow studies, e.g., in grid expansion planning, are often computationally highly demanding due to the extensive model complexity. To this end, *hynet* includes the feature- and structure-preserving network reduction proposed in [this paper](http://arxiv.org/abs/1903.11590) to appropriately reduce the model complexity and streamline such studies. Based on a (peak load) reference scenario, this method utilizes a collection of topological, electrical, and market-based approaches to identify subgrids that are suitable for reduction, which are then selectively reduced while preserving the surrounding structure and designated features of the grid. In the following, the utilization of this network reduction method is illustrated by reproducing the results [in this paper](http://arxiv.org/abs/1903.11590) for the German grid (Please note that those results are based on the *hynet* Grid Database Library v1.0). It is assumed that **IPOPT is installed**, that a Python shell was started in a directory that contains the [grid databases](https://gitlab.com/tum-msv/hynet-databases), and that the following commands were executed:

```python
import hynet as ht
import hynet.reduction.large_scale as nr
database = ht.connect('germany2030nep.db')
```

Additionally, to track the progress, it is recommended to enable the logging of info messages via

```python
import logging
logging.basicConfig(level=logging.INFO)
```

**Remarks:**

- In the parameter sweeps below, a *hynet* optimization server may be utilized. See also [Distributed Computation of Optimal Power Flows](#distributed-computation-of-optimal-power-flows).

- *hynet* also includes support for the reduction to a "copper plate" model, see ``hynet.reduction.copper_plate``.


### Selection of Reduction Parameters

This reduction method comprises a feature definition and three subsequent stages, i.e., topological, electrical, and market-based reduction, which are discussed below. Prior to these stages, the reference scenario is loaded and an OPF reference is computed:

```python
scenario = ht.load_scenario(database)
opf_reference = ht.calc_opf(scenario.copy())
print(opf_reference)
```

#### 1. Feature Definition:

Features are entities in the model that are essential to the application-relevant accuracy and validity of the derived results and conclusions. To this end, the ``bus`` and ``branch`` data frame of the scenario is equipped with an additional Boolean-valued column ``feature`` that declares such features. In order to add the proposed features in [the paper](http://arxiv.org/abs/1903.11590) to the scenario, call

```python
nr.add_standard_features(scenario, opf_reference)
```

The ``feature`` columns may also be modified to further customize the feature definition.

#### 2. Topology-Based Reduction:

In order to perform the topology based reduction, call

```python
nr.reduce_by_topology(scenario)
```

This reduces single buses, lines of buses, and small "islands" at the boundary of the grid. To parameterize the "island" reduction process, please refer to the optional parameter ``max_island_size``. The identification of "islands" can be computationally demanding and may be skipped using ``max_island_size=0``. Finally, the reduction accuracy is evaluated by

```python
evaluation = nr.evaluate_reduction(opf_reference, ht.calc_opf(scenario))
print(evaluation)
```

Please refer to the function's documentation for more information on the evaluation data.

#### 3. Electrical Coupling-Based Reduction:

This reduction step combines buses that are connected via a low series impedance, where "low" is defined by a threshold relative to the maximum series impedance modulus. To identify a proper parameterization, a sweep may be performed to select an adequate threshold:

```python
evaluation = nr.sweep_rel_impedance_thres(scenario,
                                          opf_reference=opf_reference)
print(evaluation)
```

Using the generated visualization or tabular representation, a threshold may be selected. In the vicinity of injectors, this reduction may introduce more pronounced errors, due to which a [heuristic feature refinement](http://arxiv.org/abs/1903.11590) based on the depth to critical injectors should be considered. To this end, a more ambitious selection of the threshold may be made, for example ``0.05``, and additional features may be added based on a certain depth from critical injectors. To identify a proper depth, an additional sweep is performed:

```python
evaluation = nr.sweep_feature_depth(scenario,
                                    rel_impedance_thres=0.05,
                                    opf_reference=opf_reference)
print(evaluation)
```

Using the generated visualization or tabular representation, an appropriate depth may be selected. For example, ``4`` is appropriate here and the respective reduced scenario is extracted from the evaluation data using

```python
scenario = evaluation.at[4, 'opf'].scenario
```

#### 4. Market-Based Reduction:

This approach reduces subgrids that exhibit a similar locational marginal price (LMP) or, more precisely, dual variable of the nodal active power balance. As the characteristic range for the LMP is rather specific to a scenario, it may be reasonable to inspect it beforehand (Please note that the LMP profile of this example is quite "messy" as some renewables with zero marginal cost are not fully utilized):

```python
ht.show_lmp_profile(ht.calc_opf(scenario))
```

To select an appropriate price threshold, a parameter sweep may be performed, where the sweep range is based on the previously inspected LMP profile:

```python
import numpy as np
sweep_values = list(np.around(np.linspace(0.02, 0.2, 10), decimals=2))
evaluation = nr.sweep_max_price_diff(scenario,
                                     values=sweep_values,
                                     opf_reference=opf_reference)
print(evaluation)
```

Using the generated visualization or tabular representation, an appropriate price threshold is selected, for example ``0.08``. In the following, this parameter selection is utilized in a combined reduction process and the reduced model is stored to a grid database.


### Performing and Saving a Network Reduction

Once the reduction parameters are selected, a combined reduction process may be initiated to generate the reduced model and to evaluate the individual reduction stages:

```python
scenario = ht.load_scenario(database)
evaluation, bus_id_map = nr.reduce_system(scenario,
                                          rel_impedance_thres=0.05,
                                          feature_depth=4,
                                          max_price_diff=0.08,
                                          show_evaluation=True,
                                          return_bus_id_map=True,
                                          preserve_aggregation=True)
print(evaluation)
```

This function automatically adds the standard features prior to the reduction if no features are specified. If custom features are utilized, they must be defined prior to the call of ``reduce_system``. After the reduction, ``scenario`` represents the reduced model and contains the information on aggregated buses in the column ``aggregation`` of the bus data frame, i.e., it specifies which buses were aggregated to the respective retained bus:

```python
print(scenario.bus['aggregation'].head(n=10))
```

This aggregation information is additionally stored in the bus annotation to preserve it when the model is stored to a grid database. 

```python
print(scenario.bus['annotation'].head(n=10))
```

Note that the reduction process only removes buses and branches, while all other entities are retained with the same ID and may be updated, e.g., the terminal bus of injectors within a reduced subgrid is set to the respective representative bus.

Finally, the model's name is updated and the reduced model is stored to a new database, alongside the scenarios of the original system:

```python
scenario.grid_name = 'Reduced ' + scenario.grid_name
database_nr = ht.connect('germany2030nep_nr.db')
ht.initialize_database(database_nr, scenario)
ht.copy_scenarios(database, database_nr, bus_id_map=bus_id_map)
```


### Loading a Scenario of a Reduced Model

Loading a scenario of a reduced model follows the same procedure as with any other grid database, for example

```python
database_nr = ht.connect('germany2030nep_nr.db')
scenario = ht.load_scenario(database_nr)
```

However, if the information on aggregated buses in the column ``aggregation`` of the bus data frame is required, it must be restored from the bus annotation:

```python
nr.restore_aggregation_info(scenario)
```


## Miscellaneous Aspects


### Visualization and Specification of Capability Regions

As the specification and conception of injector and converter capability regions is somewhat intricate, *hynet* includes a GUI for their visualization. For this GUI, [TkInter](https://wiki.python.org/moin/TkInter) must be installed, which may be done e.g. with [Conda](https://conda.io) by running

```sh
conda install tk
```

in the terminal. In case you are using MAC OS X, please be aware of [this issue](https://stackoverflow.com/questions/32019556/matplotlib-crashing-tkinter-application) (Set ``matplotlib``'s backend to ``TkAgg`` *before* importing *hynet*).

To demonstrate this GUI, open a Python shell, connect to the example database, and load the default scenario:

```python
import hynet as ht
database = ht.connect('pjm_hybrid.db')
scenario = ht.load_scenario(database)
```

For example, to display the parameter description and edit the capability region of injector 1, call

```python
help(ht.CapRegion)
scenario.injector.at[1, 'cap'].edit()
```

The GUI can also be used to display the operating point obtained by an OPF in the capability region. For example, for injector 2 this is achieved with

```python
result = ht.calc_opf(scenario)
scenario.injector.at[2, 'cap'].show(result.injector.at[2, 's'])
```
