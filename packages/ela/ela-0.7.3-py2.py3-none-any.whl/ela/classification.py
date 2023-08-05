from __future__ import print_function # anything else?

import pandas as pd
import numpy as np

from ela.textproc import PRIMARY_LITHO_COL, SECONDARY_LITHO_COL
from ela.spatial import *

def to_litho_class_num(lithology, kv):
    """Get a numeric code for a lithology, or NaN if not in the dictionary mapping lithologies to numeric code

        Args:
            lithology (str): Name of the lithology
            kv (dict[str,float]): lithologies keywords to numeric code
    """
    if lithology in kv.keys():
        return kv[lithology]
    else:
        return np.nan

def v_to_litho_class_num(lithologies, kv):
    """Get numeric codes for lithologies, or NaN if not in the dictionary mapping lithologies to numeric code

        Args:
            lithologies (iterable of str): Name of the lithologies
            kv (dict[str,float]): lithologies keywords to numeric code
    """
    return np.array([to_litho_class_num(x, kv) for x in lithologies])

def create_numeric_classes(lithologies):
    """Creates a dictionary mapping lithologies to numeric code

        Args:
            lithologies (iterable of str): Name of the lithologies
    """
    my_lithologies_numclasses = dict([(lithologies[i], i) for i in range(len(lithologies))])
    return my_lithologies_numclasses


def _to_int(f):
    if np.isnan(f): return f
    return int(round(f))

