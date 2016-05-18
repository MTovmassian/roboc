# coding: utf8
# python3

import time

class GameManager():
	"""
	Classe permettant de créer une partie de jeu. Elle fourni
	les fonctionnalités essentielles pour gérer les déplacements
	du joueur dans le labyrinthe.
	"""

	def __init__(self, mapfile):
		self.player_lat = int()
		self.player_lon = int()
		self.mapfile = mapfile
		self.maze_map = []
		self.maze_map_init = []

	def txtfile_to_list(self):
		"""
		Fonction servant à intégrer dans un système de liste 
		(sous-listes imbriquées dans une méta-liste) chaque 
		ligne d'un fichier texte de labyrinthe.
		"""
		with open(self.mapfile, "r") as maze_txt:
			for elmt in maze_txt:
				self.maze_map.append(list(elmt))
				self.maze_map_init.append(list(elmt))

	def find_and_save_coordinates(self, spot, coordinates_list, map_list):
		"""
		Fonction servant à repérer dans un système de liste la position
		d'un élément et à enregistrer sa latitude (= la position de sa 
		sous-liste par rapport à la méta-liste) et sa longitude (= sa position
		à l'intérieur de sa sous-liste)
		"""
		for index1, elmt1 in enumerate(map_list):
			if spot in elmt1:
				for index2, elmt2 in enumerate(elmt1):
					if elmt2 == spot:
						coordinates_list.append([index1, index2])
		return coordinates_list
	
	def locate_player(self):
		"""
		Fonction demandant à find_and_save_coordinates de
		localiser la position du joueur.
		"""
		player_coordinates = self.find_and_save_coordinates("X", [], self.maze_map)
		self.player_lat = player_coordinates[0][0]
		self.player_lon = player_coordinates[0][1]

	def display_doors(self):
		"""
		Fonction demandant à find_and_save_coordinates de localiser
		la position des portes dans le labyrinthe pour ensuite les
		réintégrer dans le système de liste à chaque fois qu'il est modifié.
		"""
		doors_coordinates = self.find_and_save_coordinates(".", [], self.maze_map_init)
		for coordinates in doors_coordinates:
			door_lat = coordinates[0]
			door_lon = coordinates[1]
			self.maze_map[door_lat][door_lon] = "."

	def move(self, new_player_lat, new_player_lon):
		"""
		Fonction servant à mettre à jour la position du joeur 
		en fonction de ses choix de déplacement et du contrôle
		de validité. 
		"""
		status = "not win"
		if self.maze_map[new_player_lat][new_player_lon] == " " or self.maze_map[new_player_lat][new_player_lon] == ".":
			self.maze_map[self.player_lat][self.player_lon] = " "
			self.display_doors()
			self.maze_map[new_player_lat][new_player_lon] = "X"
			print(self)
			return status
		elif self.maze_map[new_player_lat][new_player_lon] == "U":
			status= "win"
			alert_msg = ":-) Bravo! Vous avez réussi à sortir du Labyrinthe!"
			print(alert_msg)
			time.sleep(2)
			return status
		else:
			status = "wrong move"
			alert_msg = "/!\ Impossible de réaliser ce déplacement: un obstacle vous barre la route."
			print(alert_msg)
			return status

	def move_control(self, direction, move_nb=1):
		"""
		Fonction servant à paraméter l'exécution de la fonction move
		suivant le choix de déplacement donné par le joueur.
		"""
		if direction == "N":
			player_move = self.move(new_player_lat = self.player_lat - move_nb, new_player_lon = self.player_lon)
		elif direction == "S":
			player_move = self.move(new_player_lat = self.player_lat + move_nb, new_player_lon = self.player_lon)
		elif direction == "E":
			player_move = self.move(new_player_lat = self.player_lat, new_player_lon = self.player_lon + move_nb)
		elif direction == "O":
			player_move = self.move(new_player_lat = self.player_lat, new_player_lon = self.player_lon - move_nb)
		elif direction == "Q":
			player_move = "quit"
		else:
			player_move = "wrong direction"
			alert_msg = "/!\ Votre direction n'est pas valide."
			print(alert_msg)
		return player_move

	def __repr__(self):
		string = str()
		for elmt in self.maze_map:
			for subelmt in elmt:
				string += subelmt
		return string

	def __str__(self):
		return self.__repr__()