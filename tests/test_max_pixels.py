# -*- coding: utf-8 -*-
"""
Test image max-pixel parameters.
"""
from tests.pyxform_test_case import PyxformTestCase


class MaxPixelsTest(PyxformTestCase):
    """
    Test image max-pixel parameters.
    """

    def test_integer_max_pixels(self):
        self.assertPyxformXform(
            name="data",
            md="""
            | survey |        |          |       |                |
            |        | type   | name     | label | parameters     |
            |        | image  | my_image | Image | max-pixels=640 |
            """,
            xml__contains=[
                'xmlns:orx="http://openrosa.org/xforms"',
                '<bind nodeset="/data/my_image" type="binary" orx:max-pixels="640"/>',
            ],
        )

    def test_string_max_pixels(self):
        self.assertPyxformXform(
            name="data",
            errored=True,
            md="""
            | survey |        |          |       |                |
            |        | type   | name     | label | parameters     |
            |        | image  | my_image | Image | max-pixels=foo |
            """,
            error__contains=["Parameter max-pixels must have an integer value."],
        )

    def test_string_extra_params(self):
        self.assertPyxformXform(
            name="data",
            errored=True,
            md="""
            | survey |        |          |       |                        |
            |        | type   | name     | label | parameters             |
            |        | image  | my_image | Image | max-pixels=640 foo=bar |
            """,
            error__contains=[
                "Accepted parameters are 'max-pixels': 'foo' is an invalid parameter."
            ],
        )

    def test_image_with_no_max_pixels_should_warn(self):
        warnings = []

        self.md_to_pyxform_survey(
            """
            | survey |       |            |         |
            |        | type  | name       | label   |
            |        | image | my_image   | Image   |
            |        | image | my_image_1 | Image 1 |
            """,
            warnings=warnings,
        )

        self.assertTrue(len(warnings) == 2)
        self.assertTrue("max-pixels" in warnings[0] and "max-pixels" in warnings[1])
