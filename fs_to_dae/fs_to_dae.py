
from nibabel.freesurfer import io as fsio
import collada

def fs_to_dae( args ):

  #load in FS mesh
  verts,faces = fsio.read_geometry( args.input )

  #create collada obj
  mesh = collada.Collada()

  #add shading
  effect = collada.material.Effect("effect0",\
    [], #TEXTURES GO HERE
    "phong", diffuse=(1,0,0), specular=(0,1,0))
  mat = collada.material.Material("material0", "mymaterial", effect)
  mesh.effects.append(effect)
  mesh.materials.append(mat)

  vert_src = collada.source.FloatSource("cubeverts-array", verts, ('X', 'Y', 'Z'))

  geom = collada.geometry.Geometry(mesh, "geometry0", "fsave_test", [vert_src])

  #creates list of inputs for collada DOM obj...so many decorators 
  input_list = collada.source.InputList()

  input_list.addInput(0, 'VERTEX', "#cubeverts-array")

  #creates faces
  triset = geom.createTriangleSet(faces, input_list, "materialref")

  geom.primitives.append(triset)
  mesh.geometries.append(geom)

  #creates scene node, which causes display
  matnode = collada.scene.MaterialNode("materialref", mat, inputs=[])
  geomnode = collada.scene.GeometryNode(geom, [matnode])
  node = collada.scene.Node("node0", children=[geomnode])

  #create scene
  myscene = collada.scene.Scene("fs_base_scene", [node])
  mesh.scenes.append(myscene)
  mesh.scene = myscene

  mesh.write(args.output)

  return

if __name__ == "__main__":
  import argparse

  err_str = "[fs_to_dae]"

  parser = argparse.ArgumentParser(description=\
    "Converts FS to DAE")

  parser.add_argument("-i","--input",default=None)
  parser.add_argument("-o","--output",default=None)

  args = parser.parse_args()

  if not args.input or not args.output:
    print("%s Requires both input and output! Aborting." % err_str)
    exit(1)

  fs_to_dae(args)




