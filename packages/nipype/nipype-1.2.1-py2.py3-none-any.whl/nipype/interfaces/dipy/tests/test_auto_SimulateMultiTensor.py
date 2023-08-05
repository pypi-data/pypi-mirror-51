# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..simulate import SimulateMultiTensor


def test_SimulateMultiTensor_inputs():
    input_map = dict(
        baseline=dict(
            extensions=None,
            mandatory=True,
        ),
        bvalues=dict(usedefault=True, ),
        diff_iso=dict(usedefault=True, ),
        diff_sf=dict(usedefault=True, ),
        gradients=dict(extensions=None, ),
        in_bval=dict(extensions=None, ),
        in_bvec=dict(extensions=None, ),
        in_dirs=dict(mandatory=True, ),
        in_frac=dict(mandatory=True, ),
        in_mask=dict(extensions=None, ),
        in_vfms=dict(mandatory=True, ),
        n_proc=dict(usedefault=True, ),
        num_dirs=dict(usedefault=True, ),
        out_bval=dict(
            extensions=None,
            usedefault=True,
        ),
        out_bvec=dict(
            extensions=None,
            usedefault=True,
        ),
        out_file=dict(
            extensions=None,
            usedefault=True,
        ),
        out_mask=dict(
            extensions=None,
            usedefault=True,
        ),
        snr=dict(usedefault=True, ),
    )
    inputs = SimulateMultiTensor.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_SimulateMultiTensor_outputs():
    output_map = dict(
        out_bval=dict(extensions=None, ),
        out_bvec=dict(extensions=None, ),
        out_file=dict(extensions=None, ),
        out_mask=dict(extensions=None, ),
    )
    outputs = SimulateMultiTensor.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
