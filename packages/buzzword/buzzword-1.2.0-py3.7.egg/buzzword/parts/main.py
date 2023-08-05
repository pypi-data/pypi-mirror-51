import dash
from buzz.corpus import Corpus
import json
import os
from buzzword.parts.helpers import _preprocess_corpus
from buzzword.parts.configure import _configure_buzzword

external_stylesheets = [
    "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
app.title = "buzzword"
server = app.server

CONFIG = _configure_buzzword(__name__)


def _get_corpus_config(local_conf, global_conf):
    """
    get some configs, from json, backup from global, or none
    """
    max_ds = global_conf.get("max_dataset_rows", None)
    max_ds = local_conf.get("max_dataset_rows", max_ds)
    drop_col = global_conf.get("drop_columns", None)
    drop_col = local_conf.get("drop_columns", drop_col)
    add_gov = global_conf.get("add_governor", None)
    add_gov = local_conf.get("add_governor", add_gov)
    return dict(max_dataset_rows=max_ds, drop_columns=drop_col, add_governor=add_gov)


def _get_corpora(corpus_meta):
    """
    Load in all available corpora and make their initial tables
    """
    corpora = dict()
    tables = dict()
    for i, (corpus_name, metadata) in enumerate(corpus_meta.items(), start=1):
        if metadata.get("disabled"):
            print("Skipping corpus because it is disabled: {}".format(corpus_name))
            continue
        corpus = Corpus(metadata["path"])
        conf = _get_corpus_config(metadata, CONFIG)
        print("Loading corpus into memory: {} ...".format(corpus_name))
        corpus = corpus.load(add_governor=conf["add_governor"])
        corpus = _preprocess_corpus(corpus, **conf)
        initial_table = corpus.table(show="p", subcorpora="file")
        corpora[metadata["slug"]] = corpus
        tables[metadata["slug"]] = initial_table
    return corpora, tables


def _get_corpora_meta(config):
    """
    Get the contents of corpora.json, or an empty dict
    """
    corpora_file = config.get("corpora_file")
    exists = os.path.isfile(corpora_file)
    if not exists:
        print("Corpora file not found at {}!".format(corpora_file))
        return dict()
    with open(corpora_file, "r") as fo:
        return json.loads(fo.read())


CORPUS_META = _get_corpora_meta(CONFIG)

CORPORA, INITIAL_TABLES = _get_corpora(CORPUS_META)
