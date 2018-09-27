# -*- coding: utf-8 -*-
"""
Author: Diptyajit Das
email: <bmedasdiptyajit@gmail.com>
Lab: Auditory Cognition lab, heidelberg
"""
#######################################
# Script summary:It allows to -
#                1. Reconstruct mri surfaces
#                2. Create BEM solution
#                3. Create scalp surfaces for co-registration
#                3. Setup source space surfaces

# Comment: The script has to be executed in the terminal in order to access freesurfer environment
#######################################

# -------------------------------------------------------
# main function --> for testing purpose
# -------------------------------------------------------
if __name__ == '__main__':

    # ------------------------------------------
    # Import necessary modules and functions
    # ------------------------------------------
    import os
    from os.path import join
    from MRI_reconstruction import mri_surfaces,source_space, BEM, coreg_scalp_surfaces

    # Which steps should be performed?
    create_mri_surfaces = False
    create_source_space = False
    create_bem = False
    create_scalp_surfaces = False

    # Define path parameters
    root_dir = join('/', 'media', 'diptyajit')
    subjects_dir = join(root_dir, 'Ext_drive', 'FreeSurfer_Home', '')
    freesurfer_home = str(os.environ['FREESURFER_HOME'])

    # Define general parameter
    # Define subject ids
    subject_ids = ['20140305']

    # Define BEM parameters
    ico = 4
    conductivity = (0.3, 0.006, 0.3)
    bem_pattern = '-bem.fif'

    # Define source space parameters
    spacing = 'ico5'
    n_jobs = 3
    src_pattern = '-src.fif'

    # ---------------
    # Call function
    # ---------------

# check for mri surfaces
if create_mri_surfaces:
    mri_surfaces(subject_ids, freesurfer_home=freesurfer_home)

# check for BEM
if create_bem:
    BEM(subject_ids, subjects_dir=subjects_dir, ico=ico, conductivity=conductivity, bem_pattern=bem_pattern)

# check for scalp surfaces
if create_scalp_surfaces:
    coreg_scalp_surfaces(subject_ids, subjects_dir=subjects_dir)

# check for source space
if create_source_space:
    source_space(subject_ids, subjects_dir=subjects_dir, spacing=spacing, n_jobs=n_jobs, src_pattern=src_pattern)

