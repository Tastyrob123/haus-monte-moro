import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath='/Users/robertreff/Desktop/Website-Projekte/Tasty Webdesign Showcase/assets/3d/iphone.glb')
for o in bpy.data.objects:
    if o.type=='MESH': print('OBJ', o.name, [round(v,4) for v in o.dimensions], [m.name for m in o.data.materials][:12])
for im in bpy.data.images: print('IMG', im.name, im.size[:])
