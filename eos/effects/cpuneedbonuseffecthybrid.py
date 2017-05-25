# cpuNeedBonusEffectHybrid
#
# Used by:
# Modules named like: Algid Hybrid Administrations Unit (8 of 8)
effectType = "passive"


def handler(fit, container, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                  "cpu", container.getModifiedItemAttr("cpuNeedBonus"))
