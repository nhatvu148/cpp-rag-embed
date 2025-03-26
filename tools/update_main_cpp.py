import os

lib_py_path = os.path.join("tools", "temp_combined.py")
main_cpp_path = os.path.join("src", "main.cpp")


def update_main_cpp(lib_py_path, main_cpp_path):
    try:
        with open(lib_py_path, "r", encoding="utf-8") as lib_file:
            lib_content = lib_file.read()
            if not lib_content.strip():
                raise ValueError(f"'{lib_py_path}' is empty")

        print(f"Read content from '{os.path.abspath(lib_py_path)}'")

        with open(main_cpp_path, "r", encoding="utf-8") as cpp_file:
            cpp_lines = cpp_file.readlines()

        start_marker = 'const char* embedded_python_code = R"python('
        end_marker = ')python";'
        start_idx = None
        end_idx = None

        for i, line in enumerate(cpp_lines):
            if start_marker in line:
                start_idx = i
            if end_marker in line and start_idx is not None:
                end_idx = i
                break

        if start_idx is None or end_idx is None:
            raise ValueError(
                f"Could not find '{start_marker}' or '{end_marker}' in '{main_cpp_path}'"
            )

        new_cpp_content = (
            cpp_lines[: start_idx + 1] + [lib_content + "\n"] + cpp_lines[end_idx:]
        )

        with open(main_cpp_path, "w", encoding="utf-8") as cpp_file:
            cpp_file.writelines(new_cpp_content)

        print(
            f"Successfully updated '{os.path.abspath(main_cpp_path)}' with content from '{lib_py_path}'"
        )

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    if not os.path.exists(lib_py_path):
        print(f"Error: '{lib_py_path}' not found")
    elif not os.path.exists(main_cpp_path):
        print(f"Error: '{main_cpp_path}' not found")
    else:
        update_main_cpp(lib_py_path, main_cpp_path)
