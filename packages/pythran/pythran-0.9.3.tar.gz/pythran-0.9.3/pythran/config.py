try:
    # python3 vs. python2
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser
import logging
import numpy.distutils.system_info as numpy_sys
import numpy
import os
import sys

logger = logging.getLogger('pythran')


def get_paths_cfg(
    sys_file='pythran.cfg',
    platform_file='pythran-{}.cfg'.format(sys.platform),
    user_file='.pythranrc'
):
    """
    >>> os.environ['HOME'] = '/tmp/test'
    >>> get_paths_cfg()['user']
    '/tmp/test/.pythranrc'
    >>> os.environ['HOME'] = '/tmp/test'
    >>> os.environ['XDG_CONFIG_HOME'] = '/tmp/test2'
    >>> get_paths_cfg()['user']
    '/tmp/test2/.pythranrc'
    >>> os.environ['HOME'] = '/tmp/test'
    >>> os.environ['XDG_CONFIG_HOME'] = '/tmp/test2'
    >>> os.environ['PYTHRANRC'] = '/tmp/test3/pythranrc'
    >>> get_paths_cfg()['user']
    '/tmp/test3/pythranrc'
    """
    sys_config_dir = os.path.dirname(__file__)
    sys_config_path = os.path.join(sys_config_dir, sys_file)

    platform_config_path = os.path.join(sys_config_dir, platform_file)

    user_config_path = os.environ.get('PYTHRANRC', None)
    if not user_config_path:
        user_config_dir = os.environ.get('XDG_CONFIG_HOME', '~')
        user_config_path = os.path.expanduser(
            os.path.join(user_config_dir, user_file))
    return {"sys": sys_config_path, "platform": platform_config_path, "user": user_config_path}


def init_cfg(sys_file, platform_file, user_file):
    paths = get_paths_cfg(sys_file, platform_file, user_file)
    sys_config_path, platform_config_path, user_config_path = paths["sys"], paths["platform"], paths["user"]

    cfgp = ConfigParser()
    for required in (sys_config_path, platform_config_path):
        cfgp.read([required])
    cfgp.read([user_config_path])

    return cfgp


def lint_cfg(cfgp, **paths):
    if not paths:
        paths = get_paths_cfg()

    # Use configuration from sys and platform as "reference"
    cfgp_ref = ConfigParser()
    cfgp_ref.read([paths["sys"], paths["platform"]])

    # Check if pythran configuration files exists
    for loc, path in paths.items():
        exists = os.path.exists(path)

        msg = " ".join([
            "{} file".format(loc).rjust(13),
            "exists:" if exists else "does not exist:",
            path
        ])
        logger.info(msg) if exists else logger.warn(msg)

    for section in cfgp.sections():
        # Check if section in the current configuration exists in the
        # reference configuration
        if cfgp_ref.has_section(section):
            options = set(cfgp.options(section))
            options_ref = set(cfgp_ref.options(section))

            # Check if the options in the section are supported by the
            # reference configuration
            if options.issubset(options_ref):
                logger.info(
                    (
                        "pythranrc section [{}] is valid and options are "
                        "correct"
                    ).format(section)
                )
            else:
                logger.warn(
                    (
                        "pythranrc section [{}] is valid but options {} "
                        "are incorrect!"
                    ).format(section, options.difference(options_ref))
                )
        else:
            logger.warn("pythranrc section [{}] is invalid!".format(section))


