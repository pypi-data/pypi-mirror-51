# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..io import JSONFileGrabber


def test_JSONFileGrabber_inputs():
    input_map = dict(
        defaults=dict(),
        in_file=dict(extensions=None, ),
    )
    inputs = JSONFileGrabber.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_JSONFileGrabber_outputs():
    output_map = dict()
    outputs = JSONFileGrabber.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
