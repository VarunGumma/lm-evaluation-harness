import datasets


def process_docs_bn(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Bengali."""
    return dataset.filter(lambda doc: doc["language"] == "bn")


def process_docs_en(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for English."""
    return dataset.filter(lambda doc: doc["language"] == "en")


def process_docs_gu(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Gujarati."""
    return dataset.filter(lambda doc: doc["language"] == "gu")


def process_docs_hi(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Hindi."""
    return dataset.filter(lambda doc: doc["language"] == "hi")


def process_docs_kn(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Kannada."""
    return dataset.filter(lambda doc: doc["language"] == "kn")


def process_docs_ml(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Malayalam."""
    return dataset.filter(lambda doc: doc["language"] == "ml")


def process_docs_mr(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Marathi."""
    return dataset.filter(lambda doc: doc["language"] == "mr")


def process_docs_or(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Odia."""
    return dataset.filter(lambda doc: doc["language"] == "or")


def process_docs_pa(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Punjabi."""
    return dataset.filter(lambda doc: doc["language"] == "pa")


def process_docs_ta(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Tamil."""
    return dataset.filter(lambda doc: doc["language"] == "ta")


def process_docs_te(dataset: datasets.Dataset) -> datasets.Dataset:
    """Filter BoolQ documents for Telugu."""
    return dataset.filter(lambda doc: doc["language"] == "te")