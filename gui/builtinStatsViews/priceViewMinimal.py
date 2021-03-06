# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

# noinspection PyPackageRequirements
import wx
from gui.statsView import StatsView
from gui.bitmapLoader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from service.price import Price


class PriceViewMinimal(StatsView):
    name = "priceViewMinimal"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent

    def getHeaderText(self, fit):
        return "Price"

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        self.panel = contentPanel
        self.headerPanel = headerPanel

        headerContentSizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer = headerPanel.GetSizer()
        hsizer.Add(headerContentSizer, 0, 0, 0)
        self.labelEMStatus = wx.StaticText(headerPanel, wx.ID_ANY, "")
        headerContentSizer.Add(self.labelEMStatus)
        headerPanel.GetParent().AddToggleItem(self.labelEMStatus)

        gridPrice = wx.GridSizer(1, 3)
        contentSizer.Add(gridPrice, 0, wx.EXPAND | wx.ALL, 0)
        for _type in ("ship", "fittings", "total"):
            image = "%sPrice_big" % _type if _type != "ship" else "ship_big"
            box = wx.BoxSizer(wx.HORIZONTAL)
            gridPrice.Add(box, 0, wx.ALIGN_TOP)

            box.Add(BitmapLoader.getStaticBitmap(image, contentPanel, "gui"), 0, wx.ALIGN_CENTER)

            vbox = wx.BoxSizer(wx.VERTICAL)
            box.Add(vbox, 1, wx.EXPAND)

            vbox.Add(wx.StaticText(contentPanel, wx.ID_ANY, _type.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            vbox.Add(hbox)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.00 ISK")
            setattr(self, "labelPrice%s" % _type.capitalize(), lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):
        if fit is not None:
            self.fit = fit

            fit_items = Price.fitItemsList(fit)

            sPrice = Price.getInstance()
            sPrice.getPrices(fit_items, self.processPrices)
            self.labelEMStatus.SetLabel("Updating prices...")

        self.refreshPanelPrices(fit)
        self.panel.Layout()

    def refreshPanelPrices(self, fit=None):

        ship_price = 0
        module_price = 0

        if fit:
            ship_price = fit.ship.item.price.price

            if fit.modules:
                for _module in fit.modules:
                    if not _module.isEmpty:
                        module_price += _module.item.price.price

        # Due to popular request, removing all "below the line" items from pricing, as it's mildly confusing sincce they get lumped into a single value.
        # Many people consider below the line items to be "sunk cost" or reusable items, and thus not worth counting.
        fitting_price = module_price
        total_price = ship_price + fitting_price

        self.labelPriceShip.SetLabel("%s ISK" % formatAmount(ship_price, 3, 3, 9, currency=True))
        self.labelPriceShip.SetToolTip(wx.ToolTip('{:,.2f}'.format(ship_price)))

        self.labelPriceFittings.SetLabel("%s ISK" % formatAmount(fitting_price, 3, 3, 9, currency=True))
        self.labelPriceFittings.SetToolTip(wx.ToolTip('{:,.2f}'.format(fitting_price)))

        self.labelPriceTotal.SetLabel("%s ISK" % formatAmount(total_price, 3, 3, 9, currency=True))
        self.labelPriceTotal.SetToolTip(wx.ToolTip('{:,.2f}'.format(total_price)))

    def processPrices(self, prices):
        self.refreshPanelPrices(self.fit)

        self.labelEMStatus.SetLabel("")
        self.panel.Layout()


PriceViewMinimal.register()
