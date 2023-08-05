import argparse
import json
from pathlib import Path
from sys import stderr

from pipenv_setup import lock_file_parser, setup_filler, setup_updater


# noinspection Mypy
from pipenv_setup.setup_updater import blacken


def cmd():

    parser = argparse.ArgumentParser(description="sync pipfile with setup.py")

    # parser.add_argument(
    #     "blah",
    #     action="store",
    #     type=str,
    #     help="blah",
    # )

    # argv = parser.parse_args()

    # add your command line program here

    pipfile_path, lock_file_path, setup_file_path = required_files = [
        Path("Pipfile"),
        Path("Pipfile.lock"),
        Path("setup.py"),
    ]

    # found_files = tuple(filter(Path.exists, required_files))
    missing_files = tuple(filter(lambda x: not x.exists(), required_files))
    only_setup_missing = len(missing_files) == 1 and not setup_file_path.exists()

    if not missing_files or only_setup_missing:
        dependency_arguments = {"dependency_links": [], "install_requires": []}
        with open(lock_file_path) as lock_file:
            lock_file_data = json.load(lock_file)
        local_packages, remote_packages = lock_file_parser.get_default_packages(
            lock_file_data
        )
        for local_package in local_packages:
            print("package %s is local, omitted in setup.py" % local_package)

        success_count = 0
        for remote_package_name, remote_package_config in remote_packages.items():
            try:
                destination_kw, value = lock_file_parser.format_remote_package(
                    remote_package_name, remote_package_config
                )
            except ValueError as e:
                print(e, file=stderr)
                print(
                    "package %s is not added to setup.py" % remote_package_name,
                    file=stderr,
                )
            else:
                success_count += 1
                dependency_arguments[destination_kw].append(value)
        if only_setup_missing:
            print("setup.py not found under current directory")
            print("Creating boilerplate setup.py...")
            setup_code = setup_filler.fill_boilerplate(dependency_arguments)
            if setup_code is None:
                print("Can not find read setup.py template file", file=stderr)
                return
            try:
                with open(setup_file_path, "w") as new_setup_file:
                    new_setup_file.write(setup_code)
                blacken(str(setup_file_path))
            except OSError as e:
                print(e, file=stderr)
                print("failed to write setup.py file", file=stderr)
                return
            else:
                print("setup.py successfully generated under current directory")
                print("%d packages moved from Pipfile.lock to setup.py" % success_count)
                print("Please edit the required fields in the generated file")

        else:  # all files exist. Update setup.py
            setup_updater.update_setup(dependency_arguments, setup_file_path)
            print("setup.py successfully updated")
            print("%d packages from Pipfile.lock synced to setup.py" % success_count)

    else:
        for file in missing_files:
            print("%s not found under current directory" % file, file=stderr)
        print("can not perform sync", file=stderr)
        return
