import bpy
import os
import time
from mathutils import Euler, Vector
from math import radians, sqrt

FRONT = [0.5, 0.5, -0.5, -0.5]
BACK = [0.5, 0.5, 0.5, 0.5]
RIGHT = [0.707, 0.707, 0, 0]
LEFT = [0, 0, -0.707, -0.707]
TOP = [0.707, 0, 0, -0.707]
BOTTOM = [0, 0.707, -0.707, 0]
UPPERSLANTED1 = [0.830977, 0.405294, 0.16705, 0.342504]
UPPERSLANTED2 = [0.279699, 0.123362, 0.384227, 0.87116]
UPPERSLANTED3 = [-0.310878, -0.134529, 0.373669, 0.863498]
UPPERSLANTED4 = [-0.783845, -0.402842, 0.216002, 0.420294]
NONE_HEIGHLIGHT_COLOR = (0.8 , 0.8 , 0.8 , 0.1)
HEIGHLIGHT_COLOR = (1.0 , 1.0 , 0.0 , 0.95)

VIEWS = [FRONT, BACK, RIGHT, LEFT, TOP, BOTTOM, UPPERSLANTED1, UPPERSLANTED2, UPPERSLANTED3, UPPERSLANTED4]
VIEWS_INFO = ["front", "back", "right", "left", "top", "bottom", "angled1", "angled2", "angled3", "angled4"]

RESOLUTION_X=1080
RESOLUTION_Y=1080
PIXEL_ASPECT_X=1
PIXEL_ASPECT_Y=1
OBJECT_ID = 10450
IS_PERSPECTIVE = False


def select_by_name(name):
    ob = bpy.context.scene.objects[name]         # Get the object
    bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
    bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
    ob.select_set(True)

def select_hierarchy_by_name(name):
    ob = bpy.context.scene.objects[name]         # Get the object
    bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
    bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
    ob.select_set(True)        
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.select_grouped(extend=True, type='CHILDREN_RECURSIVE')

def get_3d_view_context():
    for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region, 'edit_object': bpy.context.edit_object}
                        return override
    return None


def assign_material(obj, name):
    mat = bpy.data.materials.get(name)
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name=name)

    # Assign it to object
    if obj.data.materials:
        # assign to 1st material slot
        temp_mat = obj.data.materials[0]
        obj.data.materials[0] = mat
        obj.data.materials.append(temp_mat)

    else:
        # no slots
        obj.data.materials.append(mat)

    obj.active_material.diffuse_color = HEIGHLIGHT_COLOR

def remove_material(obj, name):
    obj.data.materials.pop(index = 0)

def fit_viewport_on_selection_with_current_view_angle():
    #center the viewport on the mesh
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
    override = get_3d_view_context()
    bpy.ops.view3d.view_selected(override)


def set_all_transparent():
    for m in bpy.data.materials:
        m.diffuse_color = NONE_HEIGHLIGHT_COLOR

def save_all_angles_of_selected_obj(override, obj, object_name):
    r3d = override["area"].spaces[0].region_3d
    rot = r3d.view_rotation
    r3d.view_location = (0.0, 0.0, 0.0)
    r3d.view_distance = 1.393
    for count, view in enumerate(VIEWS):
        rot[:] = view
        # fit_viewport_on_selection_with_current_view_angle()
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select the mesh object
        
        bpy.context.view_layer.objects.active = obj
        material_name = "temperary_highlight"
        assign_material(obj,material_name)

        obj.select_set(True)
        bpy.context.scene.render.image_settings.file_format = "PNG"
        # Render the viewport and save the result
        bpy.ops.render.opengl(write_still=True)
        render_path = f'{OBJECT_ID}/parts_photograph/{object_name}/{VIEWS_INFO[count]}.png'
        output_path = os.path.join(rootDir, render_path)
        bpy.data.images['Render Result'].save_render(output_path)
        remove_material(obj, material_name)

