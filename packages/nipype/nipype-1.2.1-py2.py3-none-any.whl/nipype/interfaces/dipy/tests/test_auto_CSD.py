# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..reconstruction import CSD


def test_CSD_inputs():
    input_map = dict(
        b0_thres=dict(usedefault=True, ),
        in_bval=dict(
            extensions=None,
            mandatory=True,
        ),
        in_bvec=dict(
            extensions=None,
            mandatory=True,
        ),
        in_file=dict(
            extensions=None,
            mandatory=True,
        ),
        in_mask=dict(extensions=None, ),
        out_fods=dict(extensions=None, ),
        out_prefix=dict(),
        response=dict(extensions=None, ),
        save_fods=dict(usedefault=True, ),
        sh_order=dict(usedefault=True, ),
    )
    inputs = CSD.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_CSD_outputs():
    output_map = dict(
        model=dict(extensions=None, ),
        out_fods=dict(extensions=None, ),
    )
    outputs = CSD.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
