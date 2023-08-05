# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..utils import TalairachQC


def test_TalairachQC_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        log_file=dict(
            argstr='%s',
            extensions=None,
            mandatory=True,
            position=0,
        ),
        subjects_dir=dict(),
    )
    inputs = TalairachQC.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_TalairachQC_outputs():
    output_map = dict(
        log_file=dict(
            extensions=None,
            usedefault=True,
        ), )
    outputs = TalairachQC.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
