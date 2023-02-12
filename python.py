import datetime
import os
import json

def merge_videos():
    config = read_config()
    full_recordings_path = config["recordings_path"]
    merged_video_path = config["merged_video_path"]
    recordings_to_merge_text_file_path = full_recordings_path + "/files_to_merge.txt"
    recordings_to_merge_text_file = open(recordings_to_merge_text_file_path, 'w')

    for file in os.listdir(full_recordings_path):
        creation_time = os.path.getctime(full_recordings_path + "/" + file)
        dt_c = datetime.datetime.fromtimestamp(creation_time)
        if(file.endswith(".json")):
            newFileName = file.replace("'", " ")
            os.rename(full_recordings_path + "/" + file, full_recordings_path + "/" + newFileName)
            if((dt_c.date() + datetime.timedelta(days=6)) < datetime.date.today()):
                os.remove(full_recordings_path + "/" + newFileName)
        if(file.endswith(".mp4")):
            newFileName = file.replace("'", " ")
            os.rename(full_recordings_path + "/" + file, full_recordings_path + "/" + newFileName)
            if((dt_c.date() + datetime.timedelta(days=1)) == datetime.date.today()):
                recordings_to_merge_text_file.write("file '" + newFileName + "'\n")
            elif((dt_c.date() + datetime.timedelta(days=6)) < datetime.date.today()):
                os.remove(full_recordings_path + "/" + newFileName)

    recordings_to_merge_text_file.close()

    os.system('cmd /c "ffmpeg -f concat -safe 0 -i ' + recordings_to_merge_text_file_path + ' -c copy "' + merged_video_path + '/' + str(datetime.date.today()) + '.mp4"')
    
def read_config():
    with open("config.json", "r") as f:
        return json.load(f)

merge_videos()
