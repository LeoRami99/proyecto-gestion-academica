# from livereload import Server
from flask import Flask, render_template
from app import createApp 
app = createApp()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # server = Server(app.wsgi_app)
    # server.serve(debug=True, host='0.0.0.0')
