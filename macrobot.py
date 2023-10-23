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
    elif name == "Spire":
        return UnitTypeId.SPIRE, False
    elif name == "Spore_Crawler":
        return UnitTypeId.SPORECRAWLER, False
    elif name == "Ultralisk_Cavern":
        return UnitTypeId.ULTRALISKCAVERN, False

class Macrobot(BotAI):
    def __init__(self):
        BotAI.__init__(self)
        self.up_next = build_order_queue.get()
        self.taken_geysers = []
        self.bases = []
        self.attack_in = 0
        self.should_attack = False
        self.hq = -1
        self.worker_buffer = 0

    def can_build(self, unit_id, unit_name):
        if unit_name == "Baneling" and not self.structures(UnitTypeId.BANELINGNEST).ready:
            return False
        elif unit_name == "Baneling_Nest" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Brood_Lord":
            if not self.structures(UnitTypeId.GREATERSPIRE).ready or not self.units.of_type(UnitTypeId.CORRUPTOR).ready:
                return False
        elif unit_name == "Zergling" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Queen" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Corruptor" and not self.structures(UnitTypeId.SPIRE).ready:
            return False
        elif unit_name == "Greater_Spire":
            if not self.structures(UnitTypeId.HIVE).ready or not self.structures(UnitTypeId.SPIRE).ready:
                return False
        elif unit_name == "Hive":
            if not self.structures(UnitTypeId.INFESTATIONPIT).ready or not self.structures(UnitTypeId.LAIR).ready:
                return False
        elif unit_name == "Hydralisk" and not self.structures(UnitTypeId.HYDRALISKDEN).ready:
            return False
        elif unit_name == "Hydralisk_Den" and not self.structures(UnitTypeId.LAIR).ready:
            return False
        elif unit_name == "Infestation_Pit" and not self.structures(UnitTypeId.LAIR).ready:
            return False
        elif unit_name == "LurkerMP":
            if not self.structures(UnitTypeId.LURKERDEN).ready or not self.units(UnitTypeId.HYDRALISK).ready:
                return False
        elif unit_name == "Lurker_Den":
            if not self.structures(UnitTypeId.HYDRALISKDEN).ready or not self.structures(UnitTypeId.LAIR).ready:
                return False
        elif unit_name == "Nydus_Network" and not self.structures(UnitTypeId.LAIR).ready:
            return False
        elif unit_name == "Overseer":
            if not self.structures(UnitTypeId.LAIR).ready or not self.units(UnitTypeId.OVERLORD).ready:
                return False
        elif unit_name == "Ravager":
            if not self.structures(UnitTypeId.ROACHWARREN).ready or not self.units.of_type(UnitTypeId.ROACH).ready:
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

    async def attack_logic(self, iteration):
        # Attack when the last item in the build order is complete
        if self.should_attack:
            self.attack_in = max(self.attack_in - 1, 0)
            if self.attack_in <= 0 and iteration % 20 == 0:
                for unit in self.units:
                    unit.attack(self.select_target())
        else:
            await self.units_to_natural(iteration)

    async def build_extractors(self):
        while self.can_afford(UnitTypeId.EXTRACTOR) and self.workers and self.up_next['quantity'] > 0:
            for th in self.townhalls.ready:
                if self.up_next['quantity'] < 1:
                    break
                available_geysers = self.vespene_geyser.closer_than(10, th)
                available_geysers = available_geysers.filter(lambda x: x.tag not in self.taken_geysers)
                if len(available_geysers) > 0:
                    drone: Unit = self.workers.gathering.random
                    drone.return_resource()
                    drone.build_gas(available_geysers[0])
                    self.taken_geysers.append(available_geysers[0].tag)
                    self.up_next['quantity'] -= 1
                    break

    async def train_queen(self):
        have_idle_hatch = False
        for th in self.townhalls:
            if not th.is_idle:
                continue
            all_queens_away = True
            for q in self.units(UnitTypeId.QUEEN):
                if th.distance_to(q) < 10:
                    all_queens_away = False
            if all_queens_away:
                th.train(UnitTypeId.QUEEN)
                have_idle_hatch = True
        if not have_idle_hatch:
            self.townhalls.random.train(UnitTypeId.QUEEN)

    async def units_to_natural(self, iteration):
        if iteration % 200 == 0:
            for u in self.units.exclude_type(UnitTypeId.DRONE).exclude_type(UnitTypeId.QUEEN):
                if len(self.bases) > 1:
                    u.attack(self.townhalls.by_tag(self.bases[1]).position.towards(self.game_info.map_center, 10))
                else:
                    u.attack(self.townhalls.first.position.towards(self.game_info.map_center, 10))

    async def morph_from_unit(self):
        evolved_from = self.up_next['evolved_from']
        (origin_id, origin_is_unit) = find_entity_id(evolved_from)
        morpher = self.units.of_type(origin_id).ready.random
        if evolved_from == "Zergling":
            morpher(AbilityId.MORPHTOBANELING_BANELING)
        if evolved_from == "Roach":
            morpher(AbilityId.MORPHTORAVAGER_RAVAGER)
        if evolved_from == "Overlord":
            morpher(AbilityId.MORPH_OVERSEER)
        if evolved_from == "Corruptor":
            morpher(AbilityId.MORPHTOBROODLORD_BROODLORD)

    # pylint: disable=R0912
    async def on_step(self, iteration):
        # if self.up_next['name'] == "Hydralisk_Den":
        #     print("Here!")
        # At the start of the game, find our hq
        if self.hq == -1:
            self.hq: Unit = self.townhalls.first
        if len(self.townhalls) > len(self.bases):
            for th in self.townhalls:
                if th.tag not in self.bases:
                    self.bases.append(th.tag)
        entity_id = False
        origin_id = False
        origin_is_unit = False
        larvae: Units = self.larva
        if self.up_next:
            try:
                (entity_id, entity_is_unit) = find_entity_id(self.up_next['name'])
            except TypeError:
                raise KeyError(self.up_next['name'])
            if self.up_next['evolved_from'] != '':
                (origin_id, origin_is_unit) = find_entity_id(self.up_next['evolved_from'])

        await self.attack_logic(iteration)

        # Can train next unit / building
        if entity_id and self.can_build(entity_id, self.up_next['name']):
            if self.up_next['evolved_from'] == 'Larva':
                if not larvae:
                    return
                larvae.random.train(entity_id)
            elif self.up_next['name'] == 'Hatchery':
                await self.expand_now()
            elif self.up_next['name'] == 'Extractor':
                await self.build_extractors()
            elif self.up_next['name'] == "Queen":
                await self.train_queen()
            elif self.up_next['evolved_from'] == "Drone":
                await self.build(entity_id, near=self.hq.position.towards(self.game_info.map_center, 4))
            elif origin_is_unit and self.units.of_type(origin_id).ready:
                await self.morph_from_unit()
            else:
                self.structures.of_type(origin_id).random.train(entity_id)
            if self.up_next['name'] != 'Extractor':
                self.up_next['quantity'] -= 1
            if self.up_next['quantity'] <= 0:
                if build_order_queue.empty():
                    cost = self.game_data.units[entity_id.value].cost
                    self.attack_in = cost.time / 8 + 5
                    self.should_attack = True
                    self.up_next = None
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
        [Bot(Race.Zerg, Macrobot()), Computer(Race.Terran, Difficulty.VeryEasy)],
        realtime=False,
        save_replay_as="ZvT.SC2Replay",
    )

if __name__ == "__main__":
    main()
