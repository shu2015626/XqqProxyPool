# -*- coding: utf-8 -*-
"""
本模块解决因window下没有linux下的fcntl儿报错的问题。
会暴露出和linux的fcntl一样的接口（不全），需要其他功能
可以自行仿照开发。

本模块的内容改写自github----WoLpH的portalocker项目。
项目地址：https://github.com/WoLpH/portalocker
之所以不直接使用该包，基于以下两点原因：
（1）不想为项目增加额外的依赖
（2）原来的程序都已经部署好了，不想逐行修改代码。

本模块，完成后只需在使用到fcntl的脚本的开头，改一下引入方式即可，示例如下：
import os
try:
    if os.name == 'posix':
        import fcntl
    elif os.name == 'nt':
        import win_fcntl as fcntl
    else:
        raise Exception("不认识的操作系统平台，无法导入fcntl")
except Exception:
    raise

依赖库：
pywin32
"""
__author__ = 'shu2015626'

import sys
import win32con
import win32file
import pywintypes
import winerror
import msvcrt


class BaseLockException(Exception):
    # Error codes:
    LOCK_FAILED = 1


class LockException(BaseLockException):
    pass


class AlreadyLocked(BaseLockException):
    pass


class FileToLarge(BaseLockException):
    pass


class WinFcntl(object):
    """
    实现windows版本下的fcntl，最后暴露出和fcntl一样的接口
    """
    # 将锁的类型定义为类变量
    LOCK_EX = 0x1  #: exclusive lock
    LOCK_SH = 0x2  #: shared lock
    LOCK_NB = 0x4  #: non-blocking
    LOCK_UN = msvcrt.LK_UNLCK  #: unlock
    __overlapped = pywintypes.OVERLAPPED()

    def __init__(self):
        # version_info是一个named_tuple表示python的版本
        if sys.version_info.major == 2:
            self.lock_length = -1
        else:
            self.lock_length = int(2**31 - 1)

    def lock(self, obj_file, flags):
        if flags & self.LOCK_SH:
            if sys.version_info.major == 2:
                if flags & self.LOCK_NB:
                    mode = win32con.LOCKFILE_FAIL_IMMEDIATELY
                else:
                    mode = 0

            else:
                if flags & self.LOCK_NB:
                    mode = msvcrt.LK_NBRLCK
                else:
                    mode = msvcrt.LK_RLCK

            # is there any reason not to reuse the following structure?
            hfile = win32file._get_osfhandle(obj_file.fileno())
            try:
                win32file.LockFileEx(hfile, mode, 0, -0x10000, self.__overlapped)
            except pywintypes.error as exc_value:
                # error: (33, 'LockFileEx', 'The process cannot access the file
                # because another process has locked a portion of the file.')
                if exc_value.winerror == winerror.ERROR_LOCK_VIOLATION:
                    raise LockException(
                        LockException.LOCK_FAILED,
                        exc_value.strerror)
                else:
                    # Q:  Are there exceptions/codes we should be dealing with
                    # here?
                    raise
        else:
            mode = win32con.LOCKFILE_EXCLUSIVE_LOCK
            if flags & self.LOCK_NB:
                mode |= win32con.LOCKFILE_FAIL_IMMEDIATELY

            if flags & self.LOCK_NB:
                mode = msvcrt.LK_NBLCK
            else:
                mode = msvcrt.LK_LOCK

            # windows locks byte ranges, so make sure to lock from file start
            try:
                savepos = obj_file.tell()
                if savepos:
                    # [ ] test exclusive lock fails on seek here
                    # [ ] test if shared lock passes this point
                    obj_file.seek(0)
                    # [x] check if 0 param locks entire file (not documented in
                    #     Python)
                    # [x] fails with "IOError: [Errno 13] Permission denied",
                    #     but -1 seems to do the trick

                try:
                    msvcrt.locking(obj_file.fileno(), mode, self.lock_length)
                except IOError as exc_value:
                    # [ ] be more specific here
                    raise LockException(
                        LockException.LOCK_FAILED,
                        exc_value.strerror
                    )
                finally:
                    if savepos:
                        obj_file.seek(savepos)
            except IOError as exc_value:
                raise LockException(
                    LockException.LOCK_FAILED,
                    exc_value.strerror
                )

    def unlock(self, obj_file):
        try:
            savepos = obj_file.tell()
            if savepos:
                obj_file.seek(0)

            try:
                msvcrt.locking(obj_file.fileno(), self.LOCK_UN, self.lock_length)
            except IOError as exc_value:
                if exc_value.strerror == 'Permission denied':
                    hfile = win32file._get_osfhandle(obj_file.fileno())
                    try:
                        win32file.UnlockFileEx(
                            hfile, 0, -0x10000, self.__overlapped
                        )
                    except pywintypes.error as exc_value:
                        if exc_value.winerror == winerror.ERROR_NOT_LOCKED:
                            # error: (158, 'UnlockFileEx',
                            #         'The segment is already unlocked.')
                            # To match the 'posix' implementation, silently
                            # ignore this error
                            pass
                        else:
                            # Q:  Are there exceptions/codes we should be
                            # dealing with here?
                            raise
                else:
                    raise LockException(
                        LockException.LOCK_FAILED,
                        exc_value.strerror
                    )
            finally:
                if savepos:
                    obj_file.seek(savepos)
        except IOError as exc_value:
            raise LockException(
                LockException.LOCK_FAILED,
                exc_value.strerror
            )


obj_win_fcntl = WinFcntl()
flock = obj_win_fcntl.lock
lockf = obj_win_fcntl.unlock()