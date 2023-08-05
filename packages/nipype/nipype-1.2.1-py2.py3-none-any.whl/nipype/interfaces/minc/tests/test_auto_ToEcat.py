# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..minc import ToEcat


def test_ToEcat_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        ignore_acquisition_variable=dict(
            argstr='-ignore_acquisition_variable', ),
        ignore_ecat_acquisition_variable=dict(
            argstr='-ignore_ecat_acquisition_variable', ),
        ignore_ecat_main=dict(argstr='-ignore_ecat_main', ),
        ignore_ecat_subheader_variable=dict(
            argstr='-ignore_ecat_subheader_variable', ),
        ignore_patient_variable=dict(argstr='-ignore_patient_variable', ),
        ignore_study_variable=dict(argstr='-ignore_study_variable', ),
        input_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=-2,
        ),
        no_decay_corr_fctr=dict(argstr='-no_decay_corr_fctr', ),
        output_file=dict(
            argstr='%s',
            extensions=None,
            genfile=True,
            hash_files=False,
            keep_extension=False,
            name_source=['input_file'],
            name_template='%s_to_ecat.v',
            position=-1,
        ),
        voxels_as_integers=dict(argstr='-label', ),
    )
    inputs = ToEcat.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_ToEcat_outputs():
    output_map = dict(output_file=dict(extensions=None, ), )
    outputs = ToEcat.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
