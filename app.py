#---------------------------------------Necesario para funcionar----------------------------------------------------------------------------

from flask import Flask,render_template,request,redirect,url_for,flash, session
from flask_mysqldb import MySQL

RMED=0
IDMED=0

app = Flask(__name__, static_folder='static')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='medsys'
app.secret_key='mysecretkey'
mysql= MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')

#---------------------------------------------------------------------------------------------------------------------------------------

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

#---------------------------------------------------------------Ricardo------------------------------------------------------------------------

@app.route('/EXPLORACIONES')
def EXPLORACIONES():
    CC=mysql.connection.cursor()
    if RMED==1:
        CC.execute('SELECT exploraciones.id, Pacientes.Nombre, Pacientes.ap, Pacientes.am, round(DATEDIFF(NOW(), pacientes.birthdate)/365, 0) as Edad, Exploraciones.fecha, Exploraciones.peso, Exploraciones.altura, Exploraciones.altura, Exploraciones.temperatura, Exploraciones.latidos, Exploraciones.glucosa, Exploraciones.oxigeno FROM exploraciones inner join pacientes on exploraciones.paciente_id=pacientes.id where pacientes.medico_id=%s order by Exploraciones.fecha desc', (IDMED,))
    else:
        CC.execute('SELECT exploraciones.id, Pacientes.Nombre, Pacientes.ap, Pacientes.am, round(DATEDIFF(NOW(), pacientes.birthdate)/365, 0) as Edad, Exploraciones.fecha, Exploraciones.peso, Exploraciones.altura, Exploraciones.temperatura, Exploraciones.latidos, Exploraciones.glucosa, Exploraciones.oxigeno, medicos.nombre, medicos.ap, medicos.am FROM exploraciones inner join pacientes on exploraciones.paciente_id=pacientes.id inner join medicos on medicos.id=pacientes.medico_id order by Exploraciones.fecha desc')
    conExploraciones=CC.fetchall()
    return render_template('Ricardo/EXPLORACIONES.html', listExploraciones=conExploraciones, rolMedico=RMED)

@app.route('/EXPLORACIONES_GUARDAR')
def EXPLORACIONES_GUARDAR():
    CC1=mysql.connection.cursor()
    if RMED==1:
        CC1.execute('SELECT id, nombre, ap, am from pacientes where medico_id=%s', (IDMED,))
    else:
        CC1.execute('SELECT id, nombre, ap, am from pacientes')
    conExploracionesDropdown=CC1.fetchall()
    return render_template('Ricardo/EXPLORACIONES_GUARDAR.HTML', nombres=conExploracionesDropdown, rolMedico=RMED)

@app.route('/EXPLORACIONES_BORRAR/<id>')
def EXPLORACIONES_BORRAR(id):
    exploracionBorrar=mysql.connection.cursor()
    exploracionBorrar.execute("DELETE from exploraciones WHERE id=%s",(id,))
    mysql.connection.commit()
    flash('La exploración fue eliminada')
    return redirect(url_for('EXPLORACIONES'))

@app.route('/GUARDAR_EXPLORACIONES', methods=['POST', 'GET'])
def GUARDAR_EXPLORACIONES():
    if request.method == 'POST':
        Vpaciente_id=request.form['txtPaciente_id']
        Vfecha= request.form['txtFecha']
        Vpeso= request.form['txtPeso']
        Valtura= request.form['txtAltura']
        Vtemperatura=request.form['txtTemperatura']
        Vlatidos=request.form['txtLatidos']
        Vglucosa=request.form['txtGlucosa']
        Voxigeno=request.form['txtOxigeno']
        CS = mysql.connection.cursor()
        CS.execute('insert into exploraciones (paciente_id, fecha, peso, altura, temperatura, latidos, glucosa, oxigeno) values (%s, %s, %s, %s, %s, %s, %s, %s)',(Vpaciente_id, Vfecha, Vpeso, Valtura, Vtemperatura, Vlatidos, Vglucosa, Voxigeno))
        mysql.connection.commit()
    flash('La exploración fue agregada correctamente')
    return redirect(url_for('EXPLORACIONES'))

