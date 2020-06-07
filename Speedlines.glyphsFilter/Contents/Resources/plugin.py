# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from Foundation import NSClassFromString
import math, random

class Speedlines(FilterWithDialog):
	
	# Definitions of IBOutlets
	
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	
	# Text field in dialog
	numberField = objc.IBOutlet()
	thicknessField = objc.IBOutlet()
	minDistanceField = objc.IBOutlet()
	maxDistanceField = objc.IBOutlet()
	minLengthField = objc.IBOutlet()
	maxLengthField = objc.IBOutlet()
	minGapField = objc.IBOutlet()
	maxGapField = objc.IBOutlet()
	rightCheckbox = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({'en': u'Speedlines', 'de': u'Wuscher'})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)
	
	# On dialog show
	@objc.python_method
	def start(self):
		random.seed()
		
		# Set default setting if not present
		Glyphs.registerDefault('com.mekkablue.Speedlines.maxDistance', 30)
		Glyphs.registerDefault('com.mekkablue.Speedlines.maxGap', 50)
		Glyphs.registerDefault('com.mekkablue.Speedlines.maxLength', 200)
		Glyphs.registerDefault('com.mekkablue.Speedlines.minDistance', 0)
		Glyphs.registerDefault('com.mekkablue.Speedlines.minGap', 10)
		Glyphs.registerDefault('com.mekkablue.Speedlines.minLength', 50)
		Glyphs.registerDefault('com.mekkablue.Speedlines.number', 5)
		Glyphs.registerDefault('com.mekkablue.Speedlines.right', 0)
		Glyphs.registerDefault('com.mekkablue.Speedlines.thickness', 20)

		# populate GUI fields
		self.maxDistanceField.setStringValue_(Glyphs.defaults['com.mekkablue.Speedlines.maxDistance'])
		self.maxGapField.setStringValue_(Glyphs.defaults['com.mekkablue.Speedlines.maxGap'])
		self.maxLengthField.setStringValue_(Glyphs.defaults['com.mekkablue.Speedlines.maxLength'])
		self.minDistanceField.setStringValue_(Glyphs.defaults['com.mekkablue.Speedlines.minDistance'])
		self.minGapField.setStringValue_(Glyphs.defaults['com.mekkablue.Speedlines.minGap'])
		self.minLengthField.setStringValue_(Glyphs.defaults['com.mekkablue.Speedlines.minLength'])
		self.numberField.setStringValue_(Glyphs.defaults['com.mekkablue.Speedlines.number'])
		self.rightCheckbox.setIntValue_(Glyphs.defaults['com.mekkablue.Speedlines.right'])
		self.thicknessField.setStringValue_(Glyphs.defaults['com.mekkablue.Speedlines.thickness'])
		
		# Set focus to text field
		self.numberField.becomeFirstResponder()
		
	@objc.IBAction
	def setRight_( self, sender ):
		# Store right coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.right'] = sender.intValue()
		self.update()
			
	@objc.IBAction
	def setNumber_( self, sender ):
		# Store number coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.number'] = sender.intValue()
		self.update()
	
	@objc.IBAction
	def setThickness_( self, sender ):
		# Store thickness coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.thickness'] = sender.intValue()
		self.update()
	
	@objc.IBAction
	def setMinDistance_( self, sender ):
		# Store minDistance coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.minDistance'] = sender.intValue()
		self.update()
	
	@objc.IBAction
	def setMaxDistance_( self, sender ):
		# Store maxDistance coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.maxDistance'] = sender.intValue()
		self.update()
	
	@objc.IBAction
	def setMinLength_( self, sender ):
		# Store minLength coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.minLength'] = sender.intValue()
		self.update()
	
	@objc.IBAction
	def setMaxLength_( self, sender ):
		# Store maxLength coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.maxLength'] = sender.intValue()
		self.update()
	
	@objc.IBAction
	def setMinGap_( self, sender ):
		# Store minLength coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.minGap'] = sender.intValue()
		self.update()
	
	@objc.IBAction
	def setMaxGap_( self, sender ):
		# Store maxLength coming in from dialog
		Glyphs.defaults['com.mekkablue.Speedlines.maxGap'] = sender.intValue()
		self.update()
	
	@objc.python_method
	def getValueForKey( self, customParameters, key ):
		try:
			if key in customParameters:
				value = customParameters[key]
			else:
				value = float(Glyphs.defaults['com.mekkablue.Speedlines.%s'%key])
			return value
		except Exception as e:
			self.logToConsole( "getValueForKey: %s" % str(e) )
			import traceback
			print(traceback.format_exc())
			return None
	
	@objc.python_method
	def italicize( self, x, y, italicAngle=0.0, pivotalY=0.0 ):
		"""
		Returns the italicized position of an NSPoint 'thisPoint'
		for a given angle 'italicAngle' and the pivotal height 'pivotalY',
		around which the italic slanting is executed, usually half x-height.
		Usage: myPoint = italicize(myPoint,10,xHeight*0.5)
		"""
		#x = thisPoint.x
		yOffset = y - pivotalY # calculate vertical offset
		italicAngle = math.radians( italicAngle ) # convert to radians
		tangens = math.tan( italicAngle ) # math.tan needs radians
		horizontalDeviance = tangens * yOffset # vertical distance from pivotal point
		x += horizontalDeviance # x of point that is yOffset from pivotal point
		return x
	
	@objc.python_method
	def offsetLayer( self, thisLayer, offset, makeStroke=False, position=0.5, autoStroke=False ):
		offsetFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		try:
			# GLYPHS 3:	
			offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_metrics_error_shadow_capStyleStart_capStyleEnd_keepCompatibleOutlines_(
				thisLayer,
				offset, offset, # horizontal and vertical offset
				makeStroke,     # if True, creates a stroke
				autoStroke,     # if True, distorts resulting shape to vertical metrics
				position,       # stroke distribution to the left and right, 0.5 = middle
				None, None, None, 0, 0, False )
		except:
			# GLYPHS 2:
			offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
				thisLayer,
				offset, offset, # horizontal and vertical offset
				makeStroke,     # if True, creates a stroke
				autoStroke,     # if True, distorts resulting shape to vertical metrics
				position,       # stroke distribution to the left and right, 0.5 = middle
				None, None )
	
	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		# query user input
		number = int(self.getValueForKey(customParameters,"number"))
		thickness = int(self.getValueForKey(customParameters,"thickness"))
		minDistance = int(self.getValueForKey(customParameters,"minDistance"))
		maxDistance = int(self.getValueForKey(customParameters,"maxDistance"))
		minLength = int(self.getValueForKey(customParameters,"minLength"))
		maxLength = int(self.getValueForKey(customParameters,"maxLength"))
		minGap = int(self.getValueForKey(customParameters,"minGap"))
		maxGap = int(self.getValueForKey(customParameters,"maxGap"))
		number = int(self.getValueForKey(customParameters,"number"))
		right = bool(self.getValueForKey(customParameters,"right"))
		
		# query font and master settings
		font = layer.font()
		master = layer.associatedFontMaster()
		italicAngle = master.italicAngle
		
		# determine all possible bar positions through glyph bounds
		minY = int(layer.bounds.origin.y)
		maxY = int(layer.bounds.origin.y + layer.bounds.size.height - thickness)
		minX = int(layer.bounds.origin.x)
		maxX = int(layer.bounds.origin.x + layer.bounds.size.width)
		
		# layer for measuring
		measureLayer = layer.copyDecomposedLayer()
		self.offsetLayer( measureLayer, thickness*1.8 )
		
		# first bar position:
		bottomY = random.randint( min(maxY-int((minY+maxY)/number), maxY), maxY )
		
		for i in range(number):
			if not bottomY < minY:
				topY = bottomY + thickness
			
				# measure glyph at speedline height
				averageY = (topY+bottomY)*0.5
				intersections = measureLayer.intersectionsBetweenPoints(
					NSPoint( minX-1, averageY ),
					NSPoint( maxX+1, averageY ),
					components = True
				)
				leftEdge = minX
				rightEdge = maxX
				if len(intersections) > 2:
					leftEdge = intersections[1].x
					rightEdge = intersections[-2].x
			
				# distance of speedline from glyph
				try:
					distance = random.randint( minDistance, maxDistance )
				except:
					distance = minDistance
			
				# length of speedline
				try:
					length = random.randint( minLength, maxLength )
				except:
					length = minLength
			
				# determine coordinates for left or right orientation
				if right:
					leftX = rightEdge + distance
					rightX = leftX + length
				else:
					rightX = leftEdge - distance
					leftX = rightX - length
			
				# draw the bar
				pen = layer.getPen()
				pen.moveTo( (leftX, bottomY) )
				pen.lineTo( (rightX, bottomY) )
				italicTopRight = self.italicize( rightX, topY, italicAngle=italicAngle, pivotalY=bottomY )
				pen.lineTo( (italicTopRight, topY) )
				italicTopLeft = self.italicize( leftX, topY, italicAngle=italicAngle, pivotalY=bottomY )
				pen.lineTo( (italicTopLeft, topY) )
				pen.closePath()
				pen.endPath()
			
				# calculate next bar position:
				gapBetweenSpeedlineBottoms = random.randint(
					min( thickness+minGap, thickness+maxGap ), 
					thickness+maxGap
				)
				bottomY -= gapBetweenSpeedlineBottoms

	@objc.python_method
	def generateCustomParameter( self ):
		return "%s; number:%s; thickness:%s; minDistance:%s; maxDistance:%s; minLength:%s; maxLength:%s; minGap:%s; maxGap:%s; right:%i" % (
			self.__class__.__name__,
			Glyphs.defaults['com.mekkablue.Speedlines.number'],
			Glyphs.defaults['com.mekkablue.Speedlines.thickness'],
			Glyphs.defaults['com.mekkablue.Speedlines.minDistance'],
			Glyphs.defaults['com.mekkablue.Speedlines.maxDistance'],
			Glyphs.defaults['com.mekkablue.Speedlines.minLength'],
			Glyphs.defaults['com.mekkablue.Speedlines.maxLength'],
			Glyphs.defaults['com.mekkablue.Speedlines.minGap'],
			Glyphs.defaults['com.mekkablue.Speedlines.maxGap'],
			Glyphs.defaults['com.mekkablue.Speedlines.right'],
		)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
