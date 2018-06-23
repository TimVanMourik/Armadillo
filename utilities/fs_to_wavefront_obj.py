
from nibabel.freesurfer import io as fsio
import numpy as np
import trimesh

#todo: use matplotlib color functions
def color_func( scalars ):
  smin = np.min(scalars)
  smax = np.max(scalars)
  scalars = (scalars - smin) / smax

  colors = np.zeros((scalars.shape[0],3))
  colors[:,0] += scalars
  colors = colors * 256

  return colors.astype(int)

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

  #color
  if not args.color:
    color = np.ones(norms.shape) * 0.4
  else:
    scalars = fsio.read_morph_data(args.color)
    color = color_func(scalars)

  #make trimesh
  mesh = trimesh.Trimesh(\
    verts,\
    faces,\
    vertex_normals=norms,\
    vertex_colors=color)

  mesh.export(file_obj=args.output, file_type="collada")
  #mesh.export(file_obj=args.output, file_type="obj")
  #mesh.export_gltf(file_obj=args.output)

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