@app.route('/EXPLORACIONES_EDITAR/<string:id>')
def EXPLORACIONES_EDITAR(id):
    exploracionID= mysql.connection.cursor()
    exploracionID.execute('SELECT * from exploraciones where id=%s', (id,))
    CC=exploracionID.fetchone()
    CC1=mysql.connection.cursor()
    if RMED==2:
        CC1.execute('SELECT id, nombre, ap, am from pacientes')
    else:
        CC1.execute('SELECT id, nombre, ap, am, medico_id from pacientes where medico_id=%s', (IDMED,))
    conExploracionesDropdown=CC1.fetchall()
    return render_template('Ricardo/EXPLORACIONES_EDITAR.HTML', exploracion=CC, rolMedico=RMED, nombres=conExploracionesDropdown)

@app.route('/EDITAR_EXPLORACIONES/<id>', methods=['POST'])
def EDITAR_EXPLORACIONES(id):
    if request.method == 'POST':
        Vpaciente_id=request.form['txtPaciente_id']
        Vfecha= request.form['txtFecha']
        Vpeso= request.form['txtPeso']
        Valtura= request.form['txtAltura']
        Vtemperatura=request.form['txtTemperatura']
        Vlatidos=request.form['txtLatidos']
        Vglucosa=request.form['txtGlucosa']
        Voxigeno=request.form['txtOxigeno']
        CS = mysql.connection.cursor()
        CS.execute('UPDATE exploraciones set paciente_id=%s, fecha=%s, peso=%s, altura=%s, temperatura=%s, latidos=%s, glucosa=%s, oxigeno=%s where id=%s', (Vpaciente_id, Vfecha, Vpeso, Valtura, Vtemperatura,  Vlatidos, Vglucosa, Voxigeno, id))
        mysql.connection.commit()
    flash('La revision del paciente '+ Vpaciente_id + '  fue modificado correctamente' )
    return redirect(url_for('EXPLORACIONES'))

@app.route('/PACIENTES')
def PACIENTES():
    CC=mysql.connection.cursor() 
    if RMED==1:
        CC.execute('SELECT pacientes.id, pacientes.nombre, pacientes.ap, pacientes.am, medicos.nombre, medicos.ap, medicos.am, pacientes.birthdate, pacientes.alergias, pacientes.antecedentes, enfermedades.nombre FROM pacientes inner join enfermedades on enfermedades.id=pacientes.enfermedad_id inner join medicos on pacientes.medico_id=medicos.id where medicos.id=%s order by pacientes.nombre ASC', (IDMED,))
    else:
        CC.execute('SELECT pacientes.id, pacientes.nombre, pacientes.ap, pacientes.am, medicos.nombre, medicos.ap, medicos.am, pacientes.birthdate, pacientes.alergias, pacientes.antecedentes, enfermedades.nombre FROM pacientes inner join enfermedades on enfermedades.id=pacientes.enfermedad_id inner join medicos on pacientes.medico_id=medicos.id ORDER BY pacientes.nombre ASC')
    conPacientes=CC.fetchall()
    return render_template('Ricardo/PACIENTES.html', listPacientes=conPacientes, rolMedico=RMED)

@app.route('/PACIENTES_GUARDAR')
def PACIENTES_GUARDAR():
    medicoID=mysql.connection.cursor()
    medicoID.execute('SELECT id FROM medicos where rol_id != 2')
    medicos=medicoID.fetchall()
    enfermedad=mysql.connection.cursor()
    enfermedad.execute('SELECT id FROM enfermedades')
    enfermedadID=enfermedad.fetchall()
    return render_template('Ricardo/PACIENTES_GUARDAR.HTML', rolMedico=RMED, medicosid=medicos, enfermedades=enfermedadID)

