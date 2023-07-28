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
    return render_template('login.html') #el metodo index nos lleva a LOGIN.html

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

###########################################   MEDICOS   #####################################################
@app.route('/addmedicos')
def addmedicos():
    return render_template('addMedicos.html')

#Agregar un nuevo medico
@app.route('/addmedicosguardar', methods=['POST'])
def addmedicosguardar():
    if request.method == 'POST':
        # pasamos a variables el contenido de los input
        vnombre= request.form['txtnombre']
        vap= request.form['txtap']
        vam= request.form['txtam']
        vrfc=request.form['txtrfc']
        vcedula=request.form['txtcedula']
        vrol=request.form['txtrol']
        vpass=request.form['txtpass']
        
        # Conectar y ejecutar el insert
        CSGM = mysql.connection.cursor() # objeto de tipo cursor
        CSGM.execute('insert into medicos (nombre, ap, am, rfc, cedula, rol_id, pass) values (%s, %s, %s, %s, %s, %s, %s)',(vnombre, vap, vam, vrfc, vcedula, vrol, vpass))
        mysql.connection.commit()
    flash('El medico fue agregado correctamente')
    return redirect(url_for('addmedicos'))


#Mostrar lista de Medicos
@app.route('/medicos')
def medicos():
    SMCS = mysql.connection.cursor()
    SMCS.execute("SELECT * FROM medicos")
    QueryMedicos = SMCS.fetchall()
    return render_template('showMedicos.html',listMedicos = QueryMedicos)


#Editar Medico

@app.route('/editMedico/<id>')
def editMedico(id):
    EMCS = mysql.connection.cursor()
    EMCS.execute('SELECT * FROM medicos where id = %s',(id,))
    QueryEMId = EMCS.fetchone()
    print (QueryEMId)
    return render_template('editMedico.html',listEMId = QueryEMId)

