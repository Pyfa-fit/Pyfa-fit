# remoteShieldTransferFalloff
#
# Used by:
# Modules from group: Remote Shield Booster (38 of 38)
type = "projected", "active"


def handler(fit, container, context):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("shieldBonus")
        duration = container.cycleTime / 1000.0
        fit.extraAttributes.increase("shieldRepair", bonus / duration)
