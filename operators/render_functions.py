import bpy
import os

from ..preferences import get_addon_preferences
from ..misc_functions import absolute_path

#memorize render settings
def memorize_render_settings():
    scn=bpy.context.scene
    
    datas = {
        "filepath" : scn.render.filepath,
        "frame_current" : scn.frame_current,
        "file_format" : scn.render.image_settings.file_format,
        "color_depth" : scn.render.image_settings.color_depth,
        "quality" : scn.render.image_settings.quality,
        "compression" : scn.render.image_settings.compression,
        "tiff_codec" : scn.render.image_settings.tiff_codec,
        "color_mode" : scn.render.image_settings.color_mode,
        "resolution_x" : scn.render.resolution_x,
        "resolution_y" : scn.render.resolution_y,
        "resolution_percentage" : scn.render.resolution_percentage,
        "color_mode" : scn.render.image_settings.color_mode,
        "alpha_mode" : scn.render.alpha_mode,
        "use_antialiasing" : scn.render.use_antialiasing,
        "antialiasing_samples" : scn.render.antialiasing_samples,
        "camera" : scn.camera,
        "show_only_render" : bpy.context.space_data.show_only_render,
        "frame_start" : scn.frame_start,
        "frame_end" : scn.frame_end,
        }
    
    return datas

#set back render image_settings
def set_old_render_settings(datas):
    scn=bpy.context.scene
    
    scn.render.filepath = datas['filepath']
    scn.frame_current = datas['frame_current']
    scn.render.image_settings.file_format = datas['file_format']
    scn.render.image_settings.color_depth = datas['color_depth']
    scn.render.image_settings.quality = datas['quality']
    scn.render.image_settings.compression = datas['compression']
    scn.render.image_settings.tiff_codec = datas['tiff_codec']
    scn.render.image_settings.color_mode = datas['color_mode']
    scn.render.resolution_x = datas['resolution_x']
    scn.render.resolution_y = datas['resolution_y']
    scn.render.resolution_percentage = datas['resolution_percentage']
    scn.render.image_settings.color_mode = datas['color_mode']
    scn.render.alpha_mode = datas['alpha_mode']
    scn.render.use_antialiasing = datas['use_antialiasing']
    scn.render.antialiasing_samples = datas['antialiasing_samples']
    scn.camera = datas['camera']
    bpy.context.space_data.show_only_render = datas['show_only_render']
    scn.frame_start = datas['frame_start']
    scn.frame_end = datas['frame_end']

#save temp file and reopen original
def save_temp_file(addon_preferences):
    cache=addon_preferences.prefs_folderpath
    cachefolder = absolute_path(cache)
    blendpath=absolute_path(bpy.data.filepath)
    temp_filepath=os.path.join(cachefolder, bpy.path.basename(blendpath))
    
    #delete if already exists:
    if os.path.isfile(temp_filepath):
        os.remove(temp_filepath)
        
    bpy.ops.wm.save_as_mainfile(temp_filepath)
    bpy.ops.wm.open_mainfile(filepath="blendpath")
    
    return temp_filepath

#try to find biggest 3D view area:
def find_area():
    area_list=[]
    good_area=''
    
    if bpy.context.area.type=="VIEW_3D":
        good_area=bpy.context.area
    else:
        for area in bpy.context.window.screen.areas:
            if area.type=="VIEW_3D":
                area_list.append([area, area.width*area.height])
        if len(area_list)!=0:
            good_area=max(area_list, key=lambda x: x[1])[0]

    return good_area

#get 3D view area size
def get_area_size(area):
    realsize = bpy.context.scene.vcache_real_size
    print('function-----------')
    for i in area.regions:
        if i.type=='HEADER':
            if i.height!=1:
                h1=i.height
            else:
                h1=0
        elif i.type=='TOOLS' and realsize==False:
            if i.width!=1:
                w1=i.width
            else:
                w1=0
        elif i.type=='UI' and realsize==False:
            if i.width!=1:
                w2=i.width
            else:
                w2=0
    if realsize==False:
        resolution_x=area.width-(w1+w2)
        resolution_y=area.height-h1
    else:
        resolution_x=area.width
        resolution_y=area.height-h1
    print(resolution_x)
    print(resolution_y)
    print("end of function-----------")
        
    return {resolution_x, resolution_y}

#define render name and pattern
def define_pattern_render_name():
    if bpy.data.is_saved:
        blendname=(os.path.splitext(os.path.basename(bpy.data.filepath))[0])
    else:
        blendname='untitled'
    scenename=bpy.context.scene.name
    pattern=blendname + "___" + scenename + "___cache_"
    render_name=pattern + "##########"
    
    return {pattern, render_name}

#set render settings for cache
def set_cache_render_settings(addon_preferences, cachefolder, render_name, resolution_x, resolution_y, old_settings):
    scn = bpy.context.scene
    
    format = addon_preferences.cache_format
    depth = addon_preferences.cache_format_depth
    quality = addon_preferences.cache_format_quality
    compression = addon_preferences.cache_format_compression
    tiffcompression = addon_preferences.cache_tiff_compression
    channel= addon_preferences.cache_format_channel
    mult = addon_preferences.cache_dimension_coef
    realsize = scn.vcache_real_size
    draft = scn.vcache_draft
    only_render = scn.vcache_only_render
    cam = scn.vcache_camera

    scn.render.filepath = os.path.join(cachefolder, render_name)
    scn.render.image_settings.file_format = format
    scn.render.image_settings.color_mode = 'RGB'
    scn.render.resolution_x=resolution_x
    scn.render.resolution_y=resolution_y
    
    if scn.use_preview_range == True:
        scn.frame_start=scn.frame_preview_start
        scn.frame_end=scn.frame_preview_end

    if format=='JPEG':
        scn.render.image_settings.quality = quality
    elif format=='PNG':
        scn.render.image_settings.color_depth = depth
        scn.render.image_settings.compression = compression
        scn.render.image_settings.color_mode = channel
        if channel=='RGBA':
            scn.render.alpha_mode = 'TRANSPARENT'
    elif format=='TIFF':
        scn.render.image_settings.color_depth = depth
        scn.render.image_settings.compression = compression
        scn.render.image_settings.tiff_codec = tiffcompression
        scn.render.image_settings.color_mode = channel
        if channel=='RGBA':
            scn.render.alpha_mode = 'TRANSPARENT'
            
    if draft==True:
        scn.render.use_antialiasing = False
        scn.render.resolution_percentage=25
    else:
        scn.render.use_antialiasing = True
        scn.render.antialiasing_samples = '16'
        scn.render.resolution_percentage=100*mult
        
    if only_render==True:
        bpy.context.space_data.show_only_render=True
        
    chk=0
    if cam!='':
        for n in bpy.context.scene.objects:
            if n.name==cam:
                chk=1
                scn.render.resolution_x = old_settings['resolution_x']
                scn.render.resolution_y = old_settings['resolution_y']
                scn.render.resolution_percentage = opct
                
                bpy.context.scene.camera=n

        if chk==0:
            print("VCache --- Warning, "+cam+" missing - Clear it to Cache")
    
    return chk