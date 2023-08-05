import glob
import os
import sys
import numpy as np
from collections import OrderedDict
import h5py
from NuRadioMC.utilities.hdf5_manipulator import merge


def merge2(filenames, output_filename):
    data = OrderedDict()
    attrs = OrderedDict()
    groups = OrderedDict()
    group_attrs = OrderedDict()
    n_data = {}
    n_groups = {}

    for f in filenames:
        print("adding file {}".format(f))
        data[f] = {}
        groups[f] = {}
        
        fin = h5py.File(f, 'r')
        for key in fin:
            if isinstance(fin[key], h5py._hl.group.Group):
                groups[f][key] = {}
                if(key not in n_groups):
                    n_groups[key] = {}
                for key2 in fin[key]:
                    groups[f][key][key2] = fin[key][key2][...]
                    if(key2 not in n_groups[key]):
                        n_groups[key][key2] = 0
                    n_groups[key][key2] += len(groups[f][key][key2])
                if(key not in group_attrs):
                    group_attrs[key] = {}
                    for key2 in fin[key].attrs:
                        group_attrs[key][key2] = fin[key].attrs[key2]
#                 else:
#                     for key2 in fin[key].attrs:
#                         if(group_attrs[key][key2] != fin[key].attrs[key2]):
#                             raise AssertionError("group attributes {}/{} are different".format(key, key2))
            else:
                data[f][key] = fin[key][...]
                if(key not in n_data):
                    n_data[key] = 0
                n_data[key] += len(data[f][key])
            
        for key in fin.attrs:
            if(key not in attrs):
                attrs[key] = fin.attrs[key]
            else:
                if(key == "n_events"):
                    attrs['n_events'] += fin.attrs['n_events']
            if len(attrs['trigger_names']) == 0 and 'trigger_names' in fin.attrs:
                attrs['trigger_names'] = fin.attrs['trigger_names']
#             if len(data[f]['triggered']) == 0:
#                 attrs['n_events'] += fin.attrs['n_events']
#                 if(attrs[key] != f.attrs[key]):
#                     raise AssertionError("attribute {} is different".format(key))
        fin.close()

    # create data sets
    print("creating data sets")
    fout = h5py.File(output_filename, 'w')
    for key in data[filenames[0]]:
        print(key)
        shape = list(data[filenames[0]][key].shape)
        shape[0] = n_data[key]
        
        tmp = np.zeros(shape, dtype=data[filenames[0]][key].dtype)
        
        i = 0
        for f in data:
            tmp[i:(i+len(data[f][key]))] = data[f][key]
            i += len(data[f][key])
        
        fout.create_dataset(key, tmp.shape, dtype=tmp.dtype,
                         compression='gzip')[...] = tmp
    for key in groups[filenames[0]]:
        print("writing group {}".format(key))
        g = fout.create_group(key)
        for key2 in groups[filenames[0]][key]:
            print("writing data set {}".format(key2))
            shape = list(groups[filenames[0]][key][key2].shape)
            shape[0] = n_groups[key][key2]
            
            tmp = np.zeros(shape, dtype=groups[filenames[0]][key][key2].dtype)
            i = 0
            for f in groups:
                tmp[i:(i+len(groups[f][key][key2]))] = groups[f][key][key2]
                i += len(groups[f][key][key2])
            
            g.create_dataset(key2, shape, dtype=groups[filenames[0]][key][key2].dtype,
                             compression='gzip')[...] = tmp
        # save group attributes
        for key2 in group_attrs[key]:
            fout[key].attrs[key2] = group_attrs[key][key2]
    
#     # save all data to hdf5
#     for key in data[filenames[0]]:
#         print("writing data set {}".format(key))
#         i = 0
#         for f in data:
#             fout[key][i:(i+len(data[f][key]))] = data[f][key]
#             i += len(data[f][key])
    # save all group data to hdf5
#     for key in groups[filenames[0]]:
#         print("writing group {}".format(key))
#         for key2 in groups[filenames[0]][key]:
#             print("writing data set {}".format(key2))
#             i = 0
#             for f in groups:
#                 fout[key][key2][i:(i+len(groups[f][key][key2]))] = groups[f][key][key2]
#                 i += len(groups[f][key][key2])
#         # save group attributes
#         for key2 in group_attrs[key]:
#             fout[key].attrs[key2] = group_attrs[key][key2]
#             
    # save all atrributes
    for key in attrs:
        fout.attrs[key] = attrs[key]
    
    fout.close()
    

if __name__== "__main__":
    """
    merges multiple hdf5 output files into one single files.
    The merger module automatically keeps track of the total number
    of simulated events (which are needed to correctly calculate the effective volume).
    
    The script expects that the folder structure is
    ../output/energy/*.hdf5.part????
    """
    if(len(sys.argv) < 2):
        print("usage: python merge_hdf5.py /path/to/simulation/output/folder\nor python merge_hdf5.py outputfilename input1 input2 ...")
    elif(len(sys.argv) == 2):
        filenames = glob.glob("{}/*/*.hdf5.part????".format(sys.argv[1]))
        filenames2 = []
        for i, filename in enumerate(filenames):
            filename, ext = os.path.splitext(filename)
            if(ext != '.hdf5'):
                if(filename not in filenames2):
                    d = os.path.split(filename)
                    a, b = os.path.split(d[0])
                    filenames2.append(filename)
    
        for filename in filenames2:
            if(os.path.splitext(filename)[1] == '.hdf5'):
                d = os.path.split(filename)
                a, b = os.path.split(d[0])
                output_filename = os.path.join(a, d[1])  #remove subfolder from filename
                if(os.path.exists(output_filename)):
                    print('file {} already exists, skipping'.format(output_filename))
                else:
    #                 try:
                        input_files = np.array(sorted(glob.glob(filename + '.part????')))
                        mask = np.array([os.path.getsize(x) > 1000 for x in input_files], dtype=np.bool)
                        if(np.sum(~mask)):
                            print("{:d} files were deselected because their filesize was to small".format(np.sum(~mask)))
    
    
                        merge2(input_files[mask], output_filename)
    #                 except:
    #                     print("failed to merge {}".format(filename))
    elif(len(sys.argv) > 2):
        output_filename = sys.argv[1]
        if(os.path.exists(output_filename)):
            print('file {} already exists, skipping'.format(output_filename))
        else:
            input_files = sys.argv[2:]
            merge2(input_files, output_filename)