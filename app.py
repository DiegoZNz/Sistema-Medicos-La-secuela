#importación del framework
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL

#inicialización del framework (app)
app = Flask(__name__, static_folder='static')

#ingreso de las credenciales para el acceso a la bd
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='medsys' 
app.secret_key='mysecretkey'
mysql= MySQL(app)

@app.route('/')
def index(): #metodo index
    return render_template('index.html') #el metodo index nos lleva a LOGIN.html

@app.route('/diagnosticos')
def diagnosticos():
    return render_template('diagnosticos.html')

@app.route('/exploraciones')
def exploraciones():
    return render_template('exploraciones.html')

@app.route('/pacientes')
def pacientes():
    return render_template('pacientes.html')

@app.route('/pacientesguardar', methods=['POST'])
def pacientesguardar():
    if request.method == 'POST':
        # pasamos a variables el contenido de los input
        Vnombre= request.form['txtnombre']
        Vap= request.form['txtap']
        Vam= request.form['txtam']
        Vfechanac=request.form['txtfechanac']
        Videnfermedad=request.form['txtidenfermedad']
        Vantecedentes=request.form['txtantecedentes']
        # Conectar y ejecutar el insert
        CS = mysql.connection.cursor() # objeto de tipo cursor
        CS.execute('insert into pacientes (nombre, ap, am, fechanac, antecedentes, id_enfermedad_tipo) values (%s, %s, %s, %s, %s, %s)',(Vnombre, Vap, Vam, Vfechanac, Vantecedentes, Videnfermedad))
        mysql.connection.commit()
    flash('El paciente fue agregado correctamente')
    return redirect(url_for('pacientes'))    

@app.route('/addmedicos')
def addmedicos():
    return render_template('addmedicos.html')

@app.route('/addmedicosguardar', methods=['POST'])
def addmedicosguardar():
    if request.method == 'POST':
        # pasamos a variables el contenido de los input
        Vnombre= request.form['txtnombre']
        Vap= request.form['txtap']
        Vam= request.form['txtam']
        Vrfc=request.form['txtrfc']
        Vcedula=request.form['txtcedula']
        Vemail=request.form['txtemail']
        # Conectar y ejecutar el insert
        CS = mysql.connection.cursor() # objeto de tipo cursor
        CS.execute('insert into medicos (nombre, ap, am, rfc, cedula, email) values (%s, %s, %s, %s, %s, %s)',(Vnombre, Vap, Vam, Vrfc, Vcedula, Vemail))
        mysql.connection.commit()
    flash('El medico fue agregado correctamente')
    return redirect(url_for('addmedicos'))

#ejecución del servidor en el puerto 5000
if __name__ == '__main__':
    app.run(port=5000,debug=True)