def get_bound_box(object_list):
    # Initialize lists to hold all corners
    all_corners = []
    # Iterate over all mesh objects in the scene
    for obj in object_list:
        if obj.type == 'MESH':
            # Get the world matrix of the object
            mat_world = obj.matrix_world
            # Transform each bounding box corner to world space and append to all_corners
            all_corners.extend([mat_world @ Vector(corner) for corner in obj.bound_box])

    # Initialize min and max vectors with opposite infinities
    min_vec = Vector((float('inf'), float('inf'), float('inf')))
    max_vec = Vector((float('-inf'), float('-inf'), float('-inf')))

    # Find min and max across all corners
    for corner in all_corners:
        min_vec = Vector((min(min_vec.x, corner.x), min(min_vec.y, corner.y), min(min_vec.z, corner.z)))
        max_vec = Vector((max(max_vec.x, corner.x), max(max_vec.y, corner.y), max(max_vec.z, corner.z)))
    
    return min_vec, max_vec



rootDir = "/home/octipus/Projects/assetExtract/mobility/"
gltf_file_path = f"{OBJECT_ID}/mobility.gltf"
full_path = os.path.join(rootDir, gltf_file_path)
bpy.context.scene.render.resolution_x = RESOLUTION_X
bpy.context.scene.render.resolution_y = RESOLUTION_Y 
bpy.context.scene.render.pixel_aspect_x = PIXEL_ASPECT_X
bpy.context.scene.render.pixel_aspect_y = PIXEL_ASPECT_Y



# Empty the Blender scene
bpy.ops.object.select_all(action='SELECT')  # Select all objects
bpy.ops.object.delete()  # Delete the selected objects

# Create a group that will use for normalization
bpy.ops.object.empty_add(type='PLAIN_AXES', align="WORLD", location=(0, 0, 0))
parent_empty = bpy.context.object
parent_empty.name = "NormizeGroup"

# import the target object
bpy.ops.import_scene.gltf(filepath=full_path)

# move the imported object into the empty normizing group
for obj in bpy.context.selected_objects:  # This assumes the imported objects are selected
    if obj.parent is None:
        obj.parent = parent_empty
        break

# remember the empty normizing group as normalizing_node 
normalizing_node = None
for obj in bpy.context.scene.objects:  # This assumes the imported objects are selected
    if obj.parent is None:
        normalizing_node = parent_empty
        break
    
if normalizing_node is None:
    raise Exception("did not find the normalizing root")

select_hierarchy_by_name("NormizeGroup")
min_vec, max_vec = get_bound_box(bpy.context.selected_objects)

bound_sum = max_vec + min_vec
# scale_factor = 1 / max(bound_diff.x, bound_diff.y, bound_diff.z) * 
scale_factor = 1 / max(max_vec.x, max_vec.y, max_vec.z, abs(min_vec.x), abs(min_vec.y), abs(min_vec.z)) / sqrt(2)
center = bound_sum/2
normalizing_node.location = -center
normalizing_node.scale = (scale_factor, scale_factor, scale_factor)

override = get_3d_view_context()
if IS_PERSPECTIVE:
    override["area"].spaces.active.region_3d.view_perspective = "PERSP"
else:
    override["area"].spaces.active.region_3d.view_perspective = "ORTHO"

# Iterate through all areas in the current screen
for area in bpy.context.screen.areas:
    # Check if the area is a 3D View
    if area.type == 'VIEW_3D':
        # Get the space data for the 3D View area
        space_data = area.spaces.active
        # Change the shading type to 'MATERIAL'
        space_data.shading.type = 'SOLID'
        break  # Stop after finding the first 3D View area


objects = bpy.context.selected_objects
count = 0
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        # override = get_3d_view_context()
        # bpy.ops.view3d.view_selected(override)
        set_all_transparent()
        save_all_angles_of_selected_obj(override, obj, object_name=obj.name)
        count += 1
        print(f"done processing: {obj.name}")
        # if(count > 1):
        #     break


