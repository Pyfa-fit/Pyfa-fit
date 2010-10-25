import wx
import copy
from gui import bitmapLoader
import service

FitRenamed, EVT_FIT_RENAMED = wx.lib.newevent.NewEvent()
FitSelected, EVT_FIT_SELECTED = wx.lib.newevent.NewEvent()
FitRemoved, EVT_FIT_REMOVED = wx.lib.newevent.NewEvent()

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent)

        self._lastWidth = 0
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hpane = HeaderPane(self)
        mainSizer.Add(hpane, 0, wx.EXPAND)

        self.lpane = ListPane(self)
        mainSizer.Add(self.lpane, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Show()

        self.lpane.Refresh()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_SIZE, self.SizeRefreshList)
        self.stage1()

    def SizeRefreshList(self, event):
        ewidth, eheight = event.GetSize()
##            if ewidth != self._lastWidth:
##                self._lastWidth = ewidth
        self.lpane.Refresh()
        event.Skip()

    def __del__(self):
        pass

    def stage1(self):
        sMarket = service.Market.getInstance()
        self.lpane.RemoveAllChildren()
        for ID, name in sMarket.getShipRoot():
            self.lpane.AddWidget(CategoryItem(self.lpane, ID, (name, 0)))

        self.lpane.Layout()
        self.Show()

    def stage2(self, categoryID):
        sMarket = service.Market.getInstance()
        self.lpane.RemoveAllChildren()
        for ID, name, race in sMarket.getShipList(categoryID):
            self.lpane.AddWidget(ShipItem(self.lpane, ID, (name, 0), race))

        self.lpane.Layout()
        self.Show()

class HeaderPane (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 32), style=wx.TAB_TRAVERSAL)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        self.stHeader = wx.StaticText(self, wx.ID_ANY, u"Header --->", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stHeader.Wrap(-1)
        bSizer3.Add(self.stHeader, 0, wx.ALL | wx.EXPAND, 5)

class ListPane (wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__ (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)
        self._wList = []
        self._wCount = 0
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))


        self.SetVirtualSize((1, 1))
        self.SetScrollRate(0, 1)
        self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.MScrollUp)
        self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.MScrollDown)

    def MScrollUp(self, event):

        posy = self.GetScrollPos(wx.VERTICAL)
        posy -= 2
        self.Scroll(0, posy)
        self.Refresh()
        event.Skip()

    def MScrollDown(self, event):

        posy = self.GetScrollPos(wx.VERTICAL)
        posy += 2
        self.Scroll(0, posy)
        self.Refresh()
        event.Skip()


    def AddWidget(self, widget):
        widget.Reparent(self)
        self._wList.append(widget)
        self._wCount += 1

    def Layout(self):
        wx.ScrolledWindow.Layout(self)
        self.Refresh()

    def Refresh(self):
        ypos = 0
        cwidth, cheight = self.GetClientSize()
        for i in xrange(self._wCount):
            xa, ya = self.CalcScrolledPosition((0, ypos))
            iwidth, iheight = self._wList[i].GetSize()
            self._wList[i].SetPosition((xa, ya))
            self._wList[i].SetSize((cwidth, iheight))

            ypos += iheight

            self._wList[i].Show()
            self._wList[i].Refresh()
        self.SetVirtualSize((1, ypos))

    def RemoveChild(self, child):
        wx.Panel.RemoveChild(self, child)
        child.Hide()
        child.Destroy()
        self._wCount -= 1

    def RemoveAllChildren(self):
        for widget in self._wList:
            self.RemoveChild(widget)

        self._wList = []

