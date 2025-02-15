# Repository for ss24.2.1/team147

**Topic:** SS24 Assignment 2.1: Compute Blood Types

**Description**
Objective: Use Bayesian networks to calculate the probability of an individual having a specific blood type based on the blood types of their relatives.

Background on ABO Blood Group System:
    Blood Types: A (A antigens), B (B antigens), AB (both A and B antigens), O (neither A nor B antigens).
    Importance: Crucial for safe blood transfusions.
    ABO Gene Alleles: A, B, and O.
    Inheritance: Each person has two alleles, one from each parent. The A and B alleles are co-dominant, while O is recessive.
    Possible Combinations: AA (A), AO (A), AB (AB), BO (B), BB (B), OO (O).

**Dependencies**
To install the required libraries, you can use the requirements.txt file that provided. Run the following command to install all dependencies:

`pip install -r requirements/txt `

Main Libraries from the Script:

1. 'pgmpy'
'pgmpy' is a library for working with probabilistic graphical models (PGMs), including Bayesian Networks and Markov Networks.

- Usage in the Code:
BayesianNetwork: Used to define the structure of the Bayesian Network. The 'BayesianNetwork' class is instantiated to create an empty model to which nodes and edges (representing variables and their dependencies) are added.

TabularCPD: Used to define the Conditional Probability Distributions (CPDs) for the variables in the network.
In this case, there are two main distributions such that; parents' alleles-if the query has parent- and, the country-if there aren't any parent-.

VariableElimination: Instances of 'TabularCPD' are created to specify the probability tables for the variables, given their parent variables or countries.

2. 'networkx'
A Python library for the creation, manipulation, and study of complex networks of nodes and edges.

- Usage in the Code:
DiGraph: Used to represent the family tree, where nodes are individuals and directed edges represent parental relationships.

**How to Run the Code**
1. Ensure you have Python 3.8 or higher.
2. Install the dependencies via the command mentioned above.
3. Place your problem file (such as, 'problem-a-00.json') in the "problems" directory.
4. Run the main script:

`python main.py`

The script will read the input JSON file, build the Bayesian Network model, perform inference based on the queries, and will print the results. 

**Repository Structure**
Repository is structured as followed:  

- **'example-problems/'** is the directory contains JSON files with example problem definitions.
- **'example-solutions/'** is the directory contains JSON files with solution definitions to example problems.
- **'problems/'** is the directory contains JSON files with problem definitions.
- **'main.py'** is the main script to run the Bayesian Network inference. 
- **'requirements.txt'** is the file contains the list of dependencies.
- **'README.md'** is this file, provides information about the project.
- **'solution_check.py'** is the python file script to check the solution in the project script.


Input file format

- 'family_tree' is a list of dictionaries that represent family relations(Mother, father and child).
- 'country' is a string that indicates the counties (North Wumponia, South Wumponia).
- 'test-results' is a list of dictionaries that represent the results (A, B, O, AB).
- 'queries' is a list of dictionaries that represent the queries to be solved. 

Example of the input JSON Structure:
`{
    "family-tree": [
        {"relation": "father-of", "subject": "Ayansh", "object": "Maria"},
        {"relation": "mother-of", "subject": "Amanda", "object": "Maria"}
    ],
    "country": "North Wumponia",
    "test-results": [
        {"person": "Ayansh", "result": "A"},
        {"person": "Amanda", "result": "B"}
    ],
    "queries": [
        {"person": "Maria"}
    ]
}`

Output

The script outputs the inferred blood type distributions for the queried individuals.

**Solution summary**

To solve this problem, the initial approach involved calculating probabilities manually to understand the solution. However, as the family trees grew, a more scalable method was needed. After consulting with the TA, the pgmpy library was chosen to create a Bayesian Network (BN) and calculate the Conditional Probability Distribution (CPD) for the nodes. We struggled with TabularCPD for a while until we understood the parameters, but using pgmpy became easier once this was resolved.

Designing the BN architecture was tricky because each person has two alleles and a blood type, all of which are interconnected and linked to their parents' alleles. Initially, using only alleles did not work, so a blood type node was added. The country of the individuals also needed to be included in the BN as it would be used as evidence for the queries.

Only the blood type test was implemented, and the other two tests were not, meaning those parts of the problem do not give the correct solution. Another issue encountered was querying about the same person for whom there was evidence, as this caused errors with the pgmpy library.

In summary, while pgmpy helped construct and manipulate the BN, designing a comprehensive and error-free model required careful consideration of node connections and evidence handling. The implementation of the blood type test demonstrates the potential of this approach, but further work is needed to include additional tests and resolve querying issues for a fully functional solution.