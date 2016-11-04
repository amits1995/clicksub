from guessit import guessit
import SUBUtilities
import os
import shutil
import tempfile
import sys
import win32_unicode_argv
import unicodedata

def synced(file_info, subs_files):
    if not file_info.has_key('release_group'):
        return None
    isMovie = not file_info.has_key('series')
    sync_parameters = ['audio_codec','format','release_group','screen_size','video_codec']
    existing_sync_parameters = [key for key in file_info.keys() if key in sync_parameters]
    subs_file_info = [{'info':guessit(s['filename']+'.mkv'),'index':i} for (i,s) in enumerate(subs_files)]
    subs_file_info = [sfi for sfi in subs_file_info
                      if sfi['info'].has_key('release_group')
                      and sfi['info']['release_group'].lower() == file_info['release_group'].lower()]
    priority_subs = []
    for sub in subs_file_info:
        score = 0
        sub_info = sub['info']
        is_synced = True
        for sync_param in existing_sync_parameters:
            if sub_info.has_key(sync_param):
                if sub_info[sync_param].lower() != file_info[sync_param].lower():
                    is_synced = False
                else:
                    score+=1
            else:
                is_synced = False
        if is_synced:
            return subs_files[sub['index']]
        priority_subs.append({'score':score,'sub':sub})
        pass
    if len(priority_subs):
        max = 0
        index = 0
        for i, sub_s in enumerate(priority_subs):
            if sub_s['score'] > max:
                index = i
                max = sub_s['score']
        return subs_files[priority_subs[index]['sub']['index']]
    return None






def main():
    full_file_name = sys.argv[1]
    file_dir = os.path.dirname(full_file_name)
    file_name = os.path.basename(full_file_name)
    fileNameWithoutExt = os.path.splitext(file_name)[0]
    file_info = guessit(file_name)
    item = {}
    item['temp'] = False
    item['rar'] = False
    item['year'] = file_info['year'] if file_info.has_key('year') else ''  # Year
    item['season'] = file_info['season'] if file_info.has_key('season') else ''  # Season
    item['episode'] = file_info['episodeNumber'] if file_info.has_key('episodeNumber') else ''  # Episode
    item['tvshow'] = file_info['series'] if file_info.has_key('series') else ''  # Show
    item['title'] = file_info['title'] if file_info.has_key('title') else ''  # try to get original title
    item['file_original_path'] = file_name # Full path of a playing file
    item['3let_language'] = ['heb']
    item['preferredlanguage'] = 'heb'
    helper = SUBUtilities.SubscenterHelper()
    res = helper.get_subtitle_list(item)
    synced_sub = synced(file_info,res)
    if synced_sub:
        print 'found synced subs'
        subtitle_list = []
        zip_filename = tempfile.mktemp() + ".zip"
        extracted_dir = helper.download(synced_sub['id'], 'he', synced_sub['link'], synced_sub['filename'], zip_filename)
        subFileFullPath = os.path.join(extracted_dir, [f for f in os.listdir(extracted_dir) if f.endswith('srt')][0])
        shutil.copy(subFileFullPath, os.path.join(file_dir, fileNameWithoutExt + '.srt'))


if __name__=="__main__":
    main()