class CategoryItem(wx.Window):
    def __init__(self, parent, categoryID, shipFittingInfo,
                 id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(-1,16), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        if categoryID:
            self.shipBmp = bitmapLoader.getBitmap("ship_small","icons")
        else:
            self.shipBmp = wx.EmptyBitmap(16,16)

        self.categoryID = categoryID
        self.shipFittingInfo = shipFittingInfo
        self.shipName, dummy = shipFittingInfo
        self.width,self.height = size

        self.highlighted = 0
        self.editWasShown = 0


        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_LEFT_UP, self.checkPosition)
        self.Bind(wx.EVT_ENTER_WINDOW, self.enterW)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leaveW)

        self.shipBrowser = self.Parent.Parent

    def checkPosition(self, event):

        pos = event.GetPosition()
        x,y = pos
        self.shipBrowser.stage2(self.categoryID)
        event.Skip()

    def enterW(self,event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def leaveW(self,event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()


    def OnEraseBackground(self, event):
        pass

    def OnPaint(self,event):
        rect = self.GetRect()

        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        r = copy.copy(rect)
        r.top = 0
        r.left = 0
        r.height = r.height / 2
        if self.highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.Clear()
            mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            mdc.SetTextForeground(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ))
            mdc.Clear()

        mdc.DrawBitmap(self.shipBmp,5+(rect.height-self.shipBmp.GetHeight())/2,(rect.height-self.shipBmp.GetWidth())/2,0)
        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))



        shipName, fittings = self.shipFittingInfo



        xpos = self.shipBmp.GetWidth() + 10

        xtext, ytext = mdc.GetTextExtent(shipName)
        ypos = (rect.height - ytext) / 2
        mdc.DrawText(shipName, xpos, ypos)
        xpos+=xtext+5

        mdc.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        if fittings <1:
            fformat = "No fittings"
        else:
            if fittings == 1:
                fformat = "%d fitting"
            else:
                fformat = "%d fittings"

        if fittings>0:
            xtext, ytext = mdc.GetTextExtent(fformat % fittings)
            ypos = (rect.height - ytext)/2
        else:
            xtext, ytext = mdc.GetTextExtent(fformat)
            ypos = (rect.height - ytext)/2

        #seems that a scrolled window without scrollbars shown always HasScrollbar ><

        if self.Parent.HasScrollbar(wx.VERTICAL):
            addX = 20
        else:
            addX = 20

        fPosX = rect.width - addX - xtext
        fPosY = (rect.height -ytext)/2
        if fittings > 0:
            mdc.DrawText(fformat % fittings, fPosX, fPosY)
        else:
            mdc.DrawText(fformat, fPosX, fPosY)

        event.Skip()

    def Destroy(self):
        self.Unbind(wx.EVT_PAINT)
        self.Unbind(wx.EVT_ERASE_BACKGROUND)
        self.Unbind(wx.EVT_LEFT_UP)
        self.Unbind(wx.EVT_ENTER_WINDOW)
        self.Unbind(wx.EVT_LEAVE_WINDOW)
        self.Close()


