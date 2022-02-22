import arcpy
from arcgis.gis import GIS
import os
import sys

arcpy.AddMessage("Starting . . . ")

url = arcpy.GetParameterAsText(0) #optional
user = arcpy.GetParameterAsText(1) #optional
passw = arcpy.GetParameterAsText(2) #optional
folderLoc = arcpy.GetParameterAsText(3)
title = arcpy.GetParameterAsText(4) #optional
owner = arcpy.GetParameterAsText(5) #optional
layerName = arcpy.GetParameterAsText(6) 
nameField1 = arcpy.GetParameterAsText(7) #optional
nameField2 = arcpy.GetParameterAsText(8) #optional
nameField3 = arcpy.GetParameterAsText(9) #optional
nameField4 = arcpy.GetParameterAsText(10) #optional

if url != "":
    gis = GIS(url,username=user,password=passw)
    arcpy.AddMessage("Logged into your organization as {0}".format(user))
else:
    gis = GIS()
    arcpy.AddMessage("Logged in as anonymous user")





if title != "" and owner == "":
    queryResult = "title:{0}".format(title)
elif title != "" and owner != "":
    queryResult = "title:{0} & owner:{1}".format(title,owner)
elif title == "" and owner != "":
    queryResult = "owner:{0}".format(owner)
else:
    arcpy.AddError("No query has been speified, all layer would be returned."
                   "Please run again specifying either a title or owner to query")
    sys.exit(1)


fmSurveySearch = gis.content.search(query='{0}'.format(queryResult),item_type="Feature Layer")

if len(fmSurveySearch) > 1:
    arcpy.AddWarning("Query found more than 1 feature layer, the script tool will only extract photos from first layer in the list"
                     "Layer photos are being extrcted from is: {0}".format(fmSurveySearch[0]))

fmSurvey = fmSurveySearch[0]



fmSurveyLyr = None
for lyr in fmSurvey.layers:
    if lyr.properties.name == layerName:
        fmSurveyLyr = lyr
        arcpy.AddMessage("Selected layer with name {0} to extract photos from".format(layerName))
        break
if fmSurveyLyr is None:
    arcpy.AddError("Please run again specifying the correct layer name"
                   "No layer has been speified as there is no layer with the name {0}.".format(layerName))
    sys.exit(1)


PhotoPath = os.path.join(folderLoc,layerName+"_Photos")
if not os.path.exists(PhotoPath):
    os.makedirs(PhotoPath)




objIds = fmSurveyLyr.query(return_ids_only = True)
arcpy.AddMessage(objIds)
listObjIds = objIds["objectIds"]
arcpy.AddMessage(listObjIds)

for objID in listObjIds: 
    objAtt = lyr.attachments.get_list(oid=objID)
    arcpy.AddMessage(objAtt)
    sql = "OBJECTID = {}".format(objID)
    lyrQuery = fmSurveyLyr.query(where = sql, out_fields="*")
    lyrQueryFeatures = lyrQuery.features
    if nameField1 != "":
        name1 = "_{0}_".format(lyrQueryFeatures[0].attributes["{0}".format(nameField1)].replace(" ","_"))
        arcpy.AddMessage(name1)
    else:
        name1 =""
        arcpy.AddMessage("No Name field selected for Name 1")
    if nameField2 != "":
        name2 = "_{0}_".format(lyrQueryFeatures[0].attributes["{0}".format(nameField2)].replace(" ","_"))
        arcpy.AddMessage(name2)
    else:
        name2 =""
        arcpy.AddMessage("No Name field selected for Name 2")
    if nameField3 != "":
        name3 = "_{0}_".format(lyrQueryFeatures[0].attributes["{0}".format(nameField3)].replace(" ","_"))
        arcpy.AddMessage(name3)
    else:
        name3 =""
        arcpy.AddMessage("No Name field selected for Name 3")
    if nameField4 != "":
        name4 = "_{0}_".format(lyrQueryFeatures[0].attributes["{0}".format(nameField4)].replace(" ","_"))
        arcpy.AddMessage(name4)
    else:
        name4 =""
        arcpy.AddMessage("No Name field selected for Name 4")
        
    for k in range(len(objAtt)):
        attachmentName = objAtt[k]["name"]
        arcpy.AddMessage(attachmentName)
        attachmentID = objAtt[k]["id"]
        arcpy.AddMessage(attachmentID)
        pic = lyr.attachments.download(oid=objID,attachment_id=attachmentID, save_path=PhotoPath)
        newName = os.path.join(PhotoPath,layerName+str(name1)+str(name2)+str(name3)+str(name4)+str(attachmentID)+".jpg")
        os.rename(pic[0],newName)

arcpy.AddMessage("Finished")
