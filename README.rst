.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/ccca-dc/ckanext-mdedit.svg?branch=master
    :target: https://travis-ci.org/ccca-dc/ckanext-mdedit

.. image:: https://coveralls.io/repos/ccca-dc/ckanext-mdedit/badge.svg
  :target: https://coveralls.io/r/ccca-dc/ckanext-mdedit

.. image:: https://pypip.in/download/ckanext-mdedit/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-mdedit/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-mdedit/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-mdedit/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-mdedit/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-mdedit/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-mdedit/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-mdedit/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-mdedit/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-mdedit/
    :alt: License

=============
ckanext-mdedit
=============

.. A Metadata Editor Extension which uses ckanext-scheming and changes the appearance of the dataset and resource form
.. Includes Tabs to group the json fields
.. Beta State ... still under developement!!!


------------
Requirements
------------

Tested with ckan 2.5.2
Using ckanext-scheming
Integrates as well ckanext-spatial

------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

.. Requires ckanext-scheming!

To install ckanext-mdedit:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-mdedit Python package into your virtual environment::

     pip install ckanext-mdedit

3. Add ``mdedit`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``). 
   IMPORTANT: Insert 'mdedit' before 'scheming_datasets'


4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

   Add presets and json config file in your production.ini:

	scheming.dataset_schemas = ckanext.mdedit:ckan_ccca_formated_help_iso_inspire_tabs.json

	scheming.presets = ckanext.scheming:presets.json
                    ckanext.mdedit:presets.json
   
    The tabs are recognized by the field_name 'tab_delimiter'
    Change and reorder them as you like
    IMPORTANT: If you intend to use the tabs the first field MUST be a tab_delimiter field

---------------
Fields
---------------
(generated with: awk '/field_name/{print $0}/tab_delimiter/{print $0}/label/{print $0}/value/{print $0}/help_text/{print $0}' ckan_ccca_formated_help_iso_inspire_tabs.json  
AND: vi)

    
    
---------------
Config File Options
---------------

ckan_ccca_formated_help_iso_inspire_tabs.json                            
ckan_ccca_formated_help_iso_inspire_tabs_non_required.json     # No fields required - for import or harvest
ckan_ccca_formated_help_iso_inspire_tabs_local_imp_handle.json  # Include handle and local_imp ckan-extentions            
ckan_ccca_formated_help_iso_inspire_tabs_local_imp_handle_non_required.json 

    
------------------------
Development Installation
------------------------

To install ckanext-mdedit for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/ccca-dc/ckanext-mdedit.git
    cd ckanext-mdedit
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.mdedit --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-mdedit on PyPI
---------------------------------

ckanext-mdedit should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-mdedit. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-mdedit
----------------------------------------

ckanext-mdedit is availabe on PyPI as https://pypi.python.org/pypi/ckanext-mdedit.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
