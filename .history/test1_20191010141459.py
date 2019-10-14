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
import arcpy
import os
import time

generalfolder = 
servicename = 'MyFirstImageServicebyPython'
# Step1 创建GIS服务器连接文件

print u'Step1 创建GIS服务器连接文件...'

connecttype = 'ADMINISTER_GIS_SERVICES'
outdir = os.path.join(generalfolder, 'Demo_4_PublishImageService')
out_folder_path = outdir
out_name = 'ConnectToArcGISServer.ags'
server_url = 'https://localhost:6443/arcgis/admin'
use_staging_folder = False
staging_folder_path = outdir
username = 'siteadmin'
password = 'siteadmin'

arcpy.mapping.CreateGISServerConnectionFile(connecttype,
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
