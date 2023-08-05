import intake_xarray
import xarray as xr
from cached_property import cached_property
from tqdm.auto import tqdm

from . import aggregate, config
from .bld_collection_utils import _ensure_file_access, get_subset


class BaseSource(intake_xarray.base.DataSourceMixin):
    """ Base class used to load datasets from a defined collection into an xarray dataset

    Parameters
    ----------

    collection_name : str
          Name of the collection to use.

    query : dict

    storage_optinos : dict

    kwargs :
        Further parameters are passed to to_xarray() method
    """

    def __init__(self, collection_name, query={}, storage_options={}, **kwargs):
        self.collection_name = collection_name
        self.query = query
        self.urlpath = ''
        self.ds = self.get_results()
        self._ds = None
        self.storage_options = storage_options
        self.kwargs = kwargs
        super(BaseSource, self).__init__(**kwargs)
        if self.metadata is None:
            self.metadata = {}

    def get_results(self):
        """ Return collection entries matching query"""
        ds = get_subset(self.collection_name, self.query)
        return ds

    @cached_property
    def df(self):
        return self.ds.to_dataframe()

    def nunique(self):
        """Count distinct observations across dataframe columns"""
        return self.df.nunique()

    def unique(self, columns=None):
        """ Return unique values for given columns"""
        if isinstance(columns, str):
            columns = [columns]
        if not columns:
            columns = self.df.columns

        info = {}
        for col in columns:
            uniques = self.df[col].unique().tolist()
            info[col] = {'count': len(uniques), 'values': uniques}
        return info

    def _validate_kwargs(self, kwargs):

        _kwargs = kwargs.copy()
        if len(self.ds.index) == 0:
            raise ValueError(f'Query={self.query} returned empty results')

        if 'decode_times' not in _kwargs:
            _kwargs.update(decode_times=True)
        if 'compat' not in _kwargs:
            _kwargs.update(compat='no_conflicts')
        if 'time_coord_name' not in _kwargs:
            _kwargs.update(time_coord_name='time')
        if 'ensemble_dim_name' not in _kwargs:
            _kwargs.update(ensemble_dim_name='member_id')
        if 'chunks' not in _kwargs:
            _kwargs.update(chunks={_kwargs['time_coord_name']: 'auto'})
        if 'override_coords' not in _kwargs:
            _kwargs.update(override_coords=False)
        if 'join' not in _kwargs:
            _kwargs.update(join='outer')
        if 'preprocess' not in _kwargs:
            _kwargs.update(preprocess=None)
        if 'merge_exp' not in _kwargs:
            _kwargs.update(merge_exp=True)

        return _kwargs

    def _open_dataset(self):
        raise NotImplementedError()

    def _open_dataset_groups(
        self,
        dataset_fields,
        member_column_name,
        variable_column_name,
        file_fullpath_column_name='file_fullpath',
        file_basename_column_name='file_basename',
    ):
        kwargs = self._validate_kwargs(self.kwargs)

        all_dsets = {}
        ds = get_subset(self.collection_name, self.query)
        df = _ensure_file_access(ds, file_fullpath_column_name, file_basename_column_name)
        grouped = df.groupby(dataset_fields)
        for dset_keys, dset_files in tqdm(
            grouped, desc='dataset', disable=not config.get('progress-bar')
        ):
            dset_id = '.'.join(dset_keys)
            member_ids = []
            member_dsets = []
            for m_id, m_files in tqdm(
                dset_files.groupby(member_column_name),
                desc='member',
                disable=not config.get('progress-bar'),
            ):
                var_dsets = []
                for v_id, v_files in m_files.groupby(variable_column_name):
                    urlpath_ei_vi = v_files[file_fullpath_column_name].tolist()
                    dsets = [
                        aggregate.open_dataset_delayed(
                            url,
                            data_vars=[v_id],
                            chunks=kwargs['chunks'],
                            decode_times=kwargs['decode_times'],
                        )
                        for url in urlpath_ei_vi
                    ]

                    var_dset_i = aggregate.concat_time_levels(
                        dsets,
                        time_coord_name_default=kwargs['time_coord_name'],
                        override_coords=kwargs['override_coords'],
                    )
                    var_dsets.append(var_dset_i)
                member_ids.append(m_id)
                member_dset_i = aggregate.merge(dsets=var_dsets)
                member_dsets.append(member_dset_i)
            _ds = aggregate.concat_ensembles(
                member_dsets,
                member_ids=member_ids,
                join=kwargs['join'],
                override_coords=kwargs['override_coords'],
            )
            all_dsets[dset_id] = _ds

        self._ds = all_dsets

    def to_xarray(self, **kwargs):
        """Return dataset as an xarray dataset
        Additional keyword arguments are passed through to methods in aggregate.py
        """
        _kwargs = self.kwargs.copy()
        _kwargs.update(kwargs)
        self.kwargs = _kwargs
        return self.to_dask()

    def _get_schema(self):
        """Make schema object, which embeds xarray object and some details"""
        from intake.source.base import Schema

        self.urlpath = self._get_cache(self.urlpath)[0]

        if self._ds is None:
            self._open_dataset()
            metadata = {}

            self._schema = Schema(
                datashape=None, dtype=None, shape=None, npartitions=None, extra_metadata=metadata
            )

        return self._schema
