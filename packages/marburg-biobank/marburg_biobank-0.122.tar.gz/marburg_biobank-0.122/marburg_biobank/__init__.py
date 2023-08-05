import zipfile
import os
import numpy as np
import pandas as pd

try:
    from functools import lru_cache
except (ImportError, AttributeError):
    # don't know how to tell setup.py that we only need functools32 when under 2.7.
    # so we'll just include a copy (*bergh*)
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), "functools32"))
    from functools32 import lru_cache

datasets_to_cache = 32

known_compartment_columns = [
    "compartment",
    "cell_type",
    "disease",
    # these are only for backward compability
    "tissue",
    "disease-state",
]  # tissue


def lazy_member(field):
    """Evaluate a function once and store the result in the member (an object specific in-memory cache)
    Beware of using the same name in subclasses!
    """

    def decorate(func):
        if field == func.__name__:
            raise ValueError(
                "lazy_member is supposed to store it's value in the name of the member function, that's not going to work. Please choose another name (prepend an underscore..."
            )

        def doTheThing(*args, **kw):
            if not hasattr(args[0], field):
                setattr(args[0], field, func(*args, **kw))
            return getattr(args[0], field)

        return doTheThing

    return decorate


class OvcaBiobank(object):
    """An interface to a dump of our Biobank.
    Also used internally by the biobank website to access the data.

    In essence, a souped up dict of pandas dataframes stored
    as pickles in a zip file with memory caching"""

    def __init__(self, filename):
        self.filename = filename
        self.zf = zipfile.ZipFile(filename)
        self._cached_datasets = {}

    def get_all_patients(self):
        df = self.get_dataset("_meta/patient_compartment_dataset")
        return set(df["patient"].unique())

    def number_of_patients(self):
        """How many patients/indivuums are in all datasets?"""
        return len(self.get_all_patients())

    def number_of_datasets(self):
        """How many different datasets do we have"""
        return len(self.list_datasets())

    def get_compartments(self):
        """Get all compartments we have data for"""
        pcd = self.get_dataset("_meta/patient_compartment_dataset")
        return pcd

    @lru_cache(datasets_to_cache)
    def get_dataset_compartments(self, dataset):
        """Get available compartments in dataset @dataset"""
        ds = self.get_dataset(dataset)
        columns = self.get_dataset_compartment_columns(dataset)
        if not columns:
            return []
        else:
            sub_ds = ds[columns]
            sub_ds = sub_ds[~sub_ds.duplicated()]
            result = []
            for dummy_idx, row in sub_ds.iterrows():
                result.append(tuple([row[x] for x in columns]))
            return set(result)

    @lru_cache(datasets_to_cache)
    def get_dataset_compartment_columns(self, dataset):
        """Get available compartments columns in dataset @dataset"""
        ds = self.get_dataset(dataset)
        columns = [
            x for x in known_compartment_columns if x in ds.columns
        ]  # compartment included for older datasets
        return columns

    @lru_cache(datasets_to_cache)
    def get_variables_and_units(self, dataset):
        """What variables are availabe in a dataset?"""
        df = self.get_dataset(dataset)
        if len(df["unit"].cat.categories) == 1:
            vars = df["variable"].unique()
            unit = df["unit"].iloc[0]
            return set([(v, unit) for v in vars])
        else:
            x = df[["variable", "unit"]].drop_duplicates(["variable", "unit"])
            return set(zip(x["variable"], x["unit"]))

    def get_possible_values(self, dataset, variable, unit):
        df = self.get_dataset(dataset)
        return df['value'][(df['variable'] == variable) & (df['unit'] == unit)].unique()

    @lazy_member("_cache_list_datasets")
    def list_datasets(self):
        """What datasets to we have"""
        return sorted(
            [
                name
                for name in self.zf.namelist()
                if not name.startswith("_")
                and not os.path.basename(name).startswith("_")
            ]
        )

    @lazy_member("_cache_list_datasets_incl_meta")
    def list_datasets_including_meta(self):
        """What datasets to we have"""
        return sorted(self.zf.namelist())

    @lazy_member("_datasets_with_name_lookup")
    def datasets_with_name_lookup(self):
        return [ds for (ds, df) in self.iter_datasets() if "name" in df.columns]

    def name_lookup(self, dataset, variable):
        df = self.get_dataset(dataset)
        # todo: optimize using where?
        return df[df.variable == variable]["name"].iloc[0]

    def variable_or_name_to_variable_and_unit(self, dataset, variable_or_name):
        df = self.get_dataset(dataset)[["variable", "name", "unit"]]
        rows = df[(df.variable == variable_or_name) | (df.name == variable_or_name)]
        if len(rows["variable"].unique()) > 1:
            raise ValueError(
                "variable_or_name_to_variable led to multiple variables (%i): %s"
                % (len(rows["variable"].unique()), rows["variable"].unique())
            )
        try:
            r = rows.iloc[0]
        except IndexError:
            raise KeyError("Not found: %s" % variable_or_name)
        return r["variable"], r["unit"]

    def _get_dataset_columns_meta(self):
        import json

        with self.zf.open("_meta/_to_wide_columns") as op:
            return json.load(op)

    @lru_cache(maxsize=datasets_to_cache)
    def get_wide(
        self, dataset, apply_exclusion=True, standardized=False, filter_func=None
    ):
        """Return dataset in row=variable, column=patient format.
        if @standardized is True Index is always (variable, unit) or (variable, unit, name), 
        and columns always (patient, [compartment, cell_type, disease])

        Otherwise, unit and compartment will be left off if there is only a 
        single value for them in the dataset
        if @apply_exclusion is True, excluded patients will be filtered from DataFrame

         @filter_func is run on the dataset before converting to wide, it
         takes a df, returns a modified df

        """
        if dataset.startswith("tertiary/genelists"):
            raise ValueError(
                "No wide variant for gene lists available. Use get_dataset()"
            )
        df = self.get_dataset(dataset)
        if filter_func:
            df = filter_func(df)

        index = ["variable"]
        try:
            columns_to_use = self._get_dataset_columns_meta()
        except KeyError:
            columns_to_use = {}
        if dataset in columns_to_use:
            columns = columns_to_use[dataset]
        else:
            if "vid" in df.columns and not "patient" in df.columns:
                columns = ["vid"]
            elif "patient" in df.columns:
                columns = ["patient"]
            else:
                raise ValueError(
                    "Do not know how to convert this dataset (neither patient nor vid column)."
                    " Retrieve it get_dataset() and call to_wide() manually with appropriate parameters."
                )
            for x in known_compartment_columns:
                if x in df.columns or (standardized and x != "compartment"):
                    if not x in columns:
                        columns.append(x)
                    if x in df.columns and (
                        (hasattr(df[x], "cat") and (len(df[x].cat.categories) > 1))
                        or (len(df[x].unique()) > 1)
                    ):
                        pass
                    else:
                        if standardized and x not in df.columns:
                            df = df.assign(**{x: np.nan})
                        elif not standardized:
                            if ((hasattr(df[x], "cat") and (len(df[x].cat.categories) == 1))
                            or (len(df[x].unique()) == 1)):
                                if x in columns:
                                    columns.remove(x)

        if standardized or len(df.unit.cat.categories) > 1:
            index.append("unit")
        if "name" in df.columns:
            index.append("name")
        dfw = self.to_wide(df, index, columns)
        if apply_exclusion:
            return self.apply_exclusion(dataset, dfw)
        else:
            return dfw

    def to_wide(
        self,
        df,
        index=["variable"],
        columns=known_compartment_columns,
        sort_on_first_level=False,
    ):
        """Convert a dataset (or filtered dataset) to a wide DataFrame.
        Preferred to pd.pivot_table manually because it is
           a) faster and
           b) avoids a bunch of pitfalls when working with categorical data and
           c) makes sure the columns are dtype=float if they contain nothing but floats

        index = variable,unit
        columns = (patient, compartment, cell_type)
        """
        if columns == known_compartment_columns:
            columns = [x for x in columns if x in df.columns]
        df = df[["value"] + index + columns]
        set_index_on = index + columns
        columns_pos = tuple(range(len(index), len(index) + len(columns)))
        res = df.set_index(set_index_on).unstack(columns_pos)
        c = res.columns
        c = c.droplevel(0)
        # this removes categories from the levels of the index. Absolutly
        # necessary, or you can't add columns later otherwise
        if isinstance(c, pd.MultiIndex):
            try:
                c = pd.MultiIndex([list(x) for x in c.levels], codes=c.codes, names=c.names)
            except AttributeError:
                c = pd.MultiIndex([list(x) for x in c.levels], labels=c.labels, names=c.names)
        else:
            c = list(c)
        res.columns = c
        if isinstance(c, list):
            res.columns.names = columns
        if sort_on_first_level:
            # sort on first level - ie. patient, not compartment - slow though
            res = res[sorted(list(res.columns))]
        for c in res.columns:
            x = res[c].fillna(value=np.nan, inplace=False)
            if (x == None).any():  # noqa: E711
                raise ValueError("here")
            try:
                res[c] = pd.to_numeric(x, errors="raise")
            except ValueError:  # leaving the Nones as Nones
                pass
        return res

    @lru_cache(maxsize=datasets_to_cache)
    def get_excluded_patients(self, dataset):
        """Which patients are excluded from this particular dataset (or globally)?.

        May return a set of patient_id, or tuples of (('patient', 'x'y'), ('compartment1', 'xyz'),...) tuples if only
        certain compartments where excluded.

        """
        global_exclusion_df = self.get_dataset("clinical/_other_exclusion")
        excluded = set(global_exclusion_df["patient"].unique())
        # local exclusion from this dataset
        try:
            exclusion_path = (
                os.path.dirname(dataset)
                + "/"
                + "_"
                + os.path.basename(dataset)
                + "_exclusion"
            )
            exclusion_df = self.get_dataset(exclusion_path)
        except KeyError:
            return excluded
        columns = ["patient"] + self.get_dataset_compartment_columns(dataset)
        columns = [x for x in columns if x in exclusion_df.columns]
        res = exclusion_df[columns]
        if set(res.columns) == set(["patient"]):
            excluded.update(exclusion_df["patient"].unique())
        else:
            for idx, row in exclusion_df.iterrows():
                d = []
                for c in columns:
                    d.append((c, row[c]))
                excluded.add(tuple(d))
        return excluded

    def apply_exclusion(self, dataset_name, df):
        dataset_name = self.dataset_exists(dataset_name)
        excluded = self.get_excluded_patients(dataset_name)
        # columns = ["patient"] + self.get_dataset_compartment_columns(dataset_name)
        if "patient" in df.columns:  # a tall dataset
            keep = np.ones((len(df),), np.bool)
            for x in excluded:
                if isinstance(x, tuple):
                    matching = np.ones((len(df),), np.bool)
                    for column, value in x:
                        matching &= df[column] == value
                    keep = keep & ~matching
                else:
                    keep = keep & ~(df["patient"] == x)
            return df[keep]
        elif df.index.names[0] == "variable":  # a wide dataset...
            to_remove = []
            for c in df.columns:
                if isinstance(c, tuple):
                    if c[0] in excluded:  # patient totaly excluded
                        to_remove.append(c)
                    else:
                        key = tuple(zip(df.columns.names, c))
                        if key in excluded:
                            to_remove.append(c)
                else:
                    if c in excluded:
                        to_remove.append(c)
            return df.drop(to_remove, axis=1)
        else:
            raise ValueError(
                "Sorry, not a tall or wide DataFrame that I know how to handle."
            )

    @lru_cache(maxsize=1)
    def get_exclusion_reasons(self):
        """Get exclusion information for all the datasets + globally"""
        result = {}
        global_exclusion_df = self.get_dataset("clinical/_other_exclusion")
        for tup in global_exclusion_df.itertuples():
            if tup.patient not in result:
                result[tup.patient] = {}
            result[tup.patient]["global"] = tup.reason
        for dataset in self.list_datasets():
            try:
                exclusion_df = self.get_dataset(
                    os.path.dirname(dataset)
                    + "/"
                    + "_"
                    + os.path.basename(dataset)
                    + "_exclusion"
                )
                for tup in exclusion_df.itertuples():
                    if tup.patient not in result:
                        result[tup.patient] = {}
                    result[tup.patient][dataset] = tup.reason
            except KeyError:
                pass
        return result

    def iter_datasets(self, yield_meta=False):
        if yield_meta:
            lst = self.list_datasets_including_meta()
        else:
            lst = self.list_datasets()
        for name in lst:
            yield name, self.get_dataset(name)

    def dataset_exists(self, name):
        if name not in self.list_datasets_including_meta():
            next = "primary/" + name
            if next in self.list_datasets_including_meta():
                name = next
            else:
                raise KeyError(
                    "No such dataset: %s.\nAvailable: %s"
                    % (name, self.list_datasets_including_meta())
                )
        return name

    @lru_cache(datasets_to_cache)
    def get_dataset(self, name, apply_exclusion=False):
        """Retrieve a dataset"""
        name = self.dataset_exists(name)
        with self.zf.open(name) as op:
            try:
                df = pd.read_msgpack(op.read())
                if apply_exclusion:
                    df = self.apply_exclusion(name, df)
                return df
            except KeyError as e:
                if "KeyError: u'category'" in str(e):
                    raise ValueError(
                        "Your pandas is too old. You need at least version 0.18"
                    )

    def get_comment(self, name):
        comments = self.get_dataset("_meta/comments")
        if len(comments) == 0:
            return ""
        match = comments.path == name
        if match.any():
            return comments[match].iloc[0]["comment"]
        else:
            return ""


def download_and_open(username, password, revision):
    from pathlib import Path
    import requests
    import shutil

    fn = "marburg_ovca_biobank_%i.zip" % revision
    if not Path(fn).exists():
        print("downloading biobank revision %i" % revision)
        url = (
            "https://mbf.imt.uni-marburg.de/biobank/download/marburg_biobank?revision=%i"
            % revision
        )
        r = requests.get(
            url, stream=True, auth=requests.auth.HTTPBasicAuth(username, password)
        )
        if r.status_code != 200:
            raise ValueError("Non 200 OK Return - was %s" % r.status_code)
        r.raw.decode_content = True
        fh = open(fn, "wb")
        shutil.copyfileobj(r.raw, fh)
        fh.close()
    return OvcaBiobank(fn)

