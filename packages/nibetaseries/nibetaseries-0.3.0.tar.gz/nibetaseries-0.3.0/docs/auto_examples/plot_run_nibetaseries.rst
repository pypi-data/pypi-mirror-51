.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_plot_run_nibetaseries.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_run_nibetaseries.py:


Running NiBetaSeries
====================

This example runs through a basic call of NiBetaSeries using
the commandline entry point ``nibs``.
While this example is using python, typically ``nibs`` will be
called directly on the commandline.

Import all the necessary packages
=================================


.. code-block:: default


    import tempfile  # make a temporary directory for files
    import os  # interact with the filesystem
    import urllib.request  # grad data from internet
    import tarfile  # extract files from tar
    from subprocess import Popen, PIPE, STDOUT  # enable calling commandline

    import matplotlib.pyplot as plt  # manipulate figures
    import seaborn as sns  # display results
    import pandas as pd   # manipulate tabular data







Download relevant data from ds000164 (and Atlas Files)
======================================================
The subject data came from `openneuro <https://openneuro.org/datasets/ds000164/versions/00001/>`_
:cite:`n-Verstynen2014`.
The atlas data came from a `recently published parcellation <https://www.ncbi.nlm.nih.gov/pubmed/28981612>`_
in a publically accessible github repository.


.. code-block:: default


    # atlas github repo for reference:
    """https://github.com/ThomasYeoLab/CBIG/raw/master/stable_projects/\
    brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI/"""
    data_dir = tempfile.mkdtemp()
    print('Our working directory: {}'.format(data_dir))

    # download the tar data
    url = "https://www.dropbox.com/s/qoqbiya1ou7vi78/ds000164-test_v1.tar.gz?dl=1"
    tar_file = os.path.join(data_dir, "ds000164.tar.gz")
    u = urllib.request.urlopen(url)
    data = u.read()
    u.close()

    # write tar data to file
    with open(tar_file, "wb") as f:
        f.write(data)

    # extract the data
    tar = tarfile.open(tar_file, mode='r|gz')
    tar.extractall(path=data_dir)

    os.remove(tar_file)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Our working directory: /tmp/tmplj5rxow3



Display the minimal dataset necessary to run nibs
=================================================


.. code-block:: default



    # https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    def list_files(startpath):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))


    list_files(data_dir)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    tmplj5rxow3/
        ds000164/
            dataset_description.json
            task-stroop_bold.json
            README
            CHANGES
            T1w.json
            task-stroop_events.json
            derivatives/
                fmriprep/
                    sub-001/
                        func/
                            sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz
                            sub-001_task-stroop_bold_confounds.tsv
                            sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
                data/
                    Schaefer2018_100Parcels_7Networks_order.txt
                    Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz
            sub-001/
                func/
                    sub-001_task-stroop_bold.nii.gz
                    sub-001_task-stroop_events.tsv
                anat/
                    sub-001_T1w.nii.gz



Manipulate events file so it satifies assumptions
=================================================
1. the correct column has 1's and 0's corresponding to correct and incorrect,
respectively.
2. the condition column is renamed to trial_type
nibs currently depends on the "correct" column being binary
and the "trial_type" column to contain the trial types of interest.

read the file
-------------


