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
    {'name': 'Lurker', 'requires': 'Lurker_Den', 'supply': 3},
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
    {'name': 'Lurker_Den', 'evolved_from': 'Hydralisk_Den', 'requires': 'Hydralisk_Den', 'supply': 0},
    {'name': 'Nydus_Network', 'evolved_from': 'Drone', 'requires': 'Lair', 'supply': 0},
    {'name': 'Spire', 'evolved_from': 'Drone', 'requires': 'Lair', 'supply': 0},
    {'name': 'Infestation_Pit', 'evolved_from': 'Drone', 'requires': 'Lair', 'supply': 0},
    {'name': 'Hive', 'evolved_from': 'Lair', 'requires': 'Infestation_Pit', 'supply': -6},
    {'name': 'Ultralisk_Cavern', 'evolved_from': 'Drone', 'requires': 'Hive', 'supply': 0},
    {'name': 'Greater_Spire', 'evolved_from': 'Spire', 'requires': 'Hive', 'supply': 0}
]
units = {'Drone': 12, 'Overlord': 1}
buildings = {'Hatchery': 1}
build_order = []
import json
with open("bo.json", 'r') as f:
    build_order = json.load(f)
supply = [12, 14, 14]
prevBuilt = None

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

def start_push():
    Process(target=macrobot.main, args=(build_order,), daemon=True).start()

def load_image(img_path, frame):
    img = PhotoImage(file=img_path)
    label = Label(frame, image=img)
    label.photo = img
    label.pack(side="left")

class SC2BotPicker(Tk):
    def __init__(self):
        Tk.__init__(self)
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
        self.execute_button = Button(self.interface_frame, text="Build!", command=start_push)
        self.execute_button.pack(side="right")
        self.undo_button = Button(self.interface_frame, text="Undo", command=self.undo)
        self.undo_button.pack(side="right")
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
            file = f'small_icons/Icon_Zerg_{unit["name"]}.png'
            self.create_image_with_buttons(file, row, col, True)
            row += 1
            if row > 3:
                col += 1
                row = 0

        row = 0
        col = 0
        for building in buildings_defs:
            file = f'small_icons/Icon_Zerg_{building["name"]}.png'
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
        for unit in units:
            unit_text += f"{unit} x{units[unit]}, "
        self.unit_label.config(text=unit_text[:-2])
        building_text = "Buildings: "
        for building in buildings:
            building_text += f"{building} x{buildings[building]}, "
        self.building_label.config(text=building_text[:-2])
        supply_text = f"Supply: {supply[0]} / {supply[1]}"
        self.supply_label.config(text=supply_text)

    def update_build_order(self):
        build_order_text = "Build Order:\n"
        for entity in build_order:
            build_order_text += f"\t{entity['name']} x{entity['quantity']}\n"
        self.order_label.config(text=build_order_text)

    def add_to_build_order(self, addition):
        if addition['requires'] != '':
            need_lair_have_hive = addition['requires'] == "Lair" and "Hive" in buildings
            need_spire_have_gs = addition['requires'] == 'Spire' and 'Greater_Spire' in buildings
            need_hydra_have_lurker = addition['requires'] == "Hydralisk_Den" and "Lurker_Den" in buildings
            if addition['requires'] not in buildings and not need_lair_have_hive and not need_spire_have_gs \
                    and not need_hydra_have_lurker:
                return
        origin_supply = find_origin_supply(addition)
        if (addition['supply'] - origin_supply) * addition['quantity'] > supply[1] - supply[0]:
            return
        evolved_from = addition['evolved_from']
        quan = addition['quantity']
        if evolved_from != 'Larva' and addition['name'] != 'Queen':
            if evolved_from == "Drone" or addition['is_unit']:
                if evolved_from not in units or units[evolved_from] < quan:
                    return
                elif units[evolved_from] == quan:
                    del units[evolved_from]
                else:
                    units[evolved_from] -= quan

                def is_origin(item):
                    return item['name'] == evolved_from
            else:
                if evolved_from not in buildings or buildings[evolved_from] < quan:
                    return
                elif buildings[evolved_from] == quan:
                    del buildings[evolved_from]
                else:
                    buildings[evolved_from] -= quan
        if len(build_order) > 0 and build_order[-1]["name"] == addition["name"]:
            build_order[-1]["quantity"] += addition["quantity"]
        else:
            build_order.append(addition)
        if addition['is_unit']:
            if addition['name'] in units:
                units[addition['name']] += quan
            else:
                units.update({addition['name']: quan})
        else:
            if addition['name'] in buildings:
                buildings[addition['name']] += quan
            else:
                buildings.update({addition['name']: quan})

        if addition['supply'] >= 0:
            supply[0] += (addition['supply'] - origin_supply) * quan
        else:
            if origin_supply >= 0:
                supply[0] -= origin_supply
                supply[2] -= addition['supply'] * quan
                supply[1] = min(200, supply[2])
            else:
                supply[2] -= (addition['supply'] - origin_supply) * quan
                supply[1] = min(200, supply[2])

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
        elif entity == "Lurker":
            evolved_from = "Hydralisk"
        elif entity == "Lurker_Den":
            evolved_from = "Hydralisk_Den"
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
        if len(build_order) > 0:
            subtraction = build_order.pop()
            evolved_from = subtraction['evolved_from']
            if subtraction['is_unit']:
                if units[subtraction['name']] == subtraction['quantity']:
                    del units[subtraction['name']]
                else:
                    units[subtraction['name']] -= subtraction['quantity']
            else:
                if buildings[subtraction['name']] == subtraction['quantity']:
                    del buildings[subtraction['name']]
                else:
                    buildings[subtraction['name']] -= subtraction['quantity']
            if subtraction['evolved_from'] != 'Larva' and subtraction['evolved_from'] != '':
                if subtraction['evolved_from'] == 'Drone':
                    if 'Drone' in units:
                        units['Drone'] += subtraction['quantity']
                    else:
                        units['Drone'] = subtraction['quantity']
                else:
                    quantity = subtraction['quantity']
                    if subtraction['is_unit']:
                        if evolved_from in units:
                            units[evolved_from] += quantity
                        else:
                            units[evolved_from] = quantity
                    else:
                        if evolved_from in buildings:
                            buildings[evolved_from] += quantity
                        else:
                            buildings[evolved_from] = quantity

            origin_supply = find_origin_supply(subtraction)

            if subtraction["supply"] >= 0:
                supply[0] -= (subtraction["supply"] - origin_supply) * subtraction["quantity"]
            else:
                if origin_supply >= 0:
                    supply[0] += origin_supply * subtraction['quantity']
                    supply[2] += subtraction['supply'] * subtraction['quantity']
                else:
                    supply[2] += (subtraction['supply'] - origin_supply) * subtraction['quantity']
                supply[1] = min(supply[2], 200)
            self.update_build_order()
            self.update_army()

if __name__ == "__main__":
    root = SC2BotPicker()
    root.mainloop()
