from tkinter import Tk, Button, PhotoImage, Label, Frame
from multiprocessing import Process
from glob import glob
import macrobot

png_files = glob("small_icons/*.png")
units_defs = [
    {'name': 'Drone', 'requires': '', 'supply': 1},
    {'name': 'Overlord', 'requires': '', 'supply': -8},
    {'name': 'Queen', 'requires': 'Spawning_Pool', 'supply': 2},
    {'name': 'Zergling', 'requires': 'Spawning_Pool', 'supply': 1},
    {'name': 'Baneling', 'requires': 'Baneling_Nest', 'supply': 1},
    {'name': 'Roach', 'requires': 'Roach_Warren', 'supply': 2},
    {'name': 'Ravager', 'requires': 'Roach_Warren', 'supply': 3},
    {'name': 'Overseer', 'requires': 'Lair', 'supply': -8},
    {'name': 'Changeling', 'requires': '', 'supply': 0},
    {'name': 'Hydralisk', 'requires': 'Hydralisk_Den', 'supply': 2},
    {'name': 'LurkerMP', 'requires': 'Lurker_DenMP', 'supply': 3},
    {'name': 'Mutalisk', 'requires': 'Spire', 'supply': 2},
    {'name': 'Corruptor', 'requires': 'Spire', 'supply': 2},
    {'name': 'Infestor', 'requires': 'Infestation_Pit', 'supply': 2},
    {'name': 'Swarm_Host', 'requires': 'Infestation_Pit', 'supply': 3},
    {'name': 'Viper', 'requires': 'Hive', 'supply': 3},
    {'name': 'Ultralisk', 'requires': 'Ultralisk_Cavern', 'supply': 6},
    {'name': 'Brood_Lord', 'requires': 'Greater_Spire', 'supply': 4},
]
buildings_defs = [
    {'name': 'Hatchery', 'evolved_from': 'Drone', 'requires': '', 'supply': -6},
    {'name': 'Spawning_Pool', 'evolved_from': 'Drone', 'requires': 'Hatchery', 'supply': 0},
    {'name': 'Baneling_Nest', 'evolved_from': 'Drone', 'requires': 'Spawning_Pool', 'supply': 0},
    {'name': 'Roach_Warren', 'evolved_from': 'Drone', 'requires': 'Spawning_Pool', 'supply': 0},
    {'name': 'Evolution_Chamber', 'evolved_from': 'Drone', 'requires': 'Hatchery', 'supply': 0},
    {'name': 'Extractor', 'evolved_from': 'Drone', 'requires': 'Hatchery', 'supply': 0},
    {'name': 'Spine_Crawler', 'evolved_from': 'Drone', 'requires': 'Spawning_Pool', 'supply': 0},
    {'name': 'Spore_Crawler', 'evolved_from': 'Drone', 'requires': 'Spawning_Pool', 'supply': 0},
    {'name': 'Lair', 'evolved_from': 'Hatchery', 'requires': 'Spawning_Pool', 'supply': -6},
    {'name': 'Hydralisk_Den', 'evolved_from': 'Drone', 'requires': 'Lair', 'supply': 0},
    {'name': 'Lurker_DenMP', 'evolved_from': 'Drone', 'requires': 'Hydralisk_Den', 'supply': 0},
    {'name': 'Nydus_Network', 'evolved_from': 'Drone', 'requires': 'Lair', 'supply': 0},
    {'name': 'Spire', 'evolved_from': 'Drone', 'requires': 'Lair', 'supply': 0},
    {'name': 'Infestation_Pit', 'evolved_from': 'Drone', 'requires': 'Lair', 'supply': 0},
    {'name': 'Hive', 'evolved_from': 'Lair', 'requires': 'Infestation_Pit', 'supply': -6},
    {'name': 'Ultralisk_Cavern', 'evolved_from': 'Drone', 'requires': 'Hive', 'supply': 0},
    {'name': 'Greater_Spire', 'evolved_from': 'Spire', 'requires': 'Hive', 'supply': 0}
]

