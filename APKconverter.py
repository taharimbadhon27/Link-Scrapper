import os
import zipfile
import shutil

def convert_apks(input_path, output_path):
    temp_dir = "temp_apks"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Extract the APKS file
        with zipfile.ZipFile(input_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find base APK and splits
        base_apk = None
        split_apks = []
        
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.apk'):
                    full_path = os.path.join(root, file)
                    if "base.apk" in file or "split_config" not in file:
                        base_apk = full_path
                    else:
                        split_apks.append(full_path)

        if not base_apk:
            print(f"Error: No base APK found in {input_path}")
            return False

        # Merge all splits into base APK
        with zipfile.ZipFile(base_apk, 'a') as base_zip:
            for split_apk in split_apks:
                with zipfile.ZipFile(split_apk, 'r') as split_zip:
                    for file in split_zip.namelist():
                        if file not in base_zip.namelist():
                            base_zip.writestr(file, split_zip.read(file))

        # Move to output
        shutil.move(base_apk, output_path)
        return True

    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")
        return False
    finally:
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def batch_convert(input_dir):
    input_dir = input_dir.rstrip('/')
    converted = 0
    failed = 0

    for filename in os.listdir(input_dir):
        if filename.endswith('.apks'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(input_dir, filename.replace('.apks', '.apk'))
            
            print(f"Processing {filename}...")
            if convert_apks(input_path, output_path):
                converted += 1
                print(f"✅ Converted to {os.path.basename(output_path)}")
            else:
                failed += 1

    print(f"\nConversion complete! Success: {converted}, Failed: {failed}")

if __name__ == "__main__":
    apks_dir = "/storage/emulated/0/MT2/apks"
    if not os.path.exists(apks_dir):
        print(f"Error: Directory not found - {apks_dir}")
        print("Did you grant Termux storage permissions? Run: termux-setup-storage")
    else:
        batch_convert(apks_dir)