"""
Detect FHP
"""

import os
import click
from face_recognition import face_locations
from hunchback_detector import FHPDetection


@click.command()
@click.option('--show', is_flag=True, default=False, help="show the video")
@click.option('--setting', is_flag=True, default=False, help="set configure")
def main(show, setting):
    """
    start the detection of FHP
    """
    fhp_detector = FHPDetection(show=show,
                                face_detector=face_locations,
                                config_file="config.json")
    if not os.path.isfile("config.json") or setting:
        print("setting mode")
        fhp_detector.set_configure()
        fhp_detector.show = True
    fhp_detector.start_detection()


# pylint: disable=no-value-for-parameter
if __name__ == '__main__':
    main()
