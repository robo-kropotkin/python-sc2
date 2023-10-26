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
    elif name == "Lurker_DenMP":
        return UnitTypeId.LURKERDENMP, False
    elif name == "LurkerMP":
        return UnitTypeId.LURKERMP, False
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
        self.up_next: dict = build_order_queue.get()
        self.urgent = None
        self.taken_geysers: list[int] = []
        self.bases: list[int] = []
        self.should_have: list[dict] = [{'name': 'Hatchery', 'quantity': 1,
                                         'is_unit': False, 'evolved_from': 'Drone', 'requires': '', 'supply': -6}]
        self.missing = Queue()
        self.attack_in: int = 0
        self.should_attack: bool = False
        self.hq = None
        self.check_buffer: int = 0

    def can_build(self, unit_id, unit_name):
        if unit_name == "Baneling" and not self.structures(UnitTypeId.BANELINGNEST).ready:
            return False
        elif unit_name == "Baneling_Nest" and not self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            return False
        elif unit_name == "Brood_Lord":
            if not self.structures(UnitTypeId.GREATERSPIRE).ready.idle or \
                    not self.units.of_type(UnitTypeId.CORRUPTOR).ready:
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
            if not self.structures(UnitTypeId.INFESTATIONPIT).ready or \
                    not self.structures(UnitTypeId.LAIR).ready.idle:
                return False
        elif unit_name == "Hydralisk" and not self.structures(UnitTypeId.HYDRALISKDEN).ready:
            return False
        elif unit_name == "Hydralisk_Den" and \
                not (self.structures(UnitTypeId.LAIR).ready or self.structures(UnitTypeId.HIVE).ready):
            return False
        elif unit_name == "Infestation_Pit" and \
                not (self.structures(UnitTypeId.LAIR).ready or self.structures(UnitTypeId.HIVE).ready):
            return False
        elif unit_name == "Lair":
            if not self.structures(UnitTypeId.SPAWNINGPOOL).ready or not \
                    self.structures(UnitTypeId.HATCHERY).ready.idle:
                return False
        elif unit_name == "LurkerMP":
            if not self.structures(UnitTypeId.LURKERDENMP).ready or not self.units(UnitTypeId.HYDRALISK).ready:
                return False
        elif unit_name == "Lurker_DenMP":
            if not self.structures(UnitTypeId.HYDRALISKDEN).ready or not \
                    (self.structures(UnitTypeId.LAIR).ready or self.structures(UnitTypeId.HIVE).ready):
                return False
        elif unit_name == "Nydus_Network" and not \
                (self.structures(UnitTypeId.LAIR).ready or self.structures(UnitTypeId.HIVE).ready):
            return False
        elif unit_name == "Overseer":
            if not (self.structures(UnitTypeId.LAIR).ready or self.structures(UnitTypeId.HIVE).ready) \
                    or not self.units(UnitTypeId.OVERLORD).ready:
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
        elif unit_name == "Spire" and not \
                (self.structures(UnitTypeId.LAIR).ready or self.structures(UnitTypeId.HIVE).ready):
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

    def select_target(self) -> Point2:
        if self.enemy_structures:
            return random.choice(self.enemy_structures).position
        return self.enemy_start_locations[0]

    def update_should_have(self, update, entry=None):
        indices = [1 if elem['name'] == update['name'] else 0 for elem in self.should_have]
        if any(indices):
            if self.should_have[indices.index(1)]['quantity'] == -update['quantity']:
                self.should_have.remove(self.should_have[indices.index(1)])
            else:
                self.should_have[indices.index(1)]['quantity'] += update['quantity']
        else:
            self.should_have.append(entry)

    async def attack_logic(self, iteration):
        # Attack when the last item in the build order is complete
        if self.should_attack:
            self.attack_in = max(self.attack_in - 1, 0)
            if self.attack_in <= 0 and iteration % 20 == 0:
                for unit in self.units:
                    unit.attack(self.select_target())
        else:
            await self.units_to_natural(iteration)

    async def build_extractors(self, up_next):
        while self.can_afford(UnitTypeId.EXTRACTOR) and self.workers and up_next['quantity'] > 0:
            for th in self.townhalls.ready:
                if up_next['quantity'] < 1:
                    break
                available_geysers = self.vespene_geyser.closer_than(10, th)
                available_geysers = available_geysers.filter(lambda x: x.tag not in self.taken_geysers)
                if len(available_geysers) > 0:
                    drone: Unit = self.workers.gathering.random
                    drone.return_resource()
                    drone.build_gas(available_geysers[0])
                    self.taken_geysers.append(available_geysers[0].tag)
                    entry = up_next.copy()
                    entry['quantity'] = 1
                    self.update_should_have({'name': 'Extractor', 'quantity': 1}, entry=entry)
                    up_next['quantity'] -= 1
                    break

    # Prefer to train a queen where there's no queen already
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
        if iteration % 50 == 0:
            combat_units = self.units.exclude_type(UnitTypeId.DRONE).exclude_type(UnitTypeId.QUEEN)
            combat_units = combat_units.exclude_type(UnitTypeId.OVERLORD)
            for u in combat_units:
                if len(self.bases) > 1:
                    u.attack(self.townhalls.by_tag(self.bases[1]).position.towards(self.game_info.map_center, 10))
                else:
                    u.attack(self.townhalls.first.position.towards(self.game_info.map_center, 10))

    # Can only morph with the correct ability id.
    async def morph_from_unit(self):
        evolved_from = self.up_next['evolved_from']
        (origin_id, origin_is_unit) = find_entity_id(evolved_from)
        try:
            if self.up_next['is_unit']:
                morpher = self.units.of_type(origin_id).ready.idle.random
            else:
                morpher = self.structures.of_type(origin_id).ready.idle.random
        except AssertionError:
            raise AssertionError(self.up_next['name'])
        if not morpher:
            return False
        if evolved_from == "Zergling":
            morpher(AbilityId.MORPHTOBANELING_BANELING)
        elif evolved_from == "Roach":
            morpher(AbilityId.MORPHTORAVAGER_RAVAGER)
        elif evolved_from == "Overlord":
            morpher(AbilityId.MORPH_OVERSEER)
        elif evolved_from == "Hydralisk":
            morpher(AbilityId.MORPH_LURKER)
        elif evolved_from == "Corruptor":
            morpher(AbilityId.MORPHTOBROODLORD_BROODLORD)
        else:
            if evolved_from == "Hatchery":
                morpher(AbilityId.UPGRADETOLAIR_LAIR)
                self.check_buffer = 1000
            elif evolved_from == "Lair":
                self.check_buffer = 1000
                morpher(AbilityId.UPGRADETOHIVE_HIVE)
            elif evolved_from == "Spire":
                self.check_buffer = 1000
                morpher(AbilityId.UPGRADETOGREATERSPIRE_GREATERSPIRE)
            self.update_should_have({'name': evolved_from, 'quantity': -1})
        return True

    async def build_unit_or_building(self, entity_id, origin_id, up_next):
        larvae: Units = self.larva
        if up_next['evolved_from'] == 'Larva':
            if not larvae:
                return False
            larvae.random.train(entity_id)
        elif up_next['name'] == 'Hatchery':
            await self.expand_now()
        elif up_next['name'] == 'Extractor':
            await self.build_extractors(up_next)
            return False
        elif up_next['name'] == "Queen":
            await self.train_queen()
        elif up_next['evolved_from'] == "Drone":
            await self.build(entity_id, near=self.hq.position.towards(self.game_info.map_center, 4))
        elif self.structures.of_type(origin_id).ready.idle + self.units.of_type(origin_id).ready.idle:
            await self.morph_from_unit()
        if not up_next['is_unit'] and not up_next['name'] == 'Extractor':
            entry = up_next.copy()
            entry['quantity'] = 1
            self.update_should_have({'name': up_next['name'], 'quantity': 1}, entry=entry)
        self.check_buffer = 300
        return True

    # pylint: disable=R0912
    async def on_step(self, iteration):
        # At the start of the game, find our hq
        if self.hq is None:
            self.hq: Unit = self.townhalls.first
        if len(self.townhalls) > len(self.bases):
            for th in self.townhalls:
                if th.tag not in self.bases:
                    self.bases.append(th.tag)
        entity_id = False
        origin_id = False
        up_next = self.urgent or self.up_next
        if up_next:
            try:
                (entity_id, entity_is_unit) = find_entity_id(up_next['name'])
            except TypeError:
                raise KeyError(up_next['name'])
            if up_next['evolved_from'] != '':
                (origin_id, origin_is_unit) = find_entity_id(up_next['evolved_from'])

        await self.attack_logic(iteration)

        # Can train next unit / building
        if entity_id and self.can_build(entity_id, up_next['name']):
            success = await self.build_unit_or_building(entity_id, origin_id, up_next)
            # The build_extractor function subtracts quantity on its own
            if success:
                up_next['quantity'] -= 1
            if up_next['quantity'] <= 0:
                # If built from the urgent queue
                if self.urgent:
                    if self.missing.empty():
                        self.urgent = None
                    else:
                        self.urgent = self.missing.get()
                # If built from the normal queue
                elif build_order_queue.empty():
                    cost = self.game_data.units[entity_id.value].cost
                    self.attack_in = cost.time / 8 + 5
                    self.should_attack = True
                    self.up_next = None
                else:
                    self.up_next = build_order_queue.get()

        # Check that you have all buildings you should have
        if self.check_buffer > 0:
            self.check_buffer -= 1
        elif iteration % 100 == 0:
            for building in self.should_have:
                entity_id = find_entity_id(building['name'])
                if self.structures.of_type(entity_id).amount < building['quantity']:
                    correction = building.copy()
                    correction['quantity'] = correction['quantity'] - self.structures.of_type(entity_id).amount
                    building['quantity'] = self.structures.of_type(entity_id).amount
                    if self.urgent is None:
                        self.urgent = correction
                    else:
                        self.missing.put(correction)

        # Send idle queens with >=25 energy to inject
        for queen in self.units(UnitTypeId.QUEEN).idle:
            closest_hatch = min(self.townhalls, key=lambda hatch: hatch.distance_to(queen))
            if queen.energy >= 25:
                queen(AbilityId.EFFECT_INJECTLARVA, closest_hatch)

        await self.distribute_workers(resource_ratio=0)

def main(build_order):
    import json
    with open("bo.json", 'w') as f:
        json.dump(build_order, f)
    for item in build_order:
        build_order_queue.put(item)

    run_game(
        maps.get("HardwireAIE"),
        [Bot(Race.Zerg, Macrobot()), Computer(Race.Terran, Difficulty.VeryEasy)],
        realtime=False
    )

if __name__ == "__main__":
    main([])
