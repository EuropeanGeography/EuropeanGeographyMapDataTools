def process_country(country):
    locales_file = open("locales.xml", 'ab')
    locales_file.write(
        bytes('<string name=\"{0}_name\">{1}</string>\n'.format(country.iso2.lower(), country.name)))
    locales_file.write(
        bytes('<string name=\"{0}_currency\">{1}</string>\n'.format(country.iso2.lower(), __find_currency_name())))
    locales_file.close()


def __find_currency_name():
    pass


def get_additional_tags():
    pass
