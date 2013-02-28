import os
import shutil
import datetime
import tempfile
import unittest

import baggins


class TestBaggins(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        shutil.copytree('test-data', self.tmpdir)

    def tearDown(self):
        if os.path.isdir(self.tmpdir):
            shutil.rmtree(self.tmpdir)

    def test_find_new_items(self):
        target_dir = os.path.join(self.tmpdir, 'new_items')
        new_items = baggins.find_new_items(target_dir)

        # The script should have spotted all three item directories
        self.assertTrue('item1' in new_items)
        self.assertTrue('item2' in new_items)
        self.assertTrue('item3' in new_items)

        # The script should ignore the non-directory files
        self.assertTrue('ignore_file' not in new_items)

    def test_find_metadata(self):
        matches = [('item1', 'item1.xml'),
            ('item2', 'item2-dc.xml'),
            ('item3', 'item3_MRC.xml')]
        metadata_dir = os.path.join(self.tmpdir, 'metadata')

        # The script should locate the appropriate metadata file for each item
        # The test directory also contains bogus files to test against such as
        # 'item10.xml'
        for pair in matches:
            meta_path = baggins.find_metadata(pair[0], metadata_dir)
            meta_name = os.path.split(meta_path)[1]
            self.assertTrue(meta_name == pair[1])

    def test_build_foundation(self):
        item_path = os.path.join(self.tmpdir, 'new_items', 'item1')
        meta_path = os.path.join(self.tmpdir, 'metadata', 'item1.xml')
        bag_folders = [
            {'name': 'IMAGES',
             'file_types': ['jpg', 'jpeg', 'jp2', 'png', 'tiff', 'tif']},
            {'name': 'METADATA',
             'file_types': ['xml', 'mrc']},
            {'name': 'PDF',
             'file_types': ['pdf']}
        ]
        baggins.build_foundation(item_path, meta_path, bag_folders)

        # Script should have built METADATA dir
        meta_dir_path = os.path.join(item_path, 'METADATA')
        self.assertTrue(os.path.exists(meta_dir_path))
        self.assertTrue(os.path.isdir(meta_dir_path))
        # Script should have also copied the metadata file
        new_meta_path = os.path.join(meta_dir_path, 'item1.xml')
        self.assertTrue(os.path.exists(new_meta_path))
        # Make sure old copy still exists as well
        self.assertTrue(os.path.exists(meta_path))

        # Script should have built the IMAGES dir
        images_dir_path = os.path.join(item_path, 'IMAGES')
        self.assertTrue(os.path.exists(images_dir_path))
        self.assertTrue(os.path.isdir(images_dir_path))
        # Script should also have moved the image files
        image_files = ['item1_img1.jpg', 'item1_img1.tif', 'item1_img2.jpg',
            'item1_img2.tif']
        for image_file in image_files:
            new_image_path = os.path.join(images_dir_path, image_file)
            self.assertTrue(os.path.exists(new_image_path))
            # Make sure the old copies are gone
            old_image_path = os.path.join(item_path, image_file)
            self.assertFalse(os.path.exists(old_image_path))

    def test_main(self):
        target = os.path.join(self.tmpdir, 'new_items')
        export_dir = os.path.join(self.tmpdir, 'export')
        meta_dir = os.path.join(self.tmpdir, 'metadata')
        contact = 'Joshua Gomez'
        bag_folders = [
            {'name': 'IMAGES',
             'file_types': ['jpg', 'jpeg', 'jp2', 'png', 'tiff', 'tif']},
            {'name': 'METADATA',
             'file_types': ['xml', 'mrc']},
            {'name': 'PDF',
             'file_types': ['pdf']}
        ]

        # Script should run and produce bags in export directory
        baggins.main(export_dir, contact, bag_folders, meta_dir, target)
        for bag_name in ['item1', 'item2', 'item3']:
            bag_path = os.path.join(export_dir,bag_name)
            self.assertTrue(os.path.exists(bag_path))
            self.assertTrue(os.path.isdir(bag_path))


if __name__ == '__main__':
    unittest.main()