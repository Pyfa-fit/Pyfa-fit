# shipHeavyMissileThermDmgPirateCruiser
#
# Used by:
# Ship: Gnosis
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "thermalDamage", ship.getModifiedItemAttr("shipBonusRole7"))
