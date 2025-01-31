PULSONIX_LIBRARY_ASCII "SamacSys ECAD Model"
//1310419/239391/2.46/10/4/Integrated Circuit

(asciiHeader
	(fileUnits MM)
)
(library Library_1
	(padStyleDef "s25"
		(holeDiam 0)
		(padShape (layerNumRef 1) (padShapeType Rect)  (shapeWidth 0.250) (shapeHeight 0.250))
		(padShape (layerNumRef 16) (padShapeType Ellipse)  (shapeWidth 0) (shapeHeight 0))
	)
	(textStyleDef "Normal"
		(font
			(fontType Stroke)
			(fontFace "Helvetica")
			(fontHeight 1.27)
			(strokeWidth 0.127)
		)
	)
	(patternDef "BGSA12GN10E6327XTSA1" (originalName "BGSA12GN10E6327XTSA1")
		(multiLayer
			(pad (padNum 1) (padStyleRef s25) (pt -0.025, 0.600) (rotation 90))
			(pad (padNum 2) (padStyleRef s25) (pt -0.025, 0.200) (rotation 90))
			(pad (padNum 3) (padStyleRef s25) (pt -0.025, -0.200) (rotation 90))
			(pad (padNum 4) (padStyleRef s25) (pt -0.025, -0.600) (rotation 90))
			(pad (padNum 5) (padStyleRef s25) (pt 0.375, -0.600) (rotation 90))
			(pad (padNum 6) (padStyleRef s25) (pt 0.775, -0.600) (rotation 90))
			(pad (padNum 7) (padStyleRef s25) (pt 0.775, -0.200) (rotation 90))
			(pad (padNum 8) (padStyleRef s25) (pt 0.775, 0.200) (rotation 90))
			(pad (padNum 9) (padStyleRef s25) (pt 0.775, 0.600) (rotation 90))
			(pad (padNum 10) (padStyleRef s25) (pt 0.375, 0.600) (rotation 90))
		)
		(layerContents (layerNumRef 18)
			(attr "RefDes" "RefDes" (pt 0.000, 0.000) (textStyleRef "Normal") (isVisible True))
		)
		(layerContents (layerNumRef 28)
			(line (pt -0.175 0.75) (pt 0.925 0.75) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt 0.925 0.75) (pt 0.925 -0.75) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt 0.925 -0.75) (pt -0.175 -0.75) (width 0.025))
		)
		(layerContents (layerNumRef 28)
			(line (pt -0.175 -0.75) (pt -0.175 0.75) (width 0.025))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt -1.925 1.75) (pt 1.925 1.75) (width 0.1))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt 1.925 1.75) (pt 1.925 -1.75) (width 0.1))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt 1.925 -1.75) (pt -1.925 -1.75) (width 0.1))
		)
		(layerContents (layerNumRef Courtyard_Top)
			(line (pt -1.925 -1.75) (pt -1.925 1.75) (width 0.1))
		)
		(layerContents (layerNumRef 18)
			(line (pt -0.825 0.5) (pt -0.825 0.5) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(arc (pt -0.825, 0.6) (radius 0.1) (startAngle 270) (sweepAngle -180.0) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(line (pt -0.825 0.7) (pt -0.825 0.7) (width 0.2))
		)
		(layerContents (layerNumRef 18)
			(arc (pt -0.825, 0.6) (radius 0.1) (startAngle 90.0) (sweepAngle -180.0) (width 0.2))
		)
	)
	(symbolDef "BGSA12GN10E6327XTSA1" (originalName "BGSA12GN10E6327XTSA1")

		(pin (pinNum 1) (pt 0 mils 0 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -25 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 2) (pt 0 mils -100 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -125 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 3) (pt 0 mils -200 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -225 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 4) (pt 0 mils -300 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -325 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 5) (pt 0 mils -400 mils) (rotation 0) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 230 mils -425 mils) (rotation 0]) (justify "Left") (textStyleRef "Normal"))
		))
		(pin (pinNum 6) (pt 1200 mils 0 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 970 mils -25 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 7) (pt 1200 mils -100 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 970 mils -125 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 8) (pt 1200 mils -200 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 970 mils -225 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 9) (pt 1200 mils -300 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 970 mils -325 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(pin (pinNum 10) (pt 1200 mils -400 mils) (rotation 180) (pinLength 200 mils) (pinDisplay (dispPinName true)) (pinName (text (pt 970 mils -425 mils) (rotation 0]) (justify "Right") (textStyleRef "Normal"))
		))
		(line (pt 200 mils 100 mils) (pt 1000 mils 100 mils) (width 6 mils))
		(line (pt 1000 mils 100 mils) (pt 1000 mils -500 mils) (width 6 mils))
		(line (pt 1000 mils -500 mils) (pt 200 mils -500 mils) (width 6 mils))
		(line (pt 200 mils -500 mils) (pt 200 mils 100 mils) (width 6 mils))
		(attr "RefDes" "RefDes" (pt 1050 mils 300 mils) (justify Left) (isVisible True) (textStyleRef "Normal"))
		(attr "Type" "Type" (pt 1050 mils 200 mils) (justify Left) (isVisible True) (textStyleRef "Normal"))

	)
	(compDef "BGSA12GN10E6327XTSA1" (originalName "BGSA12GN10E6327XTSA1") (compHeader (numPins 10) (numParts 1) (refDesPrefix IC)
		)
		(compPin "1" (pinName "NC_1") (partNum 1) (symPinNum 1) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "2" (pinName "RF1") (partNum 1) (symPinNum 2) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "3" (pinName "GND_1") (partNum 1) (symPinNum 3) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "4" (pinName "VDD") (partNum 1) (symPinNum 4) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "5" (pinName "NC_2") (partNum 1) (symPinNum 5) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "6" (pinName "CTRL") (partNum 1) (symPinNum 6) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "7" (pinName "GND_2") (partNum 1) (symPinNum 7) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "8" (pinName "RF2") (partNum 1) (symPinNum 8) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "9" (pinName "NC_3") (partNum 1) (symPinNum 9) (gateEq 0) (pinEq 0) (pinType Unknown))
		(compPin "10" (pinName "RFC") (partNum 1) (symPinNum 10) (gateEq 0) (pinEq 0) (pinType Unknown))
		(attachedSymbol (partNum 1) (altType Normal) (symbolName "BGSA12GN10E6327XTSA1"))
		(attachedPattern (patternNum 1) (patternName "BGSA12GN10E6327XTSA1")
			(numPads 10)
			(padPinMap
				(padNum 1) (compPinRef "1")
				(padNum 2) (compPinRef "2")
				(padNum 3) (compPinRef "3")
				(padNum 4) (compPinRef "4")
				(padNum 5) (compPinRef "5")
				(padNum 6) (compPinRef "6")
				(padNum 7) (compPinRef "7")
				(padNum 8) (compPinRef "8")
				(padNum 9) (compPinRef "9")
				(padNum 10) (compPinRef "10")
			)
		)
		(attr "Manufacturer_Name" "Infineon")
		(attr "Manufacturer_Part_Number" "BGSA12GN10E6327XTSA1")
		(attr "Mouser Part Number" "726-BGSA12GN10E6327X")
		(attr "Mouser Price/Stock" "https://www.mouser.com/Search/Refine.aspx?Keyword=726-BGSA12GN10E6327X")
		(attr "RS Part Number" "")
		(attr "RS Price/Stock" "")
		(attr "Description" "RF Switch ICs CMOS SWITCH")
		(attr "<Hyperlink>" "https://www.infineon.com/dgdl/Infineon-BGSA12GN10-DS-v02_10-EN.pdf?fileId=5546d46255dd933d0155e9daddca09f6")
		(attr "<Component Height>" "0")
	)

)
