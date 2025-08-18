# pesuacademy

![PyPI](https://img.shields.io/pypi/v/pesuacademy?label=PyPI)
![Python Versions](https://img.shields.io/pypi/pyversions/pesuacademy)
![License](https://img.shields.io/pypi/l/pesuacademy)
![GitHub Release](https://img.shields.io/github/v/release/pesu-dev/pesuacademy)
![GitHub Tag](https://img.shields.io/github/v/tag/pesu-dev/pesuacademy)
![GitHub last commit](https://img.shields.io/github/last-commit/pesu-dev/pesuacademy)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/pesu-dev/pesuacademy)
![Docs Build](https://github.com/pesu-dev/pesuacademy/actions/workflows/build-docs.yml/badge.svg)

Super-fast, lightweight, asynchronous Python wrapper for the PESU Academy portal. Fetch profile, courses, attendance, announcements, results, seating information, and class materials with clean Pydantic models.

> This is an unofficial package and is not endorsed by PES University. Use at your own risk.

### Highlights

- **Typed models**: Returns rich Pydantic models for predictable usage.
- **Async-first**: Built on `httpx` AsyncClient for speed and concurrency.
- **End-to-end flows**: Includes a full materials workflow (course → unit → topic → links).
- **Simple API**: One authenticated session with clear methods for all common tasks.

---

### Table of contents

- Installation
- Quickstart
- Credentials and environment
- API overview
- Usage examples
  - Profile
  - Courses and Attendance
  - Results
  - Announcements
  - Seating information
  - Materials workflow (Units → Topics → Links)
- Error handling and troubleshooting
- Contributing
- License

---

## Installation

Install from PyPI:

```bash
pip install pesuacademy
```

Install the latest from source:

```bash
pip install git+https://github.com/pesu-dev/pesuacademy.git
```

Optional extras:

- Docs: `pip install pesuacademy[docs]`
- Tests/tooling: `pip install pesuacademy[tests]`

Requirements: Python >= 3.11

## Quickstart

```python
import asyncio
from pesuacademy import PESUAcademy

async def main():
    session = None
    try:
        # Pass credentials directly or set PESU_USERNAME/PESU_PASSWORD env vars (see below)
        session = await PESUAcademy.login("YOUR_PRN", "YOUR_PASSWORD")

        profile = await session.get_profile()
        print(f"Welcome, {profile.personal.name}")

        sem2 = await session.get_results(semester=2)
        print(f"Semester 2 SGPA: {sem2.sgpa}")
    finally:
        if session:
            await session.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Full docs: `https://pesu-dev.github.io/pesuacademy/`

## Credentials and environment

`PESUAcademy.login()` will read credentials from environment variables if not provided as arguments. You can use a local `.env` file.

```bash
# .env
PESU_USERNAME=YOUR_PRN_OR_SRN
PESU_PASSWORD=YOUR_PASSWORD
```

Then:

```python
session = await PESUAcademy.login()  # reads from PESU_USERNAME / PESU_PASSWORD
```

## API overview

All methods are asynchronous and should be awaited.

- `PESUAcademy.login(username: str | None = None, password: str | None = None) -> PESUAcademy`
- `session.get_profile() -> Profile`
- `session.get_courses(semester: int | None = None) -> dict[int, list[Course]]`
- `session.get_attendance(semester: int | None = None) -> dict[int, list[Course]]`
- `session.get_results(semester: int) -> SemesterResult`
- `session.get_announcements() -> list[Announcement]`
- `session.get_seating_info() -> list[SeatingInformation]`
- Materials workflow:
  - `session.get_units_for_course(course_id: str) -> list[Unit]`
  - `session.get_topics_for_unit(unit_id: str) -> list[Topic]`
  - `session.get_material_links(topic: Topic, material_type_id: str) -> list[MaterialLink]`

Always call `await session.close()` to release network resources.

## Usage examples

### Profile

```python
profile = await session.get_profile()
print(profile.personal.name)
print(profile.personal.branch)
```

### Courses and Attendance

Fetch for a specific semester or for all available semesters.

```python
# Courses for a specific semester
courses_by_sem = await session.get_courses(semester=4)
for course in courses_by_sem.get(4, []):
    print(course.code, course.title)

# Attendance for all semesters
attendance = await session.get_attendance()
for sem, courses in attendance.items():
    print(f"Semester {sem}")
    for c in courses:
        pct = c.attendance.percentage if c.attendance else None
        print(f"  {c.title}: {pct if pct is not None else 'NA'}%")
```

### Results

```python
try:
    result = await session.get_results(semester=3)
    print("SGPA:", result.sgpa)
    for cr in result.courses:
        print(cr.code, cr.title)
        if cr.credits:
            print("  credits:", cr.credits.earned, "/", cr.credits.total)
        for a in cr.assessments:
            print("  ", a.name, a.marks, "/", a.total)
except ValueError as e:
    print("No results:", e)
```

### Announcements

```python
announcements = await session.get_announcements()
for a in announcements:
    print(f"[{a.date}] {a.title}")
```

### Seating information

```python
seating = await session.get_seating_info()
for s in seating:
    print(s.name, s.date, s.time)
```

### Materials workflow (Units → Topics → Links)

```python
# 1) Pick a course_id (e.g., the first course from a semester)
courses = await session.get_courses(semester=4)
course = courses.get(4, [])[0]

# 2) Units in that course
units = await session.get_units_for_course(course.id)
unit = units[0]

# 3) Topics in that unit
topics = await session.get_topics_for_unit(unit.id)
topic = topics[0]

# 4) Material links
# Typical material_type_id values observed: "2" = Slides, "3" = Notes
links = await session.get_material_links(topic, "2")
for link in links:
    tag = "[PDF] " if link.is_pdf else ""
    print(f"{tag}{link.title}: {link.url}")
```

## Error handling and troubleshooting

- Missing credentials: `PESUAcademy.login()` raises `ValueError` if username/password are not provided via args or environment.
- Invalid credentials: login may raise a generic `Exception` indicating authentication failed.
- Network/HTTP issues: underlying calls may raise `httpx.HTTPStatusError` or other `httpx` exceptions.

Tips:

- Always close the session in a `finally` block.
- When scripting multiple independent calls (e.g., fetching courses for many semesters), you can parallelize at the application level using `asyncio.gather` on your own tasks that call the session methods.
- If the portal UI changes significantly, scraping selectors may need updates; please report issues with sample HTML if possible.

## Contributing

Contributions are welcome! Please:

- Discuss larger changes in an issue first.
- Write clear, well-typed, and well-formatted code.
- Add or update tests where reasonable, and run `pytest`.
- For docs, build locally or let CI validate.

Contributors: https://github.com/pesu-dev/pesuacademy/graphs/contributors

Made with `https://contrib.rocks`.

## License

MIT License. See `LICENSE` for details.
