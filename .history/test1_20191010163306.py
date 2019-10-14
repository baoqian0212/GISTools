"""
Description:自动推送数据发布服务
Author:baoqian
Prompt:code in Python27 env
"""

"""
功能描述：
参数描述：1 filepath：文件路径 2 savepath：保存路径
"""
# -*- coding: utf-8 -*-

import arcpy as ARCPY
import os as OS
import time as TIME
generalfolder = r'D:\gisdata\MosaicDataset'
servicename = 'MyImageServicebyPython'
mdpath = OS.path.join(generalfolder,
                      r'test.gdb\Gf1')
# Step1 创建GIS服务器连接文件

print u'Step1 创建GIS服务器连接文件...'

connecttype = 'ADMINISTER_GIS_SERVICES'
outdir = OS.path.join(generalfolder, 'Demo_4_PublishImageService')
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

connoctionfile = os.path.join(outdir, out_name)
service = servicename
sddraft = os.path.join(outdir, service + '.sddraft')

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
outSDfile = os.path.join(outdir, service+".sd")

ARCPY.StageService_server(sddraft, outSDfile)
print u'      Done!'

# Step5 将服务定义文件发布到服务器
print u'Step5 将服务定义文件发布到服务器...'
inSdFile = outSDfile
inServer = connoctionfile
inServiceName = service

ARCPY.UploadServiceDefinition_server(inSdFile, inServer, inServiceName)
print u'      Done!'
