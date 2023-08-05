"""
isicarchive.IsicApi

This module provides the isicapi class/object to access the ISIC
archive programmatically.

To instantiate a connection object without credentials (public use),
simply create the object without arguments:

   >>> from isicarchive import IsicApi
   >>> api = IsicApi()

If your code has only access to the username, the password will
requested using the getpass.getpass(...) call internally:

   >>> api = IsicApi(username)

If on the other hand your code already has stored the password
internally, you can also pass it to the IsicApi call:

   >>> api = IsicApi(username, password)

By default, the class uses ``https://isic-archive.com`` as hostname
(including the https protocol!), and ``/api/v1`` as the API URI.
These parameters can be overriden, which is useful should the URL
change:

   >>> api = IsicApi(hostname='https://new-archive.com')

or

   >>> api = IsicApi(api_uri='/api/v2')

For additional information on the individual endpoints as exposed by
the archive (website) in its current form, please visit

http://isic-archive.com/api/v1

You'll find documentation and examples for each of the endpoints,
together with the ability to test them separately.

Methods
-------
annotation
    Create an annotation object or retrieve a list of annotations
annotation_list
    Yields a generator for annotation JSON dicts
dataset
    Create a dataset object or retrieve a list of datasets
dataset_list
    Yields a generator for dataset JSON dicts
image
    Create an image object or retrieve a list of images
image_list
    Yields a generator for image JSON dicts
study
    Create a study object or retrieve a list of studies
study_list
    Yields a generator for study JSON dicts
"""

__version__ = '0.4.0'


import copy
import os
import tempfile
import time
from typing import Any, Optional, Tuple
import warnings

import getpass
import imageio
import json
import requests

from . import func
from . import vars
from .annotation import Annotation
from .dataset import Dataset
from .image import Image
from .study import Study

_repr_pretty_list = {
    'base_url': '_base_url',
    'username': 'username',
    'cache_folder': '_cache_folder',
    'cached_images': '_image_cache',
    'loaded_datasets': 'datasets',
    'loaded_studies': 'studies',
    'obj_annotations': '_annotation_objs',
    'obj_datasets': '_dataset_objs',
    'obj_images': '_image_objs',
    'obj_studies': '_study_objs',
}

def _mangle_id_name(object_id:str, name:str) -> Tuple[str, str]:
    """
    (Un-) Mangle possible object ID and name

    Parameters
    ----------
    object_id : str
        Object ID (or None)
    name : str
        Name (dataset, image, or study)

    Returns (Tuple)
    -------
    object_id : str
        Object id (if it is one)
    name : str
        Name (from object id, if it isn't one!)
    """
    if object_id is None:
        object_id, name = name, object_id
    elif isinstance(object_id, dict):
        if '_id' in object_id:
            object_id = object_id['_id']
        elif 'id' in object_id:
            object_id = object_id['id']
    if (not object_id is None) and ((len(object_id) != 24)
        or (not func.could_be_mongo_object_id(object_id))):
        if name is None:
            object_id, name = name, object_id
        else:
            object_id = None
    return object_id, name

