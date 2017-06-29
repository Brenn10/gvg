#!/usr/bin/python
import os
import shutil
import rospy
from gvg_mapper.msg import GVGNode,GVGEdgeMsg


class MapSaver():
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
		

	def dump(self,name):
		#safely concatenate paths
		completePath=os.path.join(self.save_dir,name+".map")
		#dump information to file and close
		with open(completePath,"w") as f:
			for edge in self.edges.values():
				pickle.dump(edge, f, pickle.HIGHEST_PROTOCOL)
			for node in self.nodes.values():
				pickle.dump(node, f, pickle.HIGHEST_PROTOCOL)
		rospy.loginfo("Saved a map update")

	def die(self):
		if(self.clean_open):
			self.dump("final")
		self.alive=False

	def node_handler(self,node):
		self.nodes[node.node_id]=node
		self.updated=True

	def edge_handler(self,node):
		self.edges[node.edge_id]=edge
		self.updated=True

	def __init__(self):
		#start node
		rospy.init_node("map_saver")
		rospy.on_shutdown(self.die)

		#get parameters from server
		self.save_dir = rospy.get_param("map_save_dir","map_log/") #default to .ros/map_log
		self.update_rate = rospy.get_param("map_save_update_rate",120) #update once every 2 min
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
				dump(str(rospy.get_time()))
				self.updated=False
			rospy.sleep(self.update_rate)
MapSaver()
