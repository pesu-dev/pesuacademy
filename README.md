# pesuacademy

![PyPI](https://img.shields.io/pypi/v/pesuacademy?label=pypi%20package)
![PyPI - Status](https://img.shields.io/pypi/status/pesuacademy)
![Status: Deprecated](https://img.shields.io/badge/status-deprecated-red)

> [!CAUTION]
> **This project is deprecated and archived. It no longer works and will not receive updates, fixes, or support.**
>
> All programmatic access to PESU Academy now goes through **[PESU OAuth2](https://github.com/pesu-dev/oauth2)**.
> Please migrate any code that depends on this package.

## Why?

`pesuacademy` scraped the PESU Academy website directly using your PESU password. That approach was fragile (it broke
whenever the site's markup changed) and required every application to handle raw student credentials.

[PESU OAuth2](https://github.com/pesu-dev/oauth2) replaces it with a standard OAuth2 / OpenID Connect authorization
server ("Sign in with PESU"), so applications can access PESU Academy data on a student's behalf without ever seeing
their password.

## Migrating

1. Remove `pesuacademy` from your dependencies:

   ```bash
   pip uninstall pesuacademy
   ```

2. Register your application and integrate with PESU OAuth2. See the
   [PESU OAuth2 repository](https://github.com/pesu-dev/oauth2) and its hosted documentation at
   <https://pesu-oauth2.onrender.com> for details.

3. For questions, reach out on the `#pesu-dev` channel of the [PESU Discord](https://discord.gg/eZ3uFs2).

## Final release

The last published version on PyPI is `1.0.1`. It is identical to `1.0.0` except that importing it emits a deprecation
warning. Existing installations are not removed, but they are not expected to work against PESU Academy.

## History

This repository is kept read-only for reference. Its issues and pull requests have been closed, and the source code
remains available under the [MIT License](LICENSE).

> [!WARNING]
> This was never an official API and was not endorsed by PES University.