@app.route('/GUARDAR_PACIENTES', methods=['POST', 'GET'])
def GUARDAR_PACIENTES():
    if request.method == 'POST':
        Vnombre=request.form['txtNombre']
        Vap= request.form['txtAp']
        Vam= request.form['txtAm']
        Vfechanacimiento= request.form['txtFechanacimiento']
        Valergias=request.form['txtAlergias']
        Vantecedentes=request.form['txtAntecedentes']
        Venfermedad=request.form['txtEnfermedad']
        Vmedico=IDMED
        CS = mysql.connection.cursor()
        CS.execute('insert into pacientes (nombre, ap, am, birthdate, alergias, antecedentes, enfermedad_id, medico_id) values (%s, %s, %s, %s, %s, %s, %s, %s)',(Vnombre, Vap, Vam, Vfechanacimiento, Valergias, Vantecedentes, Venfermedad, Vmedico))
        mysql.connection.commit()
    flash('El paciente fue agregado correctamente')
    return redirect(url_for('PACIENTES'))

@app.route('/PACIENTES_BORRAR/<id>')
def PACIENTES_BORRAR(id):
    pacienteBorrar=mysql.connection.cursor()
    pacienteBorrar.execute("DELETE from pacientes WHERE id=%s",(id))
    mysql.connection.commit()
    flash('El paciente fue eliminado')
    return redirect(url_for('PACIENTES'))

@app.route('/PACIENTES_EDITAR/<string:id>')
def PACIENTES_EDITAR(id):
    pacienteID= mysql.connection.cursor()
    pacienteID.execute('SELECT * from pacientes where id=%s', (id,))
    consulID=pacienteID.fetchone()
    medicoID=mysql.connection.cursor()
    medicoID.execute('SELECT id FROM medicos where rol_id != 2')
    medicos=medicoID.fetchall()
    enfermedad=mysql.connection.cursor()
    enfermedad.execute('SELECT id FROM enfermedades')
    enfermedadID=enfermedad.fetchall()
    return render_template('Ricardo/PACIENTES_EDITAR.HTML', paciente=consulID, medicosid=medicos, rolMedico=RMED, enfermedades=enfermedadID)

@app.route('/EDITAR_PACIENTES/<id>', methods=['POST'])
def EDITAR_PACIENTES(id):
    if request.method == 'POST':
        Vnombre=request.form['txtNombre']
        Vap= request.form['txtAp']
        Vam= request.form['txtAm']
        Vfechanacimiento= request.form['txtFechanacimiento']
        Valergias=request.form['txtAlergias']
        Vantecedentes=request.form['txtAntecedentes']
        Venfermedad=request.form['txtEnfermedad']
        if RMED==2:
            Vmedico=request.form['txtMedico']
        else:
            Vmedico=IDMED
        CS = mysql.connection.cursor()
        CS.execute('UPDATE pacientes set nombre=%s, ap=%s, am=%s, birthdate=%s, alergias=%s, antecedentes=%s, enfermedad_id=%s, medico_id=%s where id=%s', (Vnombre, Vap, Vam, Vfechanacimiento, Valergias,  Vantecedentes, Venfermedad, Vmedico, id))
        mysql.connection.commit()
    flash('El paciente '+Vnombre+' ' +Vap+ ' ' +Vam+ '  fue modificado correctamente' )
    return redirect(url_for('PACIENTES'))

@app.route('/MEDICOS')
def MEDICOS():
    return render_template('Ricardo/MEDICOS.html', rolMedico=RMED, idmedico=IDMED)

@app.route('/acceso-login', methods= ["POST", "GET"])
def login():
   
    if request.method == 'POST' and 'txtRfc' in request.form and 'txtPassword' in request.form:
       
        _rfc = request.form['txtRfc']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT id, rfc, pass FROM medicos WHERE rfc = %s AND pass = %s', (_rfc, _password,))
        account = cur.fetchone()
      
        if account:
            session['logueado'] = True
            session['id'] = account[0]

            cur2=mysql.connection.cursor()
            cur2.execute('select rol_id from medicos inner join roles on medicos.rol_id=roles.id where medicos.id=%s', (session['id'],))
            rol=cur2.fetchone()

            global RMED
            global IDMED
            RMED=rol[0]
            IDMED=session['id']

            return redirect(url_for('MEDICOS'))
        else:
            flash('Usuario O Contraseña Incorrectas')
            return render_template('login.html')

#ejecución del servidor en el puerto 5000
if __name__ == '__main__':
    app.run(port=5000,debug=True)