class IsicApi(object):
    """
    IsicApi

    Attributes
    ----------
    datasets : dict
        Resolving dataset names to unique mongodb ObjectIds (cache)
        This will be pre-loaded with all datasets, regardless of login
    images : dict
        Resolving image names to unique mongodb ObjectIds (cache)
    meta_hist : dict
        Returned JSON response from /image/histogram endpoint as dict
        This will be pre-loaded if a username is given
    studies : dict
        Resolving study names to unique mongodb ObjectIds (cache)
        This will be pre-loaded with all studies, regardless of login
    
    Methods
    -------
    annotation(object_id=None, params=None)
        Retrieve one annotation (object) or annotations (list)
    dataset(object_id=None, name=None, params=None)
        Retrieve one dataset (object) or datasets (list)
    image(object_id=None, name=None, params=None)
        Retrieve one image (object) or images (list)
    study(object_id=None, name=None, params=None)
        Retrieve one study (object) or studies (list)
    """


    def __init__(self,
        username:Optional[str] = None,
        password:Optional[str] = None,
        hostname:Optional[str] = None,
        api_uri:Optional[str] = None,
        cache_folder:Optional[str] = None,
        ):

        """IsicApi.__init__: please refer to IsicApi docstring!"""
        
        # Check input arguments
        if hostname is None or hostname == '':
            hostname = vars.ISIC_BASE_URL
        elif (len(hostname)) < 8 or (hostname[0:8].lower() != 'https://'):
            if hostname[0:7].lower() == 'http://':
                raise ValueError('IsicApi must use https:// as protocol!')
            hostname = 'https://' + hostname

        if api_uri is None:
            api_uri = vars.ISIC_API_URI
        elif api_uri == '' or api_uri[0] != '/':
            api_uri = '/' + api_uri

        # Prepare object:
        # _TYPEs: map id -> PARTIAL JSON dict (containing name!)
        # _TYPE_objs: map id -> created Object (after download)
        # TYPEs: map name -> id (for images only when downloaded)
        self._api_uri = api_uri
        self._annotation_objs = dict()
        self._auth_token = None
        self._base_url = hostname + api_uri
        self._cache_folder = None
        self._current_annotation = None
        self._current_dataset = None
        self._current_image = None
        self._current_study = None
        self._datasets = dict()
        self._dataset_objs = dict()
        self._hostname = hostname
        self._image_cache = dict()
        self._image_cache_last = '0' * 24
        self._image_cache_timeout = 0.0
        self._image_objs = dict()
        self._studies = dict()
        self._study_objs = dict()
        self._temp_file = None
        self.datasets = dict()
        self.images = dict()
        self.meta_hist = dict()
        self.studies = dict()
        self.username = None

        # accept cache folder?
        if cache_folder and os.path.exists(cache_folder):
            if os.path.isdir(cache_folder):
                try:
                    self._temp_file = tempfile.TemporaryFile(dir=cache_folder)
                    self._cache_folder = cache_folder
                    for sf in '0123456789abcdef':
                        cs_folder = cache_folder + os.sep + sf
                        if not os.path.exists(cs_folder):
                            os.mkdir(cs_folder)
                except:
                    warnings.warn('Error creating a file in ' + cache_folder)

        # Login required
        if username is not None:
            self.username = username

            # And get the password using getpass
            if password is None:
                password = getpass.getpass('Password for "%s":' % (username))

            # Login
            self._auth_token = func.isic_auth_token(
                self._base_url, username, password)

            # if login succeeded, collect meta information histogram
            if self._auth_token:
                self.meta_hist = func.get(self._base_url, 'image/histogram',
                    self._auth_token).json()

        # pre-populate information about datasets and studies
        items = self.dataset(params={'limit': 0, 'detail': 'true'})
        for item in items:
            self._datasets[item['_id']] = item
            self.datasets[item['name']] = item['_id']
        items = self.study(params={'limit': 0, 'detail': 'true'})
        for item in items:
            self._studies[item['_id']] = item
            self.studies[item['name']] = item['_id']

    # output
    def __repr__(self) -> str:
        return 'IsicApi(\'%s\', None, \'%s\', \'%s\', \'%s\')' % (
            self.username, self._hostname, self._api_uri, self._cache_folder)
    def __str__(self) -> str:
        if self._auth_token:
            return 'IsicApi logged into {0:s} with user {1:s}.'.format(
                self.username, self._hostname)
        return 'IsicApi accessing %s.' % self._hostname
    def _repr_pretty_(self, p:object, cycle:bool = False):
        func.object_pretty(self, p, cycle, _repr_pretty_list)

    # Annotation endpoint
    def annotation(self,
        object_id:str = None,
        params:dict = None,
        ) -> any:
        """
        annotation endpoint, allows to
        - retrieve information about multiple annotations
        - retrieve one specific annotation (object)

        Parameters
        ----------
        object_id : str
            Valid 24-character mongodb objectId for the annotation
        params : dict
            Optional parameters for the GET request
        
        Returns
        -------
        annotation : object
            For a single annotation, returns an Annotation object
        annotations : list
            For multiple annotations, a list of JSON dicts
        """
        object_id = _mangle_id_name(object_id, 'null')
        if isinstance(object_id, tuple):
            object_id = object_id[0]
        if object_id is None:
            if not isinstance(params, dict):
                raise ValueError(
                    'Annotation list requires a params dict with a study_id.')
            if 'study_id' in params:
                params = copy.copy(params)
                params['studyId'] = params['study_id']
                del params['study_id']
            if not 'studyId' in params:
                raise ValueError(
                    'Annotation list requires field study_id in params.')
            return func.get(self._base_url,
                'annotation', self._auth_token, params).json()
        if not func.could_be_mongo_object_id(object_id):
            raise ValueError('Invalid objectId format of object_id parameter.')
        if object_id in self._annotation_objs:
            self._current_annotation = self._annotation_objs[object_id]
            return self._current_annotation
        annotation = func.get(self._base_url,
            'annotation/' + object_id, self._auth_token, params).json()
        if not '_id' in annotation:
            raise KeyError('Annotation with id %s not found.' % (object_id))
        annotation_obj = Annotation(annotation, api=self)
        self._annotation_objs[annotation['_id']] = annotation_obj
        self._current_annotation = annotation_obj
        return annotation_obj

    def annotation_list(self, params:dict = None, as_object:bool = False) -> iter:
        """
        Annotation list/iterator

        Parameters
        ----------
        params : dict
            Dictionary with GET parameters for the query string, must
            contain 'study' (name) or 'study_id'
        as_object : bool
            If set to false (default), yields dicts, otherwise objects
        
        Yields
        ------
        object
            Annotation as JSON dict or object
        """
        if isinstance(params, str):
            params = {'study': params}
        elif isinstance(params, dict):
            params = copy.copy(params)
        else:
            raise ValueError('Invalid or missing params.')
        if 'studyId' in params:
            params['study'] = params['studyId']
        elif 'study_id' in params:
            params['study'] = params['study_id']
            del params['study_id']
        if not func.could_be_mongo_object_id(params['study']):
            if params['study'] in self.studies:
                params['study'] = self.studies[params['study']]
            else:
                raise ValueError('Unknown study: ' + params['study'])
        params['studyId'] = params['study']
        del params['study']
        if as_object:
            params['detail'] = 'true'
        items = self.annotation(params=params)
        for item in items:
            if as_object:
                yield Annotation(from_json=item, api=self)
            else:
                yield item

    # cache image information
    def _cache_images(self, from_list:dict):
        for item in from_list:
            if not item['_id'] in self._image_cache:
                self._image_cache[item['_id']] = item
    def cache_images(self):
        """
        Create or update the local image details cache file

        No input parameters and no return value.
        """
        if not self._cache_folder or (not os.path.isdir(self._cache_folder)):
            return
        if self._image_cache_timeout >= time.time():
            return
        image_cache_filename = func.cache_filename('0' * 24,
            'imcache', '.json.gz', api=self)
        if os.path.exists(image_cache_filename):
            try:
                self._image_cache = func.gzip_load_var(image_cache_filename)
                self._image_cache_last = sorted(self._image_cache.keys())[-1]
            except:
                os.remove(image_cache_filename)
                warnings.warn('Invalid image cache file.')
        initial_offset = 0
        limit = vars.ISIC_IMAGES_PER_CACHING
        limit_half = limit // 2
        offset = 0
        params = {
            'detail': 'true',
            'limit': str(limit),
            'offset': str(offset),
            'sort': '_id',
            'sortdir': '1',
        }
        num_loaded = len(self._image_cache)
        last_id = self._image_cache_last
        if num_loaded > 0:
            initial_offset = max(0, num_loaded - limit_half)
            offset = initial_offset
        params['offset'] = str(offset)
        partial_list = self.image(params=params)
        self._cache_images(partial_list)
        partial_list_ids = sorted(map(lambda item: item['_id'], partial_list))
        while partial_list_ids[0] > last_id and (offset > 0):
            offset = max(0, offset - limit)
            params['offset'] = str(offset)
            partial_list = self.image(params=params)
            self._cache_images(partial_list)
            partial_list_ids = sorted(map(lambda item: item['_id'], partial_list))
        offset = initial_offset
        while len(partial_list) == limit:
            offset += limit
            params['offset'] = str(offset)
            partial_list = self.image(params=params)
            self._cache_images(partial_list)
        try:
            if num_loaded < len(self._image_cache):
                func.gzip_save_var(image_cache_filename, self._image_cache)
                self._image_cache_last = sorted(self._image_cache.keys())[-1]
        except:
            warnings.warn('Error writing cache file.')
        self._image_cache_timeout = time.time() + vars.ISIC_IMAGE_CACHE_UPDATE_LASTS

    # Generic /dataset endpoint
    def dataset(self,
        object_id:str = None,
        name:str = None,
        params:dict = None,
        ) -> any:
        """
        dataset endpoint, allows to
        - retrieve information about all available datasets
        - retrieve one specific dataset (object)

        Parameters
        ----------
        object_id : str
            Valid 24-character mongodb objectId for the dataset
        name : str
            Alternatively the name of the dataset
        params : dict
            Optional parameters for the GET request
        
        Returns
        -------
        dataset : object
            For a single dataset, returns a Dataset object
        datasets : list
            For multiple datasets, a list of JSON objects
        """
        (object_id, name) = _mangle_id_name(object_id, name)
        if object_id is None:
            if name is None:
                return func.get(self._base_url,
                    'dataset', self._auth_token, params).json()
            try:
                if name in self.datasets:
                    object_id = self.datasets[name]
                else:
                    raise KeyError('Dataset "%s" not found.' % (name))
            except:
                raise
        if not func.could_be_mongo_object_id(object_id):
            raise ValueError('Invalid object_id format.')
        if object_id in self._dataset_objs:
            self._current_dataset = self._dataset_objs[object_id]
            return self._current_dataset
        if object_id in self._datasets:
            dataset = self._datasets[object_id]
        else:
            try:
                dataset = func.get(self._base_url,
                    'dataset/' + object_id, self._auth_token, params).json()
            except:
                raise
        if not '_id' in dataset:
            raise KeyError('Dataset with id %s not found.' % (object_id))
        if not dataset['name'] in self.datasets:
            self.datasets[dataset['name']] = dataset['_id']
        dataset_obj = Dataset(dataset, api=self)
        self._dataset_objs[dataset['_id']] = dataset_obj
        self._current_dataset = dataset_obj
        return dataset_obj

    # Dataset list (generator)
    def dataset_list(self, params:dict = None, as_object:bool = False) -> iter:
        """
        Dataset list/iterator

        Parameters
        ----------
        params : dict
            Optional GET parameters for the query string
        as_object : bool
            If set to false (default), yields dicts, otherwise objects
        
        Yields
        ------
        object
            Dataset as JSON dict or object
        """
        if as_object:
            if isinstance(params, dict):
                params = copy.copy(params)
            else:
                params = dict()
            params['detail'] = 'true'
        datasets = self.dataset(params=params)
        for dataset in datasets:
            if as_object:
                yield Dataset(from_json=dataset, api=self)
            else:
                yield dataset

    # find images
    def find_images(self, filter_spec:dict) -> Any:
        if not self._cache_folder:
            raise ValueError('Requires cache folder to be set.')
        self.cache_images()
        pass

    # Generic /image endpoint
    def image(self,
        object_id:str = None,
        name:str = None,
        params:dict = None,
        save_as:str = None,
        load_imagedata:bool = False,
        load_superpixels:bool = False,
        ) -> any:
        """
        image endpoint, allows to
        - retrieve information about images
        - retrieve (or download) one image (object)

        Parameters
        ----------
        object_id : str
            valid 24-character mongodb objectId for the dataset
        name : str
            alternatively the name of the dataset
        params : dict
            optional parameters for the GET request
        save_as : str
            Optional filename for the image to be saved as, in which
            case nothing is returned and the images is ONLY downloaded!
        
        Returns
        -------
        object
            for a single dataset, returns a JSON object with _id and name
        list
            for multiple datasets, a list of JSON objects
        """
        (object_id, name) = _mangle_id_name(object_id, name)
        if object_id is None:
            if name is None:
                return func.get(self._base_url,
                    'image', self._auth_token, params).json()
            try:
                if name in self.images:
                    object_id = self.images[name]
                else:
                    object_id = func.get(self._base_url,
                        'image', self._auth_token, params={'name': name}).json()
                    if isinstance(object_id, list):
                        object_id = object_id[0]
                    if '_id' in object_id:
                        object_id = object_id['_id']
                        self.images[name] = object_id
                    else:
                        raise KeyError('Image %s not found' % (name))
            except:
                raise
        if not func.could_be_mongo_object_id(object_id):
            raise ValueError('Invalid object_id format.')
        if not save_as is None:
            try:
                func.get(self._base_url,
                    'image/' + object_id + '/download',
                    self._auth_token, params, save_as)
            except:
                raise
            return
        if save_as is None and object_id in self._image_objs:
            self._current_image = self._image_objs[object_id]
            if load_imagedata and self._current_image.data is None:
                self._current_image.load_imagedata()
            if load_superpixels and self._current_image.superpixels['idx'] is None:
                self._current_image.load_superpixels()
            return self._current_image
        if object_id in self._image_cache:
            image = self._image_cache[object_id]
        else:
            try:
                image = func.get(self._base_url,
                    'image/' + object_id, self._auth_token, params).json()
            except:
                raise
        if not '_id' in image:
            raise KeyError('Image with id %s not found.' % (object_id))
        if not image['name'] in self.images:
            self.images[image['name']] = image['_id']
        image_obj = Image(image, api=self,
            load_imagedata=load_imagedata, load_superpixels=load_superpixels)
        self._image_objs[image['_id']] = image_obj
        self._current_image = image_obj
        return image_obj

    # Image list (generator)
    def image_list(self, params:dict = None, as_object:bool = False) -> iter:
        """
        Image list/iterator

        Parameters
        ----------
        params : dict
            Optional GET parameters for the query string
        as_object : bool
            If set to false (default), yields dicts, otherwise objects
        
        Yields
        ------
        object
            Image as JSON dict or object
        """
        if as_object:
            if isinstance(params, dict):
                params = copy.copy(params)
            else:
                params = dict()
            params['detail'] = 'true'
        images = self.image(params=params)
        for image in images:
            if as_object:
                yield Image(image, api=self)
            else:
                yield image

    # list datasets (printed)
    def list_datasets(self):
        print('List of datasets available at ' + self._hostname + ':')
        for name, object_id in self.datasets.items():
            if object_id in self._dataset_objs:
                dataset_obj = self._dataset_objs[object_id]
            else:
                dataset_obj = self.dataset(self._datasets[object_id])
            print(' * ' + name + ' (id=' + object_id + ')')
            print('     - ' + dataset_obj.description + ' (description)')
            print('     - {0:d} approved images'.format(dataset_obj.count))
            print('     - {0:d} images from cache'.format(
                len(dataset_obj.images)))
            print('     - {0:d} images for review'.format(
                len(dataset_obj.images_for_review)))

    # list studies (printed)
    def list_studies(self):
        print('List of studies available at ' + self._hostname + ':')
        for name, object_id in self.studies.items():
            if object_id in self._study_objs:
                study_obj = self._study_objs[object_id]
            else:
                study_obj = self.study(self._studies[object_id])
            print(' * ' + name + ' (id=' + object_id + ')')
            print('     - ' + study_obj.description + ' (description)')
            print('     - {0:d} annotations ({1:d} loaded)'.format(
                len(study_obj.annotations), len(study_obj._obj_annotations)))
            print('     - {0:d} features'.format(
                len(study_obj.features)))
            print('     - {0:d} images ({1:d} loaded)'.format(
                len(study_obj.images), len(study_obj._obj_images)))
            print('     - {0:d} questions'.format(
                len(study_obj.questions)))

    # Generic /study endpoint
    def study(self,
        object_id:str = None,
        name:str = None,
        params:dict = None,
        ) -> any:
        """
        study endpoint, allows to
        - retrieve information about all available studies
        - retrieve one specific study (object)

        Parameters
        ----------
        object_id : str
            Valid 24-character mongodb objectId for the study
        name : str
            Alternatively the name of the study
        params : dict
            Optional parameters for the GET request
        
        Returns
        -------
        study : object
            For a single study, returns a Study object
        studies : list
            For multiple studies, a list of JSON dicts
        """
        (object_id, name) = _mangle_id_name(object_id, name)
        if object_id is None:
            if name is None:
                return func.get(self._base_url,
                'study', self._auth_token, params=params).json()
            try:
                if name in self.studies:
                    object_id = self.studies[name]
                else:
                    raise KeyError('Study "%s" not found.' % (name))
            except:
                raise
        if not func.could_be_mongo_object_id(object_id):
            raise ValueError('Invalid object_id format.')
        if object_id in self._study_objs:
            return self._study_objs[object_id]
        if object_id in self._studies:
            study = self._studies[object_id]
        else:
            try:
                study = func.get(self._base_url,
                    'study/' + object_id, self._auth_token, params).json()
            except:
                raise
        if not '_id' in study:
            raise KeyError('Dataset with id %s not found.' % (object_id))
        if not study['name'] in self.studies:
            self.studies[study['name']] = study['_id']
        study_obj = Study(study, api=self)
        self._study_objs[study['_id']] = study_obj
        return study_obj
    
    # study list (generator)
    def study_list(self, params:dict = None, as_object:bool = False) -> iter:
        """
        Study list/iterator

        Parameters
        ----------
        params : dict
            Optional GET parameters for the query string
        as_object : bool
            If set to false (default), yields dicts, otherwise objects
        
        Yields
        ------
        object
            Study as JSON dict or object
        """
        if as_object:
            if isinstance(params, dict):
                params = copy.copy(params)
            else:
                params = dict()
            params['detail'] = 'true'
        else:
            if not isinstance(params, dict):
                params = {'detail': 'false'}
            elif not 'detail' in params:
                params = copy.copy(params)
                params['detail'] = 'false'
        studies = self.study(params=params)
        for study in studies:
            if as_object:
                yield Study(from_json=study, api=self)
            else:
                yield study
