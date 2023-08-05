import numpy
from boo.columns import SHORT_COLUMNS

QUOTE_CHAR = '"'
EMPTY = int(0)
NUMERIC_COLUMNS = SHORT_COLUMNS.numeric


# FIXME: very slow code, even on small data

#        maybe concating is faster?
# billions
#bf = df[df.unit == "385"]
#bf.loc[:,cols] = bf.loc[:, cols].multiply(1000)
#bf.loc[:, "unit"] = "384"
#index = bf.index.tolist()
#
# thousands
#tf = df[df.unit == "383"]
#tf.loc[:,cols] = tf.loc[:, cols].divide(1000).round(0).astype(int)
#tf.loc[:, "unit"] = "384"
# index.extend(rf.index.tolist())
#
# concat
#remains = df[~df.index.isin(index)]
# concat remains, bf, rf


def adjust_rub(df, cols=NUMERIC_COLUMNS):
    rows = (df.unit == "385")
    df.loc[rows, cols] = df.loc[rows, cols].multiply(1000)
    df.loc[rows, "unit"] = "384"
    rows = (df.unit == "383")
    df.loc[rows, cols] = df.loc[rows, cols].divide(1000).round(0).astype(int)
    df.loc[rows, "unit"] = "384"
    return df


def dequote(name: str):
    """Split company *name* to organisation and title."""
    # Warning: will not work well on company names with more than 4 quotechars
    parts = name.split(QUOTE_CHAR)
    org = parts[0].strip()
    cnt = name.count(QUOTE_CHAR)
    if cnt == 2:
        title = parts[1].strip()
    elif cnt > 2:
        title = QUOTE_CHAR.join(parts[1:])
    else:
        title = name
    return org, title.strip()


def replace_names(title: str):
    return title .replace(
        "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО",
        "ПАО") .replace(
        "ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО",
        "ОАО") .replace(
            "АКЦИОНЕРНОЕ ОБЩЕСТВО ЭНЕРГЕТИКИ И ЭЛЕКТРИФИКАЦИИ",
            "AO энерго") .replace(
                "НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД",
                "НПЗ") .replace(
                    "ГЕНЕРИРУЮЩАЯ КОМПАНИЯ ОПТОВОГО РЫНКА ЭЛЕКТРОЭНЕРГИИ",
                    "ОГК") .replace(
                        "ГОРНО-ОБОГАТИТЕЛЬНЫЙ КОМБИНАТ",
        "ГОК")


def add_title(df):
    s_ = df.name.apply(dequote)
    df['org'] = s_.apply(lambda x: x[0])
    df['title'] = s_.apply(lambda x: replace_names(x[1]))
    return df


def rename_rows(df):
    RENAME_DICT = {
        '2460066195': "РусГидро",
        '4716016979': "ФСК ЕЭС",
        '7702038150': "Московский метрополитен",
        '7721632827': "Концерн Росэнергоатом",
        '7706664260': "Атомэнергопром",
        '7703683145': "Холдинг ВТБ Капитал АЙ БИ",
        '9102048801': "Черноморнефтегаз",
        '7736036626': "РИТЭК"
    }
    keys = list(RENAME_DICT.keys())

    def actor(inn):
        return RENAME_DICT[inn]
    ix = df.inn.isin(keys)
    df.loc[ix, 'title'] = df.loc[ix, 'inn'].apply(actor)
    return df


class UnclassifiableCodeError(ValueError):
    pass


def split_okved(code_string: str):
    """Get 3 levels of OKVED codes from *code_string*."""
    if code_string.count(".") > 2:
        raise UnclassifiableCodeError(code_string)
    try:
        codes = [int(x) for x in code_string.split(".")]
    except ValueError:
        raise UnclassifiableCodeError(code_string)
    return codes + [0] * (3 - len(codes))


def add_okved_subcode(df):
    df['ok1'], df['ok2'], df['ok3'] = zip(*df.okved.apply(split_okved))
    return df


def fst(x):
    try:
        return int(x[0:2])
    except TypeError:
        return 0


def add_region(df):
    df['region'] = df.inn.apply(fst)
    return df


def more_columns(df):
    return add_okved_subcode(add_region(add_title(df)))


def canonic_df(df):
    """Преобразовать данные внтури датафрейма:

    - Привести все строки к одинаковым единицам измерения (тыс. руб.)
    - Убрать  неиспользуемые колонки (date_revised, report_type)
    - Новые колонки:
        * короткое название компании
        * три уровня кода ОКВЭД
        * регион (по ИНН)

    """
    df_ = more_columns(adjust_rub(df))
    return rename_rows(df_)[canonic_columns()].set_index('inn')


def canonic_columns(numeric=SHORT_COLUMNS.numeric):
    return (['title', 'org', 'okpo', 'okopf', 'okfs', 'okved', 'inn'] +
            ['unit'] +
            ['ok1', 'ok2', 'ok3', 'region'] +
            numeric)


def is_numeric_column(name, numeric=SHORT_COLUMNS.numeric):
    return name in numeric


def columns_typed_as_integer(numeric=SHORT_COLUMNS.numeric):
    return numeric + ['ok1', 'ok2', 'ok3', 'region']


def canonic_dtypes():
    int_columns = columns_typed_as_integer()

    def switch(col):
        return numpy.int64 if (col in int_columns) else str
    return {col: switch(col) for col in canonic_columns()}
