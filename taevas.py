import bpy
import csv
import math
import mathutils
import random

def delete_all():

    bpy.ops.mesh.primitive_cube_add(
        radius = 0.5,
        location=mathutils.Vector((-1, -1, -1)))

    if len(bpy.data.meshes) > 0:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete(use_global=False)

    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)

#    for item in bpy.data.materials:
#        material.user_clear();
#    bpy.data.materials.remove(material);

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

def generate_cubes(n):

    materials = generateMaterials(50)

    filename = os.path.join(os.path.dirname(bpy.data.filepath), 'cell_towers.csv')

    #max is 179.9, min is 179.1
    lonmax = 180.0
    #max is 78.22, min is 67.0
    latmax = 80.0

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        c = 0
        for row in reader:

                z = random.uniform(0.0, 50.0)
                x = (math.fabs(float(row['lon'])) / lonmax)*2.0 + random.uniform(0.0, 2*z)
                y = (math.fabs(float(row['lat'])) / latmax)*2.0 + random.uniform(0.0, 2*z)
                tmp_radius = float(random.uniform(0.01,0.1)) * z
                tmp_location = mathutils.Vector((x, y, z))
                bpy.ops.mesh.primitive_cube_add(
                    radius = tmp_radius,
                    location=tmp_location)
                setMaterial(bpy.context.object,
                    materials[random.randint(0,len(materials)-1)])
                c += 1
                if c == n:
                    break

def generate_floor(n):

    materials = generateMaterials(10)
    x = -1
    y = 0
    z = 0
    tmp_radius = 0.45
    tmp_location = mathutils.Vector((x, y, z))

    bpy.ops.mesh.primitive_cube_add(
        radius = tmp_radius,
        location=tmp_location)

    ob = bpy.context.object
    sce = bpy.context.scene
    obs = []

    for x in range(n):
        #amplitude = random.randint(2,24)
        amplitude = random.randint(2,2 + (int) (x/10))
        #left
        for y in range (-amplitude, amplitude, 1):
            if random.randint(0,1)==0 and y != 0:
                continue
            if random.randint(0,3)==1:
                z = (y**2 + y)/15
            else:
                z = 0

            copy = ob.copy()
            copy.location = mathutils.Vector((x, y, z))
            copy.data = copy.data.copy()

            setMaterial(copy,
                materials[random.randint(0,len(materials)-1)])

            if z > 0:
                length = random.uniform(0.01,0.1)*((x/5)*(z/5))
                copy.scale = (1, 1, length)
                bpy.ops.object.transform_apply(scale=True)
            obs.append(copy)

    bpy.ops.object.select_pattern(pattern="Cube")
    for ob in obs:
        sce.objects.link(ob)
    sce.update()

def run(origin):
    #remove everything
    #delete_all()

    generate_floor(1000)

if __name__ == "__main__":
    run((0,0,0))
