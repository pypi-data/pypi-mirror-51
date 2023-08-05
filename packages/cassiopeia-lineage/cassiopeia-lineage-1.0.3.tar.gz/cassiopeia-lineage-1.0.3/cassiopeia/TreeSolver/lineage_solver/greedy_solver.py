from collections import defaultdict
import networkx as nx
import numpy as np
import hashlib

from .solver_utils import root_finder

def greedy_build(nodes, priors=None, cutoff=200, considered=set(), uniq='', targets=[]):
	"""
	Greedy algorithm which finds a probable mutation subgraph for given nodes.
	This algorithm chooses splits within the tree based on which mutation occurs most frequently,
	weighted by the prior probabilities of each mutation state for each character.
	Strings with NA ('-') as a state in the split character are segregated with the
	set of nodes which they most closely match to w.r.t. all other characters.

	:param nodes:
		A list of target nodes, where each node is in the form 'Ch1|Ch2|....|Chn'
	:param priors:
		A nested dictionary containing prior probabilities for [character][state] mappings
		where characters are in the form of integers, and states are in the form of strings,
		and values are the probability of mutation from the '0' state.
	:param cutoff:
		A cutoff that tells the greedy algorithm to stop, and return a partial sub-tree
		Set to -1 to run through to the individual samples (ie return the full tree)

	:param considered:
		Internal parameter which keeps track of which mutations have been considered in a set
		DO NOT MODIFY
	:param uniq:
		Internal parameter which keeps track of the path of mutations (1 = mutation taken, 0 = mutation not taken)
		DO NOT MODIFY
	:return:
		Returns a graph which contains splits as nodes in the form "character state (uniq_identifier)", and leaves
		as either samples, or the roots of the subsets of samples that need to be considered by another algorithm.
		Edges are labeled with the corresponding mutation taken
		AND
		a list in the form [[sub_root, sub_samples],....] which is a list of subproblems still needed to be solved
	"""

	# Tracks frequency of states for each character in nodes
	character_mutation_mapping = defaultdict(int)

	# G models the network that is returned recursively
	G = nx.DiGraph()

	root = root_finder(nodes)

	# Base case check for recursion, returns a graph with one node corresponding to the root of the remaining nodes
	if len(nodes) <= cutoff or len(nodes) == 1:
		root = root_finder(nodes)
		G.add_node(root)
		return G, [[root, nodes]]

	# Accounting for frequency of mutated states per character, in order to choose the best split
	for node in nodes:
		node_list = node.split("_")[0].split('|')
		for i in range(0, len(node_list)):
			char = node_list[i]
			if char != '0' and char != '-':
				character_mutation_mapping[(str(i), char)] += 1
                        #if char != '0':
                        #    if char == "-":
                        #        character_mutation_mapping[(str(i), char)] -= 1
                        #    else:
                        #        character_mutation_mapping[(str(i), char)] += 1

	# Choosing the best mutation to split on (ie character and state)
	character, state = 0, 0
	max_cost = 0

	min_prior = 1
	if priors:
		for i in priors.keys():
			for j in priors[i].keys():
				min_prior = min(min_prior, priors[i][j])

	for i,j in character_mutation_mapping:
		if not (i,j) in considered:
			if not priors:
				if max_cost < character_mutation_mapping[(i, j)]:
					max_cost = character_mutation_mapping[(i, j)]
					character, state = i, j
			else:
				if j not in priors[int(i)]:
					priors[int(i)][j] = min_prior
				if max_cost < -np.log(priors[int(i)][j]) * character_mutation_mapping[(i, j)]:
					max_cost = -np.log(priors[int(i)][j]) * character_mutation_mapping[(i, j)]
					character, state = i, j
	character = int(character)


	# If there is no good split left, stop the process and return a graph with the remainder of nodes
	if character == 0 and state == 0:
		if len(nodes) == 1:
			G.add_node(nodes[0])
		else:
			for i in range(0, len(nodes)):
				if nodes[i] != root:
					G.add_edge(root, nodes[i])
		return G, []

	# Splitting nodes based on whether they have the mutation, don't have the mutation, or are NA('-') in that character
	# Right split is where nodes with the mutation go, everyone else goes to left split or NA chars
	left_split, right_split, NA_chars = [], [], []
	right_split_temp = []
	left_split_temp = []
	for node in nodes:
		node_list = node.split('|')
		if node_list[character] == state:
			right_split.append(node)
		elif node_list[character] == '-':
			NA_chars.append(node)
		else:
			left_split.append(node)


	# Seperates all nodes with NA in the character chosen to be split upon
	# Puts in right split or left split based on which list shares more mutated characters with this string
	for node in NA_chars:
		right_split_score = 0
		left_split_score = 0
		node_list = node.split('|')
		num_not_missing = len([n for n in node_list if n != "-"])
		for i in range(0, len(node_list)):
			if node_list[i] != '0' and node_list[i] != '-':
				for node_2 in left_split:
					node2_list = node_2.split('|')
					if node_list[i] == node2_list[i]:
						left_split_score += 1
				for node_2 in right_split:
					node2_list = node_2.split('|')
					if node_list[i] == node2_list[i]:
						right_split_score += 1

		avg_left_split_score = left_split_score / float(len(left_split) * num_not_missing + 1)
		avg_right_split_score = right_split_score / float(len(right_split) * num_not_missing + 1)

		if avg_left_split_score < avg_right_split_score:
			right_split_temp.append(node)
		else:
			left_split_temp.append(node)

	right_split += right_split_temp
	left_split += left_split_temp

	# Add character, state that split occurred to already considered mutations
	considered.add((str(character), state))
	G = nx.DiGraph()
	#splitter = str(character) + " " + str(state) + " (" + uniq + ")"
	splitter = root

	# Recursively build left side of network (ie side that did not mutation at the character with the specific state)
	G.add_node(splitter)
	left_subproblems = []
	left_network = None
	if len(left_split) != 0:
		left_root = root_finder(left_split)
		# if left_root not in left_split and left_root in targets:
		# 	left_root = left_root + "_unique"

		left_network, left_subproblems = greedy_build(left_split, priors, cutoff, considered.copy(), uniq + "0", targets=targets)

		left_nodes = [node for node in left_network.nodes() if left_network.in_degree(node) == 0]
		dup_dict = {}
		for n in left_network:
			if n in list(G.nodes()) and n != left_root:
				dup_dict[n] = n + "_" + str(hashlib.md5(left_root.encode('utf-8')).hexdigest())
		left_network = nx.relabel_nodes(left_network, dup_dict)
		G = nx.compose(G, left_network)
		if root != left_root:
			G.add_edge(splitter, left_root, weight=0, label="None")

	# Recursively build right side of network
	right_network, right_subproblems = greedy_build(right_split, priors, cutoff, considered.copy(), uniq + "1", targets=targets)
	right_nodes = [node for node in right_network.nodes() if right_network.in_degree(node) == 0]
	right_root = root_finder(right_split)

	dup_dict = {}
	for n in right_network:
		if n in list(G.nodes()) and n != right_root:
			dup_dict[n] = n + "_" + str(hashlib.md5(right_root.encode('utf-8')).hexdigest())
	for n in dup_dict:
		rename_dict = {n: dup_dict[n]}
		if right_network.out_degree(n) != 0:
			right_network = nx.relabel_nodes(right_network, rename_dict)
		else:
			rename_dict = {n: dup_dict[n]}
			G = nx.relabel_nodes(G, rename_dict)

	G = nx.compose(G, right_network)
	# if right_root not in right_split and right_root in targets:
	# 	right_root = right_root + "_unique"
	#for node in right_nodes:
	if root != right_root:
		if not priors:
			G.add_edge(splitter, right_root, weight=1, label = str(character) + ": 0 -> " + str(state))
		else:
			G.add_edge(splitter, right_root, weight=-np.log(priors[int(character)][state]), label=str(character) + ": 0 -> " + str(state))


	return G, left_subproblems + right_subproblems
