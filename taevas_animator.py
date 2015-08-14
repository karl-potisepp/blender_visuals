#!/usr/bin/python

import bpy
import math
import random
import time

magical_dwarves = "fuck yeah"

def delete_all():

    bpy.ops.mesh.primitive_cube_add(
        radius = 0.5,
        location = (-1, -1, -1))

    if len(bpy.data.meshes) > 0:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete(use_global=False)

    for item in bpy.data.meshes:
        item.user_clear()
        bpy.data.meshes.remove(item)

    for item in bpy.data.materials:
        item.user_clear();
        bpy.data.materials.remove(item);

def makeMaterial(name, diffuse, specular, alpha, glow=False):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT'
    mat.diffuse_intensity = 1.0
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    if glow:
        mat.emit = random.uniform(1.0, 2.0)
        #mat.use_shadeless = True
    #else:
        #mat.emit = 0.2
        #mat.use_shadeless = True
    mat.use_transparency = True
    return mat

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

def generateMaterials(n):
    materials = []
    for i in range(n):
        d1 = random.uniform(0.0, 0.3)
        d2 = random.uniform(0.0, 1.0)
        d3 = random.uniform(0.0, 0.3)
        diffuse = (d1, d2, d3)
        s1 = random.uniform(0.0, 1.0)
        s2 = random.uniform(0.0, 0.3)
        s3 = random.uniform(0.0, 1.0)
        specular = (s1, s2, s3)
        alpha = random.uniform(0.5, 1.0)
        #alpha = 1.0
        glow = (1 == random.randint(1,5))
        materials.append(makeMaterial('mat'+str(i), diffuse, specular, alpha, glow))

    return materials

# def generate_floor(n):
#
#     materials = bpy.data.materials
#     x = -1
#     y = 0
#     z = 0
#     tmp_radius = 0.45
#     tmp_location = (x, y, z)
#
#     bpy.ops.mesh.primitive_cube_add(
#         radius = tmp_radius,
#         location=tmp_location)
#
#     ob = bpy.context.object
#     sce = bpy.context.scene
#     obs = []
#
#     for x in range(n):
#         #amplitude = random.randint(2,24)
#         amplitude = random.randint(2,2 + (int) (x/10))
#         #left
#         for y in range (-amplitude, amplitude, 1):
#             if random.randint(0,1)==0 and y != 0:
#                 continue
#             if random.randint(0,3)==1:
#                 z = (y**2 + y)/15
#             else:
#                 z = 0
#
#             copy = ob.copy()
#             copy.location = (x, y, z)
#             copy.data = copy.data.copy()
#
#             setMaterial(copy,
#                 materials[random.randint(0,len(materials)-1)])
#
#             if z > 0:
#                 length = random.uniform(0.01,0.1)*((x/5)*(z/5))
#                 copy.scale = (1, 1, length)
#                 bpy.ops.object.transform_apply(scale=True)
#             obs.append(copy)
#
#     bpy.ops.object.select_pattern(pattern="Cube")
#     for ob in obs:
#         sce.objects.link(ob)
#     sce.update()

def build_parabol(x):

    print ("building parabol", x)

    materials = bpy.data.materials
    tmp_radius = 0.45
    tmp_location = (-1, 0, 0)

    bpy.ops.mesh.primitive_cube_add(
        radius = tmp_radius,
        location=tmp_location)

    ob = bpy.context.object
    ob.name = "_".join([str(x), "0", "Cube"])
    sce = bpy.context.scene
    obs = []

    amplitude = random.randint(2,2 + (int) (x/10))
    for y in range (-amplitude, amplitude, 1):
        if random.randint(0,1)==0 and y != 0:
            continue
        if random.randint(0,3)==1:
            z = (y**2 + y)/15
        else:
            z = 0

        copy = ob.copy()
        copy.location = (x, y, z)
        copy.data = copy.data.copy()

        setMaterial(copy,
            materials[random.randint(0,len(materials)-1)])

        if z > 0:
            length = random.uniform(0.01,0.1)*((x/5)*(z/5))
            copy.scale = (1, 1, length)
            bpy.ops.object.transform_apply(scale=True)
        obs.append(copy)

    i = 1
    for ob in obs:
        ob.name = "_".join([str(x), str(i), "Cube"])
        i += 1
        sce.objects.link(ob)
    sce.update()

def remove_parabol(x):
    print ("removing parabol", x)

    candidate_list = [item.name for item in bpy.data.objects if item.name.startswith(str(x))]
    if len(candidate_list) > 0:
        print(candidate_list)
        for object_name in candidate_list:
            bpy.data.objects[object_name].select = True
        for ob in bpy.context.selected_objects:
            if not ob.name.startswith(str(x)):
                ob.select = False

        # remove all selected.
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.delete()

    # remove the meshes, they have no users anymore.
    for item in bpy.data.meshes:
        if item.users == 0:
            bpy.data.meshes.remove(item)
    # for item in bpy.context.scene.objects:
    #     if item.type == "MESH" and item.name.startswith(str(x)):
    #         print("removing", item.name)
    #         #item.select = True
    #         item.user_clear()
    #         bpy.data.objects.remove(item)
    #bpy.ops.object.delete()

def set_object_location(n, ob):
    ob.location[0] = n

# every frame change, this function is called.
def my_handler(scene):

    step_size = 0.05

    camera = bpy.data.objects.get("Camera")
    frame = scene.frame_current
    n = -17 + (frame * step_size)

    if n % 1.0 == 0.0:
        print (magical_dwarves)
        print (frame, camera.location)
        build_parabol(n+200)
        if n > 183:
            remove_parabol(n-1)

    set_object_location(n, camera)

# import bpy
# import os
#
# filename = os.path.join(os.path.dirname(bpy.data.filepath), "taevas.py")
# exec(compile(open(filename).read(), filename, 'exec'))

def main():

    #remove everything
    delete_all()
    generateMaterials(20)
    #generate_floor(50)
    for x in range(0,200-17):
        build_parabol(x)

    #initialize camera
    camera = bpy.data.objects.get("Camera")
    camera.location = (-17.0, 0.0, 2.28703)
    #camera.location = (0.0, 0.0, 2.28703)
    camera.rotation_euler = (math.radians(88.0), 0.0, math.radians(270.0))

    bpy.app.handlers.frame_change_pre.append(my_handler)


if __name__=="__main__":
    main()
