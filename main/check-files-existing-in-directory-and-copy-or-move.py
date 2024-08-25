import os
import shutil

# Function to check if an image exists in the directory or as a full path


def check_image_existence(directory, image, recursive=False):
    if os.path.isabs(image):
        return image if os.path.exists(image) else False
    else:
        if recursive:
            for root, _, files in os.walk(directory):
                if image in files:
                    return os.path.join(root, image)
            return False
        else:
            return os.path.join(directory, image) if os.path.exists(os.path.join(directory, image)) else False


def configure_paths():
    global txt_file, image_directory, copy_directory, move_directory, recursive

    print("\n 🍯 · YAXŞI OĞLAN, BALOĞLAN  · 🧔")
    txt_file = input(
        "📒• Axtarılmalı fayl adlarının olduğu siyahı yerini daxil et (defolt:  " + txt_file + "): ") or txt_file
    image_directory = input(
        "🖼️ · Şəkillərin yerləşdiyi əsas yoxlanılmalı qovluq (default: " + image_directory + "): ") or image_directory
    copy_directory = input("📑· Kopyası hara saxlanılsın  " +
                           copy_directory + "): ") or copy_directory
    move_directory = input(
        "✂️· Koçürüləcəyi yer qeyd et (default: " + move_directory + "): ") or move_directory
    recursive_input = input(
        "Dibinə kimi soxub 'recursive'  barmaqlayımmı? (true/false, defolt:" + str(recursive) + "): ")
    recursive = recursive_input.lower() == 'true' if recursive_input else recursive
    print("\📝·Yadda saxladım, cubbulum.")


def display_counts(successful_count, unsuccessful_count):
    total_images = successful_count + unsuccessful_count
    print(
        f"\n✅◽{successful_count}\n❌◽{unsuccessful_count}\n\n📦TOPLAM FAYL SAYI📦\n {total_images}")


def process_images(option):
    global txt_file, image_directory, copy_directory, move_directory, recursive

    with open(txt_file, 'r') as file:
        image_list = file.read().splitlines()

    if option == "1":
        found_images = []
        missing_images = []
        empty_images = []

        for image in image_list:
            image_path = check_image_existence(
                image_directory, image, recursive)
            if image_path:
                if os.path.getsize(image_path) > 0:
                    found_images.append(image_path)
                    print(f'\033[92m✅•{image}\033[0m')  # Print in green
                else:
                    empty_images.append(image_path)
                    print(f'\033[93mEmpty: {image}\033[0m')  # Print in yellow
            else:
                missing_images.append(image)
                print(f'\033[91m❌•{image}\033[0m')  # Print in red

        with open('../.missing_images.txt', 'w') as file:
            for image in missing_images + empty_images:
                file.write(image + '\n')

        display_counts(len(found_images), len(
            missing_images) + len(empty_images))

    elif option == "2":
        successful_copies = []
        unsuccessful_copies = []

        for image in image_list:
            source_path = check_image_existence(
                image_directory, image, recursive)
            if source_path and os.path.getsize(source_path) > 0:
                target_path = os.path.join(
                    copy_directory, os.path.basename(source_path))
                try:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy(source_path, target_path)
                    successful_copies.append(image)
                    # Print in green
                    print(f'\033[92mℹ️ Copied: {image}\033[0m')
                except Exception as e:
                    unsuccessful_copies.append(image)
                    # Print in red
                    print(f'\033[91m🚫 Copy: {image} - {e}\033[0m')
            else:
                unsuccessful_copies.append(image)
                print(f'\033[91m🚫 Copy: {image} (Not Found or Empty)\033[0m')

        with open('../unsuccessful_copies.txt', 'w') as file:
            for image in unsuccessful_copies:
                file.write(image + '\n')

        display_counts(len(successful_copies), len(unsuccessful_copies))

    elif option == "3":
        # Move files to directory
        successful_moves = []
        unsuccessful_moves = []

        for image in image_list:
            source_path = check_image_existence(
                image_directory, image, recursive)
            if source_path and os.path.getsize(source_path) > 0:
                target_path = os.path.join(
                    move_directory, os.path.basename(source_path))
                try:
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.move(source_path, target_path)
                    successful_moves.append(image)
                    # Print in green
                    print(f'\033[92mℹ️ • Moved: {image}\033[0m')
                except Exception as e:
                    unsuccessful_moves.append(image)
                    # Print in red
                    print(f'\033[91m🚫 Move: {image} - {e}\033[0m')
            else:
                unsuccessful_moves.append(image)
                print(f'\033[91m🚫 Move: {image} (Not Found or Empty)\033[0m')

        with open('../unsuccessful_moves.txt', 'w') as file:
            for image in unsuccessful_moves:
                file.write(image + '\n')

        display_counts(len(successful_moves), len(unsuccessful_moves))


# Default paths
txt_file = "../src/input-example.txt"
image_directory = "../src/input-imgs/"
copy_directory = "../out/"
move_directory = "../out/"
recursive = True

try:
    with open('../.config/last_config.txt', 'r') as file:
        lines = file.read().splitlines()
        txt_file = lines[0]
        image_directory = lines[1]
        copy_directory = lines[2]
        move_directory = lines[3]
        recursive = lines[4].lower() == 'true' if len(lines) > 4 else False
except FileNotFoundError:
    pass

while True:
    print("\n📁 — FAYLIN MOVCULUĞUNU ÖYRƏN/AXTAR/KOPYALA/KÖCUR!\n(bir sözlə hoqqa veriyorşın)")
    print("1️⃣•🔎 MÖVCUDLUĞUNU YOXLA")
    print("2️⃣·📑 KOPYALAM")
    print("3️⃣·📋 KÖÇÜRMƏK")
    print("4️⃣·📃 KONFIQURASIYA")
    print("5️⃣·🚷 ÇIXIŞ")

    option = input("◽Seç görüm: (1-5) 🤔")

    if option in ["1", "2", "3"]:
        process_images(option)

    elif option == "4":
        # Configuration to set default paths
        configure_paths()
        with open('../.config/last_config.txt', 'w') as file:
            file.write(
                f"{txt_file}\n{image_directory}\n{copy_directory}\n{move_directory}\n{str(recursive).lower()}")

    elif option == "5":
        # Exit the script
        break

    else:
        print("⚠️ · DÜZGÜNLÜYƏ FİTVA VERDƏ, ALA! 🤪📿")
