import json
import cv2 
# Adjustable Variable 
filename='smooth_json_data.json'

def video_filter(video):
    video_key=list(video.keys())
    result={}
    for i in range(len(video_key)):
        temp=0
        for j in range(len(video[video_key[i]])):
            temp=temp+(video[video_key[i]][j][1]-video[video_key[i]][j][0])
        if(temp>10):
            result.update({video_key[i]:video[video_key[i]]})
    return result
def show_personID(video_ID):
    #read file
    with open(filename,'r') as f:
        python_dic=json.load(fp=f)
        if(video_ID==1):
            video_name='Video 1'
            video=python_dic[list(python_dic.keys())[0]]
        elif(video_ID==2):
            video_name='Video 2'
            video=python_dic[list(python_dic.keys())[1]]
    #將出現少於20 frame的人過濾掉
    video_filtered=video_filter(video)
    #建立兩個列表分別表示影片A和影片B當中出現超過20 frame的人
    person_ID=sorted(list(map(int,video_filtered.keys())))
    result=list(map(str,person_ID))
    result.insert(0,video_name)
    return result
def get_personExitFrame(videoID,personID,fps):
    #fps=fps*2
    start_frame_out = []
    with open(filename,'r') as f:
        python_dic=json.load(fp=f)
        if(videoID==1):
            video_name='Video 1'
            video=python_dic[list(python_dic.keys())[0]]
        elif(videoID==2):
            video_name='Video 2'
            video=python_dic[list(python_dic.keys())[1]]
    frame=""
    if(personID=="Video 1" or personID=="Video 2"):
        frame=""
    else:
        i=0
        timePeriodCount=0
        while(i<len(video[personID])):
            #if(video[personID][i][1]-video[personID][i][0]>20):
            start_value_s=int(video[personID][i][0]/fps)
            if(int(start_value_s%60)>=10):
                start_s=str(int(start_value_s%60))
            else:
                start_s="0"+str(int(start_value_s%60))
            if(start_value_s/60>=10):
                start_m=str(int(start_value_s/60))
            else:
                start_m="0"+str(int(start_value_s/60))
            end_value_s=int(video[personID][i][1]/fps)
            start_frame=str(video[personID][i][0])
            start_frame_out.append(int(video[personID][i][0]))
            end_frame=str(video[personID][i][1])
            ### 如果兩個frame區段的間格小於60(小於2秒) 直接結合兩個區段
            if(i+1<len(video[personID])):
                ##frame中斷
                if(video[personID][i+1][0]-video[personID][i][1]>60):
                    end_value_s=int(video[personID][i][1]/fps)
                    i=i+1
                ##frame沒有中斷
                else:
                    for j in range(i,len(video[personID])):
                        if(j+1<len(video[personID])):
                            if(video[personID][j+1][0]-video[personID][j][1]<=60):
                                #print(video[personID][j+1][0],video[personID][j][1])
                                end_value_s=int(video[personID][j+1][1]/fps)
                                end_frame=str(video[personID][j+1][1])
                                i=j+2
                            else :
                                break
                ##計算分鐘秒數
                if(int(end_value_s%60)>=10):
                    end_s=str(int(end_value_s%60))
                else:
                    end_s="0"+str(int(end_value_s%60))
                if((end_value_s/60)>=10):
                    end_m=str(int(end_value_s/60))
                else:
                    end_m="0"+str(int(end_value_s/60))    
                frame=frame+str(timePeriodCount)+"         "+start_m+":"+start_s+" - "+end_m+":"+end_s+"  ["+start_frame+", "+end_frame+"]\n"
                timePeriodCount=timePeriodCount+1
            else : 
                i=i+1
                if(int(end_value_s%60)>=10):
                    end_s=str(int(end_value_s%60))
                else:
                    end_s="0"+str(int(end_value_s%60))
                if((end_value_s/60)>=10):
                    end_m=str(int(end_value_s/60))
                else:
                    end_m="0"+str(int(end_value_s/60))    
                frame=frame+str(timePeriodCount)+"         "+start_m+":"+start_s+" - "+end_m+":"+end_s+"  ["+start_frame+", "+end_frame+"]\n"
                timePeriodCount=timePeriodCount+1 
    return start_frame_out, frame

# james
def get_bbox(valid_plist, video_id, query_pid):

    with open(filename,'r') as f:
            python_dic=json.load(fp=f)

    if video_id == 1:
        video=python_dic[list(python_dic.keys())[0]]
    elif video_id == 2:
        video=python_dic[list(python_dic.keys())[1]]

    # init var 
    seq_count = 1
    valid_pbbox = []
    person_valid = False
    
    for index in range(1, len(valid_plist)):
        if valid_plist[index] == query_pid:
            person_valid = True
    
    if person_valid == True:
        for pid in video: 
            lt = [] # list
            # check whether the pid is valid person   
            if str(pid) == query_pid:
                # find target person id
                for frame_d in video[str(pid)]:
                    first_f, last_f = frame_d[0], frame_d[1]
                    tf_info = [first_f, last_f]
                    bbox_detail = frame_d[2]
                    for bf_num in bbox_detail:
                        # frame, bbox_info[x,y,w,h]
                        # bf : record one of the existing frame of certain person id 
                        lt.append([int(bf_num), bbox_detail[str(bf_num)]])
                valid_pbbox.append([pid,lt])
            
    return person_valid, valid_pbbox




if __name__ == '__main__':
    get_personExitFrame(1,"5")
    