class ShipItem(wx.Window):
    def __init__(self, parent, shipID=None, shipFittingInfo=("Test", 2), itemData=None,
                 id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(-1, 38), style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)

        self._itemData = itemData

        self.shipBmp = wx.EmptyBitmap(32, 32)
        self.shipFittingInfo = shipFittingInfo
        self.shipName, dummy = shipFittingInfo
        self.newBmp = bitmapLoader.getBitmap("add_small", "icons")

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.editPosX = 0
        self.editPosY = 0
        self.highlighted = 0
        self.editWasShown = 0

        self.tcFitName = wx.TextCtrl(self, wx.ID_ANY, "%s fit" % self.shipName, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        self.tcFitName.Show(False)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.Bind(wx.EVT_LEFT_UP, self.checkPosition)
        self.Bind(wx.EVT_MOTION, self.cursorCheck)

        self.Bind(wx.EVT_ENTER_WINDOW, self.enterW)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.leaveW)

        self.tcFitName.Bind(wx.EVT_TEXT_ENTER, self.createNewFit)
        self.tcFitName.Bind(wx.EVT_KILL_FOCUS, self.editLostFocus)
        self.tcFitName.Bind(wx.EVT_KEY_DOWN, self.editCheckEsc)

    def SetData(self, data):
        self._itemData = data

    def GetData(self):
        return self._itemData

    def editLostFocus(self, event):
        self.tcFitName.Show(False)
        if self.highlighted == 1:
            self.editWasShown = 1

    def editCheckEsc(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.tcFitName.Show(False)
            self.editWasShown = 0
        else:
            event.Skip()

    def cursorCheck(self, event):
        pos = event.GetPosition()
        if self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16)):
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        else:
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
    def checkPosition(self, event):

        pos = event.GetPosition()
        x, y = pos
        if self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16)):
            if self.editWasShown == 1:
                self.createNewFit()
                return
            else:
                self.Refresh()
                fnEditSize = self.tcFitName.GetSize()
                wSize = self.GetSize()
                fnEditPosX = self.editPosX - fnEditSize.width - 5
                fnEditPosY = (wSize.height - fnEditSize.height) / 2
                self.tcFitName.SetPosition((fnEditPosX, fnEditPosY))
                self.tcFitName.Show(True)
                self.tcFitName.SetFocus()
                self.tcFitName.SelectAll()
                return

        if (not self.NHitTest((self.editPosX, self.editPosY), pos, (16, 16))):
            self.editWasShown = 0
            self.Refresh()


        event.Skip()

    def createNewFit(self, event=None):
        print "New :", self.tcFitName.GetValue(), "GTFO from stage2 to stage 3 (refresh stage 3)"
        self.tcFitName.Show(False)
        self.editWasShown = 0

    def NHitTest(self, target, position, area):
        x, y = target
        px, py = position
        aX, aY = area
        if (px > x and px < x + aX) and (py > y and py < y + aY):
            return True
        return False
    def enterW(self, event):
        self.highlighted = 1
        self.Refresh()
        event.Skip()

    def leaveW(self, event):
        self.highlighted = 0
        self.Refresh()
        event.Skip()

    def OnEraseBackground(self, event):
        pass

    def OnPaint(self, event):
        rect = self.GetRect()

        canvas = wx.EmptyBitmap(rect.width, rect.height)
        mdc = wx.BufferedPaintDC(self)
        mdc.SelectObject(canvas)
        r = copy.copy(rect)
        r.top = 0
        r.left = 0
        r.height = r.height / 2
        if self.highlighted:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)))
            mdc.Clear()
            mdc.SetTextForeground(wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
##
##            sr = 221
##            sg = 221
##            sb = 221
##
##            startColor = (sr,sg,sb)
##
##            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.SOUTH)
##            r.top = r.height
##            mdc.GradientFillLinear(r,startColor,wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW),wx.NORTH)
##            mdc.SetTextForeground(wx.BLACK)
            mdc.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        else:
            mdc.SetBackground(wx.Brush(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)))
            mdc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
            mdc.Clear()
            mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False))
#        mdc.DrawBitmap(self.effBmp,5+(rect.height-40)/2,(rect.height-40)/2,0)
        mdc.DrawBitmap(self.shipBmp, 5 + (rect.height - 32) / 2, (rect.height - 32) / 2, 0)




        shipName, fittings = self.shipFittingInfo


        ypos = (rect.height - 32) / 2
        textStart = 48
        xtext, ytext = mdc.GetTextExtent(shipName)
        mdc.DrawText(shipName, textStart, ypos)
        ypos += ytext

        mdc.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        xtext, ytext = mdc.GetTextExtent("%d fitting(s)")
        mdc.DrawText("%d fitting(s)" % fittings, textStart, ypos)
        mdc.SetFont(wx.Font(7, wx.SWISS, wx.NORMAL, wx.NORMAL, False))

        self.editPosX = rect.width - 20
        self.editPosY = (rect.height - 16) / 2
        mdc.DrawBitmap(self.newBmp, self.editPosX, self.editPosY, 0)
        event.Skip()

