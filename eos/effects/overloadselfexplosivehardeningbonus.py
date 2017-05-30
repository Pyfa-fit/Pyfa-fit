# overloadSelfExplosiveHardeningBonus
#
# Used by:
# Variations of module: Armor Explosive Hardener I (39 of 39)
# Variations of module: Explosive Deflection Field I (19 of 19)
# Module: Civilian Explosive Deflection Field
effectType = "overheat"


def handler(fit, container, context):
    container.boostItemAttr("explosiveDamageResistanceBonus", container.getModifiedItemAttr("overloadHardeningBonus"))
