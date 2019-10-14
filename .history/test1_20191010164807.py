"""
Description:自动推送数据发布服务
Author:baoqian
Prompt:code in Python27 env
"""

"""
功能描述：建镶嵌数据集发布成影像服务
参数描述：1 servicename：服务名 2 mdpath：镶嵌数据集路径 3 server_url：server的访问路径url
"""
# -*- coding: utf-8 -*-

import arcpy as ARCPY
import os as OS


generalfolder = OS.getcwd()
servicename = 'MyImageServicebyPython'
mdpath = r'镶嵌数据集路径'
# Step1 创建GIS服务器连接文件

print u'Step1 创建GIS服务器连接文件...'

connecttype = 'ADMINISTER_GIS_SERVICES'
# 创建一个用于存放ags和sd的文件夹,临时的下次再调用时文件内容将被覆盖
outdir = OS.path.join(generalfolder, 'PublishImageService')
if OS.path.exists(outdir):
  OS.rmdir(outdir)
OS.mkdir(outdir)

out_folder_path = outdir
out_name = 'ConnectToArcGISServer.ags'
server_url = 'https://localhost:6443/arcgis/admin'
use_staging_folder = False
staging_folder_path = outdir
username = 'siteadmin'
password = 'siteadmin'

ARCPY.mapping.CreateGISServerConnectionFile(connecttype,
                                            out_folder_path,
                                            out_name,
                                            server_url,
                                            "ARCGIS_SERVER",
                                            use_staging_folder,
                                            staging_folder_path,
                                            username,
                                            password,
                                            "SAVE_USERNAME")

print '      ' + out_name.decode('utf-8') + u' 已创建'

# Step2 创建影像服务定义草稿文件(.sddraft)

print u'Step2 创建影像服务定义草稿文件...'

connoctionfile = OS.path.join(outdir, out_name)
service = servicename
sddraft = OS.path.join(outdir, service + '.sddraft')

ARCPY.CreateImageSDDraft(mdpath, sddraft, service,
                         'ARCGIS_SERVER', copy_data_to_server=False)
print '      ' + service + '.sddraft' + u'  已创建'

# Step3 分析服务定义草稿
print u'Step3 分析服务定义草稿文件...'
analysis = ARCPY.mapping.AnalyzeForSD(sddraft)

print(u"      分析服务定义草稿结果:")
for key in list(analysis.keys()):
    print("      ---{}---".format(key.upper()))
    for ((message, code), layerlist) in analysis[key].items():
        print("        (CODE {})  {} ".format(code, message))

# Step4 过渡 sddraft 到服务定义文件sd
print u'Step4 过渡sddraft 到服务定义文件sd...'
outSDfile = OS.path.join(outdir, service+".sd")

ARCPY.StageService_server(sddraft, outSDfile)
print u'      Done!'

# Step5 将服务定义文件发布到服务器
print u'Step5 将服务定义文件发布到服务器...'
inSdFile = outSDfile
inServer = connoctionfile
inServiceName = service

ARCPY.UploadServiceDefinition_server(inSdFile, inServer, inServiceName)
print u'      Done!'
