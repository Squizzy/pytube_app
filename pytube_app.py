from pytube import YouTube
#import xml.etree.ElementTree as ET
import re
import ffmpeg

# YouTube('https://www.youtube.com/watch?v=MPDwE-DY9VQ').streams.first().download()


def main():
    yt = YouTube('https://www.youtube.com/watch?v=MPDwE-DY9VQ')
    title = yt.title
    print (yt.metadata)
    
    v, extv = largest_res(yt, "V")
    filenamev = title + " - V." + extv
    
    a, exta = largest_res(yt, "A")
    filenamea = title + " - A." + exta
    
    print(f"{v=}, {a=}")
    yt.streams.filter(adaptive=True)[v].download(filename = filenamev)
    yt.streams.filter(adaptive=True)[a].download(filename = filenamea)
    
    ffmpeg.concat(ffmpeg.input(filenamev), ffmpeg.input(filenamea), v=1, a=1).output(title + ' - AV.mp4').run()
    

def largest_res(yt, streamtype: str):
    if streamtype == "V":
        regex = r'.*res=\"([0-9]*)p\".*'
    elif streamtype == "A":
        regex = r'.*abr=\"([0-9]*)kbps\".*'
    regex_mime = r'.*mime_type="\w*\/(\w*)" .*'
        
    e = yt.streams.filter(adaptive=True)
    # print(f"{len(e)=}")
    maxres = 0
    largest_stream_index = 0
    i = 0
    mime_type = ""
    
    for info in e:
        print(f"{i=}: {str(info)=}")
        if match := re.match(regex, str(info)):
            n = int(f"{match.group(1)}")
            if n > maxres:
                largest_stream_index = i
                if match_mime := re.match(regex_mime, str(info)):
                    mime_type = match_mime.group(1)
                print(f"{mime_type = }")
                maxres = n
        i += 1
    return largest_stream_index, mime_type

            # if int(f"{match.group(1)}") 
        
        # if '"type="video"' in info:
        #     if 
    
# element = ET.XML(yt.streams.filter()[0])
# print(element)

# ET.indent(str(element[0]))
# print(ET.tostring(element, encoding='unicode'))

# yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
# yt.streams.filter(adaptive=True)[0].download()
# yt.streams.filter(adaptive=True)[5].download()

# for i in range(len(e)):
#     yt.streams.filter(adaptive=True)[i].download(filename_prefix = str(i))

if __name__ in "__main__":
    main()