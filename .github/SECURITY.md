# Security Policy

<details>
<summary>📚 Table of Contents</summary>

- [🛡️ Introduction](#-introduction)
- [🚨 Reporting a Vulnerability](#-reporting-a-vulnerability)
- [🎯 Important Disclaimer](#-important-disclaimer)
- [🔐 Security Best Practices](#-security-best-practices)

</details>

## 🛡️ Introduction

The maintainers of the `pesuacademy` Python package take security seriously. We are committed to addressing security vulnerabilities responsibly and in a timely manner. This document outlines our security policy, including how to report a vulnerability and the scope of our responsibility.

---

## 🚨 Reporting a Vulnerability

We encourage the responsible disclosure of security vulnerabilities. **Please do not open a public GitHub issue.**

- **Do NOT open a public issue** to report security problems.
- Instead, send a confidential email to the maintainers on the PESU Deverloper Group channel (`#pesu-dev`) on [PESU Discord](https://discord.gg/eZ3uFs2), or email the maintainers.
- Include as much detail as possible:
  - Steps to reproduce the issue
  - Impact of the vulnerability
  - Any suggested mitigations or fixes

We will acknowledge your report within 48 hours and keep you updated on the progress.

---

## 🎯 Important Disclaimer

It is critical to understand the role of this Python package.

- **Client library:** The `pesuacademy` package is a tool that automates interactions with the official PESU Academy website on behalf of a user. It does not store user data.
- **No Endorsement:** The existence of this package does not imply an endorsement or official partnership with PESU.
- **Responsibility of Developers:** The security of user credentials and data handled by this package is the responsibility of the developer who integrates it into their application. We are not responsible for how third-party applications use this library.

---

## 🔐 Security Best Practices

When you use `pesuacademy` in your own project, please follow these security best practices:

- **Hard-coded credentials:** Do not write your username or password directly in your source code. Use environment variables, a secrets management system (like Doppler, Vault, or GitHub secrets), or other secure methods to handle credentials.
- **Updated dependencies:** Pesuacademy library uses several open-source dependencies. We regularly monitor and update dependencies to patch known vulnerabilities.
- **Access levels:** Ensure that any systems or applications using this package have the minimum necessary permissions.

Thank you for helping us keep the `pesuacademy` package secure!
