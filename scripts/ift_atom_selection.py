import sys
import numpy as np
from model import Model

def main():
    modelfile = sys.argv[1]
    intensityfile = sys.argv[2]

    npix = 256
    intensities = np.zeros((npix,npix,npix),dtype=float)
    m = Model(modelfile)
    maxx = 0.0
    with open(intensityfile) as f:
        for l,line in enumerate(f):
            line = line.strip().split()
            for i,x in enumerate(line):
                x = float(x)
                if(x > maxx): maxx = x
                intensities[i%npix][int(i/npix)][l] = x
            print("Read in line {0}.".format(l))

    ints = np.zeros((m.natoms),dtype=float)
    for i,atom in enumerate(m.atoms):
        xbin = int((m.lx/2+atom.coord[0])/m.lx*npix)
        ybin = int((m.ly/2+atom.coord[1])/m.ly*npix)
        zbin = int((m.ly/2+atom.coord[2])/m.lz*npix)
        atom.intensity = intensities[xbin][ybin][zbin]/maxx
        ints[i] = intensities[xbin][ybin][zbin]/maxx
        #print(atom.coord[0],atom.coord[1],atom.coord[2])
        print(xbin,ybin,zbin,atom.intensity)

    print("Mean: {0}".format(np.mean(ints)))
    print("Stdev: {0}".format(np.std(ints)))
    print("Variance: {0}".format(np.var(ints)))
    print("Median: {0}".format(np.median(ints)))
    mini = np.mean(ints) + np.std(ints)/2.0
    atoms = [atom for atom in m.atoms if atom.intensity > mini]
    Model(m.comment,m.lx,m.ly,m.lz,atoms).write_cif('temp.cif')
    Model(m.comment,m.lx,m.ly,m.lz,atoms).write_our_xyz('temp.xyz')



if __name__ == '__main__':
    main()
