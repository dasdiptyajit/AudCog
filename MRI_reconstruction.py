# -*- coding: utf-8 -*-
"""
Author: Diptyajit Das
email: <bmedasdiptyajit@gmail.com>
Lab: Auditory Cognition lab, heidelberg
"""

def retcode_error(command, subject_id):

    """
        Routine to check and return errors in the code

             Parameters
             ----------
             command: string
             subject_ids: string

    """
    print('%s did not run successfully for subject %s.' % (command, subject_id))
    print('Please check the arguments, and rerun for subject.')

def mri_surfaces(subject_ids, freesurfer_home=None):

    """
        Routine to perform complete surface reconstruction

             Parameters
             ----------
             subject_ids: list of strings
                 List of subjects ids
             subjects_dir: string
                 String of subject directory
             freesurfer_home: string
                String of FreeSurfer directory
             n_jobs: default with 4 cores (automatic implemented with -parallel command)

    """
    # -----------------------------------
    # import necessary modules
    import os
    from os.path import join
    from subprocess import call
    # -----------------------------------

    if freesurfer_home == None:
        freesurfer_home = str(os.environ['FREESURFER_HOME'])
        freesurfer_bin = join(freesurfer_home, 'bin', '')

    else:
        freesurfer_bin = join(freesurfer_home, 'bin', '')

    # some commands requires it, setting it here for safety
    os.environ['DISPLAY'] = ':0'

    for id in subject_ids:
        print('Setting up freesurfer surfaces for subject id: %s' % (id))
        # Reconstruct all brain surfaces
        retcode = call([freesurfer_bin + 'recon-all', '-autorecon-all', '-parallel', '-subjid', id])
        if retcode != 0:
            retcode_error('recon-all', id)
            continue

def BEM(subject_ids, subjects_dir= None, ico=4, conductivity=(0.3, 0.006, 0.3),bem_pattern='-bem.fif'):
    """
       Routine to generate BEM surfaces and BEM solution

           Parameters
           ----------
           subject_ids: list of strings
               List of subjects ids
           subjects_dir: string
               String of subject directory
           method: watershed_bem
           ico: The surface ico downsampling to use, e.g. 5=20484, 4=5120, 3=1280.
                If None, no subsample is applied.
           conductivity: (0.3, 0.006, 0.3)
                The conductivities to use for each shell, total 3 layers.
           fn_dir: string or None
               Directory to save the data.
    """
    # -----------------------------------
    # import necessary modules
    from mne.bem import make_watershed_bem, write_bem_surfaces
    from mne import write_bem_solution, make_bem_model, make_bem_solution
    from os.path import join
    # -----------------------------------

    for id in subject_ids:

        make_watershed_bem(subject=id, subjects_dir=subjects_dir, overwrite=True)

        # Create BEM surfaces
        model= make_bem_model(id, ico=ico, conductivity=conductivity)
        fn_dir= join(subjects_dir, id, 'bem', '%s-5120-5120-5120%s'%(id, bem_pattern))
        write_bem_surfaces(fn_dir, model)

        # Create BEM solution
        bem= make_bem_solution(model)
        bem_sol_dir= join(subjects_dir, id, 'bem', '%s-5120-5120-5120-bem-sol.fif'%id)
        write_bem_solution(bem_sol_dir, bem)
        print('BEM solution is created >>>>>>')


def coreg_scalp_surfaces(subject_ids, subjects_dir=None):
    """
       Routine to generate high-resolution head surfaces for coordinate alignment

           Parameters
           ----------
           subject_ids: list of strings
               List of subjects ids
           subjects_dir: string
               String of subject directory

            output: -head-dense.fif, -head-medium.fif, -head-sparse.fif

    """
    # -----------------------------------
    # import necessary modules
    from mne.commands import mne_make_scalp_surfaces
    # -----------------------------------

    for id in subject_ids:

        try:
            print('Create high-resolution head surfaces for coordinate alignment for subject: %s'%id)
            mne_make_scalp_surfaces._run(subjects_dir, id, force=True, overwrite=True, verbose=True)
        except:
            retcode_error('mne_make_scalp_surfaces', id)
            continue


def source_space(subject_ids, subjects_dir=None, spacing='ico5', n_jobs=2, src_pattern='-src.fif'):
    """
         Routine to generate source space

             Parameters
             ----------
             subject_ids: list of strings
                 List of subjects ids
             subjects_dir: string
                 String of subject directory
             spacing: 'ico5' or 'oct6'
             n_jobs: 1 or 2 or 3 or 4
                 Parallel core jobs
             fn_dir: string or None
                 Directory to save the data.
     """
    # -----------------------------------
    # import necessary modules
    from os.path import join
    from mne import setup_source_space, write_source_spaces
    # -----------------------------------

    for id in subject_ids:
        src = setup_source_space(subject=id,spacing=spacing, surface='white', subjects_dir=subjects_dir, n_jobs=n_jobs)
        fn_dir= join(subjects_dir, id, '%s-%s%s'%(id, spacing, src_pattern))
        write_source_spaces(fn_dir, src)
        print('source space is done >>>>>>')

