from flask import Flask, render_template


from modelos.medicos import inicializar_medicos
from modelos.pacientes import inicializar_pacientes
from modelos.agendamedicos import inicializar_agenda
from modelos.turnos import inicializar_turnos

from controladores.ruta_medicos import medicos_bp
from controladores.ruta_pacientes import pacientes_bp
from controladores.ruta_agendamedicos import agendamedicos_bp
from controladores.ruta_turnos import turnos_bp

app = Flask(__name__)

inicializar_medicos()
inicializar_pacientes()
inicializar_agenda()
inicializar_turnos()

app.register_blueprint(medicos_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(agendamedicos_bp)
app.register_blueprint(turnos_bp)

@app.route('/')
def inicio():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

