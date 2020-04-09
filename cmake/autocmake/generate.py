# -*- coding: utf-8 -*-
def gen_cmake_command(config):
    """
    Generate CMake command.
    """
    from autocmake.extract import extract_list

    s = []
    s.append("\n\ndef gen_cmake_command(options, arguments):")
    s.append('    """')
    s.append("    Generate CMake command based on options and arguments.")
    s.append('    """')
    s.append("    command = []")

    for env in config['export']:
        s.append('    command.append({0})'.format(env))

    s.append("    command.append(arguments['--cmake-executable'])")

    for definition in config['define']:
        s.append('    command.append({0})'.format(definition))

    s.append("    command.append('-DCMAKE_BUILD_TYPE={0}'.format(arguments['--type']))")
    s.append("    command.append('-G\"{0}\"'.format(arguments['--generator']))")
    s.append("    if arguments['--cmake-options'] != \"''\":")
    s.append("        command.append(arguments['--cmake-options'])")
    s.append("    if arguments['--prefix']:")
    s.append("        command.append('-DCMAKE_INSTALL_PREFIX=\"{0}\"'.format(arguments['--prefix']))")

    s.append("\n    return ' '.join(command)")

    return '\n'.join(s)


def autogenerated_notice():
    from datetime import date
    from . import __version__

    current_year = date.today().year
    year_range = '2015-{0}'.format(current_year)

    s = []
    s.append('# This file is autogenerated by Autocmake v{0} http://autocmake.org'.format(__version__))
    s.append('# Copyright (c) {0} by Radovan Bast, Roberto Di Remigio, Jonas Juselius, and contributors.'.format(
        year_range))

    return '\n'.join(s)


def gen_cmake_options_wrappers():
    s = """\n# Options handling utilities
include(CMakeDependentOption)
# Macro for printing an option in a consistent manner
# Written by Lori A. Burns (@loriab) and Ryan M. Richard (@ryanmrichard)
# Syntax: print_option(<option to print> <was specified>)
macro(print_option variable default)
  if(NOT DEFINED ${variable} OR "${${variable}}" STREQUAL "")
    message(STATUS "Setting (unspecified) option ${variable}: ${default}")
  else()
    message(STATUS "Setting option ${variable}: ${${variable}}")
  endif()
endmacro()

# Wraps an option with default ON/OFF. Adds nice messaging to option()
# Written by Lori A. Burns (@loriab) and Ryan M. Richard (@ryanmrichard)
# Syntax: option_with_print(<option name> <description> <default value>)
macro(option_with_print variable msge default)
  print_option(${variable} ${default})
  option(${variable} ${msge} ${default})
endmacro()

# Wraps an option with a default other than ON/OFF and prints it
# Written by Lori A. Burns (@loriab) and Ryan M. Richard (@ryanmrichard)
# NOTE: Can't combine with above b/c CMake handles ON/OFF options specially
# NOTE2: CMake variables are always defined so need to further check for if
#       they are the NULL string. This is also why we need the force
# Syntax: option_with_default(<option name> <description> <default value>)
macro(option_with_default variable msge default)
  print_option(${variable} "${default}")
  if(NOT DEFINED ${variable} OR "${${variable}}" STREQUAL "")
    set(${variable} "${default}" CACHE STRING ${msge} FORCE)
  endif()
endmacro()"""
    return s


