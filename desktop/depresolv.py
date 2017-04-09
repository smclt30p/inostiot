import importlib
import sys
import subprocess

"""
Depresolv is a system that is constructed to prevent
runtime import errors on Windows systems. You provide a
list of deps to depresolv and it resolves them and restarts
the app. Only std dependencies
"""


def getFunctionalPip():

    try:
        subprocess.check_output(["pip"])
        return "pip"
    except BaseException:
        try:
            subprocess.check_output(["pip3"])
            return "pip3"
        except BaseException:
            print("No operational pip intallation found!")
            return False

ALL_SATISFIED = 0
INSTALLED_AND_SATISFIED = 1
INSTALL_FAILED = 2

class DependencyResolver():

    dependencies = None
    missing = []
    failed = []

    def config(self, dependencies, modulename):
        print("Resolving dependencies for {}: ".format(modulename) + str(dependencies))
        self.dependencies = dependencies

    def resolve(self):

        installed_something = False

        for module in self.dependencies:
            print("Resolving {} -- ".format(module), end="")
            try:
                importlib.import_module(module)
                print("OK!")
            except ModuleNotFoundError:
                print("Installing {} -- ".format(module), end="")
                try:
                    pip = getFunctionalPip()

                    if pip is False:
                        return INSTALL_FAILED

                    subprocess.check_output([pip, "install","--user", module], stderr=subprocess.STDOUT)
                    installed_something = True

                    print("OK")
                except subprocess.CalledProcessError as e:
                    print("Module install failed for {} with the following output:\n\n{}".format(str(e), e.output.decode("utf-8")))

                    return INSTALL_FAILED

        if installed_something: return INSTALLED_AND_SATISFIED
        else: return ALL_SATISFIED


def launch_main(deps):

        print("Resolving runtime dependencies, please wait...\n\n")
        resolver = DependencyResolver()
        resolver.config(deps, "launch_main")
        return resolver.resolve()
