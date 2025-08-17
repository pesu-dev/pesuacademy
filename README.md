# pesuacademy-py

![PyPI](https://img.shields.io/pypi/v/pesuacademy?label=pypi%20package)
![GitHub Release](https://img.shields.io/github/v/release/HackerSpace-PESU/pesuacademy-py)
![GitHub Tag](https://img.shields.io/github/v/tag/HackerSpace-PESU/pesuacademy-py)
![PyPI - Status](https://img.shields.io/pypi/status/pesuacademy)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pesuacademy)

![GitHub commit activity](https://img.shields.io/github/commit-activity/w/HackerSpace-PESU/pesuacademy-py)
![GitHub last commit](https://img.shields.io/github/last-commit/HackerSpace-PESU/pesuacademy-py)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/HackerSpace-PESU/pesuacademy-py/latest)

![build-docs.yml](https://github.com/HackerSpace-PESU/pesuacademy-py/actions/workflows/build-docs.yml/badge.svg)

This library provides a fast and lightweight Python wrapper around the PESU Academy website, enabling easy programmatic access to announcements, courses, profiles, and more.

With pesuacademy, you can: - Fetch course details and schedules - Access announcements and results - Easily integrate PESU Academy data into your Python applications

> [!WARNING]
> This is not an official Package and is not endorsed by PES University. Use at your own risk.

## 💡 Features

- **Profile**: Fetch a user's personal details.
- **Courses**: Get a list of the user's enrolled courses by semester.
- **Attendance**: Retrieve detailed attendance records.
- **Announcements**: Get the latest college announcements.
- **Exam Seating Info**: Find the user's assigned seat for upcoming ISA/ESAs.
- **Results**: Fetch the user's semester-wise results.
- **Class Materials**: A powerful module to list and download all your class notes and presentations.

## 🔨 Installation

### Installing from `pip`

```bash
pip install pesuacademy
```

### Installing from source

```bash
pip install git+https://github.com/pesu-dev/pesuacademy.git
```

## 📐 Usage

```python
import asyncio
from pesuacademy import PESUAcademy

PRN = "YOUR_PRN"
PASSWORD = "YOUR_PASSWORD"

async def main():
    session = None
    try:

        session = await PESUAcademy.login(PRN, PASSWORD)
        print("Login Successful!")

        profile = await session.get_profile()
        print(f"Welcome, {profile.personal.name}!")

        results = await session.get_results(semester=2)
        if results:
            print(f"Your SGPA for Semester 2 was: {results.sgpa}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if session:
            await session.close()
            print("Session closed.")

if __name__ == "__main__":
    asyncio.run(main())
```

The complete documentation is available here: [PESU Academy Docs](https://pesu-dev.github.io/pesuacademy/)

## 🤝 Contributing to PESUAcademy

<a href="https://github.com/pesu-dev/pesuacademy/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pesu-dev/pesuacademy" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

If you'd like to contribute, please follow our [contribution guidelines](.github/CONTRIBUTING.md).
