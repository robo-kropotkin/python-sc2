from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units
from queue import Queue


import random

build_order_queue = Queue()

def find_entity_id(name):
    if name == "Larva":
        return UnitTypeId.LARVA, True
    elif name == "Baneling":
        return UnitTypeId.BANELING, True
    elif name == "Brood_Lord":
        return UnitTypeId.BROODLORD, True
    elif name == "Changeling":
        return UnitTypeId.CHANGELING, True
    elif name == "Corruptor":
        return UnitTypeId.CORRUPTOR, True
    elif name == "Drone":
        return UnitTypeId.DRONE, True
    elif name == "Hydralisk":
        return UnitTypeId.HYDRALISK, True
    elif name == "Infestor":
        return UnitTypeId.INFESTOR, True
    elif name == "Mutalisk":
        return UnitTypeId.MUTALISK, True
    elif name == "Overlord":
        return UnitTypeId.OVERLORD, True
    elif name == "Overseer":
        return UnitTypeId.OVERSEER, True
    elif name == "Queen":
        return UnitTypeId.QUEEN, True
    elif name == "Ravager":
        return UnitTypeId.RAVAGER, True
    elif name == "Roach":
        return UnitTypeId.ROACH, True
    elif name == "Swarm_Host":
        return UnitTypeId.SWARMHOSTMP, True
    elif name == "Ultralisk":
        return UnitTypeId.ULTRALISK, True
    elif name == "Viper":
        return UnitTypeId.VIPER, True
    elif name == "Zergling":
        return UnitTypeId.ZERGLING, True
    elif name == "Baneling_Nest":
        return UnitTypeId.BANELINGNEST, False
    elif name == "Evolution_Chamber":
        return UnitTypeId.EVOLUTIONCHAMBER, False
    elif name == "Extractor":
        return UnitTypeId.EXTRACTOR, False
    elif name == "Greater_Spire":
        return UnitTypeId.GREATERSPIRE, False
    elif name == "Hatchery":
        return UnitTypeId.HATCHERY, False
    elif name == "Hive":
        return UnitTypeId.HIVE, False
    elif name == "Hydralisk_Den":
        return UnitTypeId.HYDRALISKDEN, False
    elif name == "Infestation_Pit":
        return UnitTypeId.INFESTATIONPIT, False
    elif name == "Lair":
        return UnitTypeId.LAIR, False
    elif name == "Lurker_Den":
        return UnitTypeId.LURKERDEN, False
    elif name == "Nydus_Network":
        return UnitTypeId.NYDUSNETWORK, False
    elif name == "Roach_Warren":
        return UnitTypeId.ROACHWARREN, False
    elif name == "Spawning_Pool":
        return UnitTypeId.SPAWNINGPOOL, False
    elif name == "Spine_Crawler":
        return UnitTypeId.SPINECRAWLER, False
    elif name == "Spore_Crawler":
        return UnitTypeId.SPORECRAWLER, False
    elif name == "Ultralisk_Cavern":
        return UnitTypeId.ULTRALISKCAVERN, False

