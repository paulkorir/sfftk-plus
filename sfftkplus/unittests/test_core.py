# -*- coding: utf-8 -*-
# test_py
"""
test_py

Unit tests for convert subcommand
"""

from __future__ import division

import os
import random
import shlex
import unittest

from __init__ import _random_integer, _random_float

from . import TEST_DATA_PATH
from ..core.parser import parse_args


__author__ = 'Paul K. Korir, PhD'
__email__ = 'pkorir@ebi.ac.uk, paul.korir@gmail.com'
__date__ = '2016-06-10'



# redirect sys.stderr/sys.stdout to /dev/null
# from: http://stackoverflow.com/questions/8522689/how-to-temporary-hide-stdout-or-stderr-while-running-a-unittest-in-python
# _stderr = sys.stderr
# _stdout = sys.stdout
# null = open(os.devnull, 'wb')
# sys.stderr = null
# sys.stdout = null


class TestParser_list(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roi_fn = os.path.join(TEST_DATA_PATH, 'roi', 'test_emd_1832.roi')
        cls.config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffp.conf')

    def test_default_images(self):
        """Test list image defaults"""
        args, _ = parse_args(shlex.split('list -I'))
        self.assertTrue(args.images)
        self.assertIsNone(args.image_id)
        self.assertIsNone(args.image_name)
        self.assertIsNone(args.config_path)
        self.assertIsNone(args.project)
        self.assertIsNone(args.dataset)
        self.assertFalse(args.summary)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.shipped_configs)
        self.assertFalse(args.verbose)

    def test_default_rois(self):
        """Test list rois defaults"""
        args, _ = parse_args(shlex.split('list -R'))
        self.assertTrue(args.rois)
        self.assertIsNone(args.image_id)
        self.assertIsNone(args.image_name)
        self.assertFalse(args.verbose)
        self.assertIsNone(args.project)
        self.assertIsNone(args.dataset)
        self.assertFalse(args.summary)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.shipped_configs)

    def test_image_id(self):
        """Test image ID"""
        image_id = _random_integer()
        args, _ = parse_args(shlex.split('list -R -i {}'.format(image_id)))
        self.assertEqual(args.image_id, image_id)

    def test_image_name(self):
        """Test image name"""
        image_name = 'image_name'
        args, _ = parse_args(shlex.split('list -R -n {}'.format(image_name)))
        self.assertEqual(args.image_name, image_name)

    def test_verbose(self):
        """Test verbose"""
        args, _ = parse_args(shlex.split('list -R -v'))
        self.assertTrue(args.verbose)

    def test_config_path(self):
        """Test config path"""
        args, _ = parse_args(shlex.split('list -I --config-path {}'.format(self.config_fn)))
        self.assertEqual(args.config_path, self.config_fn)

    def test_shipped_configs(self):
        """Test that we use shipped configs"""
        args, _ = parse_args(shlex.split('list -I --shipped-configs'))
        self.assertTrue(args.shipped_configs)

    def test_project(self):
        """Test project"""
        project = 'dlsjflsjdf'
        args, _ = parse_args(shlex.split('list -R -j {}'.format(project)))
        self.assertEqual(args.project, project)

    def test_dataset(self):
        """Test dataset"""
        dataset = 'sdlkflskdjf'
        args, _ = parse_args(shlex.split('list -R -d {}'.format(dataset)))
        self.assertEqual(args.dataset, dataset)

    def test_summary(self):
        """Test summary"""
        args, _ = parse_args(shlex.split('list -s'))
        self.assertTrue(args.summary)

    def test_omero_local(self):
        '''Test that --local uses local omero'''
        args, configs = parse_args(shlex.split('list -I --local'))
        self.assertEqual(configs['CONNECT_WITH'], 'LOCAL')

    def test_omero_remote(self):
        '''Test that uses remote omero'''
        args, configs = parse_args(shlex.split('list -I --remote'))
        self.assertEqual(configs['CONNECT_WITH'], 'REMOTE')


