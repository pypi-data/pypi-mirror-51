Versions
========

The format is based on `Keep a Changelog <http://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_.

All release versions should be documented here with release date and types of changes.
Unreleased changes and pre-releases (i.e. alpha/beta versions) can be documented under the section `Unreleased`.

Possible types of changes are:

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities


Unreleased
----------


1.0.0 - 27.08.2019
------------------

Changed
'''''''
- Instead of uploading all blobs as *application/octet-stream*, the MIME type is now guessed via ``mimetypes.guess_type()``.
  This enables e.g. hotlinking images directly from GCS.


0.4.2 - 30.07.2019
------------------

Fixed
'''''
- Fixed a bug where the url parameter ``strict`` was not considered by GCSFS, e.g. in ``open_fs("gs://bucket_name?strict=False")``


0.4.1 - 18.12.2018
------------------

Fixed
'''''
- Fixed a bug where ``create=True`` in combination with an "empty-ish ``root_path`` like ``""``, ``"."`` or ``"/"`` would create a directory marker.


0.4.0 - 11.12.2018
------------------

Added
'''''
- Implemented the ``create`` property on ``GCSFS`` and the corresponding opener. By default all new GCSFS instances have ``create=False`` (PyFilesystem default)
    which means they will raise a ``CreateFailed`` exception if ``root_path`` does not exist


0.3.0 - 20.11.2018
------------------

Added
'''''
- This is the first release available on `conda-forge <https://conda-forge.org/>`__

Removed
'''''''
- ``delimiter`` property from ``GCSFS`` as it was not fully functional and we currently do not have any use case for it

Fixed
'''''
- ``GCSFS.listdir()`` and ``GCSFS.scandir()`` now also correctly list blobs on the root level of a bucket


0.2.0 - 09.11.2018
------------------

Changed
'''''''
- Open-sourced GCSFS by moving it to GitHub
- ``GCSFS.getinfo()`` does not magically fix missing directory markers anymore.
  Instead, there is a new method ``GCSFS.fix_storage()`` which can be explicitly called to check and fix the entire filesystem.

Removed
'''''''
- ``project`` and ``credentials`` properties from ``GCSFS``. Instead, one can now optionally pass a ``client`` of type
  `google.cloud.storage.Client <https://googleapis.github.io/google-cloud-python/latest/storage/client.html#module-google.cloud.storage.client>`__.

0.1.6 - 30.10.2018
------------------

Fixed
'''''
- ``GCSFS.makedirs()`` is now suitable for multiprocessing


0.1.5 - 08.10.2018
------------------

Changed
'''''''
- The ``bucket`` and ``client`` properties of ``GCSFS`` are now only computed once on instance initialization (performance improvement)


0.1.4 - 08.10.2018
------------------

Fixed
'''''
- ``GCSFS.exists()`` now correctly handles existing directories that are not marked with an empty file


0.1.3 - 04.10.2018
------------------

Changed
'''''''
- Added a custom implementation of ``FS.opendir()`` in order to be able to skip the directory check if strict=False (performance improvement)


0.1.2 - 20.09.2018
------------------

Fixed
'''''
- Fixed a bug where ``listdir``/``scandir`` on the root level of a bucket would always return an empty result
