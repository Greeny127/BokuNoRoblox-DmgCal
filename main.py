import csv
import math
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class calculator:
	def __init__(self):
		self.wdata = r'data\group\weapons.csv'
		self.bdata = r'data\group\bosses.csv'

	def getall(self, mode='weapons'):
		if mode == "weapons":
			lst = []
			with open(self.wdata) as file:
				reader = csv.reader(file, delimiter=',')
				line_count = 0

				for row in reader:
					if line_count == 0:
						line_count += 1
					else:
						lst.append(row[0])

			return lst

		else:
			lst = []
			with open(self.bdata) as file:
				reader = csv.reader(file, delimiter=',')
				line_count = 0
				for row in reader:
					if line_count == 0:
						line_count += 1
					else:
						lst.append(row[0])
						line_count += 1 
			return lst          

	def find(self, mode='weapon', boss="", weapon=""):	
		if mode == 'weapon':
			with open(self.wdata) as file:
				reader = csv.reader(file, delimiter=',')
				line_count = 0

				for row in reader:
					if line_count == 0:
						line_count += 1
					else:
						if row[0].strip() == weapon.strip():
							mul = float(row[1])

							line_count += 1

			return mul

		if mode == "bosses":		
			with open(self.bdata) as file:
				reader = csv.reader(file, delimiter=',')
				line_count = 0
				for row in reader:
					if line_count == 0:
						line_count += 1
					else:
						if row[0].strip() == boss.strip():
							name = row[0]
							hp = int(row[1])
							reduction = int(row[2])

						line_count += 1

			return name, hp, reduction

	def hits(self, hp, red, st, mul=0):
		if mul == 0:
			if red == 0:
				hits = int(math.ceil(hp / st))
				return hits

			else:
				dmg = st - float(st*(red/100))
				hits = int(math.ceil(hp / dmg))
				return hits

		else:
			if red == 0:
				dmg = st * mul
				hits = int(math.ceil(hp / dmg))
				return hits

			else:
				dmg = st * mul
				dmg = dmg - float(dmg*(red/100))
				hits = int(math.ceil(hp / dmg))
				return hits


class MainGui:
	def __init__(self, master):
		self.master = master
		self.brain = calculator()

		master.title("Boku No Roblox - Damage Calculator")
		master.geometry("650x120")
		master.resizable(False, False)

		self.make(self.master)

	def make(self, master):
		weapons = self.brain.getall()
		bosses = self.brain.getall(mode="bosses")

		master.grid_rowconfigure(5, weight=1)
		master.grid_columnconfigure(5, weight=1)

		self.bossesText = tk.Label(master, text="Bosses")
		self.bossesText.grid(row=0, column=0)

		bossesChoice = ttk.Combobox(master)
		bossesChoice['values'] = bosses
		bossesChoice['state'] = 'readonly'
		bossesChoice.grid(row=0, column=1)


		self.weaponsText = tk.Label(master, text="Weapons")
		self.weaponsText.grid(row=0, column=6)

		weaponsChoice = ttk.Combobox(master)
		weaponsChoice['values'] = weapons
		weaponsChoice['state'] = 'readonly'
		weaponsChoice.grid(row=0, column=7)

		self.strengthText = tk.Label(master, text="Strength", font=("Arial", 8))
		self.strengthText.grid(row=3, column=5)

		self.strength = tk.Entry(master)
		self.strength.grid(row=4, column=5)

		self.calculate = tk.Button(master, text="Calculate", command = lambda: self.Calculate(st=self.strength.get(), boss=bossesChoice, weapon=weaponsChoice))
		self.calculate.grid(row=6, column=5)

		self.result = tk.Label(self.master)
		self.result.grid(row=7, column=5)

	def Calculate(self, st=0, boss="", weapon=""):
		boss = self.brain.find(mode='bosses', boss=boss.get().strip())
		mul = float(self.brain.find(weapon=weapon.get().strip()))

		try:
			st = st.replace(",", "")
			st = int(st)

		except:
			st = int(st)

		name = boss[0]
		hp = int(boss[1])
		reduction = int(boss[2])

		pred = self.brain.hits(hp, reduction, st, mul)

		self.result['text'] = f"You need roughly {pred} hits to kill {name}."
		self.master.update()


root = tk.Tk()
my_gui = MainGui(root)
root.mainloop()
