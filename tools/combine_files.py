import os
from collections import OrderedDict

input_files = [
    os.path.join("src", "api.py"),
]

output_file = os.path.join("tools", "temp_combined.py")


def extract_imports_and_content(file_path):
    imports = []
    content = []
    in_import_block = True

    try:
        with open(file_path, "r", encoding="utf-8") as infile:
            for line in infile:
                stripped_line = line.strip()
                if in_import_block and (
                    stripped_line.startswith("import ")
                    or stripped_line.startswith("from ")
                ):
                    imports.append(line.rstrip())
                else:
                    in_import_block = False
                    content.append(line.rstrip())
        return imports, content
    except Exception as e:
        print(f"Error reading '{file_path}': {str(e)}")
        return [], []


def combine_files(input_files, output_file):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Script running from: {script_dir}")

        all_imports = OrderedDict()
        all_contents = []

        for file_path in input_files:
            absolute_path = os.path.abspath(file_path)
            print(f"Checking file: {absolute_path}")

            if not os.path.exists(absolute_path):
                print(f"Warning: File '{absolute_path}' not found. Skipping.")
                continue

            imports, content = extract_imports_and_content(absolute_path)
            for imp in imports:
                all_imports[imp] = None

            if content:
                all_contents.append((os.path.basename(file_path), content))
                print(f"Successfully processed '{absolute_path}'")
            else:
                print(f"Warning: No non-import content found in '{absolute_path}'")

        with open(output_file, "w", encoding="utf-8") as outfile:
            if all_imports:
                for imp in all_imports.keys():
                    outfile.write(f"{imp}\n")
                outfile.write("\n")
                print(f"Combined {len(all_imports)} unique import statements")

            files_processed = 0
            for file_name, content in all_contents:
                outfile.write(f"\n# ----- {file_name} ----\n")
                for line in content:
                    outfile.write(f"{line}\n")
                files_processed += 1

            print(
                f"\nCombined {files_processed} files into '{os.path.abspath(output_file)}'"
            )
            if files_processed == 0:
                print("No files were processed. Check file paths and contents.")

    except Exception as e:
        print(f"Error writing to '{output_file}': {str(e)}")


if __name__ == "__main__":
    combine_files(input_files, output_file)
