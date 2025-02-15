from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import json
import matplotlib.pyplot as plt
import networkx as nx
import os

def solve(filename):
    with open(f'problems/{filename}', 'r') as file:
        data = json.load(file)

    family_tree = data['family-tree']
    country = data['country']
    tests = data['test-results']
    queries = data['queries']

    model = BayesianNetwork()
    relations_model = nx.DiGraph()

    # [{'relation': 'father-of', 'subject': 'Ayansh', 'object': 'Maria'}, 
    # {'relation': 'mother-of', 'subject': 'Amanda', 'object': 'Maria'}]
    for relation in family_tree:
        sub = relation['subject']
        obj = relation['object']
        relations_model.add_nodes_from([sub,obj])
        relations_model.add_edge(sub,obj)

    model.add_node("country")
    country_cpd = TabularCPD(variable= 'country', variable_card=2, values=[[0.5],[0.5]])
    model.add_cpds(country_cpd)

    for node in relations_model.nodes():
        model.add_nodes_from([f"{node}_A1",f"{node}_A2",f"{node}_BT"])
        model.add_edges_from([(f"{node}_A1",f"{node}_BT"),(f"{node}_A2",f"{node}_BT")])
        parents = list(relations_model.predecessors(node))
        if len(parents) == 2: # If we have info on two parents.
            for i,parent in enumerate(parents):
                model.add_nodes_from([f"{parent}_A1",f"{parent}_A2",f"{parent}_BT",f"{node}_A1",f"{node}_A2",f"{node}_BT"])
                model.add_edges_from([(f"{parent}_A1", f"{node}_A{i+1}"), (f"{parent}_A2", f"{node}_A{i+1}"),
                                        (f"{parent}_A1",f"{parent}_BT"),(f"{parent}_A2",f"{parent}_BT"),
                                        (f"{node}_A1",f"{node}_BT"),(f"{node}_A2",f"{node}_BT")])

                
                allele_cpd = TabularCPD(variable= f"{node}_A{i+1}", variable_card=3,
                                        values= [[1, 0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0], # Probability of A
                                                    [0, 0.5, 0, 0.5, 1, 0.5, 0, 0.5, 0],  # Probability of B
                                                    [0, 0, 0.5, 0, 0, 0.5, 0.5, 0.5, 1]], # Probability of O
                                        evidence=[f"{parent}_A1", f"{parent}_A2"], # AA AB AO BA BB BO OA OB OO
                                        evidence_card=[3, 3])
                model.add_cpds(allele_cpd)

            blood_type_cpd = TabularCPD(variable= f"{node}_BT", variable_card=4,
                                        values=[
                                            [0, 0, 0, 0, 0, 0, 0, 0, 1],  # O
                                            [1, 0, 1, 0, 0, 0, 1, 0, 0],  # A
                                            [0, 0, 0, 0, 1, 1, 0, 1, 0],  # B
                                            [0, 1, 0, 1, 0, 0, 0, 0, 0]  # AB
                                        ],
                                        evidence= [f"{node}_A1", f"{node}_A2"],
                                        evidence_card=[3, 3])
            model.add_cpds(blood_type_cpd)

        elif len(parents) == 1: # If we have info on only one parent.
            parent = parents[0]
            model.add_nodes_from([f"{parent}_A1",f"{parent}_A2",f"{parent}_BT",f"{node}_A1",f"{node}_A2",f"{node}_BT"])
            model.add_edges_from([(f"{parent}_A1", f"{node}_A1"), (f"{parent}_A2", f"{node}_A1"),
                                    (f"{parent}_A1",f"{parent}_BT"),(f"{parent}_A2",f"{parent}_BT"),
                                    (f"{node}_A1",f"{node}_BT"),(f"{node}_A2",f"{node}_BT")])

                
            allele_cpd_A1 = TabularCPD(variable= f"{node}_A1", variable_card=3,
                                    values= [[1, 0.5, 0.5, 0.5, 0, 0, 0.5, 0, 0], # Probability of A
                                                [0, 0.5, 0, 0.5, 1, 0.5, 0, 0.5, 0],  # Probability of B
                                                [0, 0, 0.5, 0, 0, 0.5, 0.5, 0.5, 1]], # Probability of O
                                    evidence=[f"{parent}_A1", f"{parent}_A2"], # AA AB AO BA BB BO OA OB OO
                                    evidence_card=[3, 3])
            model.add_cpds(allele_cpd_A1)

            model.add_edges_from([('country',f"{node}_A2")])
            allele_cpd_A2 = TabularCPD(variable= f"{node}_A2", variable_card=3,
                                        values= [[0.4,0.15], # Probability of A
                                                [0.35,0.55], # Probability of B
                                                [0.25,0.30]], # Probability of O
                                        evidence=['country'], # NW, SW
                                        evidence_card=[2])
            model.add_cpds(allele_cpd_A2)

            blood_type_cpd = TabularCPD(variable= f"{node}_BT", variable_card=4,
                                        values=[
                                            [0, 0, 0, 0, 0, 0, 0, 0, 1],  # O
                                            [1, 0, 1, 0, 0, 0, 1, 0, 0],  # A
                                            [0, 0, 0, 0, 1, 1, 0, 1, 0],  # B
                                            [0, 1, 0, 1, 0, 0, 0, 0, 0]  # AB
                                        ],
                                        evidence= [f"{node}_A1", f"{node}_A2"],
                                        evidence_card=[3, 3])
            model.add_cpds(blood_type_cpd)

        else: # They don't have parents.
            # create a CPD from the probabilities in the assignment.
            model.add_edges_from([('country',f"{node}_A1"),('country',f"{node}_A2")])
            allele_cpd_A1 = TabularCPD(variable= f"{node}_A1", variable_card=3,
                                        values= [[0.4,0.15], # Probability of A
                                                [0.35,0.55], # Probability of B
                                                [0.25,0.30]], # Probability of O
                                        evidence=['country'], # NW, SW
                                        evidence_card=[2])
            
            allele_cpd_A2 = TabularCPD(variable= f"{node}_A2", variable_card=3,
                                        values= [[0.4,0.15], # Probability of A
                                                [0.35,0.55], # Probability of B
                                                [0.25,0.30]], # Probability of O
                                        evidence=['country'], # NW, SW
                                        evidence_card=[2])
            
            model.add_cpds(allele_cpd_A1, allele_cpd_A2)

            allele_cpd_BT = TabularCPD(variable= f"{node}_BT", variable_card=4,
                                        values=[
                                            [0, 0, 0, 0, 0, 0, 0, 0, 1],  # O
                                            [1, 0, 1, 0, 0, 0, 1, 0, 0],  # A
                                            [0, 0, 0, 0, 1, 1, 0, 1, 0],  # B
                                            [0, 1, 0, 1, 0, 0, 0, 0, 0]  # AB
                                        ],
                                        evidence= [f"{node}_A1", f"{node}_A2"],
                                        evidence_card=[3, 3])
            
            model.add_cpds(allele_cpd_BT)
                
    # nx_graph = nx.DiGraph()
    # nx_graph.add_edges_from(model.edges())
    # # pos = nx.shell_layout(nx_graph)  # positions for all nodes
    # nx.draw(relations_model, with_labels = True)
    # # nx.draw(nx_graph, pos, with_labels=True, node_size=3000, node_color="lightgreen", font_size=9, font_color="red", font_weight="bold", arrows=True, arrowsize=20, edge_color="black")
    # plt.title("Bayesian Network", fontsize=20)
    # plt.show()

    model.check_model()


    inference = VariableElimination(model)
    distribution = {'O':0,'A':0,'B':0,'AB':0}
    blood_indx = {'O': 0, 'A': 1, 'B': 2, 'AB': 3}
    country_indx = {'North Wumponia': 0, 'South Wumponia': 1}

    results = []
    # Solve the quieres.
    for query in queries:
        query_person = query['person']
        evidence = {'country': country_indx[country]}
        # Add bloodtypes to evidence.
        for test in tests:
            if test['type'] == 'bloodtype-test':
                evidence[f'{test['person']}_BT'] = blood_indx[test['result']]

            elif test['type'] == 'mixed-bloodtype-test':
                pass
                # person1 = test['person-1']
                # person2 = test['person-2']
                # test_result = test['result']
                # if test_result == "AB":
                #     # evidence[f'{person1}_A1'] = blood_indx['A']
                #     # evidence[f'{person1}_A2'] = blood_indx['B']
                #     # evidence[f'{person2}_A1'] = blood_indx['A']
                #     # evidence[f'{person2}_A2'] = blood_indx['B']
                #     evidence[f'{person1}_BT'] = {
                #                 blood_indx['A']: 0.5,
                #                 blood_indx['B']: 0.5
                #             }
                #     evidence[f'{person2}_BT'] = {
                #                 blood_indx['A']: 0.5,
                #                 blood_indx['B']: 0.5
                #             }
                # else:
                #     evidence[f'{person1}_BT'] = blood_indx[test['result']]
                #     evidence[f'{person2}_BT'] = blood_indx[test['result']]

            elif test['type'] == 'pair-bloodtype-test':
                pass
                # person1 = test['person-1']
                # person2 = test['person-2']
                # test_result1 = test['result-1']
                # test_result2 = test['result-2']
                # evidence[f'{person1}_BT'] = {
                #                 blood_indx[test_result1]: 0.75,
                #                 blood_indx[test_result2]: 0.25
                #             }
                # evidence[f'{person2}_BT'] = {
                #             blood_indx[test_result2]: 0.75,
                #             blood_indx[test_result1]: 0.25
                #         }

        inf_res = inference.query(variables=[f"{query_person}_BT"], evidence= evidence)
        # print('result:', inf_res)
        # print('evidence:', evidence)
        results.append({
            "type": "bloodtype",
            "person": query_person,
            "distribution": {
                "O": inf_res.values[0],
                "A": inf_res.values[1],
                "B": inf_res.values[2],
                "AB": inf_res.values[3]
            }
        })
    problem_no = filename[7:]
    with open(f'solutions/solution{problem_no}', 'w') as json_file:
        json.dump(results, json_file, indent=4)

for filename in os.listdir("problems/"):
    solve(filename)