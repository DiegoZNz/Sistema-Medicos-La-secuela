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

###########################################   PACIENTES   #####################################################
@app.route('/addPacientes')
def addPacientes():
    # Obtener lista de medicos con nombre completo
    medicos_cur = mysql.connection.cursor()
    medicos_cur.execute("SELECT id, CONCAT(nombre, ' ', ap, ' ', am) AS nombre_completo FROM medicos")
    lista_medicos = medicos_cur.fetchall()
    
    # Obtener lista de enfermedades
    enfermedades_cur = mysql.connection.cursor()
    enfermedades_cur.execute("SELECT nombre FROM enfermedades")
    lista_enfermedades = enfermedades_cur.fetchall()
    
    return render_template('addPaciente.html', medicos=lista_medicos, enfermedades=lista_enfermedades)

# guardar nuevo paciente
@app.route('/guardarPaciente', methods=['POST', 'GET'])
def guardarPaciente():
    if request.method == 'POST':
        Vnombre = request.form['txtnombre']
        Vap = request.form['txtap']
        Vam = request.form['txtam']
        Vfechanacimiento = request.form['txtFechanacimiento']
        Valergias = request.form['txtalergias']
        Vantecedentes = request.form['txtantecedentes']
        Venfermedad = int(request.form['txtEnfermedades'])  # Asegúrate de que sea un entero
        Vmedico = int(request.form['txtmedico']) 
        CS = mysql.connection.cursor()
        CS.execute('INSERT INTO pacientes (nombre, ap, am, birthdate, alergias, antecedentes, enfermedad_id, medico_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (Vnombre, Vap, Vam, Vfechanacimiento, Valergias, Vantecedentes, Venfermedad, Vmedico))
        mysql.connection.commit()
        flash('El paciente fue agregado correctamente')
    return redirect(url_for('addPacientes'))

# Mostrar lista de pacientes
@app.route('/pacientes')
def pacientes():
    SPCS = mysql.connection.cursor()
    SPCS.execute("SELECT * FROM pacientes")
    QueryPacientes = SPCS.fetchall()
    return render_template('showPacientes.html', listPaciente=QueryPacientes)


# Editar paciente
@app.route('/editPaciente/<id>')
def editPaciente(id):
    EPCS = mysql.connection.cursor()
    EPCS.execute('SELECT * FROM pacientes WHERE id = %s', (id,))
    QueryEPId = EPCS.fetchone()
    print(QueryEPId)
    return render_template('editPaciente.html', listEPId=QueryEPId)

@app.route('/updatePaciente/<id>', methods=['POST'])
def updatePaciente(id):
    if request.method == 'POST':
        vnombre = request.form['txtnombre']
        vap = request.form['txtap']
        vam = request.form['txtam']
        vfechanacimiento = request.form['txtFechanacimiento']
        valergias = request.form['txtalergias']
        vantecedentes = request.form['txtantecedentes']
        venfermedad = int(request.form['txtEnfermedades'])  
        vmedico = int(request.form['txtmedico']) 
        UpdPCur = mysql.connection.cursor()
        UpdPCur.execute('UPDATE pacientes SET nombre = %s, ap = %s, am = %s, birthdate = %s, alergias = %s, antecedentes = %s, enfermedad_id  = %s, medico_id = %s WHERE id = %s', (vnombre,vap,vam,vfechanacimiento,valergias,vantecedentes,venfermedad,vmedico,  id))
        mysql.connection.commit()
    flash('La información del paciente fue actualizada correctamente')
    return redirect(url_for('pacientes'))


# Eliminar paciente
@app.route('/delPaciente/<id>')
def delPaciente(id):
    DPCS = mysql.connection.cursor()
    DPCS.execute('SELECT * FROM pacientes WHERE id = %s', (id,))
    QueryId = DPCS.fetchone()
    print(QueryId)
    return render_template('deletePaciente.html', listIdDlt=QueryId)

@app.route('/deletePaciente/<id>', methods=['POST'])
def deletePaciente(id):
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            DelCur = mysql.connection.cursor()
            DelCur.execute('DELETE FROM pacientes WHERE id = %s', (id,))
            mysql.connection.commit()
            flash('El paciente fue eliminado correctamente')
        elif request.form.get('action') == 'cancel':
            flash('Eliminación cancelada')
    return redirect(url_for('pacientes'))

###########################################   PACIENTES   #####################################################

###########################################   EXPLORACIONES   #####################################################


###########################################   EXPLORACIONES   #####################################################


###########################################   Enfermedades   #####################################################
@app.route('/addEnfermedades')
def addEnfermedades():
    return render_template('addEnfermedades.html')

# Agregar un nueva nueva enfermedad al catalogo de enfermedades
@app.route('/guardarEnfermedad', methods=['POST'])
def guardarEnfermedad():
    if request.method == 'POST':
        # pasamos a variables el contenido de los input
        vnombre = request.form['txtnombre']
        CSGE = mysql.connection.cursor()  # objeto de tipo cursor
        CSGE.execute('INSERT INTO enfermedades ( nombre) VALUES (%s)', ( vnombre,))
        mysql.connection.commit()
    flash('Enfermedad registrada exitosamente')
    return redirect(url_for('addEnfermedades'))

###########################################   Enfermedades   #####################################################



###########################################   ACCESO LOGIN   #####################################################


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
            rolMedico=rol[0]

            global RMED
            global IDMED
            RMED=rol[0]
            IDMED=session['id']

            if rolMedico==2:
                print ('Admin')
            else:
                print('Medico')

            return redirect(url_for('MEDICOS'))
        else:
            flash('Usuario O Contraseña Incorrectas')
            return render_template('login.html')
###########################################   ACCESO LOGIN   #####################################################

#ejecución del servidor en el puerto 5000
if __name__ == '__main__':
    app.run(port=5000,debug=True)