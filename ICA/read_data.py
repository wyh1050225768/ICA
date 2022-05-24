import pandas as pd
import random
from collections import defaultdict
import time

start_time=time.time()
class FormData():
    def __init__(self):
        self.formDict={}

    def appendForm(self,formName,path):
        self.formDict.setdefault(formName,pd.read_excel(path))



    """
    para：
        updateForm : Table that needs to be updated
        refForm : A reference table to determine whether an update is required
        key : Field that is used for the update
    
    This function provides removing field values that exist in the main table but do not appear in the association table
    """
    def delByDifferent(self,updateForm,refForm,key):
        update_key=updateForm[key]
        ref_key=refForm.drop_duplicates(subset=key)[key].tolist()
        for i in update_key:
            if i not in ref_key:
                updateForm.drop(index=updateForm[updateForm[key]==i].index,inplace=True)
        return updateForm


    def getFormRelation(self,mainForm,refForm,key,refKey):
        dict={}
        for i in mainForm[key]:
            temp=list()
            for j in refForm[refForm[key]==i][refKey]:
                temp.append(j)
            dict.setdefault(i,temp)

        return dict




forms=FormData()
forms.appendForm("培训师信息","培训师信息.xlsx")
forms.appendForm("教室信息","教室信息.xlsx")
forms.appendForm("站点信息","站点信息.xlsx")
forms.appendForm("课程信息","课程信息.xlsx")
forms.appendForm("课程培训师","课程培训师.xlsx")
forms.appendForm("课程教室关系","课程教室关系.xlsx")
forms.appendForm("课程车辆关系","课程车辆关系.xlsx")
forms.appendForm("车辆信息","车辆信息.xlsx")


forms.formDict["课程信息"].drop_duplicates(inplace=True)
a=forms.delByDifferent(forms.formDict["课程信息"],forms.formDict["课程培训师"],"course_id")
b=forms.delByDifferent(a,forms.formDict["课程教室关系"],"course_id")
b.drop_duplicates(subset="course_id",inplace=True)




#print(b.info())  #970 教室 课程车辆122 培训师 1200


courseAndClassroom=forms.getFormRelation(forms.formDict["课程信息"],forms.formDict["课程教室关系"],"course_id","classroom_id")
courseAndTrainer=forms.getFormRelation(forms.formDict["课程信息"],forms.formDict["课程培训师"],"course_id","trainer_id")



# a=forms.formDict["课程教室关系"].drop_duplicates(subset="course_id")
# print(a[a["course_id"]==1000000000000000001].index)
# print(a.drop(index=a[a["course_id"]==1000000000000000001].index))

# teacher_data=pd.read_excel("培训师信息.xlsx")
# print((teacher_data))
# print(teacher_data.info())
# print(teacher_data.describe())
# print(teacher_data.head())




def findFreeTime(List):
    MaxTime=1000000
    freeTime=list()
    List.sort(key=lambda x:x[1])
    for i in range(len(List)-1):
        if List[i][1]!=List[i+1][0]:
            freeTime.append((List[i][1],List[i+1][0]))
    freeTime.append((List[-1][1],MaxTime))
    return freeTime

def getIntersection(set1,set2):
    if set1[0]<=set2[0] and set1[1]>=set2[1]:
        return set2
    if set1[0]>=set2[0] and set1[1]>=set2[1] and set2[0]>set1[1]:
        return (set1[0],set2[1])
    if set1[0] <= set2[0] and set1[1] <= set2[1] and set1[1]>set2[0]:
        return (set2[0], set1[1])
    if set1[0]>=set2[0] and set1[1]<=set2[1]:
        return set1
    return (0,0)

# print(getIntersection((1,5),(2,4)))
# test=[(0,1),(3,4),(1,2),(8,9),(5,8)]
# print(findFreeTime(test))

#一次迭代效果
courseIdList=b["course_id"].tolist()

trainerFree=defaultdict(list)
classroomFree=defaultdict(list)
diedai_time=time.time()
for i in range(len(courseIdList)):
    randomCourse=random.choice(courseIdList) #随机获取课程
    randomTrainer=random.choice(courseAndTrainer.get(randomCourse))#随机获取课程对应培训师
    randomClassroom=random.choice(courseAndClassroom.get(randomCourse))#随机获取课程对应教室
    courseDuration=int(b[b["course_id"]==randomCourse]["ceiling(course_days / 0.5) * 0.5"].values[0])#获取课程时长

    if  trainerFree.get(randomTrainer)==None and  classroomFree.get(randomClassroom)==None:
        trainerFree[randomTrainer].append((0,courseDuration))
        classroomFree[randomClassroom].append((0,courseDuration))

    elif  trainerFree.get(randomTrainer)!=None and  classroomFree.get(randomClassroom)==None:
        for i in findFreeTime(trainerFree.get(randomTrainer)):
            if i[1]-i[0]>= courseDuration:
                trainerFree[randomTrainer].append((i[0], i[0]+courseDuration))
                classroomFree[randomClassroom].append((i[0], i[0]+courseDuration))


    elif  trainerFree.get(randomTrainer)==None and  classroomFree.get(randomClassroom)!=None:
        for i in findFreeTime(classroomFree.get(randomClassroom)):
            if i[1]-i[0]>= courseDuration:
                trainerFree[randomTrainer].append((i[0], i[0]+courseDuration))
                classroomFree[randomClassroom].append((i[0], i[0]+courseDuration))

    elif  trainerFree.get(randomTrainer)!=None and  classroomFree.get(randomClassroom)!=None:
        break_flag=False
        for i in findFreeTime(classroomFree.get(randomClassroom)):
            for j in findFreeTime(trainerFree.get(randomTrainer)):
                if getIntersection(i,j)[1]-getIntersection(i,j)[0]>=courseDuration:
                    break_flag=True
                    trainerFree[randomTrainer].append((getIntersection(i,j)[0], getIntersection(i,j)[0] + courseDuration))
                    classroomFree[randomClassroom].append((getIntersection(i,j)[0], getIntersection(i,j)[0] + courseDuration))
                break
            if break_flag:
                break


    courseIdList.remove(randomCourse)




print(randomCourse,randomClassroom,randomTrainer,courseDuration)
print(trainerFree)
print(classroomFree)

print("运行时间为",time.time()-start_time)
print("迭代时间",time.time()-diedai_time)



