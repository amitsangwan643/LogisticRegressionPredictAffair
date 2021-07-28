import pandas as pd
import pickle
from flask import Flask , render_template , request,Response
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/prediction',methods=['POST'])
def output():
    if request.method =='POST':
        try:
            rating=float(request.form['marriage_rating'])
            
            age=float(request.form['age'])
            
            yrs_married=float(request.form['Years Married'])
            
            children=float(request.form['Children'])
            
            religious=float(request.form['Religious'])
            

            educ=request.form['Education Level']
            if educ== 'Grade School':
                edu=9
            elif educ== 'High School':
                edu=12
            elif educ== 'Some College':
                edu=14
            elif educ== 'College Graduate':
                edu=16
            elif educ== 'Some Graduate School':
                edu=17
            else:
                edu=19
           
            woman_occup=request.form['Woman Occupation']
            if woman_occup== 'Student':
                w=1
            elif woman_occup== 'Farming/SemiSkilled/UnSkilled':
                w=2
            elif woman_occup== 'White Coller':
                w=3
            elif woman_occup== 'Teacher/Nurse/Writer/Technician/Skilled':
                w=4
            elif woman_occup== 'Managerial/Business':
                w=5
            else:
                w=6
            
            husb_occup=request.form['husband_occupation']
            if husb_occup== 'Student':
                m=1
            elif husb_occup== 'Farming/SemiSkilled/UnSkilled':
                m=2
            elif husb_occup== 'White Coller':
                m=3
            elif husb_occup== 'Teacher/Nurse/Writer/Technician/Skilled':
                m=4
            elif husb_occup== 'Managerial/Business':
                m=5
            else:
                m=6

            if w==1:
                if m==1:
                    data={"rating":rating,'age':age,'yrs_married':yrs_married,'children':children,'religious':religious,'educ':edu}
                else:
                    data={"rating":rating,'age':age,'yrs_married':yrs_married,'children':children,'religious':religious,'educ':edu,f'occ_husb_{m}':1}
            else:
                data={"rating":rating,'age':age,'yrs_married':yrs_married,'children':children,'religious':religious,'educ':edu,f'occ_{w}':1,f'occ_husb_{m}':1}

            print("Data Given is :\n",data)
            cols=['occ_2','occ_3','occ_4','occ_5','occ_6','occ_husb_2','occ_husb_3','occ_husb_4','occ_husb_5','occ_husb_6','rate_marriage','yrs_married','children','age','religious','educ']
            df=pd.DataFrame(data,columns=cols,index=[1,])
            df=df.fillna(0)
            print("Dataframe :\n",df)
            model=pickle.load(open('logistic.pickle','rb'))
            value=model.predict(df)
            if value == 1:
                res="having affair"
            else:
                res="not having affair"
            return render_template("result.html" , result=res)

        except Exception as e:
            print("Error Occured in output function")
            return (f"Error Occured inside output function.Reason: {e}")
        

if __name__=="__main__":
    app.run()