class ClassMapper:
    """Hold information about and perform lithology and hydraulic conductivity classification

    Attributes:
        lithology_names (iterable of str): Name of the lithologies
        mapping (dict): dictionary where keys are primary+secondary lithologies ('sand/clay') and values are numeric codes for e.g. hydraulic conductivities
        litho_numeric_mapper (np array): numeric mapper from primary+secondary lithologies to hydraulic conductivities
    """
    def __init__(self, mapping, lithology_names):
        """initialize this with a coordinate reference system object and an affine transform. See rasterio.

        Args:
            lithology_names (iterable of str): Name of the lithologies
            mapping (dict): dictionary where keys are primary+secondary lithologies ('sand/clay') and values are numeric codes for e.g. hydraulic conductivities
        """
        self.lithology_names = lithology_names
        self.mapping = mapping
        self.litho_numeric_mapper = np.empty((len(lithology_names), len(lithology_names)))
        for i in np.arange(0, len(lithology_names), 1):
            for j in np.arange(0, len(lithology_names), 1):
                self.litho_numeric_mapper[i,j] = self.class_code(lithology_names[i], lithology_names[j])
    @staticmethod
    def create_full_litho_desc(df):
        """Create strings identifying primary+secondary lithologies, used as keys in classification operations

            Args:
                df (pandas data frame): bore lithology data  with columns named PRIMARY_LITHO_COL and SECONDARY_LITHO_COL

            Returns:
                a list of strings, compound primary+optional_secondary lithology descriptions e.g. 'sand/clay', 'loam/'
        """
        p1 = df[PRIMARY_LITHO_COL].values
        p2 = df[SECONDARY_LITHO_COL].values
        return ['/'.join([p1[i], p2[i]]) for i in range(len(p1))]
    def _mapping_class(self, litho_class):
        keys = self.mapping.keys()
        if litho_class in keys:
            return self.mapping[litho_class]
        else:
            return np.nan
    def numeric_for_litho_classes(self, litho_classes):
        """Get the numeric class for primary+secondary lithologies

            Args:
                litho_classes (iterable of str): one or more strings e.g. 'sand/clay'
            Returns:
                list of numeric codes
        """
        return [self._mapping_class(x) for x in litho_classes]
    def litho_class_label(self, primary_litho_class, secondary_litho_class):
        """Get the string identifier for a set of primary+secondary lithologies

            Args:
                primary_litho_class (str, float or int): primary lithology name or numeric (lithology class) identifier
                secondary_litho_class (str, float or int): primary lithology name or numeric (lithology class) identifier

            Returns:
                string, lithologies key such as 'sand/clay'
        """
        if isinstance(primary_litho_class, float):
            if np.isnan(primary_litho_class):
                return ''
            primary_litho_class = _to_int(primary_litho_class)
        if isinstance(secondary_litho_class, float):
            if np.isnan(secondary_litho_class):
                secondary_litho_class = ''
            else:
                secondary_litho_class = _to_int(secondary_litho_class)

        if isinstance(primary_litho_class, int): primary_litho_class = self.lithology_names[primary_litho_class]
        if isinstance(secondary_litho_class, int): secondary_litho_class = self.lithology_names[secondary_litho_class]

        if isinstance(primary_litho_class, str):
            if not primary_litho_class in self.lithology_names:
                return ''
        if isinstance(secondary_litho_class, str):
            if not secondary_litho_class in self.lithology_names:
                secondary_litho_class = ''

        litho_class = '/'.join([primary_litho_class, secondary_litho_class])
        return litho_class

    def class_code(self, primary_litho_class, secondary_litho_class):
        """Get the mapping class code (e.g. hydraulic condouctivity) for a set of primary+secondary lithologies

            Args:
                primary_litho_class (str, float or int): primary lithology name or numeric (lithology class) identifier
                secondary_litho_class (str, float or int): primary lithology name or numeric (lithology class) identifier

            Returns:
                numeric, numeric code of the mapped class for this  primary+secondary lithologies
        """
        return self._mapping_class(self.litho_class_label(primary_litho_class, secondary_litho_class))
    def bivariate_mapper(self, primary_litho_code, secondary_litho_code):
        """Get the mapping class code (e.g. hydraulic conductivity) for a set of primary+secondary lithologies

            Args:
                primary_litho_class (float): primary lithology numeric (lithology class) identifier
                secondary_litho_class (float): primary lithology numeric (lithology class) identifier

            Returns:
                numeric, numeric code of the mapped class for this  primary+secondary lithologies
        """
        if np.isnan(primary_litho_code):
            return np.nan
        if np.isnan(secondary_litho_code):
            return self.litho_numeric_mapper[_to_int(primary_litho_code), _to_int(primary_litho_code)]
        return self.litho_numeric_mapper[_to_int(primary_litho_code), _to_int(secondary_litho_code)]
    def map_classes(self, primary_lithology_3d_array, secondary_lithology_3d_array):
        """(compute intensive) Get the mapping class codes (e.g. hydraulic conductivity) for grids of primary+secondary lithologies

            Args:
                primary_lithology_3d_array (np.array of dim 3): primary lithology numeric (lithology class) identifiers
                secondary_lithology_3d_array (np.array of dim 3): primary lithology numeric (lithology class) identifiers

            Returns:
                (np.array of dim 3): mapped numeric identifiers, e.g. as of hydraulic conductivities
        """
        three_k_classes = primary_lithology_3d_array.copy()
        dim_x,dim_y,dim_z = three_k_classes.shape
        for i in np.arange(0, dim_x, 1):
            for j in np.arange(0, dim_y, 1):
                for k in np.arange(0, dim_z, 1):
                    three_k_classes[i,j,k] = self.bivariate_mapper(primary_lithology_3d_array[i,j,k], secondary_lithology_3d_array[i,j,k])
        return three_k_classes
    def get_frequencies(self, mask_2d, primary_lithology_3d_array, secondary_lithology_3d_array):
        """Get the frequencies of primary+secondary for a set of x/y coordinates and all Z values in 3d lithologies

            Args:
                mask_2d (np.array of dim 2): mask to apply to the x-y dimensions of the other arguments
                primary_lithology_3d_array (np.array of dim 3): primary lithology numeric (lithology class) identifiers
                secondary_lithology_3d_array (np.array of dim 3): primary lithology numeric (lithology class) identifiers

            Returns:
                (np.array of dim 2): counts of primary/secondary lithology occurrences.
        """
        result = np.zeros([len(self.lithology_names), len(self.lithology_names)])
        ## TODO should check on dimensions...
        dim_x,dim_y,dim_z = secondary_lithology_3d_array.shape
        for i in np.arange(0, dim_x, 1):
            for j in np.arange(0, dim_y, 1):
                if mask_2d[i,j]:
                    for k in np.arange(0, dim_z, 1):
                        prim_litho_ind = _to_int(primary_lithology_3d_array[i,j,k])
                        if np.isnan(prim_litho_ind) == False:
                            sec_litho_ind = _to_int(secondary_lithology_3d_array[i,j,k])
                            if np.isnan(sec_litho_ind):
                                sec_litho_ind = prim_litho_ind
                            result[prim_litho_ind,sec_litho_ind] = result[prim_litho_ind,sec_litho_ind] + 1
        return result
    def data_frame_frequencies(self, freq_table):
        """Get the frequencies of primary+secondary as a data frame, typically from the output of get_frequencies

            Args:
                freq_table (np.array of dim 2): counts of primary/secondary lithology occurrences.

            Returns:
                (pandas data frame): counts of primary/secondary lithology occurrences.
        """
        ## TODO should check on dimensions...
        x = [(self.litho_class_label(i, j), freq_table[i,j]) for i in range(len(self.lithology_names)) for j in range(len(self.lithology_names))]
        return pd.DataFrame(x, columns=["token","frequency"])


def extract_single_lithology_class_3d(lithology_3d_classes, class_value):
    """Transform a 3D volume of lithology class codes by binary bining cells as being either of a class value or other. Preprocessing primarily for 3D visualisation for Mayavi.

        Args:
            lithology_3d_classes (np.array of dim 3): lithology numeric (lithology class) identifiers
            class_value (float): class code of interest
    """
    single_litho = np.copy(lithology_3d_classes)
    other_value = class_value-1.0
    single_litho[(single_litho != class_value)] = other_value
    # We burn the edges of the volume, as I suspect this is necessary to have a more intuitive viz (otherwuse non closed volumes)
    single_litho[0,:,:] = other_value
    single_litho[-1,:,:] = other_value
    single_litho[:,0,:] = other_value
    single_litho[:,-1,:] = other_value
    single_litho[:,:,0] = other_value
    single_litho[:,:,-1] = other_value
    return single_litho
