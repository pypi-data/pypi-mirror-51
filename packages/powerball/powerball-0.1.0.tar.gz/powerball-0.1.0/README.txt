PowerBall: A Tool for Competitive Lottery Analysis of Bacterial Groups
By Matthew Marshall and John L. Darcy

What is competitive lottery analysis?

	A competitive lottery environment is one where many species are competing for dominance of a small number of sites or patches. Species in these environments will either dominate a site, forcing all other species out, or will coexist with other species on that patch. Two important metrics here are competitiveness, which we define as the degree to which a group is consistently dominated by a small number of species within that group, and lottery-ness, which is the extent to which the same species will always dominate within a particular group of species. Competitive lottery analysis allows us to explore those metrics by analyzing population data to see which species, or groups of species, are competitive, how competitive they are relative to other species, and how deterministically they dominate their groups.

Powerball:

Powerball is a Python 3 command-line tool that can be used to perform competitive lottery analysis of user-defined groups of species using Monte Carlo Simulation. It was developed for a research project as part of the Colorado Biomedical Informatics Summer Training Fellowship at the University of Colorado Anschutz Medical Campus. The use-cases for PowerBall are varied, and clinically relevant. For example, users can find which bacteria are competing with potential pathogens, and the extent to which that competition regularly occurs. Both the competitiveness and lottery-ness results of this analysis could inform patient outcome predictions as well as potential treatment plans. This knowledge provides valuable medical insight and may help inform the discovery of novel or probiotic treatments and inform treatment decisions for known pathogens. Additionally, PowerBall can be used in an ecological research framework using many different samples to better examine how competitiveness and/or lottery-ness change across environments or across patients or across time.

Usage:
	Powerball takes one argument: the name of an input csv file where each row represents a species and each column represents a sample of population data about that species. The final column of the table is a string used for grouping species based on some user-defined grouping parameter. For example, you could decide that all species that are taxonomically similar belong in the same group. An example of what an input file should look like is given in data/example.csv

	Powerball has a default minimum group size of 3 species, this can be changed through the command-line argument --groupSize

	Basic usage for Powerball is ‘python powerball.py filename.csv’
This will show the competitiveness score, lottery score, and p-values for all groups, all rounded to 4 decimal places.
For more advanced usage, Powerball has many different command line arguments. A full list can be shown by running ‘python powerball.py --help’ or ‘python powerball.py -h’

Powerball automatically generates an interactive graph of the output data using Bokeh (can be silenced using the --chartStyle argument)
	
