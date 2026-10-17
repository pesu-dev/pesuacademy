Installation
============

.. warning::

   **pesuacademy is deprecated and archived. It no longer works.**
   All access to PESU Academy now goes through `PESU OAuth2 <https://github.com/pesu-dev/oauth2>`_.

You can install **pesuacademy** easily using `pip`:

.. code-block:: bash

   pip install pesuacademy

If you prefer to install the latest development version directly from the GitHub repository:

.. code-block:: bash

   pip install git+https://github.com/pesu-dev/pesuacademy.git

---

**Requirements:**

- Python 3.11 or higher
- Dependencies (automatically installed with uv):
  - beautifulsoup4
  - httpx
  - pydantic
  - python-dotenv
  - selectolax

---

After installation, you can import the package in your Python code:

.. code-block:: python

   import pesuacademy
