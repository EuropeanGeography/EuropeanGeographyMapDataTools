import json


def process_country(country):
    locales_file = open("locales.xml", 'ab')
    locales_file.write(
        bytes('<string name=\"{0}_name\">{1}</string>\n'.format(country.iso2.lower(), country.name), 'utf-8'))
    locales_file.write(
        bytes('<string name=\"{0}_currency\">{1}</string>\n'.format(country.iso2.lower(), __find_currency_name()),
              'utf-8'))
    locales_file.close()


def __find_currency_name():
    pass


data_cache = {}
copy_tags = ['languages', 'currency', 'area', 'borders']


def __load_data_to_cache():
    with open('countries.json', 'r') as data_file:
        countries = json.load(data_file)
    for country in countries:
        tags = {}
        for tag in copy_tags:
            tags[tag] = country[tag]
        data_cache[country['cca2']] = tags


def get_additional_tags(country):
    """
    Use this hook to add additional tags to both json and geojson representation
    :param country: country to which tags will be appended
    :return: dictionary made of extra tags
    :rtype: dict
    """
    if len(data_cache) == 0:
        __load_data_to_cache()
    if country.iso2 == '-99' or country.iso2 == 'SH':
        return {}
    return data_cache[country.iso2]


def alter_tags(tags):
    # Patch for Kosovo, which is currently unidentified
    if tags['ISO3166-1:alpha2'] == '-99' and tags['name'] == 'Kosovo':
        print('Found Kosovo, altering ISO 3166-1 tags...')
        tags['ISO3166-1:alpha2'] = 'XK'
        tags['ISO3166-1:alpha3'] = 'UNK'
    return tags
