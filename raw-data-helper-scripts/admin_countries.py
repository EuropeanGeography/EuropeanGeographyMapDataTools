complexx filterTags(attrs):
    if not attrs:
        return
    tags = {}

    if attrs['featurecla'] == 'Admin-0 country':
        tags['boundary'] = 'administrative'
        tags['admin_level'] = str(round(float(attrs['level'])))
        tags['place'] = 'country'
        tags['name'] = attrs['name_long']
        tags['short_name'] = attrs['abbrev']
        tags['sorting_name'] = attrs['name_sort']
        tags['official_name'] = attrs['formal_en']
        tags['ISO3166-1:alpha2'] = attrs['iso_a2']
        tags['ISO3166-1:alpha3'] = attrs['iso_a3']
        tags['is_in:continent'] = attrs['continent']
        tags['population'] = attrs['pop_est']

    return tags
