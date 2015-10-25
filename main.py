#!/usr/bin/env python

from flask import Flask
from flask import g
from flask import render_template
from flask import redirect
from flask import request
from flask import Response
from flask import url_for
from zlib import crc32
import sqlite3
import hashlib
import time
from rdflib import Graph
from rdflib import BNode
from rdflib import Namespace
from rdflib import Literal
from rdflib import URIRef

DATABASE = 'objects.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/t')
def status():
    return render_template("status.html")

def md5(f):
    hash = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash.update(chunk)
    f.seek(0)
    return hash.hexdigest()

def sha1(f):
    hash = hashlib.sha1()
    for chunk in iter(lambda: f.read(4096), b""):
        hash.update(chunk)
    f.seek(0)
    return hash.hexdigest()

def sha256(f):
    hash = hashlib.sha256()
    for chunk in iter(lambda: f.read(4096), b""):
        hash.update(chunk)
    f.seek(0)
    return hash.hexdigest()

def sha512(f):
    hash = hashlib.sha512()
    for chunk in iter(lambda: f.read(4096), b""):
        hash.update(chunk)
    f.seek(0)
    return hash.hexdigest()

def crc(f):
    current = 0
    while 1:
        buffer = f.read(8192)
        if not buffer: break
        current = crc32(buffer, current)
    f.seek(0)
    return current 

def size(f):
    f.seek(0,2) # move the cursor to the end of the file
    size = f.tell()
    f.seek(0)
    return size

@app.route('/s', methods=['POST'])
def store():
    upload = request.files['upload']
    md5sum = md5(upload)
    iden = str(int(time.time())) + md5sum
    sz = size(upload)
    sha1sum = sha1(upload)
    sha256sum = sha256(upload)
    sha512sum = sha512(upload)
    crc32 = crc(upload)
    src = request.remote_addr
    upload.save('objects/%s' % (md5sum,))
    upload.close()
    query = "INSERT INTO objects VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'), ?)"
    c = get_db().cursor()
    c.execute(query, (
            iden,
            sz,
            md5sum,
            sha1sum,
            sha256sum,
            sha512sum,
            crc32,
            src))
    get_db().commit()
    if 'html' in request.form.keys():
        return redirect(url_for("obj", objname=iden))
    return iden

@app.route('/o')
def objs():
    c = get_db().cursor()
    c.execute('SELECT * FROM objects ORDER BY id DESC')
    objs = c.fetchall()
    return render_template("objects.html", objs=objs)

@app.route('/o/<objname>')
def obj(objname):
    c = get_db().cursor()
    c.execute('SELECT * FROM objects WHERE id=?', (objname,))
    obj = c.fetchone()
    return render_template('object.html', obj=obj)

@app.route('/r/<objname>')
def robj(objname):
    SCHEMA = Namespace('http://schema.org/')
    SPDX = Namespace('http://www.spdx.org/rdf/terms#')
    c = get_db().cursor()
    c.execute('SELECT * FROM objects WHERE id=?', (objname,))
    obj = c.fetchone()
    g = Graph()
    objuri = URIRef("http://localhost:5000/b/" + obj[0])
    robjuri = URIRef("http://localhost:5000/r/" + obj[0])
    md5node = BNode()
    g.add((md5node, SPDX.checksumValue, Literal(obj[2])))
    g.add((md5node, SPDX.algorithm, URIRef("http://packages.qa.debian.org/#checksumAlgorithm_md5sum")))
    g.add((objuri, SPDX.checksum, md5node))
    return Response(g.serialize(), mimetype="text/plain")

@app.route('/b/<objname>')
def blob(objname):
    return redirect(url_for("obj", objname=objname))

@app.route('/h')
def help():
    return redirect('http://womaas.readthedocs.org/en/latest/')

if __name__ == '__main__':
    app.run(debug=True)

