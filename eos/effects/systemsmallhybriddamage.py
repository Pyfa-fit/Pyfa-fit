# systemSmallHybridDamage
#
# Used by:
# Celestials named like: Wolf Rayet Effect Beacon Class (6 of 6)
runTime = "early"
effectType = ("projected", "passive")


def handler(fit, container, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                     "damageMultiplier", container.getModifiedItemAttr("smallWeaponDamageMultiplier"),
                                     stackingPenalties=True)
