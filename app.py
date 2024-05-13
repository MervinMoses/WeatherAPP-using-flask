from flask import Flask,render_template,request,redirect,url_for,session
import function
import dataBaseConnect

app=Flask(__name__)
app.secret_key = 'your_secret_key' 

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        value=function.login_user()
        if value =='not':
            return render_template('Login.html',msg="Username Doesnot exist")
        if value:
            return redirect(url_for('weather'))
        return render_template('Login.html',msg="Incorrect username or password")
    return render_template('Login.html',msg=" ")





@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == 'POST':
        value=function.register_func()   
        if value=='not match':
            return render_template('register.html', msg=" password not matched")   
        if not value:
            return render_template('register.html',msg="User already exist")
       
        return redirect('/Weather')

    return render_template('register.html', msg="")




@app.route("/Weather", methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        new_city = request.form.get('city')
        if new_city:
            ispremium=function.checkPremuim()
 
            if not function.ins_cities(ispremium):
                return render_template('notPremium.html')
            if function.ins_cities(ispremium)=="False":
                return render_template('notFound.html')
                           
            
    user_session=function.session_check()
    if user_session=="NO":
        return render_template('Login.html', msg="")
    weather_data = function.getWeather()

    return render_template('weather.html', weather_data=weather_data,user_session=user_session,text="")

@app.route('/delete/<city>', methods=['POST'])
def delete_city(city):
    if city:
        
        dataBaseConnect.delete_city(city)
    return redirect(url_for('weather'))

@app.route('/city/<city>')
def city(city):
    ispremium=function.checkPremuim()
    if ispremium:
        weather_data = function.getOneWeatherDetails(city)
        return render_template('premuim.html',weather_data=weather_data)
        # return "work in process"
    return render_template('notPremium.html')


@app.route("/Logout",methods=['POST'])
def logout(): 
    function.logout()  
    return redirect(url_for('login'))

@app.route("/upgrade",methods=['GET'])
def upgrade():
    return render_template('upgrade.html')



if __name__=='__main__':
    app.run(debug=True)
