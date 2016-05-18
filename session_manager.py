# coding: utf8
# python3

from game_manager import *
import time, pickle, os

class SessionManager:
	"""
	Classe premettant de créer un session de jeu et de l'animer.
	Elle fourni les fonctionnalités essentielles pour gérer les 
	interactions entre le joueur et le jeu.
	"""
	def __init__(self):
		"""
		Stockage dans une liste des noms des fichiers texte 
		"""
		self.labyrinthe = []
		for i in os.listdir("cartes/"):
			self.labyrinthe.append(i)
		"""
		Stockage dans une liste des noms des fichiers de sauvegarde
		"""
		self.backup_files = []
		for i in os.listdir("backup/"):
			self.backup_files.append(i)
		"""
		Stockage dans une liste des différentes commandes du jeu
		"""
		self.game_cmd = [
			"N : Déplacement vers le haut",
			"S : Déplacement vers le bas",
			"E : Déplacement vers la droite",
			"O : Déplacement vers la gauche",
			"Q : Quitter de la partie",
			"ASTUCE=> Pour vous déplacer plusieurs fois de suite dans \
			 une direction ajoutez un nombre (entre 1 et 9) de déplacements \
			 après la commande de direction"
			]

	def home(self):
		"""
		Fonction qui anime le menu principal du jeu
		"""
		print("{0} ROBOC LE JEU {1}".format("/"*12, "\\"*12))
		print("1 : Commencer une nouvelle partie.\n2 : Charger un partie sauvegardée.")
		player_input = input("> ")
		try:
			if player_input == "1":
				self.new_game_play()
			elif player_input == "2":
				self.old_game_play()
			elif player_input.upper() == "Q":
				exit(0)
		except:
			self.home()

	def new_game_play(self):
		"""
		Fonction appelée lorsque le joueur débute une nouvelle partie.
		Le joueur choisi son labyrinthe et la classe GameManager est 
		instanciée avec en paramètre le nom du fichier texte correspondant.
		Le fichier texte est transformé en liste et l'objet renvoyé est
		ensuite traité par la fonction run_game.
		"""
		print("| LABYRINTHES EXISTANTS |")
		for index, value in enumerate(self.labyrinthe):
			print(str(index+1) + " : " + value[0:len(value)-4].capitalize())
		print("Tapez le numéro du labyrinthe que vous voulez jouer :")
		player_input = input("> ")
		try:
			mapfile = "cartes/" + self.labyrinthe[int(player_input)-1]
			game_play = GameManager(mapfile = mapfile)
			game_play.txtfile_to_list()
			self.run_game(game_play)
		except:
			alert_msg = "/!\ Il n'y a pas de labyrinthe correspondant à ce numéro."
			print(alert_msg)
			self.new_game_play()

	def old_game_play(self):
		"""
		Fonction appelée lorsque le joueur veut poursuivre une partie sauvegardée.
		Le joueur choisi sa sauvegarde et le nom du fichier backup correspondant est
		traité par la fonction load qui se charge d'importer l'objet enregistré.
		Celui-ci est ensuite traité par la fonction run_game.
		"""
		print("| PARTIES SAUVEGARDEES |")
		for index, value in enumerate(self.backup_files):
			print(str(index+1) + " : " + value)
		print("Tapez le numéro de la partie que vous voulez charger :")
		player_input = input("> ")
		try:
			game_play = self.load("backup/" + self.backup_files[int(player_input)-1])
			self.run_game(game_play)
		except:
			alert_msg = "/!\ Il n'y a pas de partie sauvegardée correspondant à ce numéro."
			print(alert_msg)
			time.sleep(3)
			self.old_game_play()

	def run_game(self, game_play):
		"""
		Fonction servant à animer une session de jeu en utilisant les fonctions
		de la classe GameManager. Tant que le joeur n'atteind pas l'issue ses 
		choix de déplacements sont transmis à la fonction move_control pour 
		faire évoluer la position du joueur dans le labyrinthe. Lorsque
		le joueur atteind l'issue la partie s'arrête et le joeur est redirigé vers
		le menu principal. En cours de jeu le joeur peut décider de quitter la partie
		et de la sauvegarder.
		"""
		print("| COMMANDES |")
		for i in self.game_cmd:
			print(i)
			time.sleep(1)

		while True:
			"""
			Gestion des déplacements du joueur.
			"""
			print(game_play)
			player_input = input("> ")

			if len(player_input) > 2:
				print("/!\ Votre direction n'est pas valide.")
			elif len(player_input) == 2:
				try:
					int(player_input[1])
				except:
					print("/!\ Votre nombre de déplacements n'est pas valide.")
					continue
				i = int(player_input[1]) 
				while i > 0:
					game_play.locate_player()
					player_move = game_play.move_control(player_input[0].upper())
					i -= 1
			elif len(player_input) == 1:
				game_play.locate_player()
				player_move = game_play.move_control(player_input.upper())
			"""
			Gestion de la victoire et de l'abandon d'une partie
			"""
			if player_move == "win":
				self.home()
			elif player_move == "quit":
				options = ["Continuer la partie", "Quitter et sauvegarder la partie", "Quitter la partie"]
				print("/!\ Vous-êtes sur le point de quitter la partie.")
				print("Voulez-vous:")
				for index, value in enumerate(options):
					print("{} : {}".format(int(index)+1, value))
				player_input = input("> ")
				if player_input == "1":
					continue
				elif player_input == "2":
					record_time = time.strftime("%Y%m%d-%H:%M:%S", time.localtime())
					backup_file = "backup/roboc_backup_" + record_time
					self.save(backup_file, game_play)
					print("Sauvegarde en cours ...")
					time.sleep(2)
					print("[OK] Partie sauvegardée sous " + backup_file)
					time.sleep(2)
					self.home()
				else:
					self.home()

	def save(self, backup_file, game_play):
		"""
		Fonction permettant d'enregistrer une partie en cours.
		"""
		with open(backup_file, 'wb') as backup:
			savegame = pickle.Pickler(backup)
			savegame.dump(game_play)

	def load(self, backup_file):
		"""
		Fonction permettant de charger partie sauvegardée.
		"""
		with open(backup_file, 'rb') as backup:
			load_game_play = pickle.Unpickler(backup)
			game_play = load_game_play.load()
		return game_play