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


    Group: Basics
    -------------
    Field: title
    Label: Title
    Info: A title for your dataset.
    Profile Info: ISO_resTitle (m),  INSPIRE_ResourceTitle (m)
    Field: name
    Label: URL
    Field: notes
    Label: Abstract
    Info: Brief narrative summary of the content of the dataset.
    Profile Info: ISO_idAbs (m),  INSPIRE_ResourceAbstract (m).
    Field: idStatus
    Label: Status of the resource(s)
    Info: Status of the resource(s) within this dataset.
    Profile Info: ISO_idStatus (m)  INSPIRE -
        Value: 007
        Label: under development
        Value: 001
        Label: completed
        Value: 002
        Label: historical archive
        Value: 003
        Label: obsolete
        Value: 004
        Label: ongoing
        Value: 005
        Label: planned
        Value: 006
        Label: required
    Field: mdLang
    Label: Metadata Language
    Info: Language used for the metadata (default english)
    Profile Info: ISO mdLang (o),  INSPIRE_MetadataLanguage (m).
        Value: eng
        Label: English
        Value: ger
        Label: Deutsch
    Field: mdDate
    Label: Metadata Date
    Info: Date of creation or last modification of this Dataset (automatically inserted)
    Profile Info: ISO_mdDateSt (m),  INSPIRE_MetadataDate (m).
    Field: license_id
    Label: License
    Info: License definitions and additional information can be found at
    Profile Info: ISO_accesConsts (m),  INSPIRE_LimitationsOnPublicAccessConstraints (m).
    Field: state
    Label: Server State of the Dataset
    Info: Server internal state (automatically filled)

    Group: Constraints
    ------------------
    Field: useLimit
    Label: Use Limitation
    Info: Limitation affecting the fitness for use of the resource or metadata. Example: 'not to be used for navigation'
    Profile Info: ISO_useLimit (o),  INSPIRE_ConditionsApplyingToAccessAndUse (m).
    Field: accessConsts
    Label: Access Constraints
    Info: Access constraints applied to assure the protection of privacy or intellectual property, and any special restrictions or limitations on obtaining the resource or metadata.
    Profile Info: ISO_accessConsts (o),  INSPIRE_LimitationsOnPublicAccessConstraints (c).
        Value: 001
        Label: copyright
        Value: 002
        Label: patent
        Value: 003
        Label: patent pending
        Value: 004
        Label: trademark
        Value: 005
        Label: license
        Value: 006
        Label: intellectual property rights
        Value: 007
        Label: restricted
        Value: 008
        Label: other restrictions
    Field: useConsts
    Label: Use Constraints
    Info: Constraints applied to assure the protection of privacy or intellectual property, and any special restrictions or limitations or warnings on using the resource or metadata.
    Profile Info: ISO_otherConstraints (c),  INSPIRE_LimitationsOnPublicAccessOtherConstraints (c)
        Value: 001
        Label: copyright
        Value: 002
        Label: patent
        Value: 003
        Label: patent pending
        Value: 004
        Label: trademark
        Value: 005
        Label: license
        Value: 006
        Label: intellectual property rights
        Value: 007
        Label: restricted
        Value: 008
        Label: other restrictions
    Field: class
    Label: Handling Restrictions
    Info: Handling restrictions on the resource or metadata: unclassified, restricted, confidential, top secret, ...
    Profile Info: ISO_class (c).  INSPIRE_LimitationsOnPublicAccessClassification (c).
        Value: 001
        Label: unclassified
        Value: 002
        Label: restricted
        Value: 003
        Label: confidential
        Value: 004
        Label: secret
        Value: 005
        Label: top secret

    Group: Keywords
    ------------------
    Field: tpCat
    Label: Topic Category/ies
    Info: Main theme(s) of the dataset. See
    Profile Info: ISO_tpCat (c),  INSPIRE_TopicCategory (m).
        Value: 001
        Label: farming
        Value: 002
        Label: biota
        Value: 003
        Label: boundaries
        Value: 004
        Label: climatology, meteorology, atmosphere
        Value: 005
        Label: economy
        Value: 006
        Label: elevation
        Value: 007
        Label: environment
        Value: 008
        Label: geoscientific information
        Value: 009
        Label: health
        Value: 010
        Label: imagery, basemaps, earth cover
        Value: 011
        Label: intelligence military
        Value: 012
        Label: inland waters
        Value: 013
        Label: location
        Value: 014
        Label: oceans
        Value: 015
        Label: planning cadastre
        Value: 016
        Label: society
        Value: 017
        Label: structure
        Value: 018
        Label: transportation
        Value: 019
        Label: utilities communication
    Field: tag_string
    Label: Keywords
    Info: Commonly used word(s) or formalised word(s) or phrase(s) used to describe the subject.
    Profile Info: ISO_keyword (m),  INSPIRE_KeywordValue (m).
    Field: keyTyp
    Label: Keyword Type
    Info: Subject matter used to group smimlar keywords
    Profile Info: ISO_keyTyp (o),  INSPIRE -
        Value: 001
        Label: discipline - keyword identifies a branch of instruction or specialized learning
        Value: 002
        Label:  place - keyword identifies a location
        Value: 003
        Label: stratum - keyword identifies the layer(s) of any deposited substance
        Value: 004
        Label: temporal - keyword identifies a time period related to the dataset
        Value: 005
        Label: theme - keyword identifies a particular subject or topic
      Field: thesaurusName
      Label: Thesaurus Name
      Info: Official title of the used Thesaurus, or other vocabulary or dictionary used.
      Profile Info: ISO_thesaurusName (o),  INSPIRE_OriginatingControlledVocabulary (c).
      Field: thesaRefDate
      Profile Info: ISO CI_DATE (o),  INSPIRE_DateOfPublication (o).
      Label: Reference Date
      Info: Reference date for the cited Thesaurus.
      Field: thesRrefDateType
      Profile Info: ISO_refdateType (o),  INSPIRE_DateOfPublication (o).
      Label: Date Type
      Info: Datetype for the cited Thesaurus reference date.
          {Value: 001
           Label: creation}
          {Value: 002
           Label: publication}
          {Value: 003
           Label: revision}

    Group: Spatial
    ------------------
    Field: polygon
    Label: Polygon
    Info: Select area describing the dataset spatial extend
    Field: westBL
    Profile Info: ISO_westBL (m),  INSPIRE_GeographicBoundingBox (m).
    Label: West Bound Longitude
    Info: Western-most coordinate of the limit of the resource extent, expressed in longitude in decimal degrees (positive east).
    Field: eastBL
    Profile Info: ISO ISO_eastBL (m),  INSPIRE_GeographicBoundingBox (m).
    Label: East Bound Longitude
    Info: Eastern-most coordinate of the limit of the resource extent, expressed in longitude in decimal degrees (positive east).
    Field: southBL
    Profile Info: ISO_southBL (m),  INSPIRE_GeographicBoundingBox (m).
    Label: South Bound Latitude
    Info: Southern-most coordinate of the limit of the resource extent, expressed in latitude in decimal degrees (positive north).
    Field: northBL
    Profile Info: ISO_northBL (m),  INSPIRE_GeographicBoundingBox (m).
    Label: North Bound Latitude
    Info: Northern-most coordinate of the limit of the resource extent, expressed in latitude in decimal degrees (positive north).


    Group: Time
    ------------------
    Field: sDate
    Profile Info: ISO_exTemp (m),  INSPIRE_TemporalExtent (m).
    Label: Starting Date
    Info: Starting date for the datasets temporal extent.
    Field: eDate
    Label: Ending Date
    Profile Info: ISO_exTemp (m),  INSPIRE_TemporalExtent (m).
    Info: Ending date for the datasets temporal extent.
    Field: creaDate
    Profile Info: ISO CI_DATE (o),  INSPIRE_DateOfCreation (o).
    Label: Date of creation
    Info: Date of creation of the resources within this dataset.
    Field: pubDate
    Profile Info: ISO mdDateSt (o),  INSPIRE_MetadataDate (o).
    Label: Date of publication
    Info: Date of publication of the resources within this  dataset.
    Field: revDate
    Profile Info: ISO mdDateSt (o),  INSPIRE_MetadataDate (o).
    Label: Date of revision
    Info: Date of revision of the resources within this  dataset

    Group: Quality
    ------------------
    Field: equivScale
    Profile Info: ISO equivalentScale (o),  INSPIRE_SpatialResolution (o).
    Label: Equivalent Scale
    Info: Equivalent scale:level of detail expressed as the scale denominator of a comparable hardcopy map or chart; dictance:ground sample distance
    Field: scaleDist
    Profile Info: ISO distance (o),  INSPIRE_SpatialResolution (o).
    Label: Scale Distance
    Info: Ground sample distance. Positive integer(equivalent scale); number expressing the distance Value and a unit of measure of the distance value(distance)
    Info: Ground sample distance. Positive integer(equivalent scale); number expressing the distance Value and a unit of measure of the distance value(distance)
    Field: lineage
    Profile Info: ISO_statement (o),  INSPIRE_Lineage (o).
    Label: Lineage
    Info: General explanation of the data producer's knowledge about the lineage of a dataset.


    Group: Conformity
    ------------------
    Field: Specifications
    Profile Info: ISO_conSpec (m),  INSPIRE_Specification (m).
    Label: Specification
    Info: Citation of the product specification or user requirement against which data is beeing evaluated.
        Value: 001
        Label: COMMISSION REGULATION (EC) No 1205/2008 of 3 December 2008 implementing Directive 2007/2/EC of the European Parliament and of the Council as regards metadata;2008-12-04
        Value: 002
        Label: Corrigendum to INSPIRE Metadata Regulation published in the Official Journal of the European Union, L 328, page 83;2009-12-15
        Value: 003
        Label: Commission Regulation (EU) No 1089/2010 of 23 November 2010 implementing Directive 2007/2/EC of the European Parliament and of the Council as regards interoperability of spatial data sets and services;2010-12-08
        Value: 004
        Label: COMMISSION REGULATION (EU) No 1088/2010 of 23 November 2010 amending Regulation (EC) No 976/2009 as regards download services and transformation services;2010-12-08
        Value: 005
        Label: COMMISSION REGULATION (EC) No 976/2009 of 19 October 2009 implementing Directive 2007/2/EC of the European Parliament and of the Council as regards the Network Services;2009-10-20
        Value: 006
        Label: COMMISSION REGULATION (EU) No 268/2010 of 29 March 2010 implementing Directive 2007/2/EC of the European Parliament and of the Council as regards the access to spatial data sets and services of the Member States by Community institutions and bodies under harmonised conditions;2010-03-30
        Value: 007
        Label: Commission Decision of 5 June 2009 implementing Directive 2007/2/EC of the European Parliament and of the Council as regards monitoring and reporting (notified under document number C(2009) 4199) (2009/442/EC);2009-06-11        }
    Field: degree
    Profile Info: ISO_conPass (m),  INSPIRE_Degree (m).
    Label: Degree
    Info: Indication of the conformance result.
        Value: 001
        Label:
        Value: 002
        Label: not evaluated
        Value: 003
        Label: conformant
        Value: 004
        Label: not conformant

    Group: Contact
    ------------------
    Field: owner_org
    Label: Organization
    Info: Metadata Point of Contact: Name of responsible Organization
    Profile Info: ISO_rpOrgName (c),  INSPIRE_ResponsibleParty (m).
    Field: cntOnlineRes
    Label: Webpage
    Info: Webpage of the responsible Organization.
    Profile Info: ISO_cntOnlineRes (o),  INSPIRE -.
    Field: author_citation
    Label: Citation Info
    Info: Please enter the name(s) to be used in the citation reference for this dataset and resources. Default: Dataset Creator (see field below)
    Field: maintainer
    Label: Responsible Individual
    Info: Metadata Point of Contact: Name of responsible Individual
    Profile Info: ISO_rpIndName (c),  INSPIRE_ResponsibleParty
    Field: maintainer_email
    Label:  Responsible Individual E-Mail
    Info: Mail Address of Responsible Individual
    Profile Info: ISO_eMailAdd (o),  INSPIRE_ResponsibleParty .
    Field: role
    Label: Role
    Profile Info: ISO_role (m),  INSPIRE_ResponsiblePartyRole (m).
        Value:
        Label:
        Value: author
        Label: Author
        Value: custodian
        Label: Custodian
        Value: distributor
        Label: Distributor
        Value: originator
        Label: Originator
        Value: owner
        Label: Owner
        Value: pointOfContact
        Label: Point of Contact
        Value: principalInvestigator
        Label: Principal Investigator
        Value: processor
        Label: Processor
        Value: publisher
        Label: Publisher
        Value: resourceProvider
        Label: Resource Provider
        Value: user
        Label: User
    Field: author
    Label: Dataset Creator
    Info: Creator of this Dataset including the resources
    Profile Info: ISO_rpIndName (c),  INSPIRE_ResponsibleParty
    Field: author_email
    Label: Dataset Creator E-Mail
    Info: Mailadress of Dataset Creator
    Profile Info: ISO_rpIndName (c),  INSPIRE_ResponsibleParty
    Field: author_role
    Label: Role
    Profile Info: ISO_role (m),  INSPIRE_ResponsiblePartyRole (m).
        Value: author
        Label: Author
        Value: custodian
        Label: Custodian
        Value: distributor
        Label: Distributor
        Value: originator
        Label: Originator
        Value: owner
        Label: Owner
        Value: pointOfContact
        Label: Point of Contact
        Value: principalInvestigator
        Label: Principal Investigator
        Value: processor
        Label: Processor
        Value: publisher
        Label: Publisher
        Value: resourceProvider
        Label: Resource Provider
        Value: user
        Label: User
    Field: url
    Label: URL
    Field: name
    Label: Title
    Info: Name by which the resource is known.
    Field: decription
    Label: Description
    Info: Brief narrative summary of the content of the resource.
    Field: format
    Label: Format Name
    Info: Name of the data transfer format(s) of the resource.
    Profile Info: Matches ISO_SpatialRepresentationType (156) (o) and ISO_DistributionFormat (o)
    Field: formatVer
    Label: Format Version
    Info: Version of the format(date, number, etc.).
    Field: ResourceURI
    Label: Resource URI
    Info: Uniformed Resource Identifier (URI) - world wide valid and citable. Provided automatically by the CCCA Data Center.
    Profile Info: ISO_linkage (o),  INSPIRE_ResourceLocator (m)


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