@app.route('/updateMedico/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        Vnombre= request.form['txtnombre']
        Vap= request.form['txtap']
        Vam= request.form['txtam']
        Vrfc=request.form['txtrfc']
        Vcedula=request.form['txtcedula']
        Vrol=request.form['txtrol']
        Vpass=request.form['txtpass']
        UpdMCur = mysql.connection.cursor()
        UpdMCur.execute('UPDATE medicos SET nombre = %s, ap = %s, am = %s, rfc = %s, cedula = %s, rol_id  = %s, pass=%s WHERE id = %s', (Vnombre, Vap, Vam, Vrfc, Vcedula, Vrol, Vpass, id))
        mysql.connection.commit()
    flash('La información del Medico fue actualizada correctamente')
    return redirect(url_for('medicos'))


#Eliminar Medico

@app.route('/delMedico/<id>')
def delMedico(id):
    DMCS = mysql.connection.cursor()
    DMCS.execute('SELECT * FROM medicos where id = %s',(id,))
    QueryId = DMCS.fetchone()
    print (QueryId)
    return render_template('deleteMedico.html',listIdDlt = QueryId)

@app.route('/deleteMedico/<id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            DelCur = mysql.connection.cursor()
            DelCur.execute('delete from medicos where id = %s', (id,))
            mysql.connection.commit()
            flash('El Medico fue dado de baja correctamente')
        elif request.form.get('action') == 'cancel':
            flash('Eliminación cancelada')
    return redirect(url_for('medicos'))

###########################################   MEDICOS   #####################################################

###########################################   DIAGNOSTICOS   #####################################################
@app.route('/addDiagnostico')
def addDiagnostico():
    # Obtener lista de pacientes con nombre completo
    pacientes_cur = mysql.connection.cursor()
    pacientes_cur.execute("SELECT id, CONCAT(nombre, ' ', ap, ' ', am) AS nombre_completo FROM pacientes")
    lista_pacientes = pacientes_cur.fetchall()

    # Obtener lista de exploraciones para el paciente seleccionado
    exploraciones_cur = mysql.connection.cursor()
    exploraciones_cur.execute("SELECT id FROM exploraciones WHERE paciente_id = %s", (lista_pacientes[0][0],))  # Usamos el ID del primer paciente inicialmente
    lista_exploraciones = exploraciones_cur.fetchall()

    return render_template('addDiagnostico.html', pacientes=lista_pacientes, exploraciones=lista_exploraciones)


# Agregar un nuevo diagnóstico
@app.route('/guardarDiagnostico', methods=['POST'])
def guardarDiagnostico():
    if request.method == 'POST':
        # pasamos a variables el contenido de los input
        vpaciente = request.form['txtpaciente']
        vexpediente = request.form['txtexpediente']
        vsintomas = request.form['txtsintomas']
        vtratamiento = request.form['txttratamiento']
        vmedicamentos = request.form['txtmedicamentos']
        vindicaciones = request.form['txtindicaciones']
        CSGD = mysql.connection.cursor()  # objeto de tipo cursor
        CSGD.execute('INSERT INTO diagnosticos (paciente_id, expediente_id, sintomas, tratamiento, medicamentos, indicaciones) VALUES (%s, %s, %s, %s, %s, %s)', (vpaciente, vexpediente, vsintomas, vtratamiento, vmedicamentos, vindicaciones))
        mysql.connection.commit()
    flash('El diagnóstico fue agregado correctamente')
    return redirect(url_for('addDiagnostico'))


# Mostrar lista de diagnósticos
@app.route('/diagnosticos')
def diagnosticos():
    SDCS = mysql.connection.cursor()
    SDCS.execute("SELECT * FROM diagnosticos")
    QueryDiagnostico = SDCS.fetchall()
    return render_template('showDiagnostico.html', listDiagnosticos=QueryDiagnostico)


# Editar diagnóstico
@app.route('/editDiagnostico/<id>')
def editDiagnostico(id):
    EDCS = mysql.connection.cursor()
    EDCS.execute('SELECT * FROM diagnosticos WHERE id = %s', (id,))
    QueryEDId = EDCS.fetchone()
    print(QueryEDId)
    return render_template('editDiagnostico.html', listEDId=QueryEDId)

@app.route('/updateDiagnostico/<id>', methods=['POST'])
def updateDiagnostico(id):
    if request.method == 'POST':
        Vpaciente = request.form['txtpaciente']
        Vexpediente = request.form['txtexpediente']
        Vsintomas = request.form['txtsintomas']
        Vtratamiento = request.form['txttratamiento']
        Vmedicamentos = request.form['txtmedicamentos']
        Vindicaciones = request.form['txtindicaciones']
        UpdDCur = mysql.connection.cursor()
        UpdDCur.execute('UPDATE diagnosticos SET paciente_id = %s, expediente_id = %s, sintomas = %s, tratamiento = %s, medicamentos = %s, indicaciones = %s WHERE id = %s', (Vpaciente, Vexpediente, Vsintomas, Vtratamiento, Vmedicamentos, Vindicaciones, id))
        mysql.connection.commit()
    flash('La información del diagnóstico fue actualizada correctamente')
    return redirect(url_for('diagnosticos'))


# Eliminar diagnóstico
@app.route('/delDiagnostico/<id>')
def delDiagnostico(id):
    DDCS = mysql.connection.cursor()
    DDCS.execute('SELECT * FROM diagnosticos WHERE id = %s', (id,))
    QueryId = DDCS.fetchone()
    print(QueryId)
    return render_template('deleteDiagnostico.html', listIdDlt=QueryId)

@app.route('/deleteDiagnostico/<id>', methods=['POST'])
def deleteDiagnostico(id):
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            DelCur = mysql.connection.cursor()
            DelCur.execute('DELETE FROM diagnosticos WHERE id = %s', (id,))
            mysql.connection.commit()
            flash('El diagnóstico fue eliminado correctamente')
        elif request.form.get('action') == 'cancel':
            flash('Eliminación cancelada')
    return redirect(url_for('diagnosticos'))


###########################################   DIAGNOSTICOS   #####################################################



###########################################   ESTUDIOS   #####################################################
@app.route('/addEstudio')
def addEstudio():
    # Obtener lista de pacientes con nombre completo
    pacientes_cur = mysql.connection.cursor()
    pacientes_cur.execute("SELECT id, CONCAT(nombre, ' ', ap, ' ', am) AS nombre_completo FROM pacientes")
    lista_pacientes = pacientes_cur.fetchall()
    return render_template('addEstudio.html', pacientes=lista_pacientes)


# Agregar un nuevo estudio medico
@app.route('/guardarEstudio', methods=['POST'])
def guardarEstudio():
    if request.method == 'POST':
        # pasamos a variables el contenido de los input
        vpaciente = request.form['txtpaciente']
        vnombre = request.form['txtnombre']
        vdescripcion = request.form['txtdescripcion']
        CSGE = mysql.connection.cursor()  # objeto de tipo cursor
        CSGE.execute('INSERT INTO estudios (paciente_id, nombre, descripcion) VALUES (%s, %s, %s)', (vpaciente,  vnombre, vdescripcion))
        mysql.connection.commit()
    flash('El estudio medico fue agregado correctamente')
    return redirect(url_for('addEstudio'))


# Mostrar lista de estudios medicos
@app.route('/estudios')
def estudios():
    SECS = mysql.connection.cursor()
    SECS.execute("SELECT * FROM estudios")
    QueryEstudios = SECS.fetchall()
    return render_template('showEstudio.html', listEstudios=QueryEstudios)


###########################################   ESTUDIOS   #####################################################

#ejecución del servidor en el puerto 5000
if __name__ == '__main__':
    app.run(port=5000,debug=True)