def make_extension(python, **extra):

    def parse_define(define):
        index = define.find('=')
        if index < 0:
            return (define, None)
        else:
            return define[:index], define[index + 1:]

    extension = {
        "language": "c++",
        # forcing str conversion to handle Unicode case (the default on MS)
        "define_macros": [str(x) for x in
                          cfg.get('compiler', 'defines').split()],
        "undef_macros": [str(x) for x in
                         cfg.get('compiler', 'undefs').split()],
        "include_dirs": [str(x) for x in
                         cfg.get('compiler', 'include_dirs').split()],
        "library_dirs": [str(x) for x in
                         cfg.get('compiler', 'library_dirs').split()],
        "libraries": [str(x) for x in
                      cfg.get('compiler', 'libs').split()],
        "extra_compile_args": [str(x) for x in
                               cfg.get('compiler', 'cflags').split()],
        "extra_link_args": [str(x) for x in
                            cfg.get('compiler', 'ldflags').split()],
        "extra_objects": []
    }

    if python:
        extension['define_macros'].append('ENABLE_PYTHON_MODULE')
    extension['define_macros'].append(
        '__PYTHRAN__={}'.format(sys.version_info.major))

    here = os.path.dirname(os.path.dirname(__file__)) or '.'
    # using / as separator as advised in the distutils doc
    extension["include_dirs"].append(here + '/pythran')

    extra.pop('language', None)  # forced to c++ anyway
    cxx = extra.pop('cxx', None)
    if cxx is None:
        cxx = compiler()
    if cxx is not None:
        extension['cxx'] = cxx

    for k, w in extra.items():
        extension[k].extend(w)
    if cfg.getboolean('pythran', 'complex_hook'):
        # the patch is *not* portable
        extension["include_dirs"].append(here + '/pythran/pythonic/patch')

    # Numpy can pollute stdout with warning message which should be on stderr
    old_stdout = sys.stdout
    try:
        sys.stdout = sys.stderr

        # numpy specific
        if python:
            extension['include_dirs'].append(numpy.get_include())

        # blas dependency
        user_blas = cfg.get('compiler', 'blas')
        if user_blas == 'pythran-openblas':
            try:
                import pythran_openblas as openblas
                # required to cope with atlas missing extern "C"
                extension['define_macros'].append('PYTHRAN_BLAS_OPENBLAS')
                extension['include_dirs'].extend(openblas.include_dirs)
                extension['extra_objects'].append(os.path.join(openblas.library_dir,
                                                               openblas.static_library))
            except ImportError:
                logger.warn("Failed to find 'pythran-openblas' package. "
                            "Please install it or change the compiler.blas setting. "
                            "Defaulting to 'blas'")
                user_blas = 'blas'

        if user_blas != 'pythran-openblas':
            numpy_blas = numpy_sys.get_info(user_blas)
            # required to cope with atlas missing extern "C"
            extension['define_macros'].append('PYTHRAN_BLAS_{}'
                                              .format(user_blas.upper()))
            extension['libraries'].extend(numpy_blas.get('libraries', []))
            extension['library_dirs'].extend(numpy_blas.get('library_dirs', []))
            extension['include_dirs'].extend(numpy_blas.get('include_dirs', []))
    finally:
        sys.stdout = old_stdout

    # final macro normalization
    extension["define_macros"] = [
        dm if isinstance(dm, tuple) else parse_define(dm)
        for dm in extension["define_macros"]]
    return extension


def compiler():
    """Get compiler to use for C++ to binary process. The precedence for
    choosing the compiler is as follows::

      1. `CXX` environment variable
      2. User configuration (~/.pythranrc)

    Returns None if none is set or if it's set to the empty string

    """
    cfg_cxx = str(cfg.get('compiler', 'CXX'))
    if not cfg_cxx:
        cfg_cxx = None
    return os.environ.get('CXX', cfg_cxx) or None


# load platform specific configuration then user configuration
cfg = init_cfg('pythran.cfg',
               'pythran-{}.cfg'.format(sys.platform),
               '.pythranrc')


def run():
    '''
    Dump on stdout the config flags required to compile pythran-generated code.
    '''
    import argparse
    import distutils.sysconfig
    import pythran
    import numpy

    parser = argparse.ArgumentParser(
        prog='pythran-config',
        description='output build options for pythran-generated code',
        epilog="It's a megablast!"
    )

    parser.add_argument('--compiler', action='store_true',
                        help='print default compiler')

    parser.add_argument('--cflags', action='store_true',
                        help='print compilation flags')

    parser.add_argument('--libs', action='store_true',
                        help='print linker flags')

    parser.add_argument('--no-python', action='store_true',
                        help='do not include Python-related flags')

    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help=(
                            'verbose mode: [-v] prints warnings if pythranrc '
                            'has an invalid configuration; use '
                            '[-vv] for more information')
                        )

    args = parser.parse_args(sys.argv[1:])

    args.python = not args.no_python

    output = []

    extension = pythran.config.make_extension(python=args.python)

    if args.verbose >= 1:
        if args.verbose == 1:
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.INFO)

        lint_cfg(cfg)

    if args.compiler or args.verbose >= 2:
        cxx = compiler() or 'c++'
        logger.info('CXX = '.rjust(10) + cxx)
        if args.compiler:
            output.append(cxx)

    if args.cflags or args.verbose>=2:
        def fmt_define(define):
            name, value = define
            if value is None:
                return '-D' + name
            else:
                return '-D' + name + '=' + value

        cflags = []
        cflags.extend(fmt_define(define)
                      for define in extension['define_macros'])
        cflags.extend(('-I' + include)
                      for include in extension['include_dirs'])
        if args.python:
            cflags.append('-I' + numpy.get_include())
            cflags.append('-I' + distutils.sysconfig.get_python_inc())

        logger.info('CFLAGS = '.rjust(10) + ' '.join(cflags))
        if args.cflags:
            output.extend(cflags)

    if args.libs or args.verbose>=2:
        ldflags = []
        ldflags.extend(('-L' + include)
                       for include in extension['library_dirs'])
        ldflags.extend(('-l' + include)
                       for include in extension['libraries'])

        if args.python:
            ldflags.append('-L' + distutils.sysconfig.get_config_var('LIBPL'))
            ldflags.extend(distutils.sysconfig.get_config_var('LIBS').split())
            ldflags.append('-lpython'
                           + distutils.sysconfig.get_config_var('VERSION'))

        logger.info('LDFLAGS = '.rjust(10) + ' '.join(ldflags))
        if args.libs:
            output.extend(ldflags)

    if output:
        print(' '.join(output))


if __name__ == '__main__':
    run()
