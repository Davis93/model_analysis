import sys
import copy
from model import Model
from vor import fortran_voronoi_3d
from voronoi_3d import voronoi_3d

def cn_histo(m):
    d = {}
    for atom in m.atoms:
        d[sum(atom.vp.index)] = d.get(sum(atom.vp.index),0) + 1
    l = d.keys()
    l.sort()
    for key in l:
        print("{0} {1}".format(key,d[key]))

def main():
    modelfile = sys.argv[1]

    m = Model(modelfile)
    keys = [(40,40),(29,29),(13,13),(40,29),(40,13),(29,13)]
    cuttol = 0.2
    cutdelta = 0.1
    cutoff = {}
    cutoff[(40,40)] = 3.5
    cutoff[(13,29)] = 3.5
    cutoff[(29,13)] = 3.5
    cutoff[(40,13)] = 3.5
    cutoff[(13,40)] = 3.5
    cutoff[(29,40)] = 3.5
    cutoff[(40,29)] = 3.5
    cutoff[(13,13)] = 3.5
    cutoff[(29,29)] = 3.5

    #for dc in [-0.3, -0.2, 0.0, -0.1, 0.1, 0.2, 0.3]:
    for c in [3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5]:
        cutoff2 = copy.deepcopy(cutoff)
        m = Model(modelfile)
        for key in keys:
            cutoff2[key] = c
        try:
            voronoi_3d(m,cutoff2)
            print("Cutoff = {0}".format(c))
            cn_histo(m)
        except:
            pass


if __name__ == '__main__':
    main()
