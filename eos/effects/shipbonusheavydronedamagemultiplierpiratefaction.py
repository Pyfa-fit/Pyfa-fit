# shipBonusHeavyDroneDamageMultiplierPirateFaction
#
# Used by:
# Ships named like: Rattlesnake (2 of 2)
effectType = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusRole7"))
