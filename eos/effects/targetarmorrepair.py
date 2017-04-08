# Not used by any item
type = "projected", "active"


def handler(fit, container, context):
    if "projected" in context:
        bonus = container.getModifiedItemAttr("armorDamageAmount")
        duration = container.cycleTime / 1000.0
        fit.extraAttributes.increase("armorRepair", bonus / duration)
