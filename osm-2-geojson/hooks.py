import json


def process_country(country):
    pass


data_cache = {}
copy_tags = ['languages', 'currency', 'area', 'borders', 'capital', 'latlng']


def __load_data_to_cache():
    with open('countries.json', 'r') as data_file:
        countries = json.load(data_file)
    for country in countries:
        tags = {}
        for tag in copy_tags:
            if tag == 'borders':  # Another Kosovo workaround - ISO code mixup
                borders = []
                for ccode in country[tag]:
                    if ccode == 'UNK':
                        borders.append('XXK')
                    else:
                        borders.append(ccode)
                tags[tag] = borders
            elif tag == 'languages':
                languages = dict(country[tag])
                if 'bar' in languages:  # patch for bavarian german, which is unrecognized
                    del languages['bar']
                    languages['deu'] = 'German'
                elif 'gsw' in languages:  # patch for swiss german, which is unrecognized
                    del languages['gsw']
                    languages['deu'] = 'German'
                elif 'nrf' in languages:  # Some unrecognized language...
                    del languages['nrf']
                elif 'nfr' in languages:  # Some unrecognized language...
                    del languages['nfr']
                elif 'smi' in languages:  # Some unrecognized language...
                    del languages['smi']
                tags[tag] = languages
            else:
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
        tags['ISO3166-1:alpha3'] = 'XXK'
    return tags
