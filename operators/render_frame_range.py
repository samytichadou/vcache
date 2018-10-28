import bpy
import os

from ..preferences import get_addon_preferences
from ..misc_functions import absolute_path, create_cache_folder, suppress_files_pattern
from .render_functions import *

#open gl render frame range
class VCacheOpenGLRange(bpy.types.Operator):
    bl_idname = "vcache.opengl_range"
    bl_label = "Cache Frame Range"
    bl_description = "Cache Frame Range"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        addon_preferences = get_addon_preferences()
        scn=context.scene
        
        #check if 3d area
        good_area=find_area()
        if good_area!='':
                                
            #background render
            if scn.vcache_background==True:
                
                #save file
                bpy.ops.wm.save_mainfile()
                
                #save file as and reopen original
                temp=save_temp_file(addon_preferences)
                
                #launch command line
                
                            
            #no background render pre action
            else:                
                #memorize render settings
                old_settings=memorize_render_settings()
            
            #shared actions
            if scn.vcache_background==False or scn.vcache_is_background_file==True:
                #create cache folder if needed
                create_cache_folder()
                
                #define size of the area
                resolution_x,resolution_y=get_area_size(good_area)
                
                #define render name
                cache=addon_preferences.prefs_folderpath
                cachefolder = absolute_path(cache)
                pattern, render_name= define_pattern_render_name()
                                
                #delete previous renders
                suppress_files_pattern(cachefolder, pattern)
                
                #set render settings
                    #if cam = 1, render without context
                cam=set_cache_render_settings(addon_preferences, cachefolder, render_name, resolution_x, resolution_y, old_settings)
                
                #launch render with or without context
                if cam==1:
                    bpy.ops.render.opengl(animation=True, write_still=True, view_context=False)
                else:
                    bpy.ops.render.opengl(animation=True, write_still=True, view_context=True)
                
                #launch playback
                if addon_preferences.vcache_play_after_caching==True:
                    bpy.ops.vcache.playback_rangecache()
                                
            #no background render post action
            if scn.vcache_background==False:
                #reset render settings
                set_old_render_settings(old_settings)
                #print()               
        return {'FINISHED'}