#!/usr/bin/env python
import os
from urllib import request
import time
import math
import pprint

# the link in the "Download Data" button [OLD]
# download_link = 'https://www.astro.up.pt/resources/sweet-cat/download.php'
# new link
download_link = 'http://sweetcat.iastro.pt/catalog/SWEETCAT_Dataframe.csv'

# to get the directory where SWEET-Cat data will be stored
from .config import get_data_dir, verbose

def download_data():
    """ Download SWEET-Cat data and save it to `SWEET_cat.csv` """

    with request.urlopen(download_link) as response:
       data = response.read()

    local_file = os.path.join(get_data_dir(), 'SWEET_cat.csv')
    with open(local_file, 'wb') as f:
        f.write(data)

    if verbose:
        print(f'Saved SWEET-Cat data to {local_file}')


def check_data_age():
    """ How old is `SWEET_cat.csv`, in days """
    local_file = os.path.join(get_data_dir(), 'SWEET_cat.csv')
    age = time.time() - os.path.getmtime(local_file) # in sec
    return age / (60*60*24) # in days


class DataDict(dict):
    numpy_entries = False

    __doc__ = "SWEET-Cat: a catalog of stellar parameters for stars with planets\n"+\
              "The catalog and more information can be found at www.astro.up.pt/resources/sweet-cat\n"+\
              "This dictionary has the same fields as keys "+\
              "(note that 'sigma' and 'pi' can be used instead of 'σ' and 'π')\n"+\
              "Entries are lists, see `to_numpy()` to convert them to numpy arrays."

    def __getitem__(self, key):
        # allows to do data[0] to get all columns for the 0th entry in the table
        if isinstance(key, int):
            return {k:v[key] for k, v in self.items()}

        # allows to do data['sigma_feh'] to get data['σ_feh']
        key = key.replace('sigma', 'σ').replace('pi', 'π')
        
        # allows to do data['key_nonan'] to get data['key'] without NaNs
        if key.endswith('_nonan'):
            val = super().__getitem__(key.replace('_nonan',''))
            try:
                if self.numpy_entries:
                    from numpy import isnan
                    val = val[~isnan(val)]
                else:
                    val = [v for v in val if not math.isnan(v)]
            except TypeError:
                # this column does not have floats
                pass
        else:
            val = super().__getitem__(key)

        return val

    def __str__(self):
        return 'SWEET-Cat data'
    def __repr__(self):
        return f'SWEET-Cat data: dictionary with {self.size} entries. '+\
                'Use .columns() to get the column labels.'
                
    def __len__(self):
        return len(self.__getitem__('name'))

    def columns(self):
        """ List the available columns """
        pprint.pprint(list(self.keys()), compact=True)

    @property
    def size(self):
        return len(self.__getitem__('name'))

    def find(self, name):
        if name in self.__getitem__('name'):
            return self[self['name'].index(name)]

    def to_numpy(self, inplace=True):
        """ 
        Convert entries to numpy arrays. If `inplace` is True convert
        the entries in place, else return a new dictionary.
        """
        from numpy import asarray # this assumes numpy is installed
        newself = self if inplace else DataDict()
        for k, v in self.items():
            newself[k] = asarray(v)
        newself.numpy_entries = True
        if not inplace:
            return newself


def read_data():
    def val2float(val):
        if val == '~':
            return math.nan
        try: 
            return float(val)
        except ValueError:
            return val
    def val2int(val):
        try: 
            return int(val)
        except ValueError:
            return val

    labels = [
        'name', 'HD', 
        'ra', 'dec', 'Vmag', 'σ_vmag', 'plx_flag',
        'teff', 'σ_teff', 'logg', 'σ_logg', 'vt', 'σ_vt', 'feh', 'σ_feh', 
        'reference', 'link', 'sw_flag', 'update', 'comment', 'database',
        'gaia_dr2', 'gaia_dr3', 'π', 'σ_π', 'Gmag', 'σ_Gmag'
        'RPmag', 'σ_RPmag', 'BPmag', 'σ_BPmag', 'FG', 'σ_FG', 
        'G_flux_std_n', 'logg_gaia', 'σ_logg_gaia', 'mass_t', 'σ_mass_t',
        'radius_t','σ_radius_t', 'spec_base', 'distance', 
        'ra_EU', 'dec_EU', 'ra_NASA', 'dec_NASA', 
        'distance_b', 'σ_distance_b'
    ]

    # empty dictionary to save data
    data = {label:[] for label in labels}

    # read the file
    local_file = os.path.join(get_data_dir(), 'SWEET_cat.csv')
    lines = open(local_file).readlines()

    nlab, nlin = len(labels), len(lines)
    if verbose:
        print(f'There are {nlab} columns with {nlin} entries each in `SWEET_cat.csv`')

    for line in lines:
        # split the columns
        vals = line.strip().split(',')
        # make some columns into ints
        vals = vals[:4] + list(map(val2int, vals[4:]))
        # make some columns into floats
        vals[4:-4] = list(map(val2float, vals[4:-4]))

        for i, v in enumerate(data.values()):
            v.append(vals[i])

    data = DataDict(**data)
    return data


def get_data():
    local_file = os.path.join(get_data_dir(), 'SWEET_cat.csv')

    if not os.path.exists(local_file):
        if verbose:
            print('Downloading SWEET-Cat data')
        download_data()
    
    age = check_data_age()
    if age > 5:
        if verbose:
            print('Data in `SWEET_cat.csv` is older than 5 days, downloading.')
        download_data()
    else:
        if verbose:
            print('Data in `SWEET_cat.csv` is recent.')

    data = read_data()
    return data


if __name__ == '__main__':
    data = get_data()