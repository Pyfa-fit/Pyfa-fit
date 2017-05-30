# shipBonusMiningDroneAmountPercentRookie
#
# Used by:
# Ship: Gnosis
# Ship: Taipan
# Ship: Velator
effectType = "passive"


def handler(fit, container, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Mining Drone",
                                 "miningAmount", container.getModifiedItemAttr("rookieDroneBonus"))
