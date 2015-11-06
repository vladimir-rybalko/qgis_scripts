# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import qgis.core
import qgis.utils

layer = iface.activeLayer()
dataProvider = layer.dataProvider()
layer.startEditing()

for f in layer.getFeatures():
    bboxSpliter = []
    id = f.id()
    geom = f.geometry()
    bbox = geom.boundingBox()
    
    xMin = bbox.xMinimum()
    xMax = bbox.xMaximum()
    yMin = bbox.yMinimum()
    yMax = bbox.yMaximum()
    
    width = xMax - xMin
    height = yMax - yMin

    if (width > 10500000 or height > 10500000):
        print id
        #rectangle = geom.boundingBox()
        #xMin = rectangle.xMinimum()
        #xMax = rectangle.xMaximum()
        #yMin = rectangle.yMinimum()
        #yMax = rectangle.yMaximum()
        xHalf = xMin + (xMax - xMin)/2
        yHalf = yMin + (yMax - yMin)/2 
        bboxSpliter.append(QgsGeometry.fromWkt("POLYGON(("+xMin.__str__()+" "+yMin.__str__()+","+xMin.__str__()+" "+yHalf.__str__()+","+xHalf.__str__()+" "+yHalf.__str__()+","+xHalf.__str__()+" "+yMin.__str__()+","+xMin.__str__()+" "+yMin.__str__()+"))"))
        bboxSpliter.append(QgsGeometry.fromWkt("POLYGON(("+xHalf.__str__()+" "+yMin.__str__()+","+xHalf.__str__()+" "+yHalf.__str__()+","+xMax.__str__()+" "+yHalf.__str__()+","+xMax.__str__()+" "+yMin.__str__()+","+xHalf.__str__()+" "+yMin.__str__()+"))"))
        bboxSpliter.append(QgsGeometry.fromWkt("POLYGON(("+xHalf.__str__()+" "+yHalf.__str__()+","+xHalf.__str__()+" "+yMax.__str__()+","+xMax.__str__()+" "+yMax.__str__()+","+xMax.__str__()+" "+yHalf.__str__()+","+xHalf.__str__()+" "+yHalf.__str__()+"))"))
        bboxSpliter.append(QgsGeometry.fromWkt("POLYGON(("+xMin.__str__()+" "+yHalf.__str__()+","+xMin.__str__()+" "+yMax.__str__()+","+xHalf.__str__()+" "+yMax.__str__()+","+xHalf.__str__()+" "+yHalf.__str__()+","+xMin.__str__()+" "+yHalf.__str__()+"))"))
        layer.deleteFeature(id)
        for split in bboxSpliter:
            diff = QgsFeature()
            diff.setGeometry(geom.intersection(split))
            diff.setAttributes([id])
            dataProvider.addFeatures([diff])
print "complit"
layer.commitChanges()
