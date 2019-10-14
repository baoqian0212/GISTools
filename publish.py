# -*- coding: cp936 -*-
"""
Description:�Զ��������ݷ�������
Author:baoqian
Prompt:code in Python27 env
"""

"""
��������������Ƕ���ݼ�������Ӱ�����
����������1 servicename�������� 2 mdpath����Ƕ���ݼ�·�� 3 server_url��server�ķ���·��url
"""
# -*- coding: utf-8 -*-


import arcpy as ARCPY
import os as OS
import shutil as SHUTIL
generalfolder = OS.getcwd()
servicename = 'MyImageServicebyPython2'
mdpath = r'D:\gisdata\MosaicDataset\test.gdb\Gf1'
# Step1 ����GIS�����������ļ�

print u'Step1 ����GIS�����������ļ�...'

connecttype = 'ADMINISTER_GIS_SERVICES'
# ����һ�����ڴ��ags��sd���ļ���,��ʱ���´��ٵ���ʱ�ļ����ݽ�������
outdir = OS.path.join(generalfolder, 'PublishImageService')
if OS.path.exists(outdir):
    SHUTIL.rmtree(outdir)
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

print '      ' + out_name.decode('utf-8') + u' �Ѵ���'

# Step2 ����Ӱ�������ݸ��ļ�(.sddraft)

print u'Step2 ����Ӱ�������ݸ��ļ�...'

connoctionfile = OS.path.join(outdir, out_name)
service = servicename
sddraft = OS.path.join(outdir, service + '.sddraft')

ARCPY.CreateImageSDDraft(mdpath, sddraft, service,
                         'ARCGIS_SERVER', copy_data_to_server=False)
print '      ' + service + '.sddraft' + u'  �Ѵ���'

# Step3 ����������ݸ�
print u'Step3 ����������ݸ��ļ�...'
analysis = ARCPY.mapping.AnalyzeForSD(sddraft)

print(u"      ����������ݸ���:")
for key in list(analysis.keys()):
    print("      ---{}---".format(key.upper()))
    for ((message, code), layerlist) in analysis[key].items():
        print("        (CODE {})  {} ".format(code, message))

# Step4 ���� sddraft ���������ļ�sd
print u'Step4 ����sddraft ���������ļ�sd...'
outSDfile = OS.path.join(outdir, service+".sd")

ARCPY.StageService_server(sddraft, outSDfile)
print u'      Done!'

# Step5 ���������ļ�������������
print u'Step5 ���������ļ�������������...'
inSdFile = outSDfile
inServer = connoctionfile
inServiceName = service

ARCPY.UploadServiceDefinition_server(inSdFile, inServer, inServiceName)
print u'      Done!'