def gen_setup(config, default_build_type, relative_path, setup_script_name):
    """
    Generate setup script.
    """
    from autocmake.extract import extract_list

    s = []
    s.append('#!/usr/bin/env python')
    s.append('\n{0}'.format(autogenerated_notice()))
    s.append('\nimport os')
    s.append('import sys')
    s.append('assert sys.version_info >= (2, 6), \'Python >= 2.6 is required\'')

    s.append("\nsys.path.insert(0, '{0}')".format(relative_path))

    s.append('from autocmake import configure')
    s.append('from autocmake.external import docopt')

    s.append('\n\noptions = """')
    s.append('Usage:')
    s.append('  ./{0} [options] [<builddir>]'.format(setup_script_name))
    s.append('  ./{0} (-h | --help)'.format(setup_script_name))
    s.append('\nOptions:')

    options = []

    for opt in config['docopt']:
        first = opt.split()[0].strip()
        rest = ' '.join(opt.split()[1:]).strip()
        options.append([first, rest])

    options.append([
        '--type=<TYPE>',
        'Set the CMake build type (debug, release, relwithdebinfo, minsizerel) [default: {0}].'.format(
            default_build_type)
    ])
    options.append(['--generator=<STRING>', 'Set the CMake build system generator [default: Unix Makefiles].'])
    options.append(['--show', 'Show CMake command and exit.'])
    options.append(['--cmake-executable=<CMAKE_EXECUTABLE>', 'Set the CMake executable [default: cmake].'])
    options.append(['--cmake-options=<STRING>', "Define options to CMake [default: '']."])
    options.append(['--prefix=<PATH>', 'Set the install path for make install.'])
    options.append(['<builddir>', 'Build directory.'])
    options.append(['-h --help', 'Show this screen.'])

    s.append(align_options(options))

    s.append('"""')

    s.append(gen_cmake_command(config))

    s.append("\n")
    s.append("# parse command line args")
    s.append("try:")
    s.append("    arguments = docopt.docopt(options, argv=None)")
    s.append("except docopt.DocoptExit:")
    s.append(r"    sys.stderr.write('ERROR: bad input to {0}\n'.format(sys.argv[0]))")
    s.append("    sys.stderr.write(options)")
    s.append("    sys.exit(-1)")
    s.append("\n")
    s.append("# use extensions to validate/post-process args")
    s.append("if configure.module_exists('extensions'):")
    s.append("    import extensions")
    s.append("    arguments = extensions.postprocess_args(sys.argv, arguments)")
    s.append("\n")
    s.append("root_directory = os.path.dirname(os.path.realpath(__file__))")
    s.append("\n")
    s.append("build_path = arguments['<builddir>']")
    s.append("\n")
    s.append("# create cmake command")
    s.append("cmake_command = '{0} -H{1}'.format(gen_cmake_command(options, arguments), root_directory)")
    s.append("\n")
    s.append("# run cmake")
    s.append("configure.configure(root_directory, build_path, cmake_command, arguments)")

    return s


def gen_cmakelists(project_name, project_language, min_cmake_version, default_build_type, relative_path, modules):
    """
    Generate CMakeLists.txt.
    """
    import os

    s = []

    s.append(autogenerated_notice())

    s.append('\n# set minimum cmake version')
    s.append('cmake_minimum_required(VERSION {0} FATAL_ERROR)'.format(min_cmake_version))

    s.append('\n# project name')
    s.append('project({0} LANGUAGES {1})'.format(project_name, project_language))

    s.append('\n# do not rebuild if rules (compiler flags) change')
    s.append('set(CMAKE_SKIP_RULE_DEPENDENCY TRUE)')

    build_type_capitalized = {
        'debug': 'Debug',
        'release': 'Release',
        'relwithdebinfo': 'RelWithDebInfo',
        'minsizerel': 'MinSizeRel'
    }

    _build_type = build_type_capitalized[default_build_type]
    s.append('\n# if CMAKE_BUILD_TYPE undefined, we set it to {0}'.format(_build_type))
    s.append('if(NOT CMAKE_BUILD_TYPE)')
    s.append('    set(CMAKE_BUILD_TYPE "{0}")'.format(_build_type))
    s.append('endif()')

    s.append(gen_cmake_options_wrappers())

    if len(modules) > 0:
        s.append('\n# included cmake modules')
    for module in modules:
        s.append('include({0})'.format(os.path.join('${PROJECT_SOURCE_DIR}', relative_path, module.path, module.name)))

    return s


def align_options(options):
    """
    Indents flags and aligns help texts.
    """
    l = 0
    for opt in options:
        if len(opt[0]) > l:
            l = len(opt[0])
    s = []
    for opt in options:
        s.append('  {0}{1}  {2}'.format(opt[0], ' ' * (l - len(opt[0])), opt[1]))
    return '\n'.join(s)
