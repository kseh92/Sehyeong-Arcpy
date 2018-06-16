#-*- coding: utf-8 -*-
import arcpy, os
import arcpy.mapping as map
arcpy.env.overwriteOutput = True

#                     Directory
arcpy.env.workspace = "D:\Arcpy"

# 현재 mxd 파일 불러오기
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]

# Assign variable names to the layers you want to manipulate.
dataLyr = arcpy.mapping.ListLayers(mxd)[4]


# Unique values 추출
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

# (Dataset, Field Name)
myValues = unique_values(r'D:\Arcpy\ver3.csv', 'name')

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
    out_pdf = arcpy.env.workspace + os.sep + "Results" + os.sep + "Map_" + cleanname + ".pdf"
    out_png = arcpy.env.workspace + os.sep + "Results" + os.sep + "Map_" + cleanname + ".png"
    arcpy.mapping.ExportToPDF(mxd, out_pdf, resolution=600)
    arcpy.mapping.ExportToPNG(mxd, out_png, resolution=600)
    mxd.saveACopy(r"D:\Arcpy\Results\\" + cleanname + ".mxd")
    dataLyr.definitionQuery = None

del mxd
del myValues
