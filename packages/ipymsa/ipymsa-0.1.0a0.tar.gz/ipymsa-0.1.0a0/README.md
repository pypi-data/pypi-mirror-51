ipymsa
===============================

Jupyter Widget for MSA (Multiple Sequence Alignment) Viewer.

For demo, please check `notebooks/demo.ipynb`.

Installation
------------

To install use pip:

    $ pip install ipymsa
    $ jupyter nbextension enable --py --sys-prefix ipymsa


For a development installation (requires npm),

    $ git clone https://github.com//ipymsa.git
    $ cd ipymsa
    $ python3 -m venv venv
    $ pip install -r requirements.txt
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipymsa
    $ jupyter nbextension enable --py --sys-prefix ipymsa
