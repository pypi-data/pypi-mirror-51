# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..preprocess import Automask


def test_Automask_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        brain_file=dict(
            argstr='-apply_prefix %s',
            extensions=None,
            name_source='in_file',
            name_template='%s_masked',
        ),
        clfrac=dict(argstr='-clfrac %s', ),
        dilate=dict(argstr='-dilate %s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        erode=dict(argstr='-erode %s', ),
        in_file=dict(
            argstr='%s',
            copyfile=False,
            extensions=None,
            mandatory=True,
            position=-1,
        ),
        num_threads=dict(
            nohash=True,
            usedefault=True,
        ),
        out_file=dict(
            argstr='-prefix %s',
            extensions=None,
            name_source='in_file',
            name_template='%s_mask',
        ),
        outputtype=dict(),
    )
    inputs = Automask.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_Automask_outputs():
    output_map = dict(
        brain_file=dict(extensions=None, ),
        out_file=dict(extensions=None, ),
    )
    outputs = Automask.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
