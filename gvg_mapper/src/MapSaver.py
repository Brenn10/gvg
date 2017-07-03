#!/usr/bin/python
import os
import rospy
import pickle
from gvg_mapper.msg import GVGNode,GVGEdgeMsg

'''
MapSaver.py

Brennan Cain

This class takes updates from publishes to `node` and `edge` and save all nodes and edges to a data file. Every update interval, it checks if there has been a change, and if there has been, it prints to the file. 

'''


## MapSaver class
#
# Handles the node and all saving stuff
class MapSaver():

	## Creates a directory if not exists and checks access
	#
	# @param save_dir directory to place map files
	# 
	# @return boolean success flag
	def create_dir(self):
		try:#if can create and access, good
			if not os.path.exists(self.save_dir):
				os.makedirs(self.save_dir)
			if os.access(self.save_dir, os.W_OK):
				return True
			else:
				rospy.logerr("Could not open directory for map saving. ERR: 1")
		
		except IOError: #if cannot access, bad
			rospy.logerr("Could not open directory for map saving. ERR: 2")
		return False
		
	## Dumps the nodes and edges to file
	#
	# @param name name of file
	def dump(self,name):
		#safely concatenate paths
		completePath=os.path.join(self.save_dir,name+".map")

		#dump information to file and close
		with open(completePath,"w") as f:
			pickle.dump((self.nodes.values(),self.edges.values()), f, pickle.HIGHEST_PROTOCOL)
		rospy.loginfo("Saved a map update")

	## What to do on death
	#
	# Sets alive to false and dumps to final.map
	def die(self):
		if(self.clean_open):
			self.dump("final")
		self.alive=False
	## Handles receiving a node
	#
	# @param node GVGNode from subscription to /node
	def node_handler(self,node):
		self.nodes[node.node_id]=node
		self.updated=True
	
	## Handles receiving a node
	#
	# @param edge GVGEdgeMsg from subscription to /node
	def edge_handler(self,edge):
		self.edges[edge.edge_id]=edge
		self.updated=True

	## Default constructor
	def __init__(self):
		#start node
		rospy.init_node("map_saver")
		rospy.on_shutdown(self.die)

		#get parameters from server
		self.save_dir = rospy.get_param("map_save_dir","map_log/") #default to .ros/map_log
		update_rate = rospy.get_param("map_save_update_rate",120) #update once every 2 min
		#create directory and set clean_open
		self.clean_open=self.create_dir()

		#create dictionaries
		self.edges={} #dictionary of edge_id:edge_obj
		self.nodes={} #dictionary of node_id:node_obj

		#begin listening
		rospy.Subscriber("/node",GVGNode, self.node_handler)
		rospy.Subscriber("/edge",GVGEdgeMsg, self.edge_handler)

		self.updated=False

		#while alive and able to open the file
		self.alive=True
		while(self.clean_open and self.alive):
			if(self.updated):
				self.dump(str(rospy.get_time()))
				self.updated=False
			rospy.sleep(update_rate)
MapSaver()
