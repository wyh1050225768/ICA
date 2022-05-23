import pandas as pd


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
print(forms.formDict["课程信息"].info())
a=forms.delByDifferent(forms.formDict["课程信息"],forms.formDict["课程培训师"],"course_id")
b=forms.delByDifferent(a,forms.formDict["课程教室关系"],"course_id")

print(b)  #970 教室 课程车辆122 培训师 1200

# a=forms.formDict["课程教室关系"].drop_duplicates(subset="course_id")
# print(a[a["course_id"]==1000000000000000001].index)
# print(a.drop(index=a[a["course_id"]==1000000000000000001].index))





# teacher_data=pd.read_excel("培训师信息.xlsx")
# print((teacher_data))
# print(teacher_data.info())
# print(teacher_data.describe())
# print(teacher_data.head())
