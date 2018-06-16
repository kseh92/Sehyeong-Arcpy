#-*- coding: utf-8 -*-
import arcpy, os
import arcpy.mapping as map
arcpy.env.overwriteOutput = True

# 현재 mxd 파일 불러오기
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

# Assign variable names to the layers you want to manipulate.
dataLyr = arcpy.GetParameter(0)


# Unique values 추출
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

# (Dataset, Field Name)
myTable = arcpy.GetParameterAsText(1)
myField = arcpy.GetParameterAsText(2)
myValues = unique_values(myTable, myField)

# 쿼리 돌리기 loop
for name in myValues:
    cleanname = name.strip()

    # """Field Name" =
    whereClause = """"name" = '""" + cleanname + "'"
    dataLyr.definitionQuery = whereClause
    extent = dataLyr.getSelectedExtent(False)

    # 제목 바꾸기
    title = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[1]
    title.text = cleanname

    # export 하기
    outFolder = arcpy.GetParameterAsText(3)
    output = arcpy.SetParameterAsText(3, outFolder)
    out_pdf = outFolder + os.sep + "Map_" + cleanname + ".pdf"
    out_png = outFolder + os.sep + "Map_" + cleanname + ".png"
    arcpy.mapping.ExportToPDF(mxd, out_pdf, resolution=600)
    arcpy.mapping.ExportToPNG(mxd, out_png, resolution=600)
    mxd.saveACopy(outFolder + os.sep + cleanname + ".mxd")
    dataLyr.definitionQuery = None

del mxd
del myValues
