import pytest
import scenario_tool_interface.sti as sti
import json
import time
from .credentials import USERNAME, PASSWORD

__author__ = "Christian Urich"
__copyright__ = "Christian Urich"
__license__ = "mit"


def test_login():
    assert type(sti.login(USERNAME, PASSWORD)) is str
    with pytest.raises(Exception) as e_info:
        sti.login(USERNAME, "passwod")


def test_get_region():
    token = sti.login(USERNAME, PASSWORD)

    assert type(sti.get_region(token, "melbourne")) is int

    with pytest.raises(Exception) as e_info:
        sti.login(sti.get_region(token, "melbourn"))


def test_get_assessment_model():
    token = sti.login(USERNAME, PASSWORD)

    assert type(sti.get_assessment_model(token, "Land Surface Temperature")) is int

    with pytest.raises(Exception) as e_info:
        sti.login(sti.get_assessment_model(token, "Land Surface Temperatur"))


def test_nodes():
    # Login with your username and password
    token = sti.login(USERNAME, PASSWORD)

    assert type(token) is str

    model_id = sti.upload_dynamind_model(token, "test node", "../resources/nodes/test_node.dyn")

    assert type(model_id) is int

    node_id = sti.create_node(token, "../resources/nodes/test_node.json", model_id)

    assert type(node_id) is int

    n_id = sti.get_node_id(token, "test node")

    assert type(n_id) is int

    with pytest.raises(Exception) as e_info:
        sti.get_node_id(token, "test nod")

    model_id = sti.upload_dynamind_model(token, "test node", "../resources/nodes/test_node.dyn")

    assert type(model_id) is int

    node_version_id = sti.update_node(token, node_id, "../resources/nodes/test_node.json", model_id)

    assert type(node_version_id) is int


def test_assessment_models():
    # Login with your username and password
    token = sti.login(USERNAME, PASSWORD)

    assert type(token) is str

    model_id = sti.upload_dynamind_model(token, "test node", "../resources/assessment_nodes/test_assessment_model.dyn")

    assert type(model_id) is int

    node_id = sti.create_assessment_model(token, "../resources/assessment_nodes/test_assessment_model.json", model_id)

    assert type(node_id) is int

    model_id = sti.upload_dynamind_model(token, "test node", "../resources/assessment_nodes/test_assessment_model.dyn")

    assert type(model_id) is int

    node_version_id = sti.update_assessment_model(token, node_id, "../resources/assessment_nodes/test_assessment_model.json", model_id)

    assert type(node_version_id) is int


def test_run_tutorial():
    # Login with your username and password
    token = sti.login(USERNAME, PASSWORD)

    assert type(token) is str
    # Create a new project
    project_id = sti.create_project(token)
    assert type(project_id) is int

    # Obtain region code
    region_id = sti.get_region(token, "melbourne")
    assert type(region_id) is int

    # Load geoson file
    with open("../resources/test.geojson", 'r') as file:
        geojson_file = json.loads(file.read())

    # Upload boundary
    geojson_id = sti.upload_geojson(token, geojson_file, project_id)

    # Set project parameters
    sti.update_project(token, project_id, {
        "name": "my project",
        "active": True,
        'region_id': region_id,
        "case_study_area_id": geojson_id,
    })

    # Add assessment models
    lst_model = sti.get_assessment_model(token, "Land Surface Temperature")
    assert type(lst_model) is int

    # Set assessment models
    sti.set_project_assessment_models(token, project_id, [{"assessment_model_id": lst_model}])

    # Create and run baseline
    baseline_id = sti.create_scenario(token, project_id, None)
    assert type(baseline_id) is int
    sti.execute_scenario(token, baseline_id)

    # Scenarios are executed asynchronous.
    while True:
        # A status code smaller than 7 means the simulation is still executed.
        r = sti.check_status(token, baseline_id)
        status = r["status"]
        if status > 6:
            break
        time.sleep(1)


    # Print a list of available nodes
    sti.show_nodes(token)

    #Get residential node id
    nodes = sti.get_nodes(token)
    n_id = -1
    for n in nodes:
        if n["name"] == "Residential":
            n_id = n["id"]


    # Nodes are defined as below
    residential_node = {
        "node_type_id": n_id,
        "area": geojson_id,
        "parameters":
            {
                "dance4water_building.site_coverage": 0.6,
                "dance4water_number_of_trees.equation": 1,
                "dance4water_tree_spacing.equation": 22
            }
    }

    nodes = []
    # Several nodes can are combined to a workflow be adding them to a vector. The
    # nodes are executed in the order the are added
    nodes.append(residential_node)

    # Scenarios need a parent. In this case we use the base line scenario created before
    baseline_scenario_id = sti.get_baseline(token, project_id)

    # Crate a new scenario
    scenario_id = sti.create_scenario(token, project_id, baseline_scenario_id, "my new scenario")
    assert type(scenario_id) is int
    # Set workflow
    sti.set_scenario_workflow(token, scenario_id, nodes)

    # Execute scenario
    sti.execute_scenario(token, scenario_id)

    # Scenarios are executed asynchronous
    while True:
        # A status code smaller than 7 means the simulation is still executed.
        r = sti.check_status(token, scenario_id)
        status = r["status"]
        if status > 6:
            break

        time.sleep(1)

    while True:
        r = sti.run_query(token,
                          scenario_id,
                          "SELECT avg(tree_cover_fraction) as tf from micro_climate_grid")

        if r['status'] == 'loaded':
            # Break the loop when query is loaded
            break
        time.sleep(1)

    print(r['data'])
