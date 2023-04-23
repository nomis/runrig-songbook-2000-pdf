runrig-songbook-2000-pdf
========================

Generate a PDF from scans/photos of the pages of "Flower Of The West: The Runrig
Songbook" by Calum and Rory Macdonald (ISBN 0-9539452-0-0 / 978-0-9539452-0-7).

Put image files in the sibling directory ``../pages`` named with leading zeros
like ``001.jpg`` (see `names.toml <names.toml>`_). The front and back pages are
numbered ``000a``, ``000b``, ``297a``, and ``297b``. Blank pages should be
omitted. Missing pages will not be included in the output.

Run ``make`` to generate PDFs of various sizes and JPEG quality.
