import configparser
import os
import shutil

PROMPT_INI_FILE = "prompts.ini"
OUTPUT_KEY = "output"
OUTPUT_FOLDER = "output"
FILE_KEY = "files"
MODIFY_SECTION = "Modify"
MODIFY_SUFFIX = "_modify"

OUTPUT_PREFIX_FILE = "outputPrefix.txt"

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(current_dir, PROMPT_INI_FILE))
    # clean output directory out
    output_folder_path = os.path.join(current_dir, OUTPUT_FOLDER)
    try:
        shutil.rmtree(output_folder_path)
    except FileNotFoundError as _:
        pass
    os.mkdir(output_folder_path)
    modify_text = ""
    with open(os.path.join(current_dir, config.get(MODIFY_SECTION, FILE_KEY)), "r") as f:
        modify_text = f.read()

    
    for section in config.sections():
        if config.has_option(section, FILE_KEY) and config.has_option(section, OUTPUT_KEY):
            prompt_list = []
            for file_name in config.get(section, FILE_KEY).split(","):
                with open(
                    os.path.join(
                        current_dir,
                        file_name,
                    ),
                    "r",
                ) as f:
                    prompt_list.append(f.read())
            output_file_name = config.get(section, OUTPUT_KEY)
            with open(os.path.join(output_folder_path, output_file_name), "w") as f:
                f.write("\n\n".join(prompt_list))
            ext_index = config.get(section, OUTPUT_KEY).find(".txt")
            modify_file_name = output_file_name[:ext_index] + MODIFY_SUFFIX + output_file_name[ext_index:]
            with open(os.path.join(output_folder_path, modify_file_name), "w") as f:
                f.write("\n\n".join([modify_text] + prompt_list))
    

if __name__ == "__main__":
    main()