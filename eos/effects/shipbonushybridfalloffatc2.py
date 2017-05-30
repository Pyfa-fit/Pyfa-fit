# shipBonusHybridFalloffATC2
#
# Used by:
# Ship: Adrestia
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "falloff", ship.getModifiedItemAttr("shipBonusATC2"))
