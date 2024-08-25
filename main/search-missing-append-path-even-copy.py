import os
import shutil

# Function to recursively search for images from a txt file in specified directories


def search_and_process_images():
    with open(txt_file, 'r') as file:
        image_list = file.read().splitlines()

    missing_images = []
    found_images = []

    for root, dirs, files in os.walk(start_dir, topdown=True):
        # Exclude certain directories
        dirs[:] = [d for d in dirs if os.path.join(
            root, d) not in exclude_dirs]

        for image in image_list:
            full_paths = [os.path.join(root, image) for root, dirs, files in os.walk(
                root) for image in files]

            found = False
            for path in full_paths:
                if os.path.isfile(path):
                    if os.path.getsize(path) > 0:  # Check if the file is not empty
                        found_images.append(path)
                        # Print in green
                        print(f'\033[92mFound: {path}\033[0m')
                    else:
                        # Print in yellow
                        print(
                            f'\033[93mZero-byte file (deleted): {path}\033[0m')
                        os.remove(path)  # Remove zero-byte file
                    found = True
                    break

            if not found:
                missing_images.append(image)
                print(f'\033[91mMissing: {image}\033[0m')  # Print in red

    with open('../.missing_images.txt', 'w') as file:
        for image in missing_images:
            file.write(image + '\n')

    display_counts(len(found_images), len(missing_images))

    if found_images:
        should_copy = input(
            "Do you want to copy found files to the default output path? (y/n): ").lower()
        if should_copy == 'y':
            copy_images(found_images)

        # Update input file by removing found images
        with open(txt_file, 'w') as file:
            for image in missing_images:
                file.write(image + '\n')

        print("\nUpdated the input file by removing found images.")


# Function to copy images to the default output directory
def copy_images(image_paths):
    for image in image_paths:
        target_path = os.path.join(copy_directory, os.path.basename(image))
        try:
            shutil.copy(image, target_path)
            # Print in green
            print(f'\033[92mCopied: {image} to {target_path}\033[0m')
        except Exception as e:
            # Print in red
            print(f'\033[91mFailed to Copy: {image} - {e}\033[0m')


# Function to display counts of successful and unsuccessful operations
def display_counts(successful_count, unsuccessful_count):
    total_images = successful_count + unsuccessful_count
    print(
        f"\nSuccessful: {successful_count}, Unsuccessful: {unsuccessful_count}. Total Images: {total_images}")


# Default paths
txt_file = "../src/input-example.txt"
start_dir = "/sdcard/"
exclude_dirs = ["/sdcard/Android/",
                "/sdcard/Android/data/com.luckydroid.droidba."]
copy_directory = "../result/copied-imgs"

# Main script execution
search_and_process_images()
