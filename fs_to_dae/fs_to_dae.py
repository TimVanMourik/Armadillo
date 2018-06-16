
from nibabel.freesurfer import io as fsio
import collada
import numpy as np

#todo: use matplotlib color functions
def color_func( scalars ):
  smin = np.min(scalars)
  smax = np.max(scalars)
  scalars = (scalars - smin) / smax

  colors = np.zeros((scalars.shape[0],3))
  colors[:,1] += scalars
  colors[:,2] += (1-scalars)

  return colors

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

  #color
  if not args.color:
    #color = np.ones((norms.shape[0],4))
    color = np.random.uniform(size=norms.shape)
  else:
    scalars = fsio.read_morph_data(args.color)
    color = color_func(scalars)
    #color = np.ones((norms.shape[0],3)) * 

  #create collada obj
  mesh = collada.Collada()

  #add shading
  effect = collada.material.Effect("effect0",\
    [], #TEXTURES GO HERE
    "phong", diffuse=(1,1,1), specular=(1,1,1),
    double_sided=True)
  mat = collada.material.Material("material0", "mymaterial", effect)
  mesh.effects.append(effect)
  mesh.materials.append(mat)

  vert_src = collada.source.FloatSource("cubeverts-array", verts, ('X', 'Y', 'Z'))
  #norm_src = collada.source.FloatSource("cubenormals-array", np.array(norms), ('X', 'Y', 'Z'))
  color_src = collada.source.FloatSource("cubecolors-array", np.array(color), ('R', 'G', 'B'))

  geom = collada.geometry.Geometry(mesh, "geometry0", "fsave_test",\
    [vert_src,color_src])

  #creates list of inputs for collada DOM obj...so many decorators 
  input_list = collada.source.InputList()

  input_list.addInput(0, 'VERTEX', "#cubeverts-array")
  input_list.addInput(1, 'COLOR', "#cubecolors-array")
  #input_list.addInput(2, 'NORMAL', "#cubenormals-array")

  #creates faces
  triset = geom.createTriangleSet(
    np.concatenate([faces,faces],axis=1),\
    input_list, "materialref")

  triset.generateNormals()

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
  parser.add_argument("-c","--color",default=None)

  args = parser.parse_args()

  if not args.input or not args.output:
    print("%s Requires both input and output! Aborting." % err_str)
    exit(1)

  fs_to_dae(args)




