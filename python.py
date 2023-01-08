import datetime
import os

absolute_path = os.path.dirname(__file__)

recordings_path = "wow_recordings"
merged_video_path = "G:/Mój dysk/WoW recordings"
full_recordings_path = os.path.join(absolute_path, recordings_path)
recordings_to_merge_text_file_path = full_recordings_path + "/files_to_merge.txt"

recordings_to_merge_text_file = open(recordings_to_merge_text_file_path, 'w')

for file in os.listdir(full_recordings_path):
    if(file.endswith(".mp4")):
        creation_time = os.path.getctime(full_recordings_path + "/" + file)
        dt_c = datetime.datetime.fromtimestamp(creation_time)
        if((dt_c.date() + datetime.timedelta(days=1)) == datetime.date.today()):
            recordings_to_merge_text_file.write("file '" + file + "'\n")
        elif((dt_c.date() + datetime.timedelta(days=6)) < datetime.date.today()):
            os.remove(full_recordings_path + "/" + file)

recordings_to_merge_text_file.close()

os.system('cmd /c "ffmpeg -f concat -safe 0 -i ' + recordings_to_merge_text_file_path + ' -c copy "' + merged_video_path + '/output.mp4"')
    
