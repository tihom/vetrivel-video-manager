import csv
from .models import KhanAcademyVideo, YoutubeVideo
# to run 
# python manage.py shell
# from translations import csv_import as ci
# ci.import_data('translations/fixtures/ka-vvf-master-list.csv')
# test models
# from translations.models import KhanAcademyVideo as kav
# kav.objects.count()
# m = kav.objects.first()

ka_video_field_header_map = {
    'sno': '53',
    'domain': 'Domain',
    'subject': 'Subject',
    'topic': 'Topic',
    'tutorial': 'Tutorial',
    'title': 'Title',
    'priority': 'Priority'
}

en_youtube_video_field_header_map = {
    'url': 'English Video YouTube Link',
    'title': 'English YouTube Title',
    'duration': 'Duration'
}

def import_data(fname):
    row_dicts = parse_csv(fname)
    for row_dict in row_dicts:
        create_or_update_models(row_dict)

def parse_csv(fname):
    f = open(fname, mode='r')
    reader = csv.reader(f)
    headers = reader.next()
    idx_header_map = {}
    for idx, header in enumerate(headers):
        idx_header_map[idx] = header

    res = []
    for row in reader:
        row_dict = {}
        for idx, val in enumerate(row):
            header = idx_header_map[idx]
            row_dict[header] = val
        res.append(row_dict)

    f.close()
    return res

def create_or_update_models(row_dict):
    # create khan academy video
    ka_vid_obj = {}
    for field, header in ka_video_field_header_map.items():
        ka_vid_obj[field] = row_dict[header]
    # data sanitization
    try:
        ka_vid_obj['priority'] = int(ka_vid_obj['priority'])
    except ValueError:
        ka_vid_obj['priority'] = None
    # create the ka vid object using title as identifier
    title = ka_vid_obj.pop('title')
    ka_vid, created = KhanAcademyVideo.objects.update_or_create(
        title=title,
        defaults=ka_vid_obj
    )

    # create youtube video
    yt_vid_obj = {}
    for field, header in en_youtube_video_field_header_map.items():
        yt_vid_obj[field] = row_dict[header]
    # data sanitization
    yt_vid_obj['language'] = 'en'
    # create or update based on url
    url = yt_vid_obj.pop('url')
    yt_vid, created = YoutubeVideo.objects.update_or_create(
        url=url,
        defaults=yt_vid_obj
    )

    # associate youtube vid with the khan academy video
    ka_vid.youtube_video = yt_vid
    ka_vid.save()



    





