# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..specialized import BinaryMaskEditorBasedOnLandmarks


def test_BinaryMaskEditorBasedOnLandmarks_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        inputBinaryVolume=dict(
            argstr='--inputBinaryVolume %s',
            extensions=None,
        ),
        inputLandmarkNames=dict(
            argstr='--inputLandmarkNames %s',
            sep=',',
        ),
        inputLandmarkNamesForObliquePlane=dict(
            argstr='--inputLandmarkNamesForObliquePlane %s',
            sep=',',
        ),
        inputLandmarksFilename=dict(
            argstr='--inputLandmarksFilename %s',
            extensions=None,
        ),
        outputBinaryVolume=dict(
            argstr='--outputBinaryVolume %s',
            hash_files=False,
        ),
        setCutDirectionForLandmark=dict(
            argstr='--setCutDirectionForLandmark %s',
            sep=',',
        ),
        setCutDirectionForObliquePlane=dict(
            argstr='--setCutDirectionForObliquePlane %s',
            sep=',',
        ),
    )
    inputs = BinaryMaskEditorBasedOnLandmarks.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_BinaryMaskEditorBasedOnLandmarks_outputs():
    output_map = dict(outputBinaryVolume=dict(extensions=None, ), )
    outputs = BinaryMaskEditorBasedOnLandmarks.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
