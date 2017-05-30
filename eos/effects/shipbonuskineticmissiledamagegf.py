# shipBonusKineticMissileDamageGF
#
# Used by:
# Ship: Whiptail
# Ship: Worm
effectType = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
