
from nibabel.freesurfer import io as fsio
import collada
import numpy as np

def fs_to_dae( args ):

  #load in FS mesh
  verts,faces = fsio.read_geometry( args.input )

  #dumb copypasta for mesh face normals
  norms = np.zeros( verts.shape, dtype=verts.dtype )
  tris = verts[faces]
  n = np.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )
  norm_sizes = np.sqrt(n[:,0]**2 + n[:,1]**2 + n[:,2]**2)

  for i in range(3):
    n[:,i] = n[:,i] / norm_sizes

  del norm_sizes

  #map back to vertices
  norms[ faces[:,0] ] += n
  norms[ faces[:,1] ] += n
  norms[ faces[:,2] ] += n

  del n

  norm_sizes = np.sqrt(norms[:,0]**2 + norms[:,1]**2 + norms[:,2]**2)

  for i in range(3):
    norms[:,i] = norms[:,i] / norm_sizes


  #
  # collada section
  #

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
  norm_src = collada.source.FloatSource("cubenormals-array", np.array(norms), ('X', 'Y', 'Z'))

  geom = collada.geometry.Geometry(mesh, "geometry0", "fsave_test", [vert_src,norm_src])

  #creates list of inputs for collada DOM obj...so many decorators 
  input_list = collada.source.InputList()

  input_list.addInput(0, 'VERTEX', "#cubeverts-array")
  input_list.addInput(1, 'NORMAL', "#cubenormals-array")

  #creates faces
  triset = geom.createTriangleSet(
    np.array([faces,faces]), input_list, "materialref")

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




