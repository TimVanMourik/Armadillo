
from nibabel.freesurfer import io as fsio
import numpy as np
import trimesh

def fs_to_dae( args ):

  #load in FS mesh
  verts,faces = fsio.read_geometry( args.input )

  mesh = trimesh.Trimesh(verts, faces)

  mesh.export(file_obj=args.output, file_type="obj")
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




