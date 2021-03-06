# -*- coding: utf-8 -*-
import textwrap


def test_syntax_error_in_module_doctest(testdir):

    testdir.makepyfile(textwrap.dedent("""
        '''
        .. testcode::

            3+

        .. testoutput::

            3
        '''
    """))

    result = testdir.runpytest('--doctest-modules')
    result.stdout.fnmatch_lines([
        "UNEXPECTED EXCEPTION: SyntaxError('invalid syntax',*"])


def test_failing_module_doctest(testdir):

    testdir.makepyfile(textwrap.dedent("""
        '''
        .. testcode::

            print(2+5)

        .. testoutput::

            3
        '''
    """))

    result = testdir.runpytest('--doctest-modules')
    assert 'FAILURES' in result.stdout.str()
    result.stdout.fnmatch_lines([
        '002*testcode::*',
        '004*print(2+5)*',
        '*=== 1 failed in *'])


def test_failing_function_doctest(testdir):
    testdir.makepyfile(textwrap.dedent("""
        # simple comment
        GLOBAL_VAR = True

        def func():
            '''
            .. testcode::

                print(2+5)

            .. testoutput::

                3
            '''
    """))

    result = testdir.runpytest('--doctest-modules')
    assert 'FAILURES' in result.stdout.str()
    assert 'GLOBAL_VAR' not in result.stdout.str()
    result.stdout.fnmatch_lines([
        '006*testcode::*',
        '008*print(2+5)*',
        '*=== 1 failed in *'])


def test_working_module_doctest(testdir):

    testdir.makepyfile(textwrap.dedent("""
        '''
        .. testcode::

            print(2+5)

        .. testoutput::

            7
        '''
    """))

    result = testdir.runpytest('--doctest-modules')
    result.stdout.fnmatch_lines([
        '*=== 1 passed in *'])


def test_working_function_doctest(testdir):
    testdir.makepyfile(textwrap.dedent("""
        # simple comment
        GLOBAL_VAR = True

        def func():
            '''
            .. testcode::

                print(2+5)

            .. testoutput::

                7
            '''
    """))

    result = testdir.runpytest('--doctest-modules')
    result.stdout.fnmatch_lines([
        '*=== 1 passed in *'])


def test_working_module_doctest_nospaces(testdir):

    testdir.makepyfile(textwrap.dedent("""
        '''
        .. testcode::
            print(2+5)

        .. testoutput::
            7
        '''
    """))

    result = testdir.runpytest('--doctest-modules')
    result.stdout.fnmatch_lines([
        '*=== 1 passed in *'])
