import os
import sys
import reduce_region_elev_multiprocessing as mp

if __name__ == '__main__':
    
    file = sys.argv[1]
    
    cwd = os.getcwd()
    file = os.path.join(cwd,file)
    
    print(file)
    
    resolutions = [100,200,500]
    
    x = mp.reduce_class()
    
    x.perfilecall(file,resolutions)
