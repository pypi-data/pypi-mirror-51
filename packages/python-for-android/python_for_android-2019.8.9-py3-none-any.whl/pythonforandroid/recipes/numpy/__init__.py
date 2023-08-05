from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from multiprocessing import cpu_count
from os.path import join


class NumpyRecipe(CompiledComponentsPythonRecipe):

    version = '1.16.4'
    url = 'https://pypi.python.org/packages/source/n/numpy/numpy-{version}.zip'
    site_packages_name = 'numpy'

    patches = [
        join('patches', 'add_libm_explicitly_to_build.patch'),
        join('patches', 'do_not_use_system_libs.patch'),
        join('patches', 'remove_unittest_call.patch'),
        join('patches', 'ar.patch'),
        join('patches', 'fix_setup_dependencies.patch'),
        join('patches', 'fix_environment_detection.patch'),
        ]

    call_hostpython_via_targetpython = False

    def build_compiled_components(self, arch):
        self.setup_extra_args = ['-j', str(cpu_count())]
        super(NumpyRecipe, self).build_compiled_components(arch)
        self.setup_extra_args = []

    def rebuild_compiled_components(self, arch, env):
        self.setup_extra_args = ['-j', str(cpu_count())]
        super(NumpyRecipe, self).rebuild_compiled_components(arch, env)
        self.setup_extra_args = []

    def get_recipe_env(self, arch):
        env = super(NumpyRecipe, self).get_recipe_env(arch)

        flags = " -L{} --sysroot={}".format(
            join(self.ctx.ndk_platform, 'usr', 'lib'),
            self.ctx.ndk_platform
        )

        py_ver = self.ctx.python_recipe.major_minor_version_string
        py_inc_dir = self.ctx.python_recipe.include_root(arch.arch)
        py_lib_dir = self.ctx.python_recipe.link_root(arch.arch)
        flags += ' -I{}'.format(py_inc_dir)
        flags += ' -L{} -lpython{}'.format(py_lib_dir, py_ver)
        if 'python3' in self.ctx.python_recipe.name:
            flags += 'm'

        if flags not in env['CC']:
            env['CC'] += flags
        if flags not in env['LD']:
            env['LD'] += flags + ' -shared'

        return env


recipe = NumpyRecipe()
