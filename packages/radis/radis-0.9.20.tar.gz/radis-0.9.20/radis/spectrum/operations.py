#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Handy functions for manipulation of :class:`~radis.spectrum.spectrum.Spectrum` objects

Routine Listing
---------------

Operators:

- :py:func:`~radis.spectrum.operations.multiply` : simply use ``s*2``
- :py:func:`~radis.spectrum.operations.add_constant` : simply use ``s+1``
- :py:func:`~radis.spectrum.operations.add_array` : simply use ``s+a``
- :py:func:`~radis.spectrum.operations.add_spectra` : simply use ``s1+s2`` 
- :py:func:`~radis.spectrum.operations.substract_spectra` : simply use ``s1-s2``

Note that these operators are purely algebraic and should not be used in place
of the line-of-sight functions, i.e, :py:func:`~radis.los.slabs.SerialSlabs` (``>``)
and :py:func:`~radis.los.slabs.MergeSlabs` (``//``)

Functions to manipulate one spectrum:
    
- :py:func:`~radis.spectrum.operations.crop`
- :py:func:`~radis.spectrum.operations.offset`

Play with baselines:
    
- :py:func:`~radis.spectrum.operations.get_baseline`
- :py:func:`~radis.spectrum.operations.sub_baseline`
    
Functions to discard all but one spectral quantity:
    
- :py:func:`~radis.spectrum.operations.Transmittance`
- :py:func:`~radis.spectrum.operations.Transmittance_noslit`
- :py:func:`~radis.spectrum.operations.Radiance`
- :py:func:`~radis.spectrum.operations.Radiance_noslit`

Keeps all spectral quantities, but make emission equal to 0 (useful when
calculating contributions of line of sight slabs):
    
- :py:func:`~radis.spectrum.operations.PerfectAbsorber`


Examples
--------

Most of these functions are implemented with the standard operators. Ex::
    
    ((s_exp - 0.1)*10).plot()   # works for a Spectrum s_exp

-------------------------------------------------------------------------------


"""

from __future__ import print_function, absolute_import, division, unicode_literals
#from radis.misc.curve import curve_substract, curve_add
from radis.spectrum import Spectrum
from radis.phys.convert import (cm2nm, nm2cm, cm2nm_air, nm_air2cm, air2vacuum, vacuum2air,
                                dcm2dnm, dnm2dcm)
from numpy import ones_like, hstack
from warnings import warn


# %% Filter Spectra

def Transmittance(s):
    # type: (Spectrum) -> Spectrum
    ''' Returns a new Spectrum with only the ``transmittance`` component of ``s`` 
    
    Parameters
    ----------
    
    s: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object
        
    Returns
    -------
    
    s_tr: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object, with only the ``transmittance``,
        ``absorbance`` and/or ``abscoeff`` part of ``s``, where ``radiance_noslit`` ,
        ``emisscoeff`` and ``emissivity_noslit`` (if they exist) have been set to 0
    
    See Also
    --------
    
    :py:func:`~radis.spectrum.operations.Transmittance_noslit`

    '''

    return s.copy(copy_lines=True, quantity='transmittance')

def Transmittance_noslit(s):
    ''' Returns a new Spectrum with only the ``transmittance_noslit`` component of ``s`` 
    
    Parameters
    ----------
    
    s: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object
        
    Returns
    -------
    
    s_tr: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object, with only 
        ``transmittance_noslit`` defined
 
    See Also
    --------
    
    :py:func:`~radis.spectrum.operations.Transmittance`
    '''

    return s.copy(copy_lines=True, quantity='transmittance_noslit')

def Radiance(s):
    ''' Returns a new Spectrum with only the ``radiance`` component of ``s`` 
    
    Parameters
    ----------
    
    s: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object
        
    Returns
    -------
    
    s_tr: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object, with only ``radiance``
        defined
 
    See Also
    --------
    
    :py:func:`~radis.spectrum.operations.Radiance_noslit`
    '''

    return s.copy(copy_lines=True, quantity='radiance')

def Radiance_noslit(s):
    ''' Returns a new Spectrum with only the ``radiance_noslit`` component of ``s`` 
    
    Parameters
    ----------
    
    s: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object
        
    Returns
    -------
    
    s_tr: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object, with only ``radiance_noslit``
        defined
        
    See Also
    --------
    
    :py:func:`~radis.spectrum.operations.Radiance`

    '''

    return s.copy(copy_lines=True, quantity='radiance_noslit')

# Useful for determining line-of-sight contributions:

def PerfectAbsorber(s):
    ''' Makes a new Spectrum with the same transmittance/absorbance as Spectrum
    ``s``, but with radiance set to 0. 
    Useful to get contribution of different slabs in line-of-sight 
    calculations (see example).
    
    .. note:
        
        formerly named "Transmittance", but "Transmittance(s)" wouldnt 
        return the Transmittance exactly
    
    Parameters
    ----------
    
    s: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object
        
    Returns
    -------
    
    s_tr: Spectrum
        :class:`~radis.spectrum.spectrum.Spectrum` object, with only the ``transmittance``,
        ``absorbance`` and/or ``abscoeff`` part of ``s``, where ``radiance_noslit`` ,
        ``emisscoeff`` and ``emissivity_noslit`` (if they exist) have been set to 0
        
    Examples
    --------
    
    Let's say you have a total line of sight::
    
        s_los = s1 > s2 > s3     
        
    If you now want to get the contribution of ``s2`` to the line-of-sight emission,
    you can do::
        
        (s2 > PerfectAbsorber(s3)).plot('radiance_noslit')
        
    And the contribution of ``s1`` would be::
        
        (s1 > PerfectAbsorber(s2>s3)).plot('radiance_noslit') 
    
    See more examples in :ref:`Line-of-Sight module <label_los_index>`
    
    '''
    
    s_tr = s.copy()
    for k in ['radiance_noslit', 'emisscoeff', 'emissivity_noslit']:
        if k in s_tr._q:
            s_tr._q[k] *= 0
            
    for k in ['radiance', 'emissivity']:
        if k in s_tr._q_conv:
            s_tr._q_conv[k] *= 0

    # Deactivate equilibrium conditions (so Kirchoff's law cannot be used anymore)
    s_tr.conditions['thermal_equilibrium'] = False
    
    s_tr.name = 'PureAbsorber({0})'.format(s.get_name())
    
    return s_tr
    

# %% Change wavelength
    

def crop(s, wmin=None, wmax=None, wunit=None, medium=None,
         inplace=False):
    # type: (Spectrum, float, float, str, str, bool) -> Spectrum
    ''' Crop spectrum to ``wmin-wmax`` range in ``wunit``
    
    Parameters
    ----------
    
    s: Spectrum object
        object to crop
    
    wmin, wmax: float, or None
        boundaries of spectral range (in ``wunit``)
        
    wunit: ``'nm'``, ``'cm-1'``
        which waveunit to use for ``wmin, wmax``. Default ``default``: 
        just use the Spectrum wavespace. 

    medium: 'air', vacuum'
        necessary if cropping in 'nm'
        
    Other Parameters
    ----------------
    
    inplace: bool
        if ``True``, modifiy ``s`` directly. Else, returns a copy.
    
    Returns
    -------
    
    s_crop: Spectrum
        a cropped Spectrum.
        if using ``inplace``, then ``s_crop`` and ``s`` are still the same object
    
    Examples
    --------
    
    ::
        
        crop(s, 420, 480, 'nm', 'air')
        
    Or in ``cm-1``::
        
        crop(s, 2000, 2300, 'cm-1')
    
    '''
    
    # Check inputs
    if wmin is None and wmax is None:
        raise ValueError('Choose at least `wmin=` or `wmax=`')
    if wunit is None:
        raise ValueError('Please precise unit for wmin and wmax with `unit=`')
    assert wunit in ['nm', 'cm-1']
    if wunit == 'nm' and medium is None:
        raise ValueError("Precise wavelength medium with medium='air' or "+\
                         "medium='vacuum'")
    if (wmin is not None and wmax is not None) and wmin >= wmax:
        raise ValueError('wmin should be < wmax (Got: {0:.2f}, {1:.2f})'.format(
                wmin, wmax))
    
    if len(s._q)>0 and len(s._q_conv)>0:
        raise NotImplementedError('Cant crop this Spectrum as there are both convoluted '+\
                                  'and not convoluted quantities stored')
        # Could bring unexpected errors... For instance, if cropping both 
        # with slit and without slit  quantities to the same waverange, 
        # reapplying the slit in 'valid' mode would reduce the wavelength range 
        # of the convoluted quantities 
        # Implementation: better ask User to drop some of the quantities themselves
    
    if not inplace:
        s = s.copy()
    
    # Convert wmin, wmax to Spectrum wavespace    
    # (deal with cases where wavelength are given in 'air' or 'vacuum')
    # TODO @dev: rewrite with wunit='cm-1', 'nm_air', 'nm_vac'
    waveunit = s.get_waveunit()
    wmin0, wmax0 = wmin, wmax
    if wunit == 'nm' and waveunit == 'cm-1':
        if medium == 'air':
            if wmax0: wmin = nm_air2cm(wmax0)   # reverted
            if wmin0: wmax = nm_air2cm(wmin0)   # reverted
        else:
            if wmax0: wmin = nm2cm(wmax0)   # reverted
            if wmin0: wmax = nm2cm(wmin0)   # reverted
    elif wunit == 'cm-1' and waveunit == 'nm':
        if s.get_medium() == 'air':
            if wmax0: wmin = cm2nm_air(wmax0)   # nm in air
            if wmin0: wmax = cm2nm_air(wmin0)   # nm in air
        else:
            if wmax0: wmin = cm2nm(wmax0)   # get nm in vacuum
            if wmin0: wmax = cm2nm(wmin0)   # get nm in vacuum
    elif wunit == 'nm' and waveunit == 'nm':
        if s.get_medium() == 'air' and medium == 'vacuum':
            # convert from given medium ('vacuum') to spectrum medium ('air')
            if wmin0: wmin = vacuum2air(wmin0)
            if wmax0: wmax = vacuum2air(wmax0)
        elif s.get_medium() == 'vacuum' and medium == 'air':
            # the other way around
            if wmin0: wmin = air2vacuum(wmin0)
            if wmax0: wmax = air2vacuum(wmax0)
    else:
        assert wunit == waveunit           # correct wmin, wmax
    
    # Crop non convoluted
    if len(s._q)>0:
        b = ones_like(s._q['wavespace'], dtype=bool)
        if wmin: b *= (wmin <= s._q['wavespace'])
        if wmax: b *= (s._q['wavespace'] <= wmax)
        for k, v in s._q.items():
            s._q[k] = v[b]
  
    # Crop convoluted
    if len(s._q_conv)>0:
        b = ones_like(s._q_conv['wavespace'], dtype=bool)
        if wmin: b *= (wmin <= s._q_conv['wavespace'])
        if wmax: b *= (s._q_conv['wavespace'] <= wmax)
        for k, v in s._q_conv.items():
            s._q_conv[k] = v[b]
            
    return s
    



# %% Algebric operations on Spectra
    
def _get_unique_var(s, var, inplace):
    ''' Returns the unique spectral quantity in the Spectrum ``s``. If there are more, 
    raises an error.
    '''
    # If var is undefined, get it if there is no ambiguity
    if var is None:
        quantities = s.get_vars()
        if len(quantities)>1:
            raise KeyError('There is an ambiguity with the Spectrum algebraic operation. '+\
                            'There should be only one var in Spectrum {0}. Got {1}\n'.format(
                                    s.get_name(), s.get_vars())+\
                            "Think about using 'Transmittance(s)', 'Radiance(s)', etc.")
        elif len(quantities)==0:
            raise KeyError('No spectral quantity defined in Spectrum {0}'.format(s.get_name()))
        else:
            var = quantities[0]
    # If inplace, assert there is only one var
    if inplace and len(s.get_vars())>1:
        raise ValueError('Cant modify inplace one spectral quantity of a Spectrum '+\
                         "that contains several ({0}). Use 'inplace=False'".format(
                                 s.get_vars()))
    return var

def multiply(s, coef, var=None, inplace=False):
    '''Multiply s[var] by the float 'coef'

    Parameters
    ----------
    s: Spectrum objects
        The spectra to multiply.
    coef: float
        Coefficient of the multiplication.
    var: str, or ``None``
        'radiance', 'transmittance', ... If ``None``, get the unique spectral
        quantity of ``s`` or raises an error if there is any ambiguity
    inplace: bool
        if ``True``, modifies ``s`` directly. Else, returns a copy.
        Default ``False``

    Returns
    -------
    s : Spectrum
        Spectrum object where intensity of s['var'] is multiplied by coef
        If ``inplace=True``, ``s`` has been modified directly.

    '''
    # Check input
    var = _get_unique_var(s, var, inplace)
        
    if not inplace:
        s = s.copy(quantity=var)
#        if name is not None:
#            s.name = name
    
    # Multiply inplace       ( @dev: we have copied already if needed )
    w, I = s.get(var, wunit=s.get_waveunit(), copy=False)  
    I *= coef         # @dev: updates the Spectrum directly because of copy=False

    return s

def add_constant(s, cst, unit=None, var=None, wunit='nm', inplace=False):
    '''Return a new spectrum with a constant added to s[var]. 
    Equivalent to::
        
        s + constant

    Parameters    
    ----------
    s: Spectrum objects
        Spectrum you want to modify
    cst: Float
        Constant to add.
    unit: str
        unit for ``cst``. If ``None``, uses the default unit in ``s`` for 
        variable ``var``.
    var: str, or ``None``
        'radiance', 'transmittance', ... If ``None``, get the unique spectral
        quantity of ``s`` or raises an error if there is any ambiguity
    wunit: str
        'nm'or 'cm-1'
    inplace: bool
        if ``True``, modifies ``s`` directly. Else, returns a copy. 
        Default ``False``

    Returns    
    -------
    s : Spectrum
        Spectrum object where cst is added to intensity of s['var']
        If ``inplace=True``, ``s`` has been modified directly.

    Notes   
    -----
    
    Use only for rough work. If you want to work properly with spectrum 
    objects, see :py:meth:`~radis.los.slabs.MergeSlabs`.
    '''
    # Check input
    var = _get_unique_var(s, var, inplace)

    # Convert to Spectrum unit
    if unit is not None:
        Iunit = s.units[var]
        if unit != Iunit:
            from radis.phys.convert import conv2
            cst = conv2(cst, unit, Iunit)

    if not inplace:
        s = s.copy(quantity=var)
    
    # Add inplace       ( @dev: we have copied already if needed )
    w, I = s.get(var, wunit=s.get_waveunit(), copy=False)  
    I += cst
    # @dev: updates the Spectrum directly because of copy=False
    
#    s.name = '{0}+{1}'.format(s.get_name(), cst)

    return s

def add_array(s, a, unit=None, var=None, wunit='nm', inplace=False):
    '''Return a new spectrum with a constant added to s[var]. 
    Equivalent to::
        
        s + array

    Parameters    
    ----------
    s: Spectrum objects
        Spectrum you want to modify
    a: numpy array
        array to add. Must have the same length as variable ``var`` in Spectrum 
        ``s``
    unit: str
        unit for ``a``. If ``None``, uses the default unit in ``s`` for 
        variable ``var``.
    var: str, or ``None``
        'radiance', 'transmittance', ... If ``None``, get the unique spectral
        quantity of ``s`` or raises an error if there is any ambiguity
    wunit: str
        'nm'or 'cm-1'
    inplace: bool
        if ``True``, modifies ``s`` directly. Else, returns a copy. 
        Default ``False``

    Returns    
    -------
    s : Spectrum
        Spectrum object where array ``a`` is added to intensity of s['var']
        If ``inplace=True``, ``s`` has been modified directly.

    Notes   
    -----
    Use only for rough work. If you want to work properly with spectrum 
    objects, see MergeSlabs.
    
    Examples
    --------
    
    Add Gaussian noise to your Spectrum (assuming there is only one spectral
    quantity defined)::
        
        s += np.random.normal(0,1,len(s.get_wavelength()))

    '''
    # Check input
    var = _get_unique_var(s, var, inplace)

    # Convert to Spectrum unit
    if unit is not None:
        Iunit = s.units[var]
        if unit != Iunit:
            from radis.phys.convert import conv2
            a = conv2(a, unit, Iunit)

    if not inplace:
        s = s.copy(quantity=var)
    
    # Add inplace       ( @dev: we have copied already if needed )
    w, I = s.get(var, wunit=s.get_waveunit(), copy=False)  
    I += a
    # @dev: updates the Spectrum directly because of copy=False

    return s

def sub_baseline(s, left, right, unit=None, var=None, wunit='nm',
                  inplace=False):
    '''Return a new spectrum with a baseline substracted to s[var] 
    
    Parameters    
    ----------
    
    s: Spectrum objects
        Spectrum you want to modify
    left: Float
        Constant to substract on the left of the spectrum.
    right: Float
        Constant to substract on the right of the spectrum.
    unit: str
        unit for ``cst``. If ``None``, uses the default unit in ``s`` for 
        variable ``var``.
    var: str
        'radiance', 'transmittance', ...  If ``None``, get the unique spectral
        quantity of ``s`` or raises an error if there is any ambiguity
    wunit: str
        'nm'or 'cm-1'
    inplace: bool
        if ``True``, modifies ``s`` directly. Else, returns a copy. 
        Default ``False``
        
    Returns    
    -------
    
    s: Spectrum
        Spectrum object where the baseline was substracted to intensity of s['var']
        If ``inplace=True``, ``s`` has been modified directly.

    Notes    
    -----
    Use only for rough work. 
    
    See Also
    --------
    
    :py:func:`~radis.spectrum.operations.get_baseline`
    '''
    import numpy as np
    # Check input
    var = _get_unique_var(s, var, inplace)
        
    # Convert to Spectrum unit
    if unit is not None:
        Iunit = s.units[var]
        if unit != Iunit:
            from radis.phys.convert import conv2
            left = conv2(left, unit, Iunit)
            right = conv2(right, unit, Iunit)

    if not inplace:
        s = s.copy(quantity=var)
       
    # @EP: 

    # Substract inplace       ( @dev: we have copied already if needed )
    w, I = s.get(var, wunit=s.get_waveunit(), copy=False)  
    I -= np.linspace(left, right, num=np.size(I))
    # @dev: updates the Spectrum directly because of copy=False

    return s
    
def add_spectra(s1, s2, var=None, wunit='nm', force=False):
    '''Return a new spectrum with ``s2`` added to ``s1``. 
    Equivalent to::
        
        s1 + s2
    
    .. warning::
        we are just algebrically adding the quantities. If you want to merge
        spectra while preserving the radiative transfer equation, see 
        :func:`~radis.los.slabs.MergeSlabs` and :func:`~radis.los.slabs.SerialSlabs`
    
    Parameters    
    ----------
    
    s1, s2: Spectrum objects
        Spectrum you want to substract
    var: str
        quantity to manipulate: 'radiance', 'transmittance', ... If ``None``, 
        get the unique spectral quantity of ``s1``, or the unique spectral
        quantity of ``s2``, or raises an error if there is any ambiguity
    wunit: str
        'nm'or 'cm-1'
        
    Returns    
    -------
    
    s: Spectrum
        Spectrum object with the same units and waveunits as ``s1``
        
    See Also
    --------
    
    :func:`~radis.los.slabs.MergeSlabs`,
    :func:`~radis.spectrum.operations.substract_spectra`
    
    '''
    
    # Get variable
    if var is None:
        try:
            var = _get_unique_var(s2, var, inplace=False)    # unique variable of 2nd spectrum  
        except KeyError:
            var = _get_unique_var(s1, var, inplace=False)    # if doesnt exist, unique variable of 1st spectrum
            # if it fails, let it fail
    # Make sure it is in both Spectra
    if var not in s1.get_vars():
        raise KeyError('Variable {0} not in Spectrum {1}'.format(var, s1.get_name()))
    if var not in s2.get_vars():
        raise KeyError('Variable {0} not in Spectrum {1}'.format(var, s1.get_name()))
        
    if var in ['transmittance_noslit', 'transmittance'] and not force:
        raise ValueError('It does not make much physical sense to sum transmittances. Are '+\
                         'you sure of what you are doing? See also `//` (MergeSlabs), `>` '+\
                         "(SerialSlabs) and `concat_spectra`. If you're sure, use `force=True`")
    
    # Use same units 
    Iunit = s1.units[var]            
    wunit = s1.get_waveunit()
    medium = s1.get_medium()

    # Resample
    if wunit == 'nm':
        s2 = s2.resample(s1.get_wavelength(), 'nm', inplace=False)
    elif wunit == 'cm-1':
        s2 = s2.resample(s1.get_wavenumber(), 'cm-1', inplace=False)
    else:
        raise ValueError('Unexpected wunit: {0}'.format(wunit))
    
    # Add
    w1, I1 = s1.get(var=var, Iunit=Iunit, wunit=wunit, medium=medium)
    w2, I2 = s2.get(var=var, Iunit=Iunit, wunit=wunit, medium=medium)

    name = s1.get_name()+'+'+s2.get_name()
    
    sub = Spectrum.from_array(w1, I1 + I2, var, 
                               waveunit=wunit, 
                               unit=Iunit,
                               conditions={'medium' : medium}, 
                               name=name)
#    warn("Conditions of the left spectrum were copied in the substraction.", Warning)
    return sub

def substract_spectra(s1, s2, var=None, wunit='nm'):
    '''Return a new spectrum with ``s2`` substracted from ``s1``. 
    Equivalent to::
        
        s1 - s2
    
    Parameters    
    ----------
    
    s1, s2: Spectrum objects
        Spectrum you want to substract
    var: str
        quantity to manipulate: 'radiance', 'transmittance', ... If ``None``, 
        get the unique spectral quantity of ``s1``, or the unique spectral
        quantity of ``s2``, or raises an error if there is any ambiguity
    wunit: str
        'nm'or 'cm-1'
        
    Returns    
    -------
    
    s: Spectrum
        Spectrum object with the same units and waveunits as ``s1``
        
    See Also
    --------
    
    :func:`~radis.spectrum.operations.add_spectra`
    
    '''

    # Get variable
    if var is None:
        try:
            var = _get_unique_var(s2, var, inplace=False)    # unique variable of 2nd spectrum  
        except KeyError:
            var = _get_unique_var(s1, var, inplace=False)    # if doesnt exist, unique variable of 1st spectrum
            # if it fails, let it fail
    # Make sure it is in both Spectra
    if var not in s1.get_vars():
        raise KeyError('Variable {0} not in Spectrum {1}'.format(var, s1.get_name()))
    if var not in s2.get_vars():
        raise KeyError('Variable {0} not in Spectrum {1}'.format(var, s1.get_name()))
    
    # Use same units 
    Iunit = s1.units[var]            
    wunit = s1.get_waveunit()
    medium = s1.get_medium()

    # Resample
    if wunit == 'nm':
        s2 = s2.resample(s1.get_wavelength(), 'nm', inplace=False)
    elif wunit == 'cm-1':
        s2 = s2.resample(s1.get_wavenumber(), 'cm-1', inplace=False)
    else:
        raise ValueError('Unexpected wunit: {0}'.format(wunit))
    
    # Substract
    w1, I1 = s1.get(var=var, Iunit=Iunit, wunit=wunit, medium=medium)
    w2, I2 = s2.get(var=var, Iunit=Iunit, wunit=wunit, medium=medium)

    name = s1.get_name()+'-'+s2.get_name()
    
    sub = Spectrum.from_array(w1, I1 - I2, var, 
                               waveunit=wunit, 
                               unit=Iunit,
                               conditions={'medium' : medium}, 
                               name=name)
#    warn("Conditions of the left spectrum were copied in the substraction.", Warning)
    return sub


def concat_spectra(s1, s2, var=None):
    ''' Concatenate two spectra ``s1`` and ``s2`` side by side.
    
    Note: their spectral range should not overlap 
    
    Returns    
    -------
    
    s: Spectrum
        Spectrum object with the same units and waveunits as ``s1``
        
    Parameters    
    ----------
    
    s1, s2: Spectrum objects
        Spectrum you want to concatenate
    var: str
        quantity to manipulate: 'radiance', 'transmittance', ... If ``None``, 
        get the unique spectral quantity of ``s1``, or the unique spectral
        quantity of ``s2``, or raises an error if there is any ambiguity
        
    Notes
    -----
    
    .. warning::
        
        the output Spectrum has the sum of the spectral ranges of s1 and s2. 
        It won't be evenly spaced. This means that you cannot apply a slit without
        side effects. Typically, you want to use this function for convolved 
        quantities only, such as experimental spectra. Else, use
        :func:`~radis.los.slabs.MergeSlabs` with the options 
        ``resample='full', out='transparent'``
        
    See Also
    --------
    
    :func:`~radis.spectrum.operations.add_spectra`, 
    :func:`~radis.los.slabs.MergeSlabs`
    
    '''
    
    # Get variable
    if var is None:
        try:
            var = _get_unique_var(s2, var, inplace=False)    # unique variable of 2nd spectrum  
        except KeyError:
            var = _get_unique_var(s1, var, inplace=False)    # if doesnt exist, unique variable of 1st spectrum
            # if it fails, let it fail
    # Make sure it is in both Spectra
    if var not in s1.get_vars():
        raise KeyError('Variable {0} not in Spectrum {1}'.format(var, s1.get_name()))
    if var not in s2.get_vars():
        raise KeyError('Variable {0} not in Spectrum {1}'.format(var, s1.get_name()))
        
    if var in ['transmittance_noslit', 'transmittance']:
        warn('It does not make much physical sense to sum transmittances. Are '+\
             'you sure of what you are doing? See also // (MergeSlabs) and > '+\
             '(SerialSlabs)')
    
    # Use same units 
    Iunit = s1.units[var]            
    wunit = s1.get_waveunit()
    medium = s1.get_medium()

    # Get the value, on the same wunit)
    w1, I1 = s1.get(var=var, copy=False)  # @dev: faster to just get the stored value. 
                                          # it's copied in hstack() below anyway). 
    w2, I2 = s2.get(var=var, Iunit=Iunit, wunit=wunit, medium=medium)
    
    if not (w1.max() < w2.min() or w2.max() > w1.min()):
        raise ValueError("You cannot use concat_spectra for overlapping spectral ranges. "+\
                         "Got: {0:.2f}-{1:.2f} and {2:.2f}-{3:.2f} {4}. ".format(w1.min(), w1.max(),
                                                               w2.min(), w2.max(),
                                                               wunit)+\
                         "Use MergeSlabs instead, with the correct `out=` parameter "+\
                         "for your case")
                         
    w_tot = hstack((w1, w2))
    I_tot = hstack((I1, I2))

    name = s1.get_name()+'&'+s2.get_name()     # use "&" instead of "+" 
    
    concat = Spectrum.from_array(w_tot, I_tot, var, 
                               waveunit=wunit, 
                               unit=Iunit,
                               conditions={'medium' : medium}, 
                               name=name)
    
    return concat
    

def offset(s, offset, unit, name=None, inplace=False):
    # type: (Spectrum, float, str, str, bool) -> Spectrum
    '''Offset the spectrum by a wavelength or wavenumber 

    Parameters    
    ----------
    s: Spectrum
        Spectrum you want to modify
    offset: float
        Constant to add to all quantities in the Spectrum.
    unit: 'nm' or 'cm-1'
        unit for ``offset``.
    name: str
        name of output spectrum
    inplace: bool
        if ``True``, modifies ``s`` directly. Else, returns a copy. 
        Default ``False``

    Returns    
    -------
    s : Spectrum
        Spectrum object where cst is added to intensity of s['var']
        If ``inplace=True``, ``s`` has been modified directly.
        
    See Also
    --------
    
    call as a Spectrum method directly: :py:meth:`~radis.spectrum.spectrum.Spectrum.offset`
    '''
    
    has_var = len(s._q)>0
    has_conv_var = len(s._q_conv)>0
    
    # Convert to correct unit:
    if unit == 'nm' and s.get_waveunit() == 'cm-1':
        # Note @EP: technically we should check the medium is air or vacuum...  TODO
        # Note @EP: here we're offsetting by a constant value in 'cm-1', which is
        # not a constant value in 'nm'. We end of with offset as an array 
        if has_var: offset_q = - dnm2dcm(offset, s.get_wavelength(which='non_convoluted'))  # this is an array
        if has_conv_var: offset_qconv = - dnm2dcm(offset, s.get_wavelength(which='convoluted'))  # this is an array
    elif unit == 'cm-1' and s.get_waveunit() == 'nm':
        if has_var: offset_q = - dcm2dnm(offset, s.get_wavenumber(which='non_convoluted'))  # this is an array
        if has_conv_var: offset_qconv = - dcm2dnm(offset, s.get_wavenumber(which='convoluted'))  # this is an array
    else:
        assert unit == s.get_waveunit()
        if has_var: offset_q = offset
        if has_conv_var: offset_qconv = offset
        
    if not inplace:
        s = s.copy()
        
    # Update all variables
    if has_var:
        s._q['wavespace'] += offset_q
        # @dev: updates the Spectrum directly because of copy=False
    if has_conv_var:
        s._q_conv['wavespace'] += offset_qconv
        
    if name:
        s.name = name
        
    return s

def get_baseline(s, var='radiance', wunit='nm', medium='air', Iunit=None):
    '''Calculate and returns a baseline 

    Parameters    
    ----------
    s: Spectrum
        Spectrum which needs a baseline

    Returns    
    -------
    baseline: Spectrum
        Spectrum object where intenisity is the baseline of s is computed by peakutils
        
    See Also
    --------
    
    :py:func:`~radis.spectrum.operations.sub_baseline`
    '''
    import peakutils 
    w1, I1 = s.get(var=var, Iunit=Iunit, wunit=wunit, medium=medium)
    baseline = peakutils.baseline(I1, deg=1, max_it = 500)
    baselineSpectrum = Spectrum.from_array(w1, baseline, var, 
                               waveunit=wunit, 
                               unit=Iunit,
                               conditions={'medium' : medium}, 
                               name=s.get_name()+'_baseline')
    return baselineSpectrum
# %% Tests

def test_multiplyAndAddition(*args, **kwargs):

    s = load_spec(getTestFile("CO_Tgas1500K_mole_fraction0.01.spec"), binary=True)
    s.update('radiance_noslit', verbose=False)
    s.apply_slit(0.1)
    s = Radiance(s)
    assert s.units['radiance'] == 'mW/cm2/sr/nm'

    s_bis = add_constant(s, 1, 'mW/cm2/sr/nm')
    w, Idiff = get_diff(s_bis, s, 'radiance') 
    test = Idiff[1]-1
    assert np.all(test<1e-10)

    s_ter = multiply(multiply(s, 50), 1/50)
#    plot_diff(s_ter, s_5)
    diff = get_diff(s_ter, s, 'radiance') 
    ratio = abs(np.trapz(diff[1], x=diff[0])/s.get_integral('radiance'))
    assert ratio<1e-10

def test_visualTestBaseline(plot=True, *args, **kwargs):

    s = load_spec(getTestFile("CO_Tgas1500K_mole_fraction0.01.spec"), binary=True)
    s.update('radiance_noslit', verbose=False)
    s.apply_slit(0.1)
    s = Radiance_noslit(s)
    assert s.units['radiance'] == 'mW/cm2/sr/nm'
    
    s2 = sub_baseline(s, 2e-4, -2e-4, name = 'sub_arb_baseline')
    if plot:
        plot_diff(s, s2)
    # TODO: add Test on intensity on both sides?

def test_offset(plot=True):
    
    s = load_spec(getTestFile("CO_Tgas1500K_mole_fraction0.01.spec"), binary=True)
    s.update('radiance_noslit', verbose=False)
    s.apply_slit(0.1)
    
    s2 = offset(s, 10, 'nm', name = 'offset_10nm')
    if plot:
        plot_diff(s, s2)
    assert np.allclose(s2.get_wavelength(which='convoluted'), 
                       s.get_wavelength(which='convoluted')+10)
    assert np.allclose(s2.get_wavelength(which='non_convoluted'), 
                       s.get_wavelength(which='non_convoluted')+10)
    
    # Test inplace version
    s.offset(10, 'nm')
    assert np.allclose(s2.get_wavelength(which='convoluted'), 
                       s.get_wavelength(which='convoluted'))
    

if __name__ == '__main__':
    
    from radis import load_spec, get_diff, plot_diff
    from radis.test.utils import getTestFile
    import numpy as np
    import pytest
   
    
    test_multiplyAndAddition()
    test_offset()
    
    # An implement of Spectrum Algebra
    # Reload:
    s=load_spec(getTestFile('CO_Tgas1500K_mole_fraction0.01.spec'))
    s.update()

    # Test addition of Spectra
    s.plot(lw=2, nfig='Merge: s//s')
    (s//s).plot(nfig='same')
    
    # Test substraction of Spectra
    s_tr = Transmittance_noslit(s)
    assert (s_tr-1.0*s_tr).get_integral('transmittance_noslit') == 0

    # TODO: add test
    # @EP: the test fails at the moment because multiply only works with radiance,
    # and MergeSlabs only works with non convoluted quantities
    # Do we want that? Up for discussion...
    
    # There should be an error if algebraic operations are used when 
    # multiple quantities are defined:
    with pytest.raises(KeyError):
        2*s
        
    s.apply_slit(0.1, 'nm')
    s_rad = Radiance(s)
    
    # Test multiplication with float
    s.plot(lw=2, nfig='Multiplication (by scalar): 2*s', wunit='nm')
#    (s*s).plot(nfig='same')
    (2*s_rad).plot(nfig='same', wunit='nm')
    
    # Test Serial:
    s.rescale_path_length(20)
    s.plot('radiance_noslit', lw=2, nfig='Line of sight (SerialSlabs): s > s > s')
    (s>s>s).plot('radiance_noslit', nfig='same')

    # Test algebraic addition (vs multiplication)
    assert (s_rad+s_rad).compare_with(2*s_rad, spectra_only='radiance', plot=False)

    # Test algebraic addition with different waveunits
    s_rad_nm = s_rad.resample(s_rad.get_wavelength(), 'nm', inplace=False)
    s_sum = (2*s_rad_nm-s_rad_nm)
    s_sum.compare_with(s_rad, spectra_only='radiance', plot=True)
    assert (s_rad_nm+s_rad_nm).compare_with(2*s_rad, spectra_only='radiance', plot=True,rtol=1e-3)
    