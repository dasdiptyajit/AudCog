# -*- coding: utf-8 -*-
"""
Author: Diptyajit Das <bmedasdiptyajit@gmail.com>
"""

# -------------------------------------------
# import necessary modules
# -------------------------------------------
from mne import compute_raw_covariance
from mne import pick_types, write_cov
from mne.io import Raw
from os.path import exists, join
import mne
import time
from glob import glob
from mne import read_evokeds
from mne import read_cov, read_forward_solution

def source_space(subject_ids, subjects_dir= None, spacing='ico5', n_jobs=2, src_pattern = '-src.fif',fn_dir= None):
    """
     Routine to generate source space

         Parameters
         -------------
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
    from mne import setup_source_space, write_source_spaces

    for itype, id in enumerate(subject_ids):
        src = setup_source_space(subject=id,spacing=spacing, subjects_dir=subjects_dir, n_jobs=n_jobs)
        fn_dir= join(subjects_dir, id, '%s-%s-src.fif'%(id, spacing))

        write_source_spaces(fn_dir, src)
        print('source space is done >>>>>>')

def BEM(subject_ids, subjects_dir= None, ico=4, conductivity=(0.3, 0.006, 0.3), bem_pattern='-bem.fif',fn_dir=None):
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
                The conductivities to use for each shell.
           fn_dir: string or None
               Directory to save the data.
       """
    # -----------------------------------
    # import necessary modules
    from mne import setup_source_space, write_source_spaces
    from mne.bem import make_watershed_bem, write_bem_surfaces
    from mne import write_bem_solution
    from os.path import join

    for itype, id in enumerate(subject_ids):

        make_watershed_bem(subject=id, subjects_dir=subjects_dir, overwrite=True)

        # Create BEM surfaces
        model= mne.make_bem_model(id, ico=ico, conductivity=conductivity)
        import pdb
        pdb.set_trace()
        fn_dir= join(subjects_dir, id, 'bem', '%s-5120-5120-5120%s'%(id, bem_pattern))
        write_bem_surfaces(fn_dir, model)

        # Create BEM solution
        bem= mne.make_bem_solution(model)
        bem_sol= join(subjects_dir, id, 'bem', '%s-5120-5120-5120-bem-sol.fif'%id)
        write_bem_solution(bem_sol, bem)
        print('BEM solution is created >>>>>>')




def raw_merge(subject_ids, subjects_dir= None, segments=['block3', 'block4'], raw_pattern='_passive_raw_fif', fn_dir=None):
    """
           Routine to merge two raw segments to a complete raw file

               Parameters
               ----------
               subject_ids: list of strings
                   List of subjects ids
               subjects_dir: string
                   String of subject directory

               raw_pattern: string
                    ending name for the raw file
               fn_dir: string or None
                   Directory to save the data.
           """
    # -----------------------------------
    # import necessary modules
    from os.path import join
    from glob import glob
    from mne.io import Raw, concatenate_raws

    for itype, id in enumerate(subject_ids):
        raws=[]
        for seg in segments:
            raw_seg = join(subjects_dir, id, id+'_%s_raw.fif'%seg)
            raw_read = Raw(raw_seg, preload=True)
            raws.append(raw_read)

        raw = concatenate_raws(raws)
        fn_dir = join(subjects_dir, id, id + raw_pattern)
        raw.save(fn_dir)





def noise_cov(subject_ids, subjects_dir= None, ico=4, conductivity=(0.3, 0.006, 0.3), bem_pattern='-bem.fif',fn_dir=None):
    """
          Routine to create noise covariance matrices from

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
                   The conductivities to use for each shell.
              fn_dir: string or None
                  Directory to save the data.
          """

    for itype, id in enumerate(subject_ids):

        # empty_dir= join(stage, 'Chrono', 'Chrono-empty-room-files', '')
        noise_cov_pattern = "%s_dev-cov.fif" % id
        cov_out = join(subject_dir, id, noise_cov_pattern)

        # pick only MEG channels
        picks = pick_types(raw_empty.info, meg=True, eeg=False, stim=False, eog=False)

        # calculate noise-covariance matrix
        noise_cov_mat = compute_raw_covariance(raw_empty, picks=picks, n_jobs=3)
        # write noise-covariance matrix to disk
        write_cov(cov_out, noise_cov_mat)



def forward_solution(subject_ids, subjects_dir= None):



    for itype, id in enumerate(subject_ids):

        fn_dir= join(subject_dir, id, '%s_ico-5_dev-fwd.fif' % id)

    # Make forward solution
    fwd = mne.make_forward_solution(evoked.info, fname_trans, src, fname_bem, meg=True, eeg=False, mindist=0.5, n_jobs=3)
    fwd['surf_ori'] = True
    mne.write_forward_solution(forward_out, fwd)
    print ('forward solution has done.')


    #fwd = read_forward_solution( forward_out, surf_ori=True)  # forward solution

# print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
# print ('++++++++++++++++++ Set up the inverse operator for subject: %s ++++++++++++++++++' % id)
# print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#
# inverse_out = join(subject_dir, id, '%s_dev-inv.fif' %id)
#
# if not exists(inverse_out):
#
#     inv = mne.minimum_norm.make_inverse_operator(evoked.info, fwd, noise_cov_mat, loose=0.2,
#                                                  depth=0.8, fixed=False,limit_depth_chs=False)
#     mne.minimum_norm.write_inverse_operator(inverse_out, inv)
#
#     print ('Inverse solution has done.')
#
# else:
#
#     print ('Inverse operator already exist')
#
# print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
# print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
# print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
# print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
#
# b = time.time()
# print ('Dataset for subject: %s was created succesfully. Duration: %s minutes.' % (id, ((b - a) / 60)))
#
# print ('Inverse operator has generated for subject id:..... last one', id)
#
#
#
#
#
#
#
