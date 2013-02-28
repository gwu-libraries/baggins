from os import listdir, mkdir, path
from shutil import copy, move

import bagit

import settings


def find_new_items(target=settings.READY_ITEMS_DIR):
    return [i for i in listdir(target) if path.isdir(path.join(target, i))]


def find_metadata(fname, meta_dir=settings.METADATA_DIR):
    meta_fname = fname.split('.')[0]
    for metafile in sorted(listdir(meta_dir)):
        if metafile.startswith(meta_fname):
            return path.join(meta_dir, metafile)


def build_foundation(item_path, meta_path, bag_folders=settings.BAG_FOLDERS):
    # create directories
    for folder in bag_folders:
        mkdir(path.join(item_path, folder['name']))
        # move appropriate file types to directories
        for fname in listdir(item_path):
            for ext in folder['file_types']:
                if fname.endswith(ext):
                    move(path.join(item_path, fname),
                        path.join(item_path, folder['name'], fname))
    # copy metadata files
    copy(meta_path, path.join(item_path, 'METADATA'))


def main(export_dir=settings.EXPORT_DIR, contact=settings.CONTACT_NAME,
    bag_folders=settings.BAG_FOLDERS, meta_dir=settings.METADATA_DIR,
    target=settings.READY_ITEMS_DIR):
    # Read the READY ITEMS DIRECTORY and look for new items to bag
    items = find_new_items(target)
    for item in items:
        item_path = path.join(target, item)
        fname = path.split(item_path)[1]
        # For each new item, locate its corresponding metadata
        meta_path = find_metadata(fname, meta_dir)
        # Construct the bag's directory structure (move files)
        build_foundation(item_path, meta_path, bag_folders)
        # Create the bag using bagit
        bag = bagit.make_bag(item_path,
            {'Contact-Name': contact})
        # request new ID for the item from the ID service
        # TODO
        # Notify the Inventory system about the new bag
        # TODO
        # Move the bag to the export dock
        move(item_path, export_dir)


if __name__ == "main":
    main()