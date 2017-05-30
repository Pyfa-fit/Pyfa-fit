# shipBonusLETOptimalRangePirateFaction
#
# Used by:
# Ship: Nestor
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Energy Turret"),
                                  "maxRange", ship.getModifiedItemAttr("shipBonusRole7"))