.. code-block:: default


    events_file = os.path.join(data_dir,
                               "ds000164",
                               "sub-001",
                               "func",
                               "sub-001_task-stroop_events.tsv")
    events_df = pd.read_csv(events_file, sep='\t', na_values="n/a")
    print(events_df.head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

        onset  duration correct  condition  response_time
    0   0.342         1       Y    neutral          1.186
    1   3.345         1       Y  congruent          0.667
    2  12.346         1       Y  congruent          0.614
    3  15.349         1       Y    neutral          0.696
    4  18.350         1       Y    neutral          0.752



replace condition with trial_type
---------------------------------


.. code-block:: default


    events_df.rename({"condition": "trial_type"}, axis='columns', inplace=True)
    print(events_df.head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

        onset  duration correct trial_type  response_time
    0   0.342         1       Y    neutral          1.186
    1   3.345         1       Y  congruent          0.667
    2  12.346         1       Y  congruent          0.614
    3  15.349         1       Y    neutral          0.696
    4  18.350         1       Y    neutral          0.752



save the file
-------------


.. code-block:: default


    events_df.to_csv(events_file, sep="\t", na_rep="n/a", index=False)







Manipulate the region order file
================================
There are several adjustments to the atlas file that need to be completed
before we can pass it into nibs.
Importantly, the relevant column names **MUST** be named "index" and "regions".
"index" refers to which integer within the file corresponds to which region
in the atlas nifti file.
"regions" refers the name of each region in the atlas nifti file.

read the atlas file
-------------------


.. code-block:: default


    atlas_txt = os.path.join(data_dir,
                             "ds000164",
                             "derivatives",
                             "data",
                             "Schaefer2018_100Parcels_7Networks_order.txt")
    atlas_df = pd.read_csv(atlas_txt, sep="\t", header=None)
    print(atlas_df.head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

       0                   1    2   3    4  5
    0  1  7Networks_LH_Vis_1  120  18  131  0
    1  2  7Networks_LH_Vis_2  120  18  132  0
    2  3  7Networks_LH_Vis_3  120  18  133  0
    3  4  7Networks_LH_Vis_4  120  18  135  0
    4  5  7Networks_LH_Vis_5  120  18  136  0



drop coordinate columns
-----------------------


.. code-block:: default


    atlas_df.drop([2, 3, 4, 5], axis='columns', inplace=True)
    print(atlas_df.head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

       0                   1
    0  1  7Networks_LH_Vis_1
    1  2  7Networks_LH_Vis_2
    2  3  7Networks_LH_Vis_3
    3  4  7Networks_LH_Vis_4
    4  5  7Networks_LH_Vis_5



rename columns with the approved headings: "index" and "regions"
----------------------------------------------------------------


.. code-block:: default


    atlas_df.rename({0: 'index', 1: 'regions'}, axis='columns', inplace=True)
    print(atlas_df.head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

       index             regions
    0      1  7Networks_LH_Vis_1
    1      2  7Networks_LH_Vis_2
    2      3  7Networks_LH_Vis_3
    3      4  7Networks_LH_Vis_4
    4      5  7Networks_LH_Vis_5



remove prefix "7Networks"
-------------------------


.. code-block:: default


    atlas_df.replace(regex={'7Networks_(.*)': '\\1'}, inplace=True)
    print(atlas_df.head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

       index   regions
    0      1  LH_Vis_1
    1      2  LH_Vis_2
    2      3  LH_Vis_3
    3      4  LH_Vis_4
    4      5  LH_Vis_5



write out the file as .tsv
--------------------------


.. code-block:: default


    atlas_tsv = atlas_txt.replace(".txt", ".tsv")
    atlas_df.to_csv(atlas_tsv, sep="\t", index=False)







Run nibs
========


.. code-block:: default


    out_dir = os.path.join(data_dir, "ds000164", "derivatives")
    work_dir = os.path.join(out_dir, "work")
    atlas_mni_file = os.path.join(data_dir,
                                  "ds000164",
                                  "derivatives",
                                  "data",
                                  "Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz")
    cmd = """\
    nibs -c WhiteMatter CSF \
    --participant-label 001 \
    -w {work_dir} \
    -a {atlas_mni_file} \
    -l {atlas_tsv} \
    {bids_dir} \
    fmriprep \
    {out_dir} \
    participant
    """.format(atlas_mni_file=atlas_mni_file,
               atlas_tsv=atlas_tsv,
               bids_dir=os.path.join(data_dir, "ds000164"),
               out_dir=out_dir,
               work_dir=work_dir)

    # Since we cannot run bash commands inside this tutorial
    # we are printing the actual bash command so you can see it
    # in the output
    print("The Example Command:\n", cmd)

    # call nibs
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(line)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    The Example Command:
     nibs -c WhiteMatter CSF --participant-label 001 -w /tmp/tmplj5rxow3/ds000164/derivatives/work -a /tmp/tmplj5rxow3/ds000164/derivatives/data/Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz -l /tmp/tmplj5rxow3/ds000164/derivatives/data/Schaefer2018_100Parcels_7Networks_order.tsv /tmp/tmplj5rxow3/ds000164 fmriprep /tmp/tmplj5rxow3/ds000164/derivatives participant

    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/grabbit/core.py:449: UserWarning: Domain with name 'bids' already exists; returning existing Domain configuration.\n"
    b'  warnings.warn(msg)\n'
    b'190703-16:05:55,61 nipype.workflow INFO:\n'
    b"\t Workflow nibetaseries_participant_wf settings: ['check', 'execution', 'logging', 'monitoring']\n"
    b'190703-16:05:55,72 nipype.workflow INFO:\n'
    b'\t Running in parallel.\n'
    b'190703-16:05:55,75 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 1 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:05:55,115 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "nibetaseries_participant_wf.single_subject001_wf.betaseries_wf.betaseries_node" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/betaseries_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/betaseries_node".\n'
    b'190703-16:05:55,120 nipype.workflow INFO:\n'
    b'\t [Node] Running "betaseries_node" ("nibetaseries.interfaces.nistats.BetaSeries")\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b'/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nibabel/nifti1.py:582: DeprecationWarning: The binary mode of fromstring is deprecated, as it behaves surprisingly on unicode inputs. Use frombuffer instead\n'
    b'  ext_def = np.fromstring(ext_def, dtype=np.int32)\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nistats/hemodynamic_models.py:268: DeprecationWarning: object of type <class 'numpy.float64'> cannot be safely interpreted as an integer.\n"
    b'  frame_times.max() * (1 + 1. / (n - 1)), n_hr)\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nistats/hemodynamic_models.py:55: DeprecationWarning: object of type <class 'float'> cannot be safely interpreted as an integer.\n"
    b'  time_stamps = np.linspace(0, time_length, float(time_length) / dt)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'190703-16:05:57,78 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 1 tasks, and 0 jobs ready. Free memory (GB): 10.26/10.46, Free processors: 3/4.\n'
    b'                     Currently running:\n'
    b'                       * nibetaseries_participant_wf.single_subject001_wf.betaseries_wf.betaseries_node\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 0 seconds\n'
    b'\n'
    b'Computing run 1 out of 1 runs (go take a coffee, a big one)\n'
    b'\n'
    b'Computation of 1 runs done in 1 seconds\n'
    b'\n'
    b'/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nipype/pipeline/engine/utils.py:307: DeprecationWarning: use "HasTraits.trait_set" instead\n'
    b'  result.outputs.set(**modify_paths(tosave, relative=True, basedir=cwd))\n'
    b'190703-16:07:45,776 nipype.workflow INFO:\n'
    b'\t [Node] Finished "nibetaseries_participant_wf.single_subject001_wf.betaseries_wf.betaseries_node".\n'
    b'190703-16:07:47,179 nipype.workflow INFO:\n'
    b'\t [Job 0] Completed (nibetaseries_participant_wf.single_subject001_wf.betaseries_wf.betaseries_node).\n'
    b'190703-16:07:47,185 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 1 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:07:49,182 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 3 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:07:49,251 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_atlas_corr_node0" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/atlas_corr_node/mapflow/_atlas_corr_node0".\n'
    b'190703-16:07:49,255 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_atlas_corr_node1" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/atlas_corr_node/mapflow/_atlas_corr_node1".\n'
    b'190703-16:07:49,255 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_atlas_corr_node2" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/atlas_corr_node/mapflow/_atlas_corr_node2".\n'
    b'190703-16:07:49,258 nipype.workflow INFO:\n'
    b'\t [Node] Running "_atlas_corr_node2" ("nibetaseries.interfaces.nilearn.AtlasConnectivity")\n'
    b'190703-16:07:49,258 nipype.workflow INFO:\n'
    b'\t [Node] Running "_atlas_corr_node1" ("nibetaseries.interfaces.nilearn.AtlasConnectivity")\n'
    b'190703-16:07:49,270 nipype.workflow INFO:\n'
    b'\t [Node] Running "_atlas_corr_node0" ("nibetaseries.interfaces.nilearn.AtlasConnectivity")\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b'190703-16:07:51,183 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 3 tasks, and 0 jobs ready. Free memory (GB): 9.86/10.46, Free processors: 1/4.\n'
    b'                     Currently running:\n'
    b'                       * _atlas_corr_node2\n'
    b'                       * _atlas_corr_node1\n'
    b'                       * _atlas_corr_node0\n'
    b'[NiftiLabelsMasker.fit_transform] loading data from /tmp/tmplj5rxow3/ds000164/derivatives/data/Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz\n'
    b'[NiftiLabelsMasker.fit_transform] loading data from /tmp/tmplj5rxow3/ds000164/derivatives/data/Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz\n'
    b'Resampling labels\n'
    b'[NiftiLabelsMasker.fit_transform] loading data from /tmp/tmplj5rxow3/ds000164/derivatives/data/Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz\n'
    b'Resampling labels\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Loading data from /tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/betaseries_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/betaseries_node/betaseries_trialtyp\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Loading data from /tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/betaseries_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/betaseries_node/betaseries_trialtyp\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Extracting region signals\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b'Resampling labels\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Loading data from /tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/betaseries_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/betaseries_node/betaseries_trialtyp\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Extracting region signals\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Extracting region signals\n'
    b"/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/importlib/_bootstrap.py:219: ImportWarning: can't resolve package from __spec__ or __package__, falling back on __name__ and __path__\n"
    b'  return f(*args, **kwds)\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Cleaning extracted signals\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Cleaning extracted signals\n'
    b'[NiftiLabelsMasker.transform_single_imgs] Cleaning extracted signals\n'
    b'/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nibetaseries/interfaces/nilearn.py:80: RuntimeWarning: invalid value encountered in greater\n'
    b'  n_lines = int(np.sum(connmat > 0) / 2)\n'
    b'/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nibetaseries/interfaces/nilearn.py:80: RuntimeWarning: invalid value encountered in greater\n'
    b'  n_lines = int(np.sum(connmat > 0) / 2)\n'
    b'/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nibetaseries/interfaces/nilearn.py:80: RuntimeWarning: invalid value encountered in greater\n'
    b'  n_lines = int(np.sum(connmat > 0) / 2)\n'
    b'/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nipype/pipeline/engine/utils.py:307: DeprecationWarning: use "HasTraits.trait_set" instead\n'
    b'  result.outputs.set(**modify_paths(tosave, relative=True, basedir=cwd))\n'
    b'190703-16:07:59,850 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_atlas_corr_node1".\n'
    b'/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nipype/pipeline/engine/utils.py:307: DeprecationWarning: use "HasTraits.trait_set" instead\n'
    b'  result.outputs.set(**modify_paths(tosave, relative=True, basedir=cwd))\n'
    b'190703-16:07:59,854 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_atlas_corr_node0".\n'
    b'/media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/nipype/pipeline/engine/utils.py:307: DeprecationWarning: use "HasTraits.trait_set" instead\n'
    b'  result.outputs.set(**modify_paths(tosave, relative=True, basedir=cwd))\n'
    b'190703-16:08:00,562 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_atlas_corr_node2".\n'
    b'190703-16:08:01,192 nipype.workflow INFO:\n'
    b'\t [Job 5] Completed (_atlas_corr_node0).\n'
    b'190703-16:08:01,193 nipype.workflow INFO:\n'
    b'\t [Job 6] Completed (_atlas_corr_node1).\n'
    b'190703-16:08:01,194 nipype.workflow INFO:\n'
    b'\t [Job 7] Completed (_atlas_corr_node2).\n'
    b'190703-16:08:01,198 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 1 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:08:01,242 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "nibetaseries_participant_wf.single_subject001_wf.correlation_wf.atlas_corr_node" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/atlas_corr_node".\n'
    b'190703-16:08:01,245 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_atlas_corr_node0" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/atlas_corr_node/mapflow/_atlas_corr_node0".\n'
    b'190703-16:08:01,246 nipype.workflow INFO:\n'
    b'\t [Node] Cached "_atlas_corr_node0" - collecting precomputed outputs\n'
    b'190703-16:08:01,246 nipype.workflow INFO:\n'
    b'\t [Node] "_atlas_corr_node0" found cached.\n'
    b'190703-16:08:01,247 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_atlas_corr_node1" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/atlas_corr_node/mapflow/_atlas_corr_node1".\n'
    b'190703-16:08:01,248 nipype.workflow INFO:\n'
    b'\t [Node] Cached "_atlas_corr_node1" - collecting precomputed outputs\n'
    b'190703-16:08:01,249 nipype.workflow INFO:\n'
    b'\t [Node] "_atlas_corr_node1" found cached.\n'
    b'190703-16:08:01,250 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_atlas_corr_node2" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/atlas_corr_node/mapflow/_atlas_corr_node2".\n'
    b'190703-16:08:01,251 nipype.workflow INFO:\n'
    b'\t [Node] Cached "_atlas_corr_node2" - collecting precomputed outputs\n'
    b'190703-16:08:01,251 nipype.workflow INFO:\n'
    b'\t [Node] "_atlas_corr_node2" found cached.\n'
    b'190703-16:08:01,254 nipype.workflow INFO:\n'
    b'\t [Node] Finished "nibetaseries_participant_wf.single_subject001_wf.correlation_wf.atlas_corr_node".\n'
    b'190703-16:08:03,193 nipype.workflow INFO:\n'
    b'\t [Job 1] Completed (nibetaseries_participant_wf.single_subject001_wf.correlation_wf.atlas_corr_node).\n'
    b'190703-16:08:03,199 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 2 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:08:05,204 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 6 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:08:05,264 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_fig0" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_fig/mapflow/_ds_correlation_fig0".\n'
    b'190703-16:08:05,266 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_fig1" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_fig/mapflow/_ds_correlation_fig1".\n'
    b'190703-16:08:05,267 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_fig0" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:05,268 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_fig2" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_fig/mapflow/_ds_correlation_fig2".\n'
    b'190703-16:08:05,270 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_fig1" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:05,272 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_fig2" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:05,272 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_rename_matrix_node0" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/rename_matrix_node/mapflow/_rename_matrix_node0".\n'
    b'190703-16:08:05,275 nipype.workflow INFO:\n'
    b'\t [Node] Running "_rename_matrix_node0" ("nipype.interfaces.utility.wrappers.Function")\n'
    b'190703-16:08:05,278 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_fig0".\n'
    b'190703-16:08:05,281 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_fig1".\n'
    b'190703-16:08:05,282 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_fig2".\n'
    b'190703-16:08:05,283 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_rename_matrix_node0".\n'
    b'190703-16:08:07,199 nipype.workflow INFO:\n'
    b'\t [Job 8] Completed (_ds_correlation_fig0).\n'
    b'190703-16:08:07,201 nipype.workflow INFO:\n'
    b'\t [Job 9] Completed (_ds_correlation_fig1).\n'
    b'190703-16:08:07,203 nipype.workflow INFO:\n'
    b'\t [Job 10] Completed (_ds_correlation_fig2).\n'
    b'190703-16:08:07,205 nipype.workflow INFO:\n'
    b'\t [Job 11] Completed (_rename_matrix_node0).\n'
    b'190703-16:08:07,211 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 3 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:08:07,259 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "nibetaseries_participant_wf.single_subject001_wf.ds_correlation_fig" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_fig".\n'
    b'190703-16:08:07,261 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_rename_matrix_node1" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/rename_matrix_node/mapflow/_rename_matrix_node1".\n'
    b'190703-16:08:07,263 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_rename_matrix_node2" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/rename_matrix_node/mapflow/_rename_matrix_node2".\n'
    b'190703-16:08:07,264 nipype.workflow INFO:\n'
    b'\t [Node] Running "_rename_matrix_node1" ("nipype.interfaces.utility.wrappers.Function")\n'
    b'190703-16:08:07,264 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_fig0" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_fig/mapflow/_ds_correlation_fig0".\n'
    b'190703-16:08:07,266 nipype.workflow INFO:\n'
    b'\t [Node] Running "_rename_matrix_node2" ("nipype.interfaces.utility.wrappers.Function")\n'
    b'190703-16:08:07,268 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_fig0" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:07,270 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_rename_matrix_node1".\n'
    b'190703-16:08:07,275 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_rename_matrix_node2".\n'
    b'190703-16:08:07,278 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_fig0".\n'
    b'190703-16:08:07,279 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_fig1" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_fig/mapflow/_ds_correlation_fig1".\n'
    b'190703-16:08:07,281 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_fig1" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:07,288 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_fig1".\n'
    b'190703-16:08:07,289 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_fig2" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_fig/mapflow/_ds_correlation_fig2".\n'
    b'190703-16:08:07,292 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_fig2" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:07,298 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_fig2".\n'
    b'190703-16:08:07,300 nipype.workflow INFO:\n'
    b'\t [Node] Finished "nibetaseries_participant_wf.single_subject001_wf.ds_correlation_fig".\n'
    b'190703-16:08:09,201 nipype.workflow INFO:\n'
    b'\t [Job 2] Completed (nibetaseries_participant_wf.single_subject001_wf.ds_correlation_fig).\n'
    b'190703-16:08:09,203 nipype.workflow INFO:\n'
    b'\t [Job 12] Completed (_rename_matrix_node1).\n'
    b'190703-16:08:09,205 nipype.workflow INFO:\n'
    b'\t [Job 13] Completed (_rename_matrix_node2).\n'
    b'190703-16:08:09,210 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 1 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:08:09,267 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "nibetaseries_participant_wf.single_subject001_wf.correlation_wf.rename_matrix_node" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/rename_matrix_node".\n'
    b'190703-16:08:09,271 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_rename_matrix_node0" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/rename_matrix_node/mapflow/_rename_matrix_node0".\n'
    b'190703-16:08:09,273 nipype.workflow INFO:\n'
    b'\t [Node] Cached "_rename_matrix_node0" - collecting precomputed outputs\n'
    b'190703-16:08:09,273 nipype.workflow INFO:\n'
    b'\t [Node] "_rename_matrix_node0" found cached.\n'
    b'190703-16:08:09,276 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_rename_matrix_node1" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/rename_matrix_node/mapflow/_rename_matrix_node1".\n'
    b'190703-16:08:09,278 nipype.workflow INFO:\n'
    b'\t [Node] Cached "_rename_matrix_node1" - collecting precomputed outputs\n'
    b'190703-16:08:09,278 nipype.workflow INFO:\n'
    b'\t [Node] "_rename_matrix_node1" found cached.\n'
    b'190703-16:08:09,280 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_rename_matrix_node2" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/correlation_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/rename_matrix_node/mapflow/_rename_matrix_node2".\n'
    b'190703-16:08:09,282 nipype.workflow INFO:\n'
    b'\t [Node] Cached "_rename_matrix_node2" - collecting precomputed outputs\n'
    b'190703-16:08:09,282 nipype.workflow INFO:\n'
    b'\t [Node] "_rename_matrix_node2" found cached.\n'
    b'190703-16:08:09,287 nipype.workflow INFO:\n'
    b'\t [Node] Finished "nibetaseries_participant_wf.single_subject001_wf.correlation_wf.rename_matrix_node".\n'
    b'190703-16:08:11,206 nipype.workflow INFO:\n'
    b'\t [Job 3] Completed (nibetaseries_participant_wf.single_subject001_wf.correlation_wf.rename_matrix_node).\n'
    b'190703-16:08:11,214 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 1 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:08:13,209 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 3 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:08:13,273 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_matrix0" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_matrix/mapflow/_ds_correlation_matrix0".\n'
    b'190703-16:08:13,275 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_matrix1" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_matrix/mapflow/_ds_correlation_matrix1".\n'
    b'190703-16:08:13,276 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_matrix0" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:13,278 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_matrix1" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:13,280 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_matrix2" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_matrix/mapflow/_ds_correlation_matrix2".\n'
    b'190703-16:08:13,284 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_matrix2" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:13,287 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_matrix1".\n'
    b'190703-16:08:13,288 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_matrix0".\n'
    b'190703-16:08:13,292 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_matrix2".\n'
    b'190703-16:08:15,207 nipype.workflow INFO:\n'
    b'\t [Job 14] Completed (_ds_correlation_matrix0).\n'
    b'190703-16:08:15,210 nipype.workflow INFO:\n'
    b'\t [Job 15] Completed (_ds_correlation_matrix1).\n'
    b'190703-16:08:15,211 nipype.workflow INFO:\n'
    b'\t [Job 16] Completed (_ds_correlation_matrix2).\n'
    b'190703-16:08:15,216 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 1 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'
    b'190703-16:08:15,272 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "nibetaseries_participant_wf.single_subject001_wf.ds_correlation_matrix" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_matrix".\n'
    b'190703-16:08:15,275 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_matrix0" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_matrix/mapflow/_ds_correlation_matrix0".\n'
    b'190703-16:08:15,279 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_matrix0" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:15,284 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_matrix0".\n'
    b'190703-16:08:15,285 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_matrix1" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_matrix/mapflow/_ds_correlation_matrix1".\n'
    b'190703-16:08:15,287 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_matrix1" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:15,292 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_matrix1".\n'
    b'190703-16:08:15,292 nipype.workflow INFO:\n'
    b'\t [Node] Setting-up "_ds_correlation_matrix2" in "/tmp/tmplj5rxow3/ds000164/derivatives/work/NiBetaSeries_work/nibetaseries_participant_wf/single_subject001_wf/c8ac4a2904204022161c2da4fe23a12e598eb170/ds_correlation_matrix/mapflow/_ds_correlation_matrix2".\n'
    b'190703-16:08:15,295 nipype.workflow INFO:\n'
    b'\t [Node] Running "_ds_correlation_matrix2" ("nibetaseries.interfaces.bids.DerivativesDataSink")\n'
    b'190703-16:08:15,299 nipype.workflow INFO:\n'
    b'\t [Node] Finished "_ds_correlation_matrix2".\n'
    b'190703-16:08:15,301 nipype.workflow INFO:\n'
    b'\t [Node] Finished "nibetaseries_participant_wf.single_subject001_wf.ds_correlation_matrix".\n'
    b'190703-16:08:17,210 nipype.workflow INFO:\n'
    b'\t [Job 4] Completed (nibetaseries_participant_wf.single_subject001_wf.ds_correlation_matrix).\n'
    b'190703-16:08:17,216 nipype.workflow INFO:\n'
    b'\t [MultiProc] Running 0 tasks, and 0 jobs ready. Free memory (GB): 10.46/10.46, Free processors: 4/4.\n'



Observe generated outputs
=========================


.. code-block:: default


    list_files(data_dir)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    tmplj5rxow3/
        ds000164/
            dataset_description.json
            task-stroop_bold.json
            README
            CHANGES
            T1w.json
            task-stroop_events.json
            derivatives/
                work/
                    NiBetaSeries_work/
                        nibetaseries_participant_wf/
                            d3.js
                            graph.json
                            index.html
                            graph1.json
                            single_subject001_wf/
                                correlation_wf/
                                    c8ac4a2904204022161c2da4fe23a12e598eb170/
                                        rename_matrix_node/
                                            _0xbb18dbbc19b4767abfa9ce29cc892aa2.json
                                            _node.pklz
                                            _inputs.pklz
                                            result_rename_matrix_node.pklz
                                            mapflow/
                                                _rename_matrix_node1/
                                                    result__rename_matrix_node1.pklz
                                                    _0x66a999f9349ac73e15e2e3d8cee2789e.json
                                                    _node.pklz
                                                    _inputs.pklz
                                                    correlation-matrix_trialtype-congruent.tsv
                                                    _report/
                                                        report.rst
                                                _rename_matrix_node0/
                                                    _0xfb91976740006eaa6a3590c5c8b2ae66.json
                                                    _node.pklz
                                                    result__rename_matrix_node0.pklz
                                                    correlation-matrix_trialtype-neutral.tsv
                                                    _inputs.pklz
                                                    _report/
                                                        report.rst
                                                _rename_matrix_node2/
                                                    _node.pklz
                                                    _0xd19260ea5d627e438edc236206987ec2.json
                                                    correlation-matrix_trialtype-incongruent.tsv
                                                    _inputs.pklz
                                                    result__rename_matrix_node2.pklz
                                                    _report/
                                                        report.rst
                                            _report/
                                                report.rst
                                        atlas_corr_node/
                                            result_atlas_corr_node.pklz
                                            _node.pklz
                                            _inputs.pklz
                                            _0xd615b0bfa3ea3056ef2521b30d034d98.json
                                            mapflow/
                                                _atlas_corr_node1/
                                                    _0x90ead4af678370cddd01b8c88ab068be.json
                                                    fisher_z_correlation.tsv
                                                    congruent.svg
                                                    _node.pklz
                                                    _inputs.pklz
                                                    result__atlas_corr_node1.pklz
                                                    _report/
                                                        report.rst
                                                _atlas_corr_node0/
                                                    fisher_z_correlation.tsv
                                                    _node.pklz
                                                    _inputs.pklz
                                                    neutral.svg
                                                    result__atlas_corr_node0.pklz
                                                    _0xf5301f2da4ac7b178cd169e869f08078.json
                                                    _report/
                                                        report.rst
                                                _atlas_corr_node2/
                                                    fisher_z_correlation.tsv
                                                    _node.pklz
                                                    result__atlas_corr_node2.pklz
                                                    _inputs.pklz
                                                    _0xf65db338fa08812be6dd87e8e0721835.json
                                                    incongruent.svg
                                                    _report/
                                                        report.rst
                                            _report/
                                                report.rst
                                c8ac4a2904204022161c2da4fe23a12e598eb170/
                                    ds_correlation_matrix/
                                        _node.pklz
                                        _inputs.pklz
                                        _0xf044e5652d2fb7864881a41dea3a196a.json
                                        result_ds_correlation_matrix.pklz
                                        mapflow/
                                            _ds_correlation_matrix1/
                                                _node.pklz
                                                result__ds_correlation_matrix1.pklz
                                                _inputs.pklz
                                                _0x12cc168f83350bf34fdb9f4afcc261ef.json
                                                _report/
                                                    report.rst
                                            _ds_correlation_matrix2/
                                                _node.pklz
                                                result__ds_correlation_matrix2.pklz
                                                _inputs.pklz
                                                _0xf5cc019c65642cca0e5653a74322b48e.json
                                                _report/
                                                    report.rst
                                            _ds_correlation_matrix0/
                                                _node.pklz
                                                _inputs.pklz
                                                _0x4913213bdeac3d0cd370f0535f4a4516.json
                                                result__ds_correlation_matrix0.pklz
                                                _report/
                                                    report.rst
                                        _report/
                                            report.rst
                                    ds_correlation_fig/
                                        _0xd75886f3c1b628ebde185814c9ee74a5.json
                                        _node.pklz
                                        result_ds_correlation_fig.pklz
                                        _inputs.pklz
                                        mapflow/
                                            _ds_correlation_fig1/
                                                _node.pklz
                                                _inputs.pklz
                                                result__ds_correlation_fig1.pklz
                                                _0xfd0ad2ccb301ac1e29b6cc57d958e8b8.json
                                                _report/
                                                    report.rst
                                            _ds_correlation_fig0/
                                                result__ds_correlation_fig0.pklz
                                                _0x12bebcb878d040e57277a752ef0db4e7.json
                                                _node.pklz
                                                _inputs.pklz
                                                _report/
                                                    report.rst
                                            _ds_correlation_fig2/
                                                _node.pklz
                                                _0xc7b5d88b57cad1447b73ee4e38525d60.json
                                                _inputs.pklz
                                                result__ds_correlation_fig2.pklz
                                                _report/
                                                    report.rst
                                        _report/
                                            report.rst
                                betaseries_wf/
                                    c8ac4a2904204022161c2da4fe23a12e598eb170/
                                        betaseries_node/
                                            betaseries_trialtype-congruent.nii.gz
                                            result_betaseries_node.pklz
                                            _node.pklz
                                            betaseries_trialtype-neutral.nii.gz
                                            _inputs.pklz
                                            _0x65702f21118795f03b3c0640dc7c9185.json
                                            betaseries_trialtype-incongruent.nii.gz
                                            _report/
                                                report.rst
                fmriprep/
                    sub-001/
                        func/
                            sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_brainmask.nii.gz
                            sub-001_task-stroop_bold_confounds.tsv
                            sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc.nii.gz
                data/
                    Schaefer2018_100Parcels_7Networks_order.txt
                    Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz
                    Schaefer2018_100Parcels_7Networks_order.tsv
                NiBetaSeries/
                    nibetaseries/
                        sub-001/
                            func/
                                sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc_trialtype-congruent_matrix.tsv
                                sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc_trialtype-neutral_matrix.tsv
                                sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc_trialtype-neutral_fig.svg
                                sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc_trialtype-incongruent_matrix.tsv
                                sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc_trialtype-congruent_fig.svg
                                sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc_trialtype-incongruent_fig.svg
                    logs/
            sub-001/
                func/
                    sub-001_task-stroop_bold.nii.gz
                    sub-001_task-stroop_events.tsv
                anat/
                    sub-001_T1w.nii.gz



Collect results
===============


.. code-block:: default


    corr_mat_path = os.path.join(out_dir, "NiBetaSeries", "nibetaseries", "sub-001", "func")
    trial_types = ['congruent', 'incongruent', 'neutral']
    filename_template = "sub-001_task-stroop_bold_space-MNI152NLin2009cAsym_preproc_trialtype-{trial_type}_matrix.tsv"
    pd_dict = {}
    for trial_type in trial_types:
        file_path = os.path.join(corr_mat_path, filename_template.format(trial_type=trial_type))
        pd_dict[trial_type] = pd.read_csv(file_path, sep='\t', na_values="n/a", index_col=0)
    # display example matrix
    print(pd_dict[trial_type].head())





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

              LH_Vis_1  LH_Vis_2  LH_Vis_3  LH_Vis_4  LH_Vis_5  ...  RH_Default_PFCm_1  RH_Default_PFCm_2  RH_Default_PFCm_3  RH_Default_PCC_1  RH_Default_PCC_2
    LH_Vis_1       NaN  0.092135 -0.003990  0.075498  0.314494  ...           0.303994           0.196831           0.343553          0.095624          0.016799
    LH_Vis_2  0.092135       NaN  0.216346 -0.088788  0.354525  ...           0.222549           0.032079           0.086436         -0.119613         -0.007679
    LH_Vis_3 -0.003990  0.216346       NaN  0.121108  0.024211  ...           0.506486           0.193366           0.207421          0.202673          0.177828
    LH_Vis_4  0.075498 -0.088788  0.121108       NaN  0.391487  ...           0.196155           0.378814           0.258830         -0.019256         -0.034034
    LH_Vis_5  0.314494  0.354525  0.024211  0.391487       NaN  ...           0.092790           0.252374           0.382709         -0.235334          0.032317

    [5 rows x 100 columns]



Graph the results
=================


.. code-block:: default


    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, sharey=True, figsize=(10, 30),
                             gridspec_kw={'wspace': 0.025, 'hspace': 0.075})

    cbar_ax = fig.add_axes([.91, .3, .03, .4])
    r = 0
    for trial_type, df in pd_dict.items():
        g = sns.heatmap(df, ax=axes[r], vmin=-.5, vmax=1., square=True,
                        cbar=True, cbar_ax=cbar_ax)
        axes[r].set_title(trial_type)
        # iterate over rows
        r += 1
    plt.tight_layout()




.. image:: /auto_examples/images/sphx_glr_plot_run_nibetaseries_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /media/Data/Documents/devel/NiBetaSeries/.tox/docs/lib/python3.6/site-packages/matplotlib/figure.py:2299: UserWarning: This figure includes Axes that are not compatible with tight_layout, so results might be incorrect.
      warnings.warn("This figure includes Axes that are not compatible "



References
==========
.. bibliography:: ../references.bib
   :style: plain
   :labelprefix: notebook-
   :keyprefix: n-



.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 2 minutes  32.276 seconds)


.. _sphx_glr_download_auto_examples_plot_run_nibetaseries.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_run_nibetaseries.py <plot_run_nibetaseries.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_run_nibetaseries.ipynb <plot_run_nibetaseries.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
