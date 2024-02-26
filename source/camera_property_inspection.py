import bpy
from math import pi


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "camera zoom"

    def draw(self, context):
        layout = self.layout
        [a.tag_redraw() for a in context.screen.areas]  # If we don't do this, values don't update unless you hover your mouse over the panel
        space = context.area.spaces.active
        region = space.region_3d
        loc, rot, sca = region.view_matrix.decompose()
        lrs = {"loc":loc, "rot":rot, "sca":sca}
        col = layout.column()
        lrsbox = col.box()
        
        lrsbox.label(text = f"loc : {loc}")
        lrsbox.label(text = f"rot : {rot}")
        lrsbox.label(text = f"sca : {sca}")
        col.prop(space, "lens")
        # This is some kind of "zoom" but it doesn't go beyond 0 (eg. You can't zoom past region.view_location) :
        col.prop(region, "view_distance")
        col.prop(region, "is_perspective")
        col.prop(region, "view_perspective")
        col.prop(region, "view_location")
        col.prop(region, "view_rotation")
        euler = region.view_rotation.to_euler()
        # Seeing Euler values is far more convenient to the layman. So we convert the quaternion to euler angles :
        box = col.box()
        box.label(text="View Rotation")
        for axis in "x", "y", "z":
            angle = round(getattr(euler, axis) * 180 / pi, 2)
            box.label(text=f"{axis.upper()} : {angle}°")
        col.prop(region, "view_matrix")
        col.prop(region, "window_matrix")
        col.prop(region, "perspective_matrix")  # Per the docs this is readonly and = to window_matrix * view_matrix
        col.enabled=True # Comment this if you want to be able to tweak the fields
        

def register():
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)


if __name__ == "__main__":
    register()