class TestParser_createroi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roi_fn = os.path.join(TEST_DATA_PATH, 'roi', 'test_emd_1832.roi')
        cls.config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffp.conf')

    def test_default(self):
        """Test default form"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi'))
        self.assertEqual(args.sff_file, 'file.sff')
        self.assertEqual(args.output, 'file.roi')
        self.assertIsNone(args.primary_descriptor)
        self.assertFalse(args.verbose)
        self.assertEqual(args.transparency, 0.5)
        self.assertIsNone(args.image_name_root)
        self.assertEqual(args.mask_value, 1)
        self.assertFalse(args.normals_off)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.shipped_configs)
        self.assertIsNone(args.quick_pick)
        self.assertFalse(args.reset_ids)

    def test_roi_file(self):
        """Test that we can start with an ROI file"""
        args, _ = parse_args(shlex.split('createroi file.roi -o new_file.roi -I emd_1234 --reset-ids'))
        self.assertEqual(args.sff_file, 'file.roi')
        self.assertEqual(args.output, 'new_file.roi')
        self.assertEqual(args.image_name_root, 'emd_1234')
        self.assertTrue(args.reset_ids)

    def test_roi_file_reset_ids_image_name_root_together(self):
        """Test that we ensure that if --reset-ids then --image-name-root must not be None"""
        with self.assertRaises(ValueError):
            parse_args(shlex.split('createroi file.roi --reset-ids -o new_file.roi'))

        # self.assertEqual(args.sff_file, 'file.roi')
        # self.assertTrue(args.reset_ids)
        # self.assertEqual(args.image_name_root, 'emd_1234')
        # self.assertEqual(args.output, 'new_file.roi')

    def test_primary_descriptor(self):
        """Test specifying primary descriptor"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -R threeDVolume'))
        self.assertEqual(args.primary_descriptor, 'threeDVolume')
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -R meshList'))
        self.assertEqual(args.primary_descriptor, 'meshList')
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -R contourList'))
        self.assertEqual(args.primary_descriptor, 'contourList')
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -R shapePrimitiveList'))
        self.assertEqual(args.primary_descriptor, 'shapePrimitiveList')

    def test_wrong_primary_descriptor(self):
        """Test wrong primary descriptor"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -R something'))
        self.assertIsNone(args)

    def test_verbose(self):
        """Test verbose"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -v'))
        self.assertTrue(args.verbose)

    def test_transparency(self):
        """Test specifying transparency"""
        transparency = _random_float()
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -t {}'.format(transparency)))
        self.assertEqual(round(args.transparency, 6), round(transparency, 6))

    def test_invalid_transparency(self):
        """Test invalid transparency"""
        transparency = _random_integer(start=2)
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -t {}'.format(transparency)))
        self.assertIsNone(args)

    def test_image_name_root(self):
        """Test image name root"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -I emd_1234'))
        self.assertEqual(args.image_name_root, 'emd_1234')

    def test_quick_pick(self):
        """Test that we have right value for quick pick"""
        quick_pick = _random_integer(start=1)
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi --quick-pick {}'.format(quick_pick)))
        self.assertEqual(args.quick_pick, quick_pick - 1)

    def test_invalid_quick_pick_value(self):
        """Test that a --quick-pick <= 0 terminates"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi --quick-pick 0'))
        self.assertIsNone(args)
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi --quick-pick -1'))
        self.assertIsNone(args)

    def test_mask_value(self):
        """Test specifying mask value"""
        mask_value = _random_integer()
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -m {}'.format(mask_value)))
        self.assertEqual(args.mask_value, mask_value)

    def test_normals_off(self):
        """Test normals off"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi -N'))
        self.assertTrue(args.normals_off)

    def test_config_path(self):
        """Test config path"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi --config-path {}'.format(self.config_fn)))
        self.assertEqual(args.config_path, self.config_fn)

    def test_shipped_configs(self):
        """Test that we use shipped configs"""
        args, _ = parse_args(shlex.split('createroi file.sff -o file.roi --shipped-configs'))
        self.assertTrue(args.shipped_configs)


class TestParser_attachroi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roi_fn = os.path.join(TEST_DATA_PATH, 'roi', 'test_emd_1832.roi')
        cls.config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffp.conf')

    def test_default(self):
        """Test default form"""
        args, _ = parse_args(shlex.split('attachroi file.roi'))
        self.assertEqual(args.roi_file, 'file.roi')
        self.assertIsNone(args.x_image_id)
        self.assertIsNone(args.y_image_id)
        self.assertIsNone(args.z_image_id)
        self.assertFalse(args.verbose)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.shipped_configs)

    def test_verbose(self):
        """Test verbose"""
        args, _ = parse_args(shlex.split('attachroi file.roi -v'))
        self.assertTrue(args.verbose)

    def test_config_path(self):
        """Test config path"""
        args, _ = parse_args(shlex.split('attachroi file.roi --config-path {}'.format(self.config_fn)))
        self.assertEqual(args.config_path, self.config_fn)

    def test_shipped_configs(self):
        """Test that we used shipped configs"""
        args, _ = parse_args(shlex.split('attachroi file.roi --shipped-configs'))
        self.assertTrue(args.shipped_configs)

    def test_omero_local(self):
        '''Test that --local uses local omero'''
        args, configs = parse_args(shlex.split('attachroi file.roi --local'))
        self.assertEqual(configs['CONNECT_WITH'], 'LOCAL')

    def test_omero_remote(self):
        '''Test that uses remote omero'''
        args, configs = parse_args(shlex.split('attachroi file.roi --remote'))
        self.assertEqual(configs['CONNECT_WITH'], 'REMOTE')


class TestParser_delroi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roi_fn = os.path.join(TEST_DATA_PATH, 'roi', 'test_emd_1832.roi')
        cls.config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffp.conf')

    def test_default(self):
        """Test default form"""
        roi_id = _random_integer()
        args, _ = parse_args(shlex.split('delroi -r {}'.format(roi_id)))
        self.assertEqual(args.roi_id, roi_id)
        self.assertIsNone(args.image_id)
        self.assertFalse(args.verbose)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.shipped_configs)

    def test_image_id(self):
        """Test specify image ID"""
        image_id = _random_integer()
        args, _ = parse_args(shlex.split('delroi -i {}'.format(image_id)))
        self.assertEqual(args.image_id, image_id)

    def test_verbose(self):
        """Test verbose"""
        args, _ = parse_args(shlex.split('delroi -r {} -v'.format(_random_integer())))
        self.assertTrue(args.verbose)

    def test_config_path(self):
        """Test config path"""
        args, _ = parse_args(shlex.split('delroi -i {} --config-path {}'.format(_random_integer(), self.config_fn)))
        self.assertEqual(args.config_path, self.config_fn)

    def test_shipped_configs(self):
        """Test that we use shipped configs"""
        args, _ = parse_args(shlex.split('delroi -i {} --shipped-configs'.format(_random_integer())))
        self.assertTrue(args.shipped_configs)

    def test_omero_local(self):
        '''Test that --local uses local omero'''
        args, configs = parse_args(shlex.split('delroi -i {} --local'.format(_random_integer())))
        self.assertEqual(configs['CONNECT_WITH'], 'LOCAL')

    def test_omero_remote(self):
        '''Test that uses remote omero'''
        args, configs = parse_args(shlex.split('delroi -i {} --remote'.format(_random_integer())))
        self.assertEqual(configs['CONNECT_WITH'], 'REMOTE')


class TestParser_view3d(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roi_fn = os.path.join(TEST_DATA_PATH, 'roi', 'test_emd_1832.roi')
        cls.config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffp.conf')

    def test_default(self):
        """Test default form"""
        args, _ = parse_args(shlex.split('view3d file.sff'))
        self.assertEqual(args.sff_file, 'file.sff')
        self.assertFalse(args.all_contours)
        self.assertFalse(args.keep_contours)
        self.assertFalse(args.full_screen)
        self.assertFalse(args.exclude_mesh)
        self.assertFalse(args.x_contours)
        self.assertFalse(args.y_contours)
        self.assertFalse(args.z_contours)
        self.assertFalse(args.no_orientation_axes)
        self.assertItemsEqual(args.background_colour, [0.1, 0.2, 0.4])
        self.assertIsNone(args.cube_axes)
        self.assertFalse(args.view_edges)
        self.assertFalse(args.fill_holes)
        self.assertFalse(args.normals_off)
        self.assertFalse(args.wireframe)
        self.assertIsNone(args.primary_descriptor)
        self.assertEqual(args.transparency, 0.5)
        self.assertFalse(args.verbose)
        self.assertEqual(args.mask_value, 1)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.shipped_configs)

    def test_view_all_contours(self):
        """Test specifying view all contours"""
        args, _ = parse_args(shlex.split('view3d file.sff -A'))
        self.assertTrue(args.all_contours)

    def test_keep_contour(self):
        """Test specifying keep contours"""
        args, _ = parse_args(shlex.split('view3d file.sff -C'))
        self.assertTrue(args.keep_contours)

    def test_full_screen(self):
        """Test specifying full screen"""
        args, _ = parse_args(shlex.split('view3d file.sff -F'))
        self.assertTrue(args.full_screen)
    def test_exclude_mesh(self):
        """Test specifying exclude mesh"""
        args, _ = parse_args(shlex.split('view3d file.sff -M'))
        self.assertTrue(args.exclude_mesh)

    def test_show_x_contours(self):
        """Test specifying show x contours"""
        args, _ = parse_args(shlex.split('view3d file.sff -X'))
        self.assertTrue(args.x_contours)

    def test_show_y_contours(self):
        """Test specifying show y contours"""
        args, _ = parse_args(shlex.split('view3d file.sff -Y'))
        self.assertTrue(args.y_contours)

    def test_show_z_contours(self):
        """Test specifying show z contours"""
        args, _ = parse_args(shlex.split('view3d file.sff -Z'))
        self.assertTrue(args.z_contours)

    def test_no_orientation_axes(self):
        """Test specifying no orientation axes"""
        args, _ = parse_args(shlex.split('view3d file.sff -a'))
        self.assertTrue(args.no_orientation_axes)

    def test_background_colour(self):
        """Test specifying background colour"""
        r, g, b = _random_float(), _random_float(), _random_float()
        args, _ = parse_args(shlex.split('view3d file.sff -B {} {} {}'.format(r, g, b)))
        self.assertItemsEqual(map(lambda c: round(c, 6), args.background_colour), map(lambda c: round(c, 6), [r, g, b]))

    def test_cube_axes(self):
        """Test specifying cube axes to display"""
        cube_axes = _random_integer(0, 4)
        args, _ = parse_args(shlex.split('view3d file.sff -c {}'.format(cube_axes)))
        self.assertEqual(args.cube_axes, cube_axes)

    def test_view_edges(self):
        """Test specifying to view edges"""
        args, _ = parse_args(shlex.split('view3d file.sff -e'))
        self.assertTrue(args.view_edges)

    def test_fill_holes(self):
        """Test specifying fill holes"""
        args, _ = parse_args(shlex.split('view3d file.sff -f'))
        self.assertTrue(args.fill_holes)

    def test_normals_off(self):
        """Test specifying normals off"""
        args, _ = parse_args(shlex.split('view3d file.sff -N'))
        self.assertTrue(args.normals_off)

    def test_wireframe(self):
        """Test specifying display as wireframe """
        args, _ = parse_args(shlex.split('view3d file.sff -w'))
        self.assertTrue(args.wireframe)

    def test_primaryDescriptor(self):
        """Test specifying primary descriptor"""
        primaryDescriptor = random.choice(['contourList', 'meshList', 'threeDVolume', 'shapePrimitiveList'])
        args, _ = parse_args(shlex.split('view3d file.sff -R {}'.format(primaryDescriptor)))
        self.assertEqual(args.primary_descriptor, primaryDescriptor)

    def test_transparency(self):
        """Test specifying transparency"""
        transparency = _random_float()
        args, _ = parse_args(shlex.split('view3d file.sff -t {}'.format(transparency)))
        self.assertEqual(round(args.transparency, 6), round(transparency, 6))

    def test_verbose(self):
        """Test specifying verbose"""
        args, _ = parse_args(shlex.split('view3d file.sff -v'))
        self.assertTrue(args.verbose)

    def test_mask_value(self):
        """Test specifying mask value"""
        mask_value = _random_integer()
        args, _ = parse_args(shlex.split('view3d file.sff -m {}'.format(mask_value)))
        self.assertEqual(args.mask_value, mask_value)

    def test_config_path(self):
        """Test that we can set a config path"""
        args, _ = parse_args(shlex.split('view3d file.sff --config-path {}'.format(self.config_fn)))
        self.assertEqual(args.config_path, self.config_fn)

    def test_shipped_configs(self):
        """Test that we can use shipped configs"""
        args, _ = parse_args(shlex.split('view3d file.sff --shipped-configs'))
        self.assertTrue(args.shipped_configs)


