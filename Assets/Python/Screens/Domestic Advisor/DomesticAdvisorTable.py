## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

# Helper class to create and fill tables for Domestic Advisor
# Most pages use mostly the same approach and this class is to simply and reuse code for setup.
# Hopefully this will make the code for the individual tables easier to read and less buggy.
# Nightinggale


# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class DomesticAdvisorTable:
	def __init__(self, parent):
		
		# When auto adding columns, resize to fill full width if all columns combined takes up more than this
		self.iFillWidthWhenOverPercentage = 90
		
		# When autofilling columns, always use full width if there is only one subpage
		self.bFillSinglePage = True

		# set the width of autogenerated columns
		self.defaultColumnWidth = parent.parent.DEFAULT_COLUMN_WIDTH
	
		# the rest are unlikely to be touched by outside classes
		self.parent = parent
		self.MainAdvisor = parent.parent
		self.iWidth = self.MainAdvisor.nTableWidth
		self.iRowHeight = self.MainAdvisor.ROW_HIGHT
		self.InfoArray = None
		self.columnWidth = [[]]
		self.columnName = [[]]
		self.columnsOnPage = []
		self.curPage = 0
		self.pagesNotSet = []
		
		self.pagesNotSet.append(True)
	
	# show/hide table
	# any custom addition to the page apart from the table will not be hidden and needs to be done manually
	def show(self):
		self.__show()
	
	def hide(self):
		self.__hide()
		
	# tell if the table headers have ever been drawn
	# most likely only used by BaseAdvisorWindow
	def isNeedInit(self):
		return self.__isNeedInit()
	
	# draw table headers if needed
	# should be called automatically by BaseAdvisorWindow
	def setHeader(self):
		self.__setHeader()

	# set up enable, select and row height. Usually defaults are good enough
	def enableSelect(self):
		self.__enableSelect()

	def enableSort(self):
		self.__enableSort()

	def setRowHeight(self, iHeight = 0):
		self.__setRowHeight(iRows)

	# note 0 means default height
	def setNumRows(self, iRows, iHeight = 0):
		self.__setNumRows(iRows, iHeight)
		
	# reset for drawing all over
	def clearRows(self):
		self.__clearRows()
	
	# add column headers to the table
	def addHeaderTxt(self, szName, iWidth):
		self.__addHeaderTxt(szName, iWidth)
		
	def addHeaderButton(self, szTitle = ""):
		self.__addHeaderButton(szTitle)
		
	def addHeaderCityName(self, szName = "TXT_KEY_DOMESTIC_ADVISOR_NAME"):
		self.__addHeaderCityName(szName)
		
	def addHeaderChar(self, iChar, iWidth = 50):
		self.__addHeaderChar(iChar, iWidth)

	# add an array telling which columns to add
	# this will split the page into multiple subpages if needed
	def addHeaderArray(self, infoArray):
		self.__addHeaderArrayCustom(infoArray)

	def addHeaderArrayBuildings(self):
		self.__addHeaderArrayBuildings()

	def addHeaderArrayYields(self):
		self.__addHeaderArrayYields()

	# get the size of the current cell. Useful when cell contains a panel for adding widgets like buttons
	def getCellHeight(self):
		return self.__getCellHeight()
	
	def getCellWidth(self):
		return self.__getCellWidth()


	#
	# Fill cells while updating
	#

	
	def addText(self, szText, iData1 = -1, iData2 = -1, widget = WidgetTypes.WIDGET_GENERAL, justified = CvUtil.FONT_LEFT_JUSTIFY):
		self.__addText(szText, iData1, iData2, widget, justified)

	def addTextRight(self, szText, iData1 = -1, iData2 = -1, widget = WidgetTypes.WIDGET_GENERAL):
		self.__addText(szText, iData1, iData2, widget, CvUtil.FONT_RIGHT_JUSTIFY)

	def addInt(self, iValue, iData1 = -1, iData2 = -1, widget = WidgetTypes.WIDGET_GENERAL, justified = CvUtil.FONT_RIGHT_JUSTIFY):
		self.__addInt(iValue, iData1, iData2, widget, justified)
		
	def drawChar(self, pInstance ):
		self.__drawChar(pInstance)
		
	def addPanelButton(self, buttonArt, widget = WidgetTypes.WIDGET_GENERAL, iData1 = -1, iData2 = -1):
		self.__addPanelButton(buttonArt, widget, iData1, iData2)
	
	# if the cell needs to be blank
	def skipCell(self):
		self.__skipCell()

	# cells set by an InfoArray
	def autofillRow(self, iCity, pCity):
		self.__autofillRow(iCity, pCity)


	#
	# Subpage control 
	#

	def nextPage(self):
		self.__nextPage()
		
	def prevPage(self):
		self.__prevPage()
		
	def isFirstPage(self):
		return self.__isFirstPage()
		
	def isLastPage(self):
		return self.__isLastPage()

	def currentPage(self):
		return self.__currentPage()

	def currentPageName(self):
		return self.__currentPageName()

	def numPages(self):
		return self.__numPages()

	def setPage(self, iPage):
		self.__setPage()

	def getScreen(self):
		return self.__getScreen()
	
	
	###
	### The rest of the file is private
	###
	
	def __show(self):
		self.__getScreen().show( self.currentPageName() )
	
	def __hide(self):
		self.__getScreen().hide( self.currentPageName() )
		
	def __isNeedInit(self):
		return len(self.columnWidth[0]) == 0
		
	def __enableSelect(self):
		self.__getScreen().enableSelect( self.currentPageName(), True )
		
	def __enableSort(self):
		self.__getScreen().enableSort( self.currentPageName() )
	
	def __setHeader(self):
		if (self.pagesNotSet[self.currentPage()]):
			self.pagesNotSet[self.currentPage()] = False
			self.__tableHeaderComplete()
	
	def __tableHeaderComplete(self):
		self.__getScreen().addTableControlGFC( self.__currentPageName(), self.__columnsOnCurrentPage(), (self.MainAdvisor.nScreenWidth - self.iWidth) / 2, 60, self.iWidth, self.MainAdvisor.nTableHeight, True, False, self.MainAdvisor.iCityButtonSize, self.MainAdvisor.iCityButtonSize, TableStyles.TABLE_STYLE_STANDARD )
		self.__getScreen().setStyle( self.__currentPageName(), "Table_StandardCiv_Style" )
		
		for i in range(len(self.columnWidth[self.__currentPage()])):
			self.__getScreen().setTableColumnHeader( self.__currentPageName(), i, "<font=2>" + self.columnName[self.__currentPage()][i] + "</font>", self.columnWidth[self.__currentPage()][i] )
		
	# note 0 means default height
	def __setNumRows(self, iRows, iHeight = 0):
		if (iRows != self.__getScreen().getTableNumRows(self.__currentPageName())):
			self.__getScreen().setTableNumRows ( self.__currentPageName(), iRows)
			self.__setRowHeight(iHeight)
		elif iRows == 1:
			# The table inits to 1 line, not 0
			# Assume the height not to be set if there is just one line
			self.__setRowHeight(iHeight)
		
		
	def __setRowHeight(self, iHeight = 0):
		if iHeight != 0:
			self.iRowHeight = iHeight
		for i in range(self.__getScreen().getTableNumRows(self.__currentPageName())):
			self.__getScreen().setTableRowHeight(self.__currentPageName(), i, self.iRowHeight)
		
	def __addHeaderDirect(self, iWidth, szName):
		self.columnWidth[self.__currentPage()].append(iWidth)
		self.columnName[self.__currentPage()].append(szName)
		
	def __addHeaderTxt(self, szName, iWidth):
		self.__addHeaderDirect(iWidth, localText.getText(szName, ()).upper())
		
	def __addHeaderButton(self, szTitle = ""):
		self.__addHeaderDirect(self.MainAdvisor.ROW_HIGHT, szTitle)
		
	def __addHeaderCityName(self, szName = "TXT_KEY_DOMESTIC_ADVISOR_NAME"):
		self.__addHeaderTxt(szName, self.MainAdvisor.CITY_NAME_COLUMN_WIDTH)
		
	def __addHeaderChar(self, iChar, iWidth = 50):
		char = (u" %c" % iChar)
		self.__addHeaderDirect(iWidth, char)

	def __addHeaderArrayCustom(self, infoArray):
		self.InfoArray = infoArray
		iTableWidth = self.iWidth - self.columnWidth[0][0] - self.columnWidth[0][1]
		self.__addHeaderArray(iTableWidth)
		
	def __addHeaderArrayBuildings(self):
		self.InfoArray = gc.getPlayer(CyGame().getActivePlayer()).getSpecialBuildingTypes()
		iTableWidth = self.iWidth - self.columnWidth[0][0] - self.columnWidth[0][1]
		self.__addHeaderArray(iTableWidth)
		self.curPage = JITarrayTypes.JIT_ARRAY_BUILDING_SPECIAL

	def __addHeaderArrayYields(self):
		self.InfoArray = gc.getPlayer(CyGame().getActivePlayer()).getStoredYieldTypes()
		iTableWidth = self.iWidth - self.columnWidth[0][0] - self.columnWidth[0][1]
		self.__addHeaderArray(iTableWidth)
		self.curPage = JITarrayTypes.JIT_ARRAY_YIELD

	def __addHeaderArray(self, iTableWidth):
		iMaxColumnsOnPage = iTableWidth // self.defaultColumnWidth
		iNumColumns = self.InfoArray.getLength()
		
		# add sub pages to allow enough room for all of the array content
		while (iNumColumns > iMaxColumnsOnPage):
			iNumColumns -= iMaxColumnsOnPage
			self.columnsOnPage.append(iMaxColumnsOnPage)
			self.pagesNotSet.append(True)
			self.columnWidth.append(self.columnWidth[0][:])
			self.columnName.append(self.columnName[0][:])
		self.columnsOnPage.append(iNumColumns)

		# fill each sub page with columns
		for i in range(len(self.columnsOnPage)):
			self.curPage = i
			iColumnOffset = len(self.columnWidth)
		
			iOffset = self.__getCurrentOffset()
			iIndex = self.__currentPage()
			iColumn = len(self.columnWidth)
			
			iNumColumnsOnPage = self.columnsOnPage[iIndex]
			
			iColumnWidth = self.defaultColumnWidth
			iNumExtraPixels = 0
			iColumnLength = iColumnWidth * iNumColumnsOnPage
			
			iFillPercentage = ((self.iWidth - self.__widthLeft() + iColumnLength) * 100) / self.iWidth
			
			bFill = self.bFillSinglePage and len(self.columnsOnPage) == 1
			
			if (bFill or iFillPercentage > self.iFillWidthWhenOverPercentage):
				iColumnWidth = int(self.__widthLeft() // iNumColumnsOnPage)
				iNumExtraPixels = self.__widthLeft() - (iColumnWidth * iNumColumnsOnPage)
			
			for iNum in range(iNumColumnsOnPage):
				iArrayIndex = iOffset + iNum
				
				iWidth = iColumnWidth
				if (iNum < iNumExtraPixels):
					iWidth += 1
				
				self.__addHeaderDirect(iWidth, self.__getColumnHeader(iArrayIndex))
		self.curPage = 0

	def __clearRows(self):
		# removes all rows and sets the counters to be ready to start on the first row
		self.curRow = -1
		self.curColumn = self.__columnsOnCurrentPage()

	def __getCellHeight(self):
		return self.iRowHeight
	
	def __getCellWidth(self):
		return self.columnWidth[self.__currentPage()][self.curColumn]

	def __progressCell(self):
		self.curColumn += 1
		if self.curColumn >= self.__columnsOnCurrentPage():
			self.curRow += 1
			self.curColumn = 0
			if self.__getScreen().getTableNumRows(self.__currentPageName()) == self.curRow:
				self.__getScreen().appendTableRow( self.__currentPageName() )
				self.__getScreen().setTableRowHeight(self.__currentPageName(), self.curRow, self.MainAdvisor.ROW_HIGHT)
	
	def __addText(self, szText, iData1 = -1, iData2 = -1, widget = WidgetTypes.WIDGET_GENERAL, justified = CvUtil.FONT_LEFT_JUSTIFY):
		self.__progressCell()
		self.__getScreen().setTableText(self.__currentPageName(), self.curColumn, self.curRow, "<font=2>" + szText + "</font>", "", widget, iData1, iData2, justified )

	def __addTextRight(self, szText, iData1 = -1, iData2 = -1, widget = WidgetTypes.WIDGET_GENERAL):
		self.__addText(szText, iData1, iData2, widget, CvUtil.FONT_RIGHT_JUSTIFY)

	def __addInt(self, iValue, iData1 = -1, iData2 = -1, widget = WidgetTypes.WIDGET_GENERAL, justified = CvUtil.FONT_RIGHT_JUSTIFY):
		self.__progressCell()
		self.__getScreen().setTableInt(self.__currentPageName(), self.curColumn, self.curRow, "<font=2>" + unicode(iValue) + "</font>", "", widget, iData1, iData2, justified )
		
	def __drawChar(self, pInstance ):
		self.__progressCell()
		eChar = u" %c" % pInstance.getChar()
		self.__getScreen().setTableText(self.__currentPageName(), self.curColumn, self.curRow, "<font=2>" + eChar + "</font>", "", pInstance.getWikiWidget(), pInstance.getID(), -1, CvUtil.FONT_LEFT_JUSTIFY )
		
	def __applyPanel(self):
		self.__progressCell()
		name = self.__currentPageName() + "-" + str(self.curRow) + "-" + str(self.curColumn)
		self.__getScreen().addPanel(name, u"", u"", True, False, 0, 0, self.__getCellWidth(), self.__getCellHeight(), PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.__getScreen().attachControlToTableCell(name, self.__currentPageName(), self.curRow, self.curColumn )
		return name
		
	def __addPanelButton(self, buttonArt, widget = WidgetTypes.WIDGET_GENERAL, iData1 = -1, iData2 = -1):
		name = self.__applyPanel()
		szButtonName = self.__currentPageName() + "Button-" + str(self.curRow) + "-" + str(self.curColumn)
		self.__getScreen().setImageButtonAt(szButtonName, name, buttonArt, 0, 0, self.__getCellWidth(), self.__getCellHeight(), widget, iData1, iData2)
		
	def __skipCell(self):
		self.__addText("")

	def __autofillRow(self, iCity, pCity):
		iOffset = self.__getCurrentOffset()
		iNumColumnsOnPage = self.columnsOnPage[self.currentPage()]
		for i in range(iNumColumnsOnPage):
			iType = self.InfoArray.get(i + iOffset)
			self.parent.drawColonyCell(iCity, pCity, iType, self.__getInfoForType(iType))
		
	def __getCurrentOffset(self):
		iOffset = 0
		iPage = self.__currentPage()
		if (iPage > 0):
			for i in range(iPage):
				iOffset += self.columnsOnPage[i]
		return iOffset
	
	def __columnsOnCurrentPage(self):
		return len(self.columnWidth[self.__currentPage()])
		
	def __widthLeft(self):
		iWidth = self.iWidth
		for i in (self.columnWidth[self.__currentPage()]):
			iWidth -= i
		return iWidth
	
	def __getColumnHeader(self, iColumn):
		if self.__hasGetChar():
			info = self.__getInfoForColumn(iColumn)
			if (info != None):
				return (u" %c" % info.getChar())
			
		return ""
	
	def __hasGetChar(self):
		if (self.InfoArray != None):
			if (self.InfoArray.getType(0) == JITarrayTypes.JIT_ARRAY_BUILDING_SPECIAL):
				return True
			if (self.InfoArray.getType(0) == JITarrayTypes.JIT_ARRAY_YIELD):
				return True
			
		return False
	
	def __getInfoForType(self, iType):
		if (self.InfoArray != None):
			if (self.InfoArray.getType(0) == JITarrayTypes.JIT_ARRAY_BUILDING_SPECIAL):
				return gc.getSpecialBuildingInfo(iType)
			if (self.InfoArray.getType(0) == JITarrayTypes.JIT_ARRAY_UNIT):
				return gc.getUnitInfo(iType)
			if (self.InfoArray.getType(0) == JITarrayTypes.JIT_ARRAY_YIELD):
				return gc.getYieldInfo(iType)
			
		return None
	
	def __getInfoForColumn(self, iColumn):
		if (self.InfoArray != None):
			return self.__getInfoForType(self.InfoArray.get(iColumn))
			
		return None

	def __nextPage(self):
		self.__setPage(self.__currentPage() + 1)
		
	def __prevPage(self):
		self.__setPage(self.__currentPage() - 1)
		
	def __isFirstPage(self):
		return self.__currentPage() == 0
		
	def __isLastPage(self):
		return (self.__currentPage() + 1) == self.__numPages()

	def __currentPage(self):
		if (self.curPage ==JITarrayTypes.JIT_ARRAY_BUILDING_SPECIAL):
			return self.MainAdvisor.iCurrentBuildingSubPage
		if (self.curPage == JITarrayTypes.JIT_ARRAY_YIELD):
			return self.MainAdvisor.iCurrentYieldSubPage
		return self.curPage

	def __currentPageName(self):
		return self.parent.screenName + str(self.__currentPage())

	def __numPages(self):
		return len(self.columnWidth)

	def __setPage(self, iPage):
		if (iPage >= 0 and iPage < self.__numPages() and iPage != self.__currentPage()):
			self.parent.hide()
			if (self.curPage == JITarrayTypes.JIT_ARRAY_BUILDING_SPECIAL):
				self.MainAdvisor.iCurrentBuildingSubPage = iPage
			elif (self.curPage == JITarrayTypes.JIT_ARRAY_YIELD):
				self.MainAdvisor.iCurrentYieldSubPage = iPage
			else:
				self.curPage = iPage
			self.parent.draw()

	def __getScreen(self):
		return CyGInterfaceScreen( "DomesticAdvisor", CvScreenEnums.DOMESTIC_ADVISOR )
