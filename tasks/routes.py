from tasks import app
from flask import render_template, request, url_for, redirect
from tasks.forms import TaskForm, ProcessTaskForm
from datetime import date
import csv, sqlite3, os

BASE_DATOS = './data/tasks.db'
cabecera = ['title', 'description', 'date']


def openFiles(DATOS, COPIA):
    original = open(DATOS, 'r')
    copia = open(COPIA, 'w')
    return original, copia

def closeFiles(original, copia):
    original.close()
    copia.close()

def renameFiles(DATOS, COPIA):
    os.remove(DATOS)
    os.rename(COPIA, DATOS)


@app.route("/")
def index():
    fOpen = open('./data/tareas.dat', 'r')

    cvsreader = csv.reader(fOpen, delimiter=',', quotechar='"')

    registros= []

    for linea in cvsreader:
        registros.append(linea)
    
    fOpen.close()
    return render_template("index.html", registros=registros)


@app.route("/newTask", methods =('GET', 'POST') )
def newTask():
    form = TaskForm(request.form)

    if request.method == 'GET':
        return render_template("task.html", form=form)
    
    if form.validate():
        fDatos = open('./data/tareas.dat','a')
        csvwiter = csv.writer(fDatos, delimiter=',', quotechar='"')

        title = request.values.get('title')
        desc = request.values.get('description')
        fx = request.values.get('fx')
        csvwiter.writerow((title, desc, fx))

        fDatos.close()

        return redirect(url_for('index'))#Va a redirigir a index.
    else:
        return render_template("task.html", form=form)

@app.route("/processtask", methods=('GET', 'POST'))
def processTask():
    form = ProcessTaskForm(request.form)

    if request.method == 'GET':
        fOpen = open('./data/tareas.dat', 'r')
        cvsreader = csv.reader(fOpen, delimiter=',', quotechar='"')

        registroAct = None
        ilinea=1

        ix = request.values.get('ix')
        if ix:
            for linea in cvsreader:
                if ilinea == int(ix):
                    registroAct = linea
                    break

                ilinea += 1

            if registroAct:
                if registroAct[2]:
                    fechaTarea = date(int(registroAct[2][:4]), int(registroAct[2][5:7]), int(registroAct[2][8:]))
                else:
                    fechaTarea = None
                
                accion = ''

                if 'btnModificar' in request.values:
                    accion = 'M'
                if 'btnBorrar' in request.values:
                    accion = 'B'
                    
                form = ProcessTaskForm(data={'ix': ix, 'title': registroAct[0], 'description': registroAct[1], 'fx': fechaTarea, 'btn': accion})
            
            return render_template("processtask.html", form=form)
        else:
            return redirect(url_for('index'))

    if form.btn.data == 'B':    
            
        fOriginal = open('./data/tareas.dat', 'r')
        fCopy = open('./data/copy.dat', 'w')


        cvsreader = csv.reader(fOriginal, delimiter=',', quotechar='"')

        ix = request.values.get('ix')

        for ilinea, linea in enumerate(cvsreader, start=1):
                
            csvwiter = csv.writer(fCopy, delimiter=',', quotechar='"')

            if int(ix) == ilinea:
                continue

            title = linea[0]
            desc = linea[1]
            fx = linea[2]
            csvwiter.writerow((title, desc, fx))

        fCopy.close()
        fOriginal.close()

        os.remove('./data/tareas.dat')
        os.rename('./data/copy.dat','./data/tareas.dat')
        
        return redirect(url_for('index'))
                
    if form.btn.data == 'M':
        if form.validate():
            fOriginal = open('./data/tareas.dat', 'r')
            fCopy = open('./data/copy.dat', 'w')

            cvsreader = csv.reader(fOriginal, delimiter=',', quotechar='"')

            ix = request.values.get('ix')

            for ilinea, linea in enumerate(cvsreader, start=1):    
                csvwiter = csv.writer(fCopy, delimiter=',', quotechar='"')

                if int(ix) == ilinea:
                    title = request.values.get('title')
                    desc = request.values.get('description')
                    fx = request.values.get('fx')
                    csvwiter.writerow((title, desc, fx))
                else:
                    title = linea[0]
                    desc = linea[1]
                    fx = linea[2]
                    csvwiter.writerow((title, desc, fx))
                pass

            os.remove('./data/tareas.dat')
            os.rename('./data/copy.dat','./data/tareas.dat')
        return redirect(url_for('index'))

    return render_template("processtask.html", form=form)