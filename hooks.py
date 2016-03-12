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


def get_additional_tags():
    """
    Use this hook to add additional tags to both json  and geojson representation
    :return: dictionary made of extra tags
    :rtype: dict
    """
    return {}


def alter_tags(tags):
    # Patch for Kosovo, which is currently unidentified
    if tags['ISO3166-1:alpha2'] == '-99' and tags['name'] == 'Kosovo':
        print('Found Kosovo')
        tags['ISO3166-1:alpha2'] = 'XK'
        tags['ISO3166-1:alpha3'] = 'UNK'
    return tags