class Macrobot(BotAI):
    def __init__(self):
        BotAI.__init__(self)
        self.up_next = build_order_queue.get()
        self.attack_in = -1

    def can_build(self, unit_id, unit_name):
        if unit_name == "Baneling" and not self.structures(UnitTypeId.BANELINGNEST).ready:
            return False
        elif unit_name == "Baneling_Nest" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Brood_Lord" and not self.structures(UnitTypeId.GREATERSPIRE).ready:
            return False
        elif unit_name == "Zergling" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Queen" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Corruptor" and not self.structures(UnitTypeId.SPIRE).ready:
            return False
        elif unit_name == "Greater_Spire" and not self.structures(UnitTypeId.HIVE).ready:
            return False
        elif unit_name == "Hive" and not self.structures(UnitTypeId.INFESTATIONPIT).ready:
            return False
        elif unit_name == "Hydralisk" and not self.structures(UnitTypeId.HYDRALISKDEN).ready:
            return False
        elif unit_name == "Hydralisk_Den" and not self.structures(UnitTypeId.LAIR).ready:
            return False
        elif unit_name == "Infestation_Pit" and not self.structures(UnitTypeId.LAIR).ready:
            return False
        elif unit_name == "Lurker" and not self.structures(UnitTypeId.HYDRALISKDEN).ready:
            return False
        elif unit_name == "Nydus_Network" and not self.structures(UnitTypeId.LAIR).ready:
            return False
        elif unit_name == "Overseer" and not self.structures(UnitTypeId.LAIR).ready:
            return False
        elif unit_name == "Ravager" and not self.structures(UnitTypeId.ROACHWARREN).ready:
            return False
        elif unit_name == "Roach" and not self.structures(UnitTypeId.ROACHWARREN).ready:
            return False
        elif unit_name == "Roach_Warren" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Spine_Crawler" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Spire" and not self.structures(UnitTypeId.LAIR).ready:
            return False
        elif unit_name == "Mutalisk" and not self.structures(UnitTypeId.SPIRE).ready:
            return False
        elif unit_name == "Spore_Crawler" and not self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready:
            return False
        elif unit_name == "Swarm_Host" and not self.structures(UnitTypeId.INFESTATIONPIT).ready:
            return False
        elif unit_name == "Ultralisk" and not self.structures(UnitTypeId.ULTRALISKCAVERN).ready:
            return False
        elif unit_name == "Ultralisk_Cavern" and not self.structures(UnitTypeId.HIVE).ready:
            return False
        elif unit_name == "Viper" and not self.structures(UnitTypeId.HIVE).ready:
            return False
        return self.can_afford(unit_id)

    def dist_to_friendly_structures(self, expo):
        return min([expo.distance_to(structure) for structure in self.structures])

    def select_target(self) -> Point2:
        if self.enemy_structures:
            return random.choice(self.enemy_structures).position
        return self.enemy_start_locations[0]

    # pylint: disable=R0912
    async def on_step(self, iteration):
        entity_id = False
        origin_id = False
        larvae: Units = self.larva
        hq: Unit = self.townhalls.first
        if self.up_next:
            (entity_id, entity_is_unit) = find_entity_id(self.up_next['name'])
            if self.up_next['evolved_from'] != '':
                (origin_id, origin_is_unit) = find_entity_id(self.up_next['evolved_from'])

        # Attack when the last item in the build order is complete
        if self.attack_in != -1:
            self.attack_in -= 1
        if self.attack_in == 0:
            for unit in self.units:
                unit.attack(self.select_target())

        # Can train next unit / building
        if entity_id and self.can_build(entity_id, self.up_next['name']):
            if self.up_next['evolved_from'] == 'Larva':
                if not larvae:
                    return
                larvae.random.train(entity_id)
            elif self.up_next['name'] == 'Hatchery':
                planned_hatch_locations = {ph.position for ph in self.placeholders}
                my_structure_locations = {structure.position for structure in self.structures}
                enemy_structure_locations = {structure.position for structure in self.enemy_structures}
                blocked_locations = planned_hatch_locations | my_structure_locations | enemy_structure_locations
                available_locations = self.expansion_locations_list.copy()
                for location in available_locations:
                    if location in blocked_locations:
                        available_locations.remove(location)
                closest_expansion = min(available_locations,
                                        key=lambda loc: self.dist_to_friendly_structures(loc))
                self.workers.collecting.random.build(entity_id, closest_expansion)
            elif self.up_next['name'] == "Queen":
                hatcheries = self.structures.of_type(UnitTypeId.HATCHERY)
                lairs = self.structures.of_type(UnitTypeId.LAIR)
                hives = self.structures.of_type(UnitTypeId.HIVE)
                (hatcheries + lairs + hives).random.train(UnitTypeId.QUEEN)
            elif self.up_next['evolved_from'] == "Drone":
                await self.build(entity_id, near=hq.position.towards(self.game_info.map_center, 4))
            elif origin_is_unit:
                self.units.of_type(origin_id).random.train(entity_id)
            else:
                self.structures.of_type(origin_id).random.train(entity_id)
            self.up_next['quantity'] -= 1
            if self.up_next['quantity'] == 0:
                if build_order_queue.empty():
                    cost = self.game_data.units[entity_id.value].cost
                    self.attack_in = cost.time + 1
                else:
                    self.up_next = build_order_queue.get()

        # Send idle queens with >=25 energy to inject
        for queen in self.units(UnitTypeId.QUEEN).idle:
            closest_hatch = min(self.townhalls, key=lambda hatch: hatch.distance_to(queen))
            if queen.energy >= 25:
                queen(AbilityId.EFFECT_INJECTLARVA, closest_hatch)

        # Saturate gas
        for a in self.gas_buildings:
            if a.assigned_harvesters < a.ideal_harvesters:
                w: Units = self.workers.closer_than(10, a)
                if w:
                    w.random.gather(a)

        await self.distribute_workers()

def main(build_order):
    import json
    with open("bo.json", 'w') as f:
        json.dump(build_order, f)
    for item in build_order:
        build_order_queue.put(item)

    run_game(
        maps.get("HardwireAIE"),
        [Bot(Race.Zerg, Macrobot()), Computer(Race.Terran, Difficulty.Easy)],
        realtime=False,
        save_replay_as="ZvT.SC2Replay",
    )

if __name__ == "__main__":
    main()