class TestParser_export(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.roi_fn = os.path.join(TEST_DATA_PATH, 'roi', 'test_emd_1832.roi')
        cls.config_fn = os.path.join(TEST_DATA_PATH, 'configs', 'sffp.conf')

    def test_default(self):
        """Test default form"""
        args, _ = parse_args(shlex.split('export file.sff'))
        self.assertEqual(args.sff_file, 'file.sff')
        self.assertIsNone(args.primary_descriptor)
        self.assertFalse(args.normals_off)
        self.assertEqual(args.mask_value, 1)
        self.assertFalse(args.verbose)
        self.assertIsNone(args.config_path)
        self.assertFalse(args.shipped_configs)

    def test_primaryDescriptor(self):
        """Test specifying primary descriptor"""
        primaryDescriptor = random.choice(['contourList', 'meshList', 'threeDVolume', 'shapePrimitiveList'])
        args, _ = parse_args(shlex.split('export file.sff -R {}'.format(primaryDescriptor)))
        self.assertEqual(args.primary_descriptor, primaryDescriptor)

    def test_normals_off(self):
        """Test specifying normals off"""
        args, _ = parse_args(shlex.split('export file.sff -N'))
        self.assertTrue(args.normals_off)

    def test_mask_value(self):
        """Test specifying mask value"""
        mask_value = _random_integer()
        args, _ = parse_args(shlex.split('export file.sff -m {}'.format(mask_value)))
        self.assertEqual(args.mask_value, mask_value)

    def test_verbose(self):
        """Test specifying verbose"""
        args, _ = parse_args(shlex.split('export file.sff -v'))
        self.assertTrue(args.verbose)

    def test_config_path(self):
        """Test that we can set a config path"""
        args, _ = parse_args(shlex.split('export file.sff --config-path {}'.format(self.config_fn)))
        self.assertEqual(args.config_path, self.config_fn)

    def test_shipped_configs(self):
        """Test that we can use shipped configs"""
        args, _ = parse_args(shlex.split('export file.sff --shipped-configs'))
        self.assertTrue(args.shipped_configs)
