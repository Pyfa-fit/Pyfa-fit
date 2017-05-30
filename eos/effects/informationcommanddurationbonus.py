# informationCommandDurationBonus
#
# Used by:
# Skill: Information Command
effectType = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Information Command"), "buffDuration",
                                  src.getModifiedItemAttr("durationBonus") * lvl)
