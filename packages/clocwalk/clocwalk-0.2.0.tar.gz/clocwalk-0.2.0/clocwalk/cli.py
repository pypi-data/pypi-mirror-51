#!/usr/bin/env python
# coding: utf-8

import inspect
import os
import sys
import pprint
import json

from clocwalk.lib.common import banner
from clocwalk.lib.common import setPath
from clocwalk.lib.common import weAreFrozen
from clocwalk.lib.cmdline import cmdLineParser
from clocwalk.lib.data import paths
from clocwalk.lib.data import conf
from clocwalk.lib.data import kb
from clocwalk.lib.data import logger
from clocwalk.lib.exception import UserQuitException, CodeDirIsNoneException
from clocwalk.lib.option import init
from clocwalk.lib.clocwrapper import ClocCode


def modulePath():
    """
    This will get us the program's directory, even if we are frozen
    using py2exe
    """

    try:
        _ = sys.executable if weAreFrozen() else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)

    return os.path.dirname(os.path.realpath(_))


class ClocDetector(object):
    """"""

    def __init__(self, **kwargs):
        """
        Constructor
        """
        conf.verbose = conf.verbose or 1
        paths.ROOT_PATH = modulePath()
        setPath()
        init()

        code_dir = kwargs.get('code_dir', None)
        skip_check_new_version = kwargs.get('skip_check_new_version', False)
        self.tag_filter = kwargs.get('tag_filter', [])
        self.timeout = kwargs.get('timeout', 5)

        if not code_dir:
            raise CodeDirIsNoneException('"code_dir" parameter cannot be empty!')
        self.code_dir = code_dir
        self.skip_check_new_version = skip_check_new_version
        self._result = {'cloc': None, 'depends': []}
        self.cloc = ClocCode()

    def start(self):
        """

        :return:
        """

        retVal = False

        try:
            logger.info('analysis statistics code ...')
            self.cloc.start(code_dir=self.code_dir, args=conf.cloc['cloc']['args'])
            self._result['cloc'] = json.loads(self.cloc.result)
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            logger.warning(ex)

        for func, product in kb.pluginFunctions:
            try:
                logger.debug("test item depends on package using '%s'" % product)
                result = func(
                    code_dir=self.code_dir,
                    skipNewVerCheck=self.skip_check_new_version,
                    timeout=self.timeout,
                    tag_filter=self.tag_filter
                )
            except Exception as ex:
                import traceback;
                traceback.print_exc()
                errMsg = "exception occurred while running "
                errMsg += "script for '%s' ('%s')" % (product, ex)
                logger.critical(errMsg)

                result = None

            if result:
                retVal = True
                self._result['depends'].append({product: result})

        return retVal

    @property
    def getResult(self):
        return self._result

    @property
    def getPluginNames(self):
        return [i for i in kb.pluginFunctions]


def main():
    """
    main function
    """

    try:
        cmdLineParser()
        banner()

        if not os.path.exists(conf.code_dir):
            msg = '[%s] path does not exist!' % conf.code_dir
            logger.critical(msg)
            raise Exception(msg)

        c = ClocDetector(code_dir=conf.code_dir, skip_check_new_version=conf.skip_check_new_version)
        logger.info("%d fingerprints plugin loaded." % len(c.getPluginNames))
        logger.info("checking depends ...")
        c.start()
        pprint.pprint(c.getResult)

    except UserQuitException:
        logger.error("user quit")

    except KeyboardInterrupt:
        logger.error("user aborted")

    except EOFError:
        logger.error("exit")

    except SystemExit:
        raise


if __name__ == "__main__":
    main()