def find_origin_supply(item):
    evolved_from = item['evolved_from']
    if evolved_from == 'Larva' or evolved_from == '':
        return 0
    else:
        def is_origin(element):
            return element['name'] == evolved_from

        try:
            origin = next(filter(is_origin, units_defs + buildings_defs))
        except StopIteration:
            raise StopIteration(f"Origin of {item['name']} not found!")
        return origin['supply']

def load_image(img_path, frame):
    img = PhotoImage(file=img_path)
    label = Label(frame, image=img)
    label.photo = img
    label.pack(side="left")

class SC2BotPicker(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.build_order = []
        self.supply = [12, 14, 14]
        self.units = {'Drone': 12, 'Overlord': 1}
        self.buildings = {'Hatchery': 1}
        self.title("Macrobot Config")
        self.interface_frame = Frame(self, bg="black")
        self.unit_grid_frame = Frame(self.interface_frame)
        self.building_grid_frame = Frame(self.interface_frame)
        self.grid = []
        self.summary_frame = Frame(self.interface_frame)
        self.unit_label = Label(self.summary_frame, width=80, anchor="w")
        self.building_label = Label(self.summary_frame, width=80, anchor="w")
        self.unit_grid_frame.pack(pady=20, anchor='w')
        self.building_grid_frame.pack(anchor='w')
        self.create_grid()
        self.summary_frame.pack()
        self.unit_label.grid(row=0, sticky="nesw")
        self.building_label.grid(row=1, sticky="nesw")
        self.supply_label = Label(self.summary_frame, width=80, anchor='w')
        self.supply_label.grid(row=2, sticky='nesw')
        self.execute_button = Button(self.interface_frame, text="Build!", command=self.start_push)
        self.execute_button.pack(side="right")
        self.undo_button = Button(self.interface_frame, text="Undo", command=self.undo)
        self.undo_button.pack(side="right")
        self.reuse_button = Button(self.interface_frame, text="Use Last Build", command=self.reload_build_order)
        self.reuse_button.pack(side="right")
        self.reuse_button = Button(self.interface_frame, text="Clear", command=self.clear)
        self.reuse_button.pack(side="right")
        self.reuse_button = Button(self.interface_frame, text="One of Each", command=self.build_each)
        self.reuse_button.pack(side="right")
        self.interface_frame.grid(row=0, column=0)
        self.order_frame = Frame(self, bg="red", width=50, height=100)
        self.order_text = "Build Order:\n"
        self.order_label = Label(self.order_frame, text=self.order_text, width=50, anchor='w', justify='left')
        self.order_label.pack(anchor='w')
        self.order_frame.grid(row=0, column=1, sticky="nesw")
        self.update_army()
        self.update_build_order()

    def create_grid(self):
        row = 0
        col = 0
        for unit in units_defs:
            file = f'small_icons/Units/Icon_Zerg_{unit["name"]}.png'
            self.create_image_with_buttons(file, row, col, True)
            row += 1
            if row > 3:
                col += 1
                row = 0

        row = 0
        col = 0
        for building in buildings_defs:
            file = f'small_icons/Buildings/Icon_Zerg_{building["name"]}.png'
            self.create_image_with_buttons(file, row, col, False)
            row += 1
            if row > 3:
                col += 1
                row = 0

    def create_image_with_buttons(self, img_path, row, col, is_unit):
        frame = Frame(self.unit_grid_frame if is_unit else self.building_grid_frame)
        frame.grid(row=row, column=col)
        self.grid.append({'frame': frame, 'row': row, 'col': col})

        load_image(img_path, frame)
        entity = img_path.split("Icon_Zerg_")[1].split(".png")[0]
        self.create_buttons(frame, entity, is_unit)

    def update_army(self):
        unit_text = "Units: "
        for unit in self.units:
            unit_text += f"{unit} x{self.units[unit]}, "
        self.unit_label.config(text=unit_text[:-2])
        building_text = "Buildings: "
        for building in self.buildings:
            building_text += f"{building} x{self.buildings[building]}, "
        self.building_label.config(text=building_text[:-2])
        supply_text = f"Supply: {self.supply[0]} / {self.supply[1]}"
        self.supply_label.config(text=supply_text)

    def update_build_order(self):
        build_order_text = "Build Order:\n"
        for entity in self.build_order:
            build_order_text += f"\t{entity['name']} x{entity['quantity']}\n"
        self.order_label.config(text=build_order_text)

    def add_to_build_order(self, addition):
        if addition['requires'] != '':
            need_lair_have_hive = addition['requires'] == "Lair" and "Hive" in self.buildings
            need_spire_have_gs = addition['requires'] == 'Spire' and 'Greater_Spire' in self.buildings
            if addition['requires'] not in self.buildings and not need_lair_have_hive and not need_spire_have_gs:
                return
        origin_supply = find_origin_supply(addition)
        if (addition['supply'] - origin_supply) * addition['quantity'] > self.supply[1] - self.supply[0]:
            return
        evolved_from = addition['evolved_from']
        quan = addition['quantity']
        if evolved_from != 'Larva' and addition['name'] != 'Queen':
            if evolved_from == "Drone" or addition['is_unit']:
                if evolved_from not in self.units or self.units[evolved_from] < quan:
                    return
                elif self.units[evolved_from] == quan:
                    del self.units[evolved_from]
                else:
                    self.units[evolved_from] -= quan

                def is_origin(item):
                    return item['name'] == evolved_from
            else:
                if evolved_from not in self.buildings or self.buildings[evolved_from] < quan:
                    return
                elif self.buildings[evolved_from] == quan:
                    del self.buildings[evolved_from]
                else:
                    self.buildings[evolved_from] -= quan
        if len(self.build_order) > 0 and self.build_order[-1]["name"] == addition["name"]:
            self.build_order[-1]["quantity"] += addition["quantity"]
        else:
            self.build_order.append(addition)
        if addition['is_unit']:
            if addition['name'] in self.units:
                self.units[addition['name']] += quan
            else:
                self.units.update({addition['name']: quan})
        else:
            if addition['name'] in self.buildings:
                self.buildings[addition['name']] += quan
            else:
                self.buildings.update({addition['name']: quan})

        if addition['supply'] >= 0:
            self.supply[0] += (addition['supply'] - origin_supply) * quan
        else:
            if origin_supply >= 0:
                self.supply[0] -= origin_supply
                self.supply[2] -= addition['supply'] * quan
                self.supply[1] = min(200, self.supply[2])
            else:
                self.supply[2] -= (addition['supply'] - origin_supply) * quan
                self.supply[1] = min(200, self.supply[2])

        self.update_build_order()
        self.update_army()

    def create_buttons(self, frame, entity, is_unit):
        evolved_from = "Larva"
        if entity == "Baneling_Nest" or entity == "Evolution_Chamber" or entity == "Extractor" or entity == \
                "Hydralisk_Den" or entity == "Infestation_Pit" or entity == "Hatchery" or entity == "Nydus_Network" \
                or entity == "Roach_Warren" or entity == "Spawning_Pool" or entity == "Spine_Crawler" or entity == \
                "Spore_Crawler" or entity == "Spire" or entity == "Ultralisk_Cavern":
            evolved_from = "Drone"
        elif entity == "Baneling":
            evolved_from = "Zergling"
        elif entity == "Brood_Lord":
            evolved_from = "Corruptor"
        elif entity == "Greater_Spire":
            evolved_from = "Spire"
        elif entity == "Lair":
            evolved_from = "Hatchery"
        elif entity == "Hive":
            evolved_from = "Lair"
        elif entity == "LurkerMP":
            evolved_from = "Hydralisk"
        elif entity == "Overseer":
            evolved_from = "Overlord"
        elif entity == "Queen":
            evolved_from = ""
        elif entity == "Ravager":
            evolved_from = "Roach"

        def find_entity(item):
            return item['name'] == entity

        if is_unit:
            try:
                unit_def = next(filter(find_entity, units_defs))
                requires = unit_def['requires']
                entity_supply = unit_def['supply']
            except StopIteration:
                raise StopIteration(f"Unit {entity} not found!")
        else:
            try:
                building_def = next(filter(find_entity, buildings_defs))
                requires = building_def['requires']
                entity_supply = building_def['supply']
            except StopIteration:
                raise StopIteration(f"Building {entity} not found!")

        def create_button(quantity):
            return Button(frame, text=f"+{quantity}",
                          command=lambda: self.add_to_build_order({'name': entity,
                                                                   'quantity': quantity,
                                                                   'is_unit': is_unit,
                                                                   'evolved_from': evolved_from,
                                                                   'requires': requires,
                                                                   'supply': entity_supply}))

        button_plus_1 = create_button(1)
        button_plus_5 = create_button(5)
        button_plus_10 = create_button(10)

        button_plus_1.pack(side="left")
        button_plus_5.pack(side="left")
        button_plus_10.pack(side="left")

    def undo(self):
        if len(self.build_order) > 0:
            subtraction = self.build_order.pop()
            evolved_from = subtraction['evolved_from']
            quan = subtraction['quantity']
            if subtraction['is_unit']:
                if self.units[subtraction['name']] == quan:
                    del self.units[subtraction['name']]
                else:
                    self.units[subtraction['name']] -= quan
            else:
                if self.buildings[subtraction['name']] == quan:
                    del self.buildings[subtraction['name']]
                else:
                    self.buildings[subtraction['name']] -= subtraction['quantity']
            if subtraction['evolved_from'] != 'Larva' and subtraction['evolved_from'] != '':
                if subtraction['is_unit'] or subtraction['evolved_from'] == "Drone":
                    if evolved_from in self.units:
                        self.units[evolved_from] += quan
                    else:
                        self.units[evolved_from] = quan
                else:
                    if evolved_from in self.buildings:
                        self.buildings[evolved_from] += quan
                    else:
                        self.buildings[evolved_from] = quan

            origin_supply = find_origin_supply(subtraction)

            if subtraction["supply"] >= 0:
                self.supply[0] -= (subtraction["supply"] - origin_supply) * subtraction["quantity"]
            else:
                if origin_supply >= 0:
                    self.supply[0] += origin_supply * subtraction['quantity']
                    self.supply[2] += subtraction['supply'] * subtraction['quantity']
                else:
                    self.supply[2] += (subtraction['supply'] - origin_supply) * subtraction['quantity']
                self.supply[1] = min(self.supply[2], 200)
            self.update_build_order()
            self.update_army()

    def reload_build_order(self):
        import json
        with open("bo.json", 'r') as f:
            new_order = json.load(f)
        self.clear()
        for addition in new_order:
            self.add_to_build_order(addition)
        self.update_army()
        self.update_build_order()

    def build_each(self):
        import json
        with open("everything.json", 'r') as f:
            new_order = json.load(f)
        self.clear()
        for addition in new_order:
            self.add_to_build_order(addition)
        self.update_army()
        self.update_build_order()

    def clear(self):
        self.units = {"Drone": 12, "Overlord": 1}
        self.buildings = {"Hatchery": 1}
        self.supply = [12, 14, 14]
        self.build_order = []
        self.update_army()
        self.update_build_order()

    def start_push(self):
        Process(target=macrobot.main, args=(self.build_order,), daemon=True).start()

if __name__ == "__main__":
    root = SC2BotPicker()
    root.